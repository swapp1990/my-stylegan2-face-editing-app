import numpy as np
from matplotlib import pyplot as plt
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import os
import json
import mpld3
import pickle
import gzip
import time

from server.threads import Worker as workerCls
from app.search import search
from easydict import EasyDict
import faceMicrosoft as faceMicro

network_pkl = 'cache/generator_model-stylegan2-config-f.pkl'
facial_attributes_list = 'https://drive.google.com/uc?id=1xMM3AFq0r014IIhBLiMCjKJJvbhLUQ9t'

class SGEThread():
    def __init__(self, threadId = 0):
        self.attr_list = ['smile', 'gender', 'age', 'beauty', 'glasses', 'race_black', 'race_yellow', 'emotion_fear', 'emotion_angry', 'emotion_disgust', 'emotion_easy', 'eyes_open', 'angle_horizontal', 'angle_pitch', 'face_shape', 'height', 'width']
        self.fixedLayerRanges = [0,8]
        self.img_size = 512

        self.selected_attr = self.attr_list[0]
        self.threadId = threadId

        self.w_src = None
        self.w_src_orig = None
        self.w_src_curr = None
        self.freezeIdxs = []
    
        self.call_func_names = {
            'generateRandomImg': self.generateRandomSrcImg,
            'randomize': self.generateRandomSrcImg,
            'changeCoeff': self.changeCoeff_clipped,
            'clear': self.clear,
            'sendSearchedImages': self.generateSearchedImgs,
            'saveLatent': self.saveLatent,
            'mixStyleImg': self.mixStyleImg,
            'send_wSrc': self.got_wSrc,
            'send_GImgs': self.got_GImgs,
            'send_Img_W': self.got_Img_W,
            'send_stylemix_imgs': self.got_stylemix
        }
        
        self.direction = np.load('latent_directions/' + self.selected_attr +'.npy')
        self.stylemix_latents = []
        self.sendStyleMixGallery()

    ############################## Client Edit Actions ###################
    def generateRandomSrcImg(self, params=None):
        print("Thread generateRandomSrcImg ", params)
        outParams = EasyDict({})
        self.broadcastToMainThread("runRandomMapping", outParams)
        self.sendSavedGallery()
    
    def got_wSrc(self, params=None):
        print("Thread got_wSrc ", params.keys())
        self.w_src = params.w_src
        self.w_src_orig = self.w_src
        self.w_src_curr = self.w_src
        self.moveLatent(self.w_src, self.direction, 0.0)
    
    def got_GImgs(self, params=None):
        print("Thread got_GImgs ", params.keys())
        g_images = params.G_imgs
        if "tag" in params.keys():
            if params.tag == "gallery":
                self.sendGalleryToClient(g_images)
        else:
            resImg = PIL.Image.fromarray(g_images[0], 'RGB')
            resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
            self.broadcastImgToClient(resImg, imgSize=self.img_size)
    
    def got_Img_W(self, params=None):
        print("Thread got_GImgs ", params.keys())
        self.w_src = params.w_src
        self.w_src_curr = params.w_src
        g_images = params.G_imgs
        resImg = PIL.Image.fromarray(g_images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        self.broadcastImgToClient(resImg, imgSize=self.img_size)
    
    def got_stylemix(self, params=None):
        print("Thread got_stylemix ", params.keys())
        g_images = params.imgs
        self.stylemix_latents = params.stylemix_latents
        self.sendGalleryToClient(g_images, tag='styleMixGallery')

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
        self.w_src_curr = self.moveLatent_clipped(self.w_src, self.direction, coeffVal, hasAttrChanged=hasAttrChanged)
        outParams = EasyDict({"w_src": self.w_src_curr})
        self.broadcastToMainThread("generateImgFromWSrc", outParams)
    
    def clear(self, params=None):
        print("clear ", params)
        self.w_src = self.w_src_orig
        self.w_src_curr = self.w_src_orig
        self.selected_attr = self.attr_list[0]
        self.direction = np.load('latent_directions/' + self.selected_attr + '.npy')
        self.moveLatent(self.w_src, self.direction, 0.0)
        self.freezeIdxs = []
    
    def generateSearchedImgs(self, params=None):
        searchTxt = params.text
        #Get ordered direction list
        dir_list_ordered = search.getDirListfromSearchTxt(searchTxt)
        outParams = EasyDict({})
        outParams.dir_list_ordered = dir_list_ordered
        self.broadcastToMainThread("generateSearchedImgs", outParams)

    def saveLatent(self, params=None):
        print('saveLatent')
        pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
        savedAttrs = pickle.load(pkl_file)
        pkl_file.close()
        
        self.currAttrDictToSave = {'wlatent': self.w_src_curr}
        savedAttrs.append(self.currAttrDictToSave)
        output = open('results/savedAttrFromClient.pkl', 'wb')
        pickle.dump(savedAttrs,output)
        output.close()

        time.sleep(0.5)
        self.sendSavedGallery()
  
    def sendStyleMixGallery(self):
        outParams = EasyDict({})
        self.broadcastToMainThread("generateStylemixGalleryImages", outParams)

    def mixStyleImg(self, params=None):
        outParams = EasyDict({})
        outParams.selectedStyle = np.array(self.stylemix_latents[int(params.styleImgIdx)])
        outParams.w_src_curr = self.w_src_curr
        outParams.mixLayers = [0,8]
        outParams.mixIdx = [0, 512]
        self.broadcastToMainThread("generateStyleMixedImg", outParams)

    ############################## Clipping W ###################################
    def moveLatent_clipped(self,latent_vector, direction,coeff, hasAttrChanged=False):
        w_curr = latent_vector.copy()
        w_orig = latent_vector.copy()
        
        #Apply latent direction using the coeff value to the original w
        w_curr[0][0:18] = (latent_vector[0] + coeff*direction)[0:18]
        w_curr = self.clipW(w_orig, w_curr, hasAttrChanged=hasAttrChanged)
        return w_curr

    def clipW(self, w_orig, w_curr, hasAttrChanged=False):
        fig = plt.figure(figsize=(6, 4))
        y = np.arange(512)
        #Plot two graphs, original diff and after clipped diff
        
        mean1 = np.mean(w_orig[0], axis=0)
        mean2 = np.mean(w_curr[0], axis=0)
        w_diff = np.subtract(mean2, mean1)
        #Plot the original difference after latent direction is applied to w
        # axes = fig.add_subplot(2,1,1)
        # axes.plot(y, w_diff, 'r')

        #Clip top differences from the modified w
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
        #Plot the clipped differences
        # axes = fig.add_subplot(2,1,2)
        # axes.plot(y, w_diff, 'r')
        # plt.savefig('results/resPlot.jpg')
        return w_curr

    def getPossibleClippedIdxs(self, w_diff):
        clipLimit = 0.5
        topIx = []
        botIx = []
        topIx = np.where(w_diff>clipLimit)[0]
        botIx = np.where(w_diff<-clipLimit)[0]
        ix = np.concatenate((topIx, botIx), axis=0)
        while ix.shape[0] == 0 and clipLimit >0.06:
            clipLimit -= 0.05
            topIx = []
            botIx = []
            topIx = np.where(w_diff>clipLimit)[0]
            botIx = np.where(w_diff<-clipLimit)[0]
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
    ############################## Utils ########################################
    # Move latent vector to a selected attribute direction using coeff value
    def moveLatent(self, latent_vector, direction, coeff, hasAttrChanged=False):
        coeff = -1 * coeff
        new_latent_vector = latent_vector.copy()
        minLayerIdx = self.fixedLayerRanges[0]
        maxLayerIdx = self.fixedLayerRanges[1]
        new_latent_vector[0][minLayerIdx:maxLayerIdx] = (latent_vector[0] + coeff*direction)[minLayerIdx:maxLayerIdx]
        if hasAttrChanged:
            self.w_src = new_latent_vector
        self.w_src_curr = new_latent_vector

        outParams = EasyDict({"w_src": new_latent_vector})
        self.broadcastToMainThread("generateImgFromWSrc", outParams)

    def setNewAttr(self, attrName):
        self.selected_attr = attrName
        self.direction = np.load('latent_directions/' + self.selected_attr +'.npy')

    def sendSavedGallery(self):
        pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
        savedAttrs = pickle.load(pkl_file)
        pkl_file.close()

        w_srsc = []
        for i in range(len(savedAttrs)):
            w_srsc.append(savedAttrs[i]['wlatent'])
        if len(w_srsc) > 0:
            w_srsc = np.asarray(w_srsc)
            w_srsc = np.squeeze(w_srsc, axis=1)
            outParams = EasyDict({"w_src": w_srsc, "tag": "gallery"})
            self.broadcastToMainThread("generateImgFromWSrc", outParams)

    def sendGalleryToClient(self, images, tag='gallery'):
        galleryImgs = []
        for idx in range(images.shape[0]):
            resImg = PIL.Image.fromarray(images[idx], 'RGB')
            resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
            mp_fig = self.getImageFig(resImg)
            galleryImgs.append({'id': idx, 'mp_fig': mp_fig})
        payload = {'action': 'sendGallery', 'gallery': galleryImgs, 'tag': tag}
        self.broadcastToClient(EasyDict(payload))

    def getImageFig(self, img, imgSize=512):
        my_dpi = 96
        fig = plt.figure(figsize=(imgSize/my_dpi, imgSize/my_dpi), dpi=my_dpi)
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.imshow(img, cmap='plasma')
        mp_fig = mpld3.fig_to_dict(fig)
        plt.close('all')
        return mp_fig

    def broadcastImgToClient(self, img, imgSize=256, tag='type', filename='filename'):
        # img.save("results/clientImg.jpg")
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
        payload = {'action': 'sendImg', 'fig': mp_fig, 'tag': tag, 'filename': filename}
        self.broadcastToClient(EasyDict(payload))
    
    def broadcastToClient(self, payload, broadcastToAll=False):
        payload.id = self.threadId
        payload.broadcastToAll = broadcastToAll
        workerCls.broadcast_event(payload)
    
    def broadcastToMainThread(self, action, params):
        msg = EasyDict({})
        msg.action = action
        msg.id = 0
        params.clientSessId = self.threadId
        msg.params = params
        workerCls.broadcast_event(msg)

    ################### Thread Methods ###################################
    def doWork(self, payload):
        assert(isinstance(payload, EasyDict))
        self.call_func_names[payload.action](payload.params)

class StyleGanEncoding():
    def __init__(self):
        self.threadId = 0
        self.Gs = None

        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        self.Gs_kwargs.randomize_noise = False
        self.Gs_kwargs.minibatch_size = 1

        self.truncation_psi = 0.5
        self.attr_list = ['smile', 'gender', 'age', 'beauty', 'glasses', 'race_black', 'race_yellow', 'emotion_fear', 'emotion_angry', 'emotion_disgust', 'emotion_easy', 'eyes_open', 'angle_horizontal', 'angle_pitch', 'face_shape', 'height', 'width']
        self.selected_attr = self.attr_list[0] +'.npy'

        self.direction = None
        self.all_directions = {}
        self.w_avg = None
        self.w_src = None
        self.w_src_orig = None
        self.w_src_curr = None
        #Search
        # self.attr_labels = []
        # self.dlatent_to_labels = None
        self.savedAttrs = []
        self.currAttrDictToSave = {}
        self.freezeIdxs = []

        self.img_size = 512
        self.fixedLayerRanges = [0,8]

        self.call_func_names = {
            'initApp': self.makeModels,
            'runRandomMapping': self.runRandomMapping,
            'generateImgFromWSrc': self.generateImgFromWSrc,
            'generateSearchedImgs': self.generateSearchedImgs,
            'generateStylemixGalleryImages': self.generateStylemixGalleryImages,
            'generateStyleMixedImg': self.generateStyleMixedImg,
            'getAttributes': self.getAttributes,
        }
        
    ############################## Client Edit Actions #####################################
    def makeModels(self, params=None):
        _G, _D, self.Gs = pretrained_networks.load_networks(network_pkl)
        self.w_avg = self.Gs.get_var('dlatent_avg')
        print("made models ", self.w_avg.shape)
        
        self.direction = np.load('latent_directions/' + self.selected_attr)
        print("loaded latents ", self.direction.shape)

        self.loadAttributeLabelMapping()
        self.loadAllDirections()
        self.resetSavedLatents()
    
    def runRandomMapping(self, params=None):
        print("runRandomMapping ", params)
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        msg = {'action': 'send_wSrc', 'params': {'w_src': w_src}}
        self.broadcastToThread(EasyDict(msg), params.clientSessId)
    
    def generateImgFromWSrc(self, params=None):
        print("generateImgFromWSrc ", params.keys())
        w_src = params.w_src
        if "tag" in params.keys():
            if params.tag == "gallery":
                G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
                msg = {'action': 'send_GImgs', 'params': {'G_imgs': G_imgs, 'tag': params.tag}}
        else:
            G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
            msg = {'action': 'send_GImgs', 'params': {'G_imgs': G_imgs}}
       
        self.broadcastToThread(EasyDict(msg), params.clientSessId)

    def generateSearchedImgs(self, params=None):
        print("generateSearchedImgs ", params.keys())
        dir_list_ordered = params.dir_list_ordered
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        w_src_orig = w_src.copy()
        for j,attr in enumerate(dir_list_ordered):
            direction = self.all_directions[attr['name']]
            coeff = attr['coeff']
            w_src = self.moveLatent_clipped(w_src, direction, coeff)
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        msg = {'action': 'send_Img_W', 'params': {'G_imgs': G_imgs, 'w_src': w_src}}
        self.broadcastToThread(EasyDict(msg), params.clientSessId)
    
    def moveLatent_clipped(self,latent_vector, direction,coeff, hasAttrChanged=False):
        w_curr = latent_vector.copy()
        w_orig = latent_vector.copy()
        
        #Apply latent direction using the coeff value to the original w
        w_curr[0][0:18] = (latent_vector[0] + coeff*direction)[0:18]
        w_curr = self.clipW(w_orig, w_curr)
        return w_curr
    
    def clipW(self, w_orig, w_curr):
        mean1 = np.mean(w_orig[0], axis=0)
        mean2 = np.mean(w_curr[0], axis=0)
        w_diff = np.subtract(mean2, mean1)

        #Clip top differences from the modified w
        pos_ix = self.getPossibleClippedIdxs(w_diff)
        n_layers = 18
        all_freeze = []
        curr_freeze = []
        overlapping_idxs = []
        for idx in range(512):
            if idx in pos_ix:
                if idx not in all_freeze:
                    curr_freeze.append(idx)
                else:
                    overlapping_idxs.append(idx)
            if idx in all_freeze:
                for l in range(n_layers):
                    w_curr[0][l][idx] = w_orig[0][l][idx]
        return w_curr
    
    def getPossibleClippedIdxs(self, w_diff):
        clipLimit = 0.5
        topIx = []
        botIx = []
        topIx = np.where(w_diff>clipLimit)[0]
        botIx = np.where(w_diff<-clipLimit)[0]
        ix = np.concatenate((topIx, botIx), axis=0)
        while ix.shape[0] == 0 and clipLimit >0.06:
            clipLimit -= 0.05
            topIx = []
            botIx = []
            topIx = np.where(w_diff>clipLimit)[0]
            botIx = np.where(w_diff<-clipLimit)[0]
            ix = np.concatenate((topIx, botIx), axis=0)
        # print("ix len %d, clip limit %f"% (ix.shape[0], clipLimit))
        return ix

    def changeFixedLayers(self, params=None):
        print("changeFixedLayers ", params)
        self.fixedLayerRanges = params.fix_layer_ranges
        # self.moveLatentAndGenerate(self.w_src, self.direction, 0.0)

    def getAttributes(self, params=None):
        print('getAttributes')
        self.currAttrDictToSave = faceMicro.callApi(self.w_src_curr)
        msg = {'action': 'sendAttr', 'attr': self.currAttrDictToSave['facesAttr']}
        self.broadcast(msg)

    def generateStylemixGalleryImages(self, params=None):
        print("sendStylemixGalleryImages")
        stylemix_latents = []
        for i in range(4):
            z = np.random.randn(1, *self.Gs.input_shape[1:])
            w_src = self.Gs.components.mapping.run(z, None)
            w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
            w_src = np.squeeze(w_src)
            stylemix_latents.append(w_src)
        stylemix_latents = np.array(stylemix_latents)
        print("stylemix_latents ", stylemix_latents.shape)
        images = self.Gs.components.synthesis.run(stylemix_latents, **self.Gs_kwargs)
        msg = {'action': 'send_stylemix_imgs', 'params': {'imgs': images, 'stylemix_latents': stylemix_latents}}
        self.broadcastToThread(EasyDict(msg), params.clientSessId)

    ############################## Client Search Actions #####################################
    def loadAttributeLabelMapping(self):
        pkl_file = open('results/savedAttr.pkl', 'rb')
        self.savedAttrs = pickle.load(pkl_file)
        print("loaded attributes mapping ", len(self.savedAttrs))

    def loadAllDirections(self):
        for a in self.attr_list:
            selectAttr = a+'.npy'
            direction = np.load('latent_directions/' + selectAttr)
            self.all_directions[a] = direction

    def getImageByText(self, text=""):
        dir_list_ordered = search.getDirListfromSearchTxt(text)
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        path = "results/mix/"
        for j,attr in enumerate(dir_list_ordered):
            self.selected_attr = attr['name']+'.npy'
            direction = self.all_directions[attr['name']]
            coeff = attr['coeff']
            filename = path+ attr['name'] + str(j) + ".jpg"
            resImg, w_src = self.moveLatent_clipped(w_src, direction, coeff, filename=filename)
            # print(attr['name'], self.freezeIdxs)
        return resImg, w_src
    #Testing
    def getSearchImage(self):
        mini_bs = 1
        w_src_all = []
        
        dir_list = [{'name': 'smile', 'coeff': -5.5, 'order': 1},
                    {'name': 'gender', 'coeff': 16.5, 'order': 0},
                    {'name': 'race_black', 'coeff': 3.0, 'order': 2},
                    {'name': 'age', 'coeff': -5.5, 'order': 3}]
        dir_list_ordered = sorted(dir_list, key=lambda k: k['order'])
        # print(dir_list_ordered)
        
        fig = plt.figure(figsize=(6, 4))
        
        np.random.seed(10)
        for i in range(mini_bs):
            z = np.random.randn(1, *self.Gs.input_shape[1:])
            w_src = self.Gs.components.mapping.run(z, None)
            w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
            w_src_orig = w_src.copy()
            for j,attr in enumerate(dir_list_ordered):
                direction = self.all_directions[attr['name']]
                coeff = attr['coeff']
                w_src = self.moveLatent_clipped(w_src, direction, coeff)

            w_src_all.append(w_src)
        
        # plt.savefig('resPlot.jpg')
        w_src_all = np.stack(w_src_all, axis=1)
        self.Gs_kwargs.minibatch_size = mini_bs
        images = self.Gs.components.synthesis.run(w_src_all[0], **self.Gs_kwargs)
        # print(images.shape)
        canvas = PIL.Image.new('RGB', (512*mini_bs, 512), 'white')
        for (i,img) in enumerate(images):
            resImg = PIL.Image.fromarray(img, 'RGB')
            resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
            canvas.paste(resImg, (512*i,0))
        canvas.save("g_img.jpg")
            # self.broadcastImg(img)

    def testRandomSavedAttribute(self):
        start_idx = np.random.randint(0, len(self.savedAttrs)-1)
        # print(start_idx)
        # print(self.savedAttrs[start_idx]['facesAttr'])
        w_src = self.savedAttrs[start_idx]['wlatent']
        images = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        self.broadcastImg(resImg, imgSize=self.img_size, tag="search")

    #Testing
    def loadFaceAttributes(self):
        with dnnlib.util.open_url(facial_attributes_list, cache_dir='cache') as f:
            qlatent_data, dlatent_data, labels_data = pickle.load(gzip.GzipFile(fileobj=f))
        # print(labels_data[0])
        dlatent_added = []
        for i, l in enumerate(labels_data):
            # if i == 0:
            l_dict = EasyDict(l)
            hairColors = l_dict.faceAttributes.hair.hairColor
            for c in hairColors:
                if c.confidence == 1.0:
                    if c.color == 'brown':
                        dlatent_added.append(dlatent_data[i])
        # print(len(dlatent_added))
        print(dlatent_added[0].shape)
        _G, _D, self.Gs = pretrained_networks.load_networks(network_pkl)
        new_latent_vector = np.array(dlatent_added[:2])
        print(new_latent_vector.shape)
        images = self.Gs.components.synthesis.run(new_latent_vector, **self.Gs_kwargs)
        print(images.shape)
        # canvas = PIL.Image.new('RGB', (1024*2, 1024), 'white')
        # image_iter = iter(list(images))
        # for i in range(len(list(images))):
        #     image = PIL.Image.fromarray(next(image_iter), 'RGB')
        #     canvas.paste(image, (0*i,0))
        # canvas.save('resimg.jpg')
        resImg = PIL.Image.fromarray(images[1], 'RGB')
        # resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        resImg.save("resImg.jpg") 

    ############################# Style Mixing ###############################################
    def generateStyleMixedImg(self, params):
        print("sendStyleMixedImg ", params.keys())
        selectedStyle = params.selectedStyle
        sl = params.mixLayers[0]
        el = params.mixLayers[1]
        si= params.mixIdx[0]
        ei= params.mixIdx[1]
        w_src_curr = params.w_src_curr
        for idx in range(si, ei):
            for l in range(sl,el):
                w_src_curr[0][l][idx] = selectedStyle[l][idx]
        images = self.Gs.components.synthesis.run(w_src_curr, **self.Gs_kwargs)
        msg = {'action': 'send_Img_W', 'params': {'G_imgs': images, 'w_src': w_src_curr}}
        self.broadcastToThread(EasyDict(msg), params.clientSessId)

    #Testing
    def doStyleMixing(self, si=0, ei=512):
        print(si, ei)
        sl = 0
        el = 18
        path = "results/mix/"
        img, w_src_1 = self.getImageByText("black man")
        img.save(path+"img1.jpg")
        img, w_src_2 = self.getImageByText("white woman")
        img.save(path+"img2.jpg")

        w_src_1c = w_src_1.copy()
        w_src_2c = w_src_2.copy()
        for idx in range(si, ei):
            for l in range(sl,el):
                w_src_1c[0][l][idx] = w_src_2c[0][l][idx]

        images = self.Gs.components.synthesis.run(w_src_1c, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        resImg.save(path+"img4.jpg")

###############################################################################################
    def broadcast(self, msg):
        msg.id = self.threadId
        workerCls.broadcast_event(msg)
    
    def broadcastToThread(self, msg, threadId):
        msg.id = threadId
        workerCls.broadcast_event(msg)

    def sendTest(self):
        msg = {'action': 'testAction'}
        self.broadcast(msg)
            
    def resetSavedLatents(self):
        savedDicts = []
        output = open('results/savedAttrFromClient.pkl', 'wb')
        pickle.dump(savedDicts,output)
        output.close()
    ################### Thread Methods ###################################
    def doWork(self, payload):
        assert(isinstance(payload, EasyDict))
        self.call_func_names[payload.action](payload.params)

    ############### Main 
if __name__ == "__main__":
    sge = StyleGanEncoding()
    # sge.loadFaceAttributes()
    sge.makeModels()
    # sge.loadAttributeLabelMapping()
    sge.loadAllDirections()
    # sge.getSearchImage()

    # sge.sendSearchedImages(EasyDict({"text": "a older smiling black girl"}))
    # sge.getDirListfromSearchTxt("a young black girl")
    # sge.getDirListfromSearchTxt("a older white man")

    sge.doStyleMixing()
    # sge.getImageByText("older smiling black man")
    
    # params = EasyDict({'name': 'gender', 'coeff': '-5.75', 'clipTop': True, 'clipBottom': True, 'clipLimit': 0.1})
    # sge.changeCoeff_clipped(params)
    # params = EasyDict({'name': 'smile', 'coeff': '4.75', 'clipTop': True, 'clipBottom': True, 'clipLimit': 0.1})
    # sge.changeCoeff_clipped(params)
    # params = EasyDict({'name': 'race_black', 'coeff': '-8', 'clipTop': True, 'clipBottom': True, 'clipLimit': 0.3})
    # sge.changeCoeff_clipped(params)