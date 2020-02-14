import numpy as np
import tensorflow as tf
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
from dnnlib import EasyDict

from training import misc
from dnnlib.tflib.ops.fused_bias_act import fused_bias_act
import faceMicrosoft as faceMicro
from dnnlib.tflib.autosummary import autosummary

network_pkl = 'cache/generator_model-stylegan2-config-f.pkl'

def get_weight(shape, gain=1, use_wscale=True, lrmul=1, weight_var='weight'):
    fan_in = np.prod(shape[:-1]) # [kernel, kernel, fmaps_in, fmaps_out] or [in, out]
    he_std = gain / np.sqrt(fan_in) # He init

    # Equalized learning rate and custom learning rate multiplier.
    if use_wscale:
        init_std = 1.0 / lrmul
        runtime_coef = he_std * lrmul
    else:
        init_std = he_std / lrmul
        runtime_coef = lrmul

    # Create variable.
    init = tf.initializers.random_normal(0, init_std)
    return tf.get_variable(weight_var, shape=shape, initializer=init) * runtime_coef

def dense_layer(x, fmaps, gain=1, use_wscale=True, lrmul=1, weight_var='weight'):
    if len(x.shape) > 2:
        x = tf.reshape(x, [-1, np.prod([d.value for d in x.shape[1:]])])
    w = get_weight([x.shape[1].value, fmaps], gain=gain, use_wscale=use_wscale, lrmul=lrmul, weight_var=weight_var)
    w = tf.cast(w, x.dtype)
    return tf.matmul(x, w)

def apply_bias_act(x, act='linear', alpha=None, gain=None, lrmul=1, bias_var='bias'):
    b = tf.get_variable(bias_var, shape=[x.shape[1]], initializer=tf.initializers.zeros()) * lrmul
    return fused_bias_act(x, b=tf.cast(b, x.dtype), act=act, alpha=alpha, gain=gain)

def only_mapping_network(
    latents_in,                             # First input: Latent vectors (Z) [minibatch, latent_size]
    latent_size             = 512,
    mapping_layers          = 8,
    dlatent_broadcast       = None,
    normalize_latents       = True,         # Normalize latent vectors (Z) before feeding them to the mapping layers?
    dtype                   = 'float32',
    **_kwargs):

    act = 'lrelu'

    latents_in.set_shape([None, latent_size])
    latents_in = tf.cast(latents_in, dtype)
    x = latents_in
    if normalize_latents:
        with tf.variable_scope('Normalize'):
            x *= tf.rsqrt(tf.reduce_mean(tf.square(x), axis=1, keepdims=True) + 1e-8)
    
    # Mapping layers.
    for layer_idx in range(mapping_layers):
        with tf.variable_scope('Dense%d' % layer_idx):
            fmaps = 512
            x = apply_bias_act(dense_layer(x, fmaps=fmaps, lrmul=0.01), act=act, lrmul=0.01)

    if dlatent_broadcast is not None:
        with tf.variable_scope('Broadcast'):
            x = tf.tile(x[:, np.newaxis], [1, dlatent_broadcast, 1])
    
    # Output.
    assert x.dtype == tf.as_dtype(dtype)
    return tf.identity(x, name='dlatents_out')

# Initialize dnnlib and TensorFlow.
tflib.init_tf()

#Trainable mapping
M_args = EasyDict(func_name=globals()['only_mapping_network'], dlatent_broadcast=18)
with tf.device('/gpu:0'):
    M = tflib.Network('only_mapping', **M_args)
M.print_layers()

G_args = EasyDict(func_name='training.networks.G_main', mapping_network=M)
D_args = EasyDict(func_name='training.networks.D_stylegan2')
with tf.device('/gpu:0'):
    G = tflib.Network('G', **G_args)
    D = tflib.Network('D', **D_args)
    Gs = G.clone('Gs')
rG, rD, rGs = misc.load_pkl(network_pkl)
G.copy_vars_from(rG); D.copy_vars_from(rD); Gs.copy_vars_from(rGs)

Gs_kwargs = dnnlib.EasyDict()
Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
Gs_kwargs.randomize_noise = False
Gs_kwargs.minibatch_size = 1

