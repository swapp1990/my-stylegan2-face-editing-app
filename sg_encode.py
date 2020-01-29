import numpy as np
from matplotlib import pyplot as plt
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import os
import mpld3
from server.threads import Worker as workerCls

import EasyDict as ED

network_pkl = 'cache/generator_model-stylegan2-config-f.pkl' 

class StyleGanEncoding():
    def __init__(self):
        self.Gs = None

        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        self.Gs_kwargs.randomize_noise = False
        self.Gs_kwargs.minibatch_size = 1

        self.truncation_psi = 0.5
        self.attr_list = ['smile', 'gender', 'age', 'beauty', 'glasses', 'race_black', 'race_yellow', 'emotion_fear', 'emotion_angry', 'emotion_disgust', 'emotion_easy', 'eyes_open', 'angle_horizontal', 'angle_pitch', 'face_shape', 'height', 'width']
        self.selected_attr = self.attr_list[0] +'.npy'

        self.direction = None
        self.w_avg = None
        self.w_src = None
        self.w_src_orig = None

        self.img_size = 512
        self.fixedLayerRanges = [0,8]

        self.call_func_names = {
            'initApp': self.makeModels,
            'randomize': self.generateRandomSrcImg,
            'changeCoeff': self.changeCoeff,
            'changeFixedLayers': self.changeFixedLayers,
            'clear': self.clear
        }

    ############################## Client Edit Actions #####################################
    def makeModels(self, params=None):
        _G, _D, self.Gs = pretrained_networks.load_networks(network_pkl)
        self.w_avg = self.Gs.get_var('dlatent_avg')
        print("made models")
        
        self.direction = np.load('latent_directions/' + self.selected_attr)
        print("loaded latents")
        # Generate random latent
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        self.w_src = self.Gs.components.mapping.run(z, None)
        self.w_src = self.w_avg + (self.w_src - self.w_avg) * self.truncation_psi
        self.w_src_orig = self.w_src
        self.moveLatentAndGenerate(self.w_src, self.direction, 0.0)
    
    def generateRandomSrcImg(self, params=None):
        print("generateRandomSrcImg ", params)
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        self.w_src = self.Gs.components.mapping.run(z, None)
        self.w_src = self.w_avg + (self.w_src - self.w_avg) * self.truncation_psi
        self.w_src_orig = self.w_src
        self.moveLatentAndGenerate(self.w_src, self.direction, 0.0)

    def changeCoeff(self, params=None):
        print("changeCoeff ", params)
        attrName = params.attrName
        hasAttrChanged = False
        if attrName != self.selected_attr[:-4]:
            if attrName in self.attr_list:
                self.setNewAttr(attrName)
                hasAttrChanged = True
        else:
            hasAttrChanged = False
        coeffVal = float(params.coeff)
        self.moveLatentAndGenerate(self.w_src, self.direction, coeffVal, hasAttrChanged=hasAttrChanged)
    
    def changeFixedLayers(self, params=None):
        print("changeFixedLayers ", params)
        self.fixedLayerRanges = params.fix_layer_ranges
        # self.moveLatentAndGenerate(self.w_src, self.direction, 0.0)
    
    def clear(self, params=None):
        print("clear ", params)
        self.w_src = self.w_src_orig
        self.selected_attr = self.attr_list[0]+'.npy'
        self.direction = np.load('latent_directions/' + self.selected_attr)
        self.moveLatentAndGenerate(self.w_src, self.direction, 0.0)
###############################################################################################
    def setNewAttr(self, attrName):
        self.selected_attr = attrName+'.npy'
        self.direction = np.load('latent_directions/' + self.selected_attr)

    def moveLatentAndGenerate(self, latent_vector, direction, coeff, hasAttrChanged=False):
        coeff = -1 * coeff
        new_latent_vector = latent_vector.copy()
        minLayerIdx = self.fixedLayerRanges[0]
        maxLayerIdx = self.fixedLayerRanges[1]
        new_latent_vector[0][minLayerIdx:maxLayerIdx] = (latent_vector[0] + coeff*direction)[minLayerIdx:maxLayerIdx]
        if hasAttrChanged:
            self.w_src = new_latent_vector
        images = self.Gs.components.synthesis.run(new_latent_vector, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        # resImg.save("resImg.jpg") 
        self.broadcastImg(resImg, imgSize=self.img_size)

    def broadcastImg(self, img, imgSize=256, tag='type', filename='filename'):
        my_dpi = 96
        # img_size = (256,256)
        fig = plt.figure(figsize=(imgSize/my_dpi, imgSize/my_dpi), dpi=my_dpi)
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.imshow(img, cmap='plasma')
        # plt.show()
        mp_fig = mpld3.fig_to_dict(fig)
        plt.close('all')
        msg = {'action': 'sendImg', 'fig': mp_fig, 'tag': tag, 'filename': filename}
        self.broadcast(msg)
    
    def broadcast(self, msg):
        msg["id"] = 1
        workerCls.broadcast_event(msg)

    ################### Thread Methods ###################################
    def doWork(self, msg):
        if isinstance(msg, ED.EasyDict):
            self.call_func_names[msg.actionData.action](ED.EasyDict(msg.actionData.params))
        elif msg['action'] == 'initApp':
            self.initApp(msg['config'])
        elif msg['action'] == 'makeModel':
            self.makeModels()
        # elif msg['action'] == 'randomize':
        #     self.generateRandomSrcImg()