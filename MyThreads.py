# import queue
# import threading

# class SomeClass(threading.Thread):
#     def __init__(self, loop_time = 1.0/60):
#         self.mailbox = queue.Queue()
#         self.timeout = loop_time
#         super(SomeClass, self).__init__()

#     def onThread(self, function, *args, **kwargs):
#         self.mailbox.put((function, args, kwargs))

#     def run(self):
#         while True:
#             try:
#                 function, args, kwargs = self.mailbox.get(timeout=self.timeout)
#                 function(*args, **kwargs)
#             except queue.Empty:
#                 return

#     def idle(self):
#         # put the code you would have put in the `run` loop here 
#         print("idle")

#     def doSomething(self):
#         print("do something")

#         pass

#     def doSomethingElse(self):
#         print("do something else")
#         pass

# someClass = SomeClass()
# someClass.start()
# someClass.onThread(someClass.doSomething)
# someClass.onThread(someClass.doSomethingElse)
# someClass.onThread(someClass.doSomething)

import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import numpy as np
from traceback import print_exc
import pickle
import PIL.Image
import mpld3
from matplotlib import pyplot as plt
SG2_PKL_PATH = 'cache/generator_model-stylegan2-config-f.pkl'

import pretrained_networks
import dnnlib
import dnnlib.tflib as tflib
from easydict import EasyDict
from server.threads import Worker as workerCls
from app.search import search

executor = futures.ThreadPoolExecutor(max_workers=1)
chats = []

class StyleGanGenerator(object):
    def __init__(self):
        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
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
            return self.self.cachedGallery
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        return G_imgs

############ Test
def testGenerator():
    gen = StyleGanGenerator()
    with ThreadPoolExecutor(max_workers=1) as executor:
        f_results = [executor.submit(gen.makeModels)]
        concurrent.futures.wait(f_results)
        # print(f_results.)
        f_results = [executor.submit(gen.getRandomImage)]
        concurrent.futures.wait(f_results)
        gen_image = f_results[0].result()
        print("got image ", gen_image.shape)

# testGenerator()

main_generator = StyleGanGenerator()