G.print_layers()
D.print_layers()

print('Initializing logs...')
summary_log = tf.summary.FileWriter("logs")

def calculateLoss(G, M, D, minibatch_size):
    z_latent_dim = G.input_shapes[0][1:]
    latents = tf.random_normal([minibatch_size] + z_latent_dim)

    # fake_images_out = G.components.synthesis.run(M, **Gs_kwargs)
    fake_images_out, fake_dlatents_out = G.get_output_for(latents, is_training=False, return_dlatents=True, **Gs_kwargs)
    fake_scores_out = D.get_output_for(fake_images_out, is_training=False)

    return [fake_images_out, fake_scores_out]

def generateAvgImg(Gs):
    z_latent_dim = Gs.input_shapes[0][1:]
    latents = tf.random_normal([1] + z_latent_dim)
    fake_images_out = Gs.get_output_for(latents, is_training=False, return_dlatents=False)
    return fake_images_out

with tf.name_scope('Inputs'), tf.device('/cpu:0'):
    lrate_in = tf.placeholder(tf.float32, name='lrate_in', shape=[])
    minibatch_size_in = tf.placeholder(tf.int32, name='minibatch_size_in', shape=[])
    loss_in = tf.placeholder(tf.float32, name='loss_in', shape=[1,1])
# M.copy_vars_from(Gs)

# Setup optimizers.
# Default optimizer used ("tf.train.AdamOptimizer")
M_opt_args = dict(EasyDict(beta1=0.0, beta2=0.99, epsilon=1e-8))
for args in [(M_opt_args)]:
    args['learning_rate'] = lrate_in
M_opt = tflib.Optimizer(name='TrainM', **M_opt_args)

#build training graph
gpu = 0
with tf.name_scope('GPU%d' % gpu), tf.device('/gpu:%d' % gpu):
    with tf.name_scope('M_loss'):
        fake_result = calculateLoss(G, M, D, minibatch_size_in)
        avg_img = generateAvgImg(Gs)
    M_opt.register_gradients(tf.reduce_mean(loss_in), M.trainables)

M_train_op = M_opt.apply_updates()

cur_nimg = 0
total_kimg = 10000
G_lrate = 0.002
curr_loss = tf.nn.softplus(0.01)
while cur_nimg < total_kimg*1000:
    feed_dict = {lrate_in: G_lrate, minibatch_size_in: 1}
    res = tflib.run(fake_result, feed_dict)
    # print(res[1])
    if cur_nimg % 10 == 0:
        print("Number of images shown till now ", cur_nimg)
        # print(imgs.shape)
        # resImg = PIL.Image.fromarray(imgs[0], 'RGB')
        # resImg.save('gImg.jpg')
        misc.save_image_grid(res[0], dnnlib.make_run_dir_path('genImg.jpg'), drange=[-1,1])

        imgs_avg = tflib.run(avg_img)
        misc.save_image_grid(imgs_avg, dnnlib.make_run_dir_path('genImgAvg.jpg'), drange=[-1,1])
        attrJson = faceMicro.callApi_wSrc()
        moustache = attrJson[0]['faceAttributes']['facialHair']['moustache']
        beard = attrJson[0]['faceAttributes']['facialHair']['beard']
        sideburns = attrJson[0]['faceAttributes']['facialHair']['sideburns']

        autosummary('Loss/scores/disc_loss_b4', res[1][0])
        all_losses = (0.99-moustache) + (0.99-beard) + (0.99-sideburns)
        print("all_losses ", all_losses)

       # if gender == "female":
        #     curr_loss = tf.nn.softplus(0.99)
        # print(curr_loss.eval())
        res[1] -= all_losses * 2
        print(res[1])
        curr_loss = autosummary('Loss/scores/moustache', all_losses)
        autosummary('Loss/scores/disc_loss', res[1][0])
        tflib.autosummary.save_summaries(summary_log, cur_nimg)

    feed_dict = {lrate_in: G_lrate, minibatch_size_in: 1, loss_in: res[1]}
    tflib.run(M_train_op, feed_dict)
        # print(attrJson[0]['faceAttributes']['gender'])
    cur_nimg += 1


