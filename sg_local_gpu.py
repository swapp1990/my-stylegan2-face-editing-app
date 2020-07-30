import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
import dnnlib.tflib as tflib
import dnnlib
import pretrained_networks
import numpy as np

executor = futures.ThreadPoolExecutor(max_workers=1)


class StyleGanGenerator(object):
    def __init__(self):
        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(
            func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        self.Gs_kwargs.randomize_noise = False
        self.Gs_kwargs.minibatch_size = 1
        self.truncation_psi = 0.5
        self.modelsBuilt = False
        self.cachedGallery = None

    def makeModels(self, params=None):
        if self.modelsBuilt:
            print("models already built")
            return
        _G, _D, self.Gs = pretrained_networks.load_networks(SG2_PKL_PATH)
        self.w_avg = self.Gs.get_var('dlatent_avg')
        print("made models ", self.w_avg.shape)
        self.modelsBuilt = True

    def generateRandomImages(self, batch_size=1):
        z = np.random.randn(batch_size, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        # print(G_imgs.shape)
        return G_imgs, w_src

    def generateImageFromWsrc(self, w_src):
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        # print(G_imgs.shape)
        return G_imgs

    def getRandomWSrc(self, batch_size=1):
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * (self.truncation_psi+0.1)
        return w_src

    def getCachedGallery(self, w_src):
        if self.cachedGallery is not None:
            return self.cachedGallery
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        return G_imgs


def testGenerator():
    gen = StyleGanGenerator()
    with ThreadPoolExecutor(max_workers=1) as executor:
        f_results = [executor.submit(gen.makeModels)]
        futures.wait(f_results)
        # print(f_results.)
        f_results = [executor.submit(gen.generateRandomImages)]
        futures.wait(f_results)
        gen_image = f_results[0].result()
        print("got image ", gen_image.shape)
