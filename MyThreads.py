import uuid
from app.search import search
from server.threads import Worker as workerCls
from easydict import EasyDict
import dnnlib.tflib as tflib
import dnnlib
import pretrained_networks
import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import numpy as np
from traceback import print_exc
import pickle
import PIL.Image
import mpld3
from matplotlib import pyplot as plt
from sg_colab_server import StyleGanColab
from sg_local_gpu import StyleGanGenerator
import gallery
SG2_PKL_PATH = 'cache/generator_model-stylegan2-config-f.pkl'

executor = futures.ThreadPoolExecutor(max_workers=1)


def submitExecutor(func, *args, **kwargs):
    f = executor.submit(func, *args, **kwargs)
    error = f.exception()
    if error is not None:
        return
    # if f.result() == 1:
    #     print("success")
    # else:
    #     print("error")
    return f.result()


chats = []
cachedGallery = None
# main_generator = StyleGanGenerator()
main_generator = StyleGanColab(local=True)


class ClientThread():
    def __init__(self, threadId=0):
        self.IMG_SIZE = 512
        self.STYLEMIX_N = 4
        self.GALLERY_MAX = 10
        self.threadId = threadId
        self.username = "anon"
        self.call_func_names = {
            'setUser': self.setUser,
            'generateRandomImg': self.generateRandomImg,
            'gotRandomImages': self.gotRandomImages,
            'randomize': self.generateRandomImg,
            'changeCoeff': self.changeCoeff_clipped,
            'gotWsrcImage': self.gotWsrcImage,
            'gotStyleMixImages': self.gotStyleMixImages,
            'gotGalleryImages': self.gotGalleryImages,
            'gotSearchedImage': self.gotSearchedImage,
            'mixStyleImg': self.mixStyleImg,
            'sendSearchedImages': self.generateSearchedImgs,
            'lockStyle': self.lockStyle,
            'loveGalleryImage': self.loveGalleryImage,
            'saveLatent': self.saveLatent,
            'sendGallery': self.sendMainGallery,
            'sendStyleMixGallery': self.sendStyleMixGallery,
            'sendChat': self.gotNewChat,
            'sendChats': self.sendChats
        }

        # Attributes editing
        self.attr_list = ['smile', 'gender', 'age', 'beauty', 'glasses', 'race_black', 'race_yellow', 'emotion_fear', 'emotion_angry',
                          'emotion_disgust', 'emotion_easy', 'eyes_open', 'angle_horizontal', 'angle_pitch', 'face_shape', 'height', 'width']
        self.fixedLayerRanges = [0, 8]
        self.selected_attr = self.attr_list[0]
        self.direction = np.load(
            'latent_directions/' + self.selected_attr + '.npy')
        self.all_directions = {}
        self.w_src = None
        self.w_src_orig = None
        self.w_src_curr = None
        self.w_src_mix = None
        self.freezeIdxs = []

        self.stylemix_latents = []
        self.loadAllDirections()
    ############################## Colab Inference ###################

    def gotRandomImages(self, params=None):
        print("gotRandomImages ", params.keys())
        self.w_src = params.w_srcs
        self.w_src_orig = self.w_src
        self.w_src_curr = self.w_src
        # print("got images ", w_srcs.shape)

        mp_fig = self.processGeneratedImages(params.images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)

    def gotWsrcImage(self, params=None):
        print("gotWsrcImage ", params.keys())
        mp_fig = self.processGeneratedImages(params.images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)

    def gotStyleMixImages(self, params=None):
        print("gotStyleMixImages ", params.keys())
        self.stylemix_latents = params.w_srcs
        gen_images = self.processGeneratedImages(params.images)
        self.broadcastGalleryToClient(gen_images, tag='styleMixGallery')

    def gotGalleryImages(self, params=None):
        print("gotGalleryImages ", params.keys())
        gen_images = self.processGeneratedImages(params.images)
        metadata = gallery.getMetadataFromSaved(
            self.GALLERY_MAX, self.username)
        self.broadcastGalleryToClient(
            gen_images, metadata=metadata, tag='gallery')

    def gotSearchedImage(self, params=None):
        print("gotSearchedImage ", params.keys())
        mp_fig = self.processGeneratedImages(params.images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)
    ############################## Client Actions ###################

    def setUser(self, params=None):
        print("Thread setUser ", params)
        if params.username:
            self.username = params.username
        # f_results = [executor.submit(main_generator.makeModels)]
        # futures.wait(f_results)
        # print("built model ", self.username)

    def generateRandomImg(self, params=None):
        print("Thread generateRandomSrcImg ", params)

        # Commented: building on colab now
        # f_results = [executor.submit(main_generator.makeModels)]
        # futures.wait(f_results)
        # print("built model")

        # f_results = [executor.submit(
        #     main_generator.generateRandomImages, batch_size=1)]
        # futures.wait(f_results)
        # (gen_images, w_srcs) = f_results[0].result()
        # executor.submit(main_generator.generateRandomImages(
        #     self.threadId, batch_size=1))
        res = submitExecutor(main_generator.generateRandomImages,
                             self.threadId, 1)
        if res != 1:
            print("send error to client")
            self.broadcastRestErrorToClient()

    def generateSearchedImgs(self, params=None):
        searchTxt = params.text
        # Get ordered direction list
        dir_list_ordered = search.getDirListfromSearchTxt(searchTxt)
        # f_results = [executor.submit(main_generator.getRandomWSrc)]
        # futures.wait(f_results)
        # w_src = f_results[0].result()
        w_src = self.w_src
        for j, attr in enumerate(dir_list_ordered):
            direction = self.all_directions[attr['name']]
            coeff = attr['coeff']
            w_src = self.moveLatent_clipped(w_src, direction, coeff)

        # f_results = [executor.submit(
        #     main_generator.generateImageFromWsrc, self.threadId, w_src)]
        # futures.wait(f_results)
        # gen_images = f_results[0].result()
        self.w_src = w_src
        self.w_src_orig = self.w_src
        self.w_src_curr = self.w_src
        # mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        # self.broadcastImgToClient(mp_fig)

        executor.submit(main_generator.generateImageFromWsrc,
                        self.threadId, w_src=w_src, tag="forSearch")

    def changeCoeff_clipped(self, params=None):
        print("changeCoeff_clipped ", params)
        coeffVal = -float(params.coeff)
        attrName = params.name
        hasAttrChanged = False
        if attrName != self.selected_attr:
            if attrName in self.attr_list:
                self.setNewAttr(attrName)
                print("attr changed to " + attrName)
                hasAttrChanged = True
                self.w_src = self.w_src_curr
        else:
            hasAttrChanged = False
        self.w_src_curr = self.moveLatent_clipped(
            self.w_src, self.direction, coeffVal, hasAttrChanged=hasAttrChanged)

        # Old code directly sent the image to ui
        # f_results = [executor.submit(
        #     main_generator.generateImageFromWsrc, w_src=self.w_src_curr)]
        # futures.wait(f_results)
        # gen_images = f_results[0].result()

        # mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        # self.broadcastImgToClient(mp_fig)

        # new code sents request to colab, and colab sends image back as a post request
        res = submitExecutor(main_generator.generateImageFromWsrc, self.threadId,
                             w_src=self.w_src_curr)
        if res != 1:
            # Rest error
            self.broadcastRestErrorToClient()

    def mixStyleImg(self, params=None):
        selectedStyle = np.array(
            self.stylemix_latents[int(params.styleImgIdx)])
        w_src_curr = self.w_src_curr.copy()
        mixLayers = np.arange(0, 8)
        si = 0
        ei = 512
        layersMixMap = []
        if "layersMixMap" in params.keys():
            layersMixMap = params.layersMixMap
            mixLayers = []
            for l in layersMixMap:
                if l['checked'] == True:
                    mixLayers.append(int(l['id']))
            mixLayers = mixLayers
        for l in mixLayers:
            for idx in range(si, ei):
                w_src_curr[0][l][idx] = selectedStyle[l][idx]

        self.w_src_mix = w_src_curr
        # f_results = [executor.submit(
        #     main_generator.generateImageFromWsrc, w_src=w_src_curr)]
        # futures.wait(f_results)
        # gen_images = f_results[0].result()

        # mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        # self.broadcastImgToClient(mp_fig)
        res = submitExecutor(main_generator.generateImageFromWsrc, self.threadId,
                             w_src=w_src_curr)
        if res != 1:
            print("send error to client")

    def lockStyle(self, params=None):
        print("lockStyle")
        self.w_src = self.w_src_mix
        self.w_src_curr = self.w_src_mix

    # Gallery
    def sendStyleMixGallery(self, params=None):
        print("Thread sendStyleMixGallery ", params)
        # Old code for local
        # f_results = [executor.submit(
        #     main_generator.generateRandomImages, batch_size=self.STYLEMIX_N)]
        # futures.wait(f_results)
        # (gen_images, w_srcs) = f_results[0].result()
        # print("got images ", gen_images.shape)
        # self.stylemix_latents = w_srcs
        # gen_images = self.processGeneratedImages(gen_images)
        # self.broadcastGalleryToClient(gen_images, tag='styleMixGallery')

        # colab call
        res = submitExecutor(main_generator.generateRandomImages,
                             self.threadId, batch_size=self.STYLEMIX_N, tag="forStyleMix")
        if res != 1:
            print("send error to client")

    def sendMainGallery(self, params=None):
        print("Thread sendMainGallery ", params)
        w_srsc = gallery.loadGallery(self.GALLERY_MAX)
        # print(len(w_srsc))
        if len(w_srsc) > 0:
            res = submitExecutor(main_generator.generateImageFromWsrc, self.threadId,
                                 w_src=w_srsc, tag="forGallery")
            if res != 1:
                print("send error to client")

    def loveGalleryImage(self, params=None):
        print("Thread loveGalleryImage ", params)
        gallery.love(params, self.username)
        metadata = gallery.getMetadataFromSaved(
            self.GALLERY_MAX, self.username)
        self.broadcastGalleryMetadataToClient(metadata=metadata, tag='gallery')

    def saveLatent(self, params=None):
        currAttrDictToSave = {
            'idx': uuid.uuid4().hex, 'wlatent': self.w_src_curr, 'username': self.username, 'usersWhoLoved': [self.username]}
        gallery.saveLatent(currAttrDictToSave)
        self.sendMainGallery()

    # Chats
    def gotNewChat(self, params=None):
        print('gotNewChat ', params)
        global chats
        chats.append({'user': self.username, 'chatTxt': params.chatTxt})
        self.sendChats()

    def sendChats(self, params=None):
        global chats
        print("chats len ", len(chats))
        chats_to_send = chats.copy()
        chats_to_send.reverse()
        self.broadcastChatToClient(chats_to_send)
    ############################## Clipping W ###################################

    def moveLatent_clipped(self, latent_vector, direction, coeff, hasAttrChanged=False):
        if latent_vector is None:
            return None
        w_curr = latent_vector.copy()
        w_orig = latent_vector.copy()

        # Apply latent direction using the coeff value to the original w
        w_curr[0][0:18] = (latent_vector[0] + coeff*direction)[0:18]
        w_curr = self.clipW(w_orig, w_curr, hasAttrChanged=hasAttrChanged)
        return w_curr

    def clipW(self, w_orig, w_curr, hasAttrChanged=False):
        fig = plt.figure(figsize=(6, 4))
        y = np.arange(512)
        # Plot two graphs, original diff and after clipped diff

        mean1 = np.mean(w_orig[0], axis=0)
        mean2 = np.mean(w_curr[0], axis=0)
        w_diff = np.subtract(mean2, mean1)
        # Plot the original difference after latent direction is applied to w
        # axes = fig.add_subplot(2,1,1)
        # axes.plot(y, w_diff, 'r')

        # Clip top differences from the modified w
        pos_ix = self.getPossibleClippedIdxs(w_diff)
        n_layers = 18
        curr_freeze, all_freeze = self.getFreezeIdxs()
        # if not hasAttrChanged:
        curr_freeze = []
        overlapping_idxs = []
        # print("freezeIdxs ", self.freezeIdxs)
        for idx in range(512):
            if idx in pos_ix:
                if idx not in all_freeze:
                    curr_freeze.append(idx)
                else:
                    overlapping_idxs.append(idx)
            if idx in all_freeze:
                for l in range(n_layers):
                    w_curr[0][l][idx] = w_orig[0][l][idx]
        self.setFreezeIdxs(curr_freeze)
        # print("overlapping_idxs ", overlapping_idxs)
        # print("curr_freeze ", curr_freeze)

        mean2 = np.mean(w_curr[0], axis=0)
        w_diff = np.subtract(mean2, mean1)
        # Plot the clipped differences
        # axes = fig.add_subplot(2,1,2)
        # axes.plot(y, w_diff, 'r')
        # plt.savefig('results/resPlot.jpg')
        return w_curr

    def getPossibleClippedIdxs(self, w_diff):
        clipLimit = 0.5
        topIx = []
        botIx = []
        topIx = np.where(w_diff > clipLimit)[0]
        botIx = np.where(w_diff < -clipLimit)[0]
        ix = np.concatenate((topIx, botIx), axis=0)
        while ix.shape[0] == 0 and clipLimit > 0.06:
            clipLimit -= 0.05
            topIx = []
            botIx = []
            topIx = np.where(w_diff > clipLimit)[0]
            botIx = np.where(w_diff < -clipLimit)[0]
            ix = np.concatenate((topIx, botIx), axis=0)
        # print("ix len %d, clip limit %f"% (ix.shape[0], clipLimit))
        return ix

    def getFreezeIdxs(self):
        attrName = self.selected_attr
        currFreezeIdx = []
        allFreezeIdx = []
        found = False
        for idx_dict in self.freezeIdxs:
            currFreezeIdx = idx_dict['freeze']
            if idx_dict['name'] == attrName:
                found = True
            else:
                allFreezeIdx = allFreezeIdx + currFreezeIdx
        if not found:
            self.freezeIdxs.append({'name': attrName, 'freeze': []})
        # print(len(currFreezeIdx), len(allFreezeIdx))
        return currFreezeIdx, allFreezeIdx

    def setFreezeIdxs(self, idxs):
        attrName = self.selected_attr
        for idx_dict in self.freezeIdxs:
            if idx_dict['name'] == attrName:
                idx_dict['freeze'] = idxs

    def setNewAttr(self, attrName):
        self.selected_attr = attrName
        self.direction = np.load(
            'latent_directions/' + self.selected_attr + '.npy')

    def loadAllDirections(self):
        for a in self.attr_list:
            selectAttr = a+'.npy'
            direction = np.load('latent_directions/' + selectAttr)
            self.all_directions[a] = direction
    ########################## Image Utils ###################################

    def processGeneratedImages(self, images, returnAsList=True):
        if not returnAsList:
            resImg = PIL.Image.fromarray(images[0], 'RGB')
            resImg = resImg.resize(
                (self.IMG_SIZE, self.IMG_SIZE), PIL.Image.LANCZOS)
            mp_fig = self.getImageFig(resImg, self.IMG_SIZE)
            return mp_fig

        galleryImgs = []
        for idx in range(images.shape[0]):
            resImg = PIL.Image.fromarray(images[idx], 'RGB')
            resImg = resImg.resize(
                (self.IMG_SIZE, self.IMG_SIZE), PIL.Image.LANCZOS)
            mp_fig = self.getImageFig(resImg, self.IMG_SIZE)
            galleryImgs.append({'id': idx, 'mp_fig': mp_fig})
        return galleryImgs

    def getImageFig(self, img, imgSize=512):
        my_dpi = 96
        fig = plt.figure(figsize=(imgSize/my_dpi, imgSize/my_dpi), dpi=my_dpi)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.imshow(img, cmap='plasma')
        mp_fig = mpld3.fig_to_dict(fig)
        plt.close('all')
        return mp_fig
    ################### Client Broadcast #################################

    def broadcastImgToClient(self, mp_fig, tag='type'):
        payload = {'action': 'sendImg', 'fig': mp_fig, 'tag': tag}
        self.broadcastToClient(EasyDict(payload))

    def broadcastGalleryToClient(self, galleryImgs, metadata=None, tag='gallery'):
        # Final gallery payload to send to client
        payload = {'action': 'sendGallery', 'gallery': galleryImgs,
                   'metadata': metadata, 'tag': tag}
        broadcastToAll = True
        if tag == 'styleMixGallery':
            broadcastToAll = False
        # print("broadcastToClient ", broadcastToAll, tag)
        self.broadcastToClient(
            EasyDict(payload), broadcastToAll=broadcastToAll)

    def broadcastGalleryMetadataToClient(self, metadata, tag='gallery'):
        payload = {'action': 'sendGalleryMetadata',
                   'metadata': metadata, 'tag': tag}
        self.broadcastToClient(EasyDict(payload), broadcastToAll=False)

    def broadcastChatToClient(self, chats):
        payload = {'action': 'gotNewChat', 'chats': chats}
        self.broadcastToClient(EasyDict(payload), broadcastToAll=True)

    def broadcastRestErrorToClient(self):
        payload = {'action': 'gotRestError'}
        self.broadcastToClient(EasyDict(payload), broadcastToAll=False)

    def broadcastToClient(self, payload, broadcastToAll=False):
        payload.id = self.threadId
        payload.broadcastToAll = broadcastToAll
        workerCls.broadcast_event(payload)
    ################### Thread Methods ###################################
    # *Required

    def doWork(self, payload):
        assert(isinstance(payload, EasyDict))
        self.call_func_names[payload.action](payload.params)