#####################################################################################
class ClientThread():
    def __init__(self, threadId = 0):
        self.IMG_SIZE = 512
        self.STYLEMIX_N = 4
        self.GALLERY_MAX = 10
        self.threadId = threadId
        self.username = "anon"
        self.call_func_names = {
            'setUser': self.setUser,
            'generateRandomImg': self.generateRandomImg,
            'randomize': self.generateRandomImg,
            'changeCoeff': self.changeCoeff_clipped,
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

        #Attributes editing
        self.attr_list = ['smile', 'gender', 'age', 'beauty', 'glasses', 'race_black', 'race_yellow', 'emotion_fear', 'emotion_angry', 'emotion_disgust', 'emotion_easy', 'eyes_open', 'angle_horizontal', 'angle_pitch', 'face_shape', 'height', 'width']
        self.fixedLayerRanges = [0,8]
        self.selected_attr = self.attr_list[0]
        self.direction = np.load('latent_directions/' + self.selected_attr +'.npy')
        self.all_directions = {}
        self.w_src = None
        self.w_src_orig = None
        self.w_src_curr = None
        self.w_src_mix = None
        self.freezeIdxs = []

        self.stylemix_latents = []
        self.loadAllDirections()
    
    ############################## Client Actions ###################
    def setUser(self, params=None):
        print("Thread setUser ", params)
        if params.username:
            self.username = params.username
        f_results = [executor.submit(main_generator.makeModels)]
        futures.wait(f_results)
        print("built model ", self.username)
    
    def generateRandomImg(self, params=None):
        print("Thread generateRandomSrcImg ", params)

        f_results = [executor.submit(main_generator.makeModels)]
        futures.wait(f_results)
        print("built model")

        f_results = [executor.submit(main_generator.generateRandomImages, batch_size=1)]
        futures.wait(f_results)
        (gen_images, w_srcs) = f_results[0].result()
        self.w_src = w_srcs
        self.w_src_orig = self.w_src
        self.w_src_curr = self.w_src
        # print("got images ", w_srcs.shape)
        
        mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)
    
    def generateSearchedImgs(self, params=None):
        searchTxt = params.text
        #Get ordered direction list
        dir_list_ordered = search.getDirListfromSearchTxt(searchTxt)
        f_results = [executor.submit(main_generator.getRandomWSrc)]
        futures.wait(f_results)
        w_src = f_results[0].result()
        for j,attr in enumerate(dir_list_ordered):
            direction = self.all_directions[attr['name']]
            coeff = attr['coeff']
            w_src = self.moveLatent_clipped(w_src, direction, coeff)
        
        f_results = [executor.submit(main_generator.generateImageFromWsrc, w_src=w_src)]
        futures.wait(f_results)
        gen_images = f_results[0].result()
        self.w_src = w_src
        self.w_src_orig = self.w_src
        self.w_src_curr = self.w_src
        mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)

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
        f_results = [executor.submit(main_generator.generateImageFromWsrc, w_src=self.w_src_curr)]
        futures.wait(f_results)
        gen_images = f_results[0].result()

        mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)
    
    def mixStyleImg(self, params=None):
        selectedStyle = np.array(self.stylemix_latents[int(params.styleImgIdx)])
        w_src_curr = self.w_src_curr.copy()
        mixLayers = np.arange(0,8)
        si= 0
        ei= 512
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
        f_results = [executor.submit(main_generator.generateImageFromWsrc, w_src=w_src_curr)]
        futures.wait(f_results)
        gen_images = f_results[0].result()

        mp_fig = self.processGeneratedImages(gen_images, returnAsList=False)
        self.broadcastImgToClient(mp_fig)

    def lockStyle(self, params=None):
        print("lockStyle")
        self.w_src = self.w_src_mix
        self.w_src_curr = self.w_src_mix

    #### Gallery
    def sendStyleMixGallery(self, params=None):
        print("Thread sendStyleMixGallery ", params)
        f_results = [executor.submit(main_generator.generateRandomImages, batch_size=self.STYLEMIX_N)]
        futures.wait(f_results)
        (gen_images, w_srcs) = f_results[0].result()
        print("got images ", gen_images.shape)
        self.stylemix_latents = w_srcs
        gen_images = self.processGeneratedImages(gen_images)
        self.broadcastGalleryToClient(gen_images, tag='styleMixGallery')

    def sendMainGallery(self, params=None):
        print("Thread sendMainGallery ", params)
        pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
        savedAttrs = pickle.load(pkl_file)
        pkl_file.close()

        w_srsc = []
        for i in range(len(savedAttrs)):
            w_srsc.append(savedAttrs[i]['wlatent'])
        if len(w_srsc) == 0:
            print("No gallry found")
        if len(w_srsc) > 0:
            w_srsc.reverse()
            w_srsc = w_srsc[:self.GALLERY_MAX]
            w_srsc = np.asarray(w_srsc)
            w_srsc = np.squeeze(w_srsc, axis=1)
            f_results = [executor.submit(main_generator.getCachedGallery, w_src=w_srsc)]
            futures.wait(f_results)
            gen_images = f_results[0].result()
            print("Gallery ", gen_images.shape)

            gen_images = self.processGeneratedImages(gen_images)
            metadata = self.getMetadataFromSaved(savedAttrs)
            self.broadcastGalleryToClient(gen_images, metadata=metadata, tag='gallery')
    
    def getMetadataFromSaved(self, savedAttrs):
        metadata = []
        attrs = savedAttrs.copy()
        attrs.reverse()
        attrs = attrs[:self.GALLERY_MAX]
        for i in range(len(attrs)):
            md = EasyDict({})
            md.idx = attrs[i]["idx"]
            md.isCurrUserLoved = False
            if attrs[i].get("usersWhoLoved"):
                users = attrs[i]["usersWhoLoved"]
                md.totalLoved = len(users)
                if self.username in users:
                    md.isCurrUserLoved = True
            else:
                md.totalLoved = 0
            if attrs[i].get("username"):
                md.username = attrs[i]["username"]
            else:
                md.username = "unknown"
            metadata.append(md)
        return metadata

    def loveGalleryImage(self, params=None):
        print("Thread loveGalleryImage ", params)
        pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
        savedAttrs = pickle.load(pkl_file)
        pkl_file.close()

        idx = params.idx
        matches = [x for x in savedAttrs if x['idx']]
        isLoved = params.isLoved
        if isLoved:
            if matches[0].get('usersWhoLoved'):
                if self.username not in matches[0]['usersWhoLoved']:
                    matches[0]['usersWhoLoved'].append(self.username)
                    print(idx, matches[0]['usersWhoLoved'])
            else:
                matches[0]['usersWhoLoved'] = [self.username]
        else:
            if self.username in savedAttrs[idx]['usersWhoLoved']:
                matches[0]['usersWhoLoved'].remove(self.username)
        
        # print("usersWhoLoved ", matches[0]['usersWhoLoved'])
        
        output = open('results/savedAttrFromClient.pkl', 'wb')
        pickle.dump(savedAttrs, output)
        output.close()

        metadata = self.getMetadataFromSaved(savedAttrs)
        self.broadcastGalleryMetadataToClient(metadata=metadata, tag='gallery')
    
    def saveLatent(self, params=None):
        print('saveLatent')
        pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
        savedAttrs = pickle.load(pkl_file)
        pkl_file.close()
        
        print("Total gallery ", len(savedAttrs))
        self.currAttrDictToSave = {'idx': len(savedAttrs), 'wlatent': self.w_src_curr, 'username': self.username}
        savedAttrs.append(self.currAttrDictToSave)
        output = open('results/savedAttrFromClient.pkl', 'wb')
        pickle.dump(savedAttrs,output)
        output.close()

        sleep(0.5)
        self.sendMainGallery()

    #### Chats
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
    
    def setNewAttr(self, attrName):
        self.selected_attr = attrName
        self.direction = np.load('latent_directions/' + self.selected_attr +'.npy')
    
    def loadAllDirections(self):
        for a in self.attr_list:
            selectAttr = a+'.npy'
            direction = np.load('latent_directions/' + selectAttr)
            self.all_directions[a] = direction
    ########################## Image Utils ###################################
    def processGeneratedImages(self, images, returnAsList=True):
        if not returnAsList:
            resImg = PIL.Image.fromarray(images[0], 'RGB')
            resImg = resImg.resize((self.IMG_SIZE,self.IMG_SIZE),PIL.Image.LANCZOS)
            mp_fig = self.getImageFig(resImg, self.IMG_SIZE)
            return mp_fig

        galleryImgs = []
        for idx in range(images.shape[0]):
            resImg = PIL.Image.fromarray(images[idx], 'RGB')
            resImg = resImg.resize((self.IMG_SIZE,self.IMG_SIZE),PIL.Image.LANCZOS)
            mp_fig = self.getImageFig(resImg, self.IMG_SIZE)
            galleryImgs.append({'id': idx, 'mp_fig': mp_fig})
        return galleryImgs

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
    ################### Client Broadcast #################################
    def broadcastImgToClient(self, mp_fig, tag='type'):
        payload = {'action': 'sendImg', 'fig': mp_fig, 'tag': tag}
        self.broadcastToClient(EasyDict(payload))
    
    def broadcastGalleryToClient(self, galleryImgs, metadata=None, tag='gallery'):
        #Final gallery payload to send to client
        payload = {'action': 'sendGallery', 'gallery': galleryImgs, 'metadata': metadata, 'tag': tag}
        broadcastToAll = True
        if tag=='styleMixGallery':
            broadcastToAll = False
        print("broadcastToClient ", broadcastToAll, tag)
        self.broadcastToClient(EasyDict(payload), broadcastToAll=broadcastToAll)
    
    def broadcastGalleryMetadataToClient(self, metadata, tag='gallery'):
        payload = {'action': 'sendGalleryMetadata','metadata': metadata, 'tag': tag}
        self.broadcastToClient(EasyDict(payload), broadcastToAll=False)
    
    def broadcastChatToClient(self, chats):
        payload = {'action': 'gotNewChat', 'chats': chats}
        self.broadcastToClient(EasyDict(payload), broadcastToAll=True)

    def broadcastToClient(self, payload, broadcastToAll=False):
        payload.id = self.threadId
        payload.broadcastToAll = broadcastToAll
        workerCls.broadcast_event(payload)
    ################### Thread Methods ###################################
    #*Required
    def doWork(self, payload):
        assert(isinstance(payload, EasyDict))
        self.call_func_names[payload.action](payload.params)


###################
def resetSaved():
    pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
    savedAttrs = pickle.load(pkl_file)
    pkl_file.close()

    savedAttrs = []

    output = open('results/savedAttrFromClient.pkl', 'wb')
    pickle.dump(savedAttrs, output)
    output.close()

# resetSaved()

