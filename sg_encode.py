import numpy as np
from matplotlib import pyplot as plt
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import os
import mpld3
import pickle
import gzip
from server.threads import Worker as workerCls
from easydict import EasyDict

network_pkl = 'cache/generator_model-stylegan2-config-f.pkl'
facial_attributes_list = 'https://drive.google.com/uc?id=1xMM3AFq0r014IIhBLiMCjKJJvbhLUQ9t'

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
        #Search
        # self.attr_labels = []
        # self.dlatent_to_labels = None
        self.savedAttrs = []

        self.img_size = 512
        self.fixedLayerRanges = [0,8]

        self.call_func_names = {
            'initApp': self.makeModels,
            'randomize': self.generateRandomSrcImg,
            'changeCoeff': self.changeCoeff,
            'changeFixedLayers': self.changeFixedLayers,
            'clear': self.clear,
            'sendSearchedImages': self.sendSearchedImages
        }

    ############################## Client Edit Actions #####################################
    def makeModels(self, params=None):
        _G, _D, self.Gs = pretrained_networks.load_networks(network_pkl)
        self.w_avg = self.Gs.get_var('dlatent_avg')
        print("made models ", self.w_avg.shape)
        
        self.direction = np.load('latent_directions/' + self.selected_attr)
        print("loaded latents ", self.direction.shape)

        self.loadAttributeLabelMapping()

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

    ############################## Client Search Actions #####################################
    def loadAttributeLabelMapping(self):
        pkl_file = open('results/savedAttr.pkl', 'rb')
        self.savedAttrs = pickle.load(pkl_file)
        print("loaded attributes mapping ", len(self.savedAttrs))
    
    def sendSearchedImages(self, params=None):
        searchTxt = "hair is gray"
        if params is not None:
            searchTxt = params.searchTxt.lower()
        attr_dict = self.getAttributesFromSearchtxt(searchTxt)
        attr_dict_keys = list(attr_dict.keys())
        print(attr_dict_keys, attr_dict)
        dlatent_added = []
        for i, l in enumerate(self.savedAttrs):
            # print(len(l['facesAttr']))
            if len(l['facesAttr']) > 0:
                l_dict = EasyDict(l['facesAttr'][0])
                if "hair" in attr_dict_keys:
                    hairColors = l_dict.faceAttributes.hair.hairColor
                    attr_vals = [attr_dict['hair']]
                    filtered_haircolors = [h for h in hairColors if h.color in attr_vals]
                    # print("filtered_haircolors ", filtered_haircolors)
                    for c in filtered_haircolors:
                        if c.confidence == 1.0:
                            dlatent = self.savedAttrs[i]['facesAttr']
                            dlatent_added.append(dlatent)
                    if len(dlatent_added) == 0:
                        for c in filtered_haircolors:
                            if c.confidence >= 0.9:
                                dlatent = self.savedAttrs[i]['facesAttr']
                                dlatent_added.append(dlatent)

        print("Found %d matching results" % len(dlatent_added))
        start_idx = np.random.randint(0, len(dlatent_added))
        print(start_idx)
        mini_batch_size = 1
        w_src = self.savedAttrs[start_idx]['wlatent']
        images = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        resImg.save("resImg.jpg")
        self.broadcastImg(resImg, imgSize=self.img_size, tag="search")
    
    def testRandomSavedAttribute(self):
        start_idx = np.random.randint(0, len(self.savedAttrs)-1)
        # print(start_idx)
        print(self.savedAttrs[start_idx]['facesAttr'])
        w_src = self.savedAttrs[start_idx]['wlatent']
        images = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        self.broadcastImg(resImg, imgSize=self.img_size, tag="search")

    def getAttributesFromSearchtxt(self, searchTxt):
        searchfor = ["hair", "haircolor"]
        matchingAttr = [s for s in searchfor if s in searchTxt]
        # print(matchingAttr)
        if "hair" in matchingAttr:
            searchfor = ["black", "brown", "blond", "red"]
            matchingAttrVal = [s for s in searchfor if s in searchTxt]
            # print(matchingAttr, matchingAttrVal)
        attr_dict = EasyDict({})
        for key, val in zip(matchingAttr, matchingAttrVal):
            attr_dict[key] = val
        return attr_dict

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

###############################################################################################
    def setNewAttr(self, attrName):
        self.selected_attr = attrName+'.npy'
        self.direction = np.load('latent_directions/' + self.selected_attr)

    def moveLatentAndGenerate(self, latent_vector, direction, coeff, hasAttrChanged=False):
        coeff = -1 * coeff
        new_latent_vector = latent_vector.copy()
        print(type(new_latent_vector), new_latent_vector.shape)
        minLayerIdx = self.fixedLayerRanges[0]
        maxLayerIdx = self.fixedLayerRanges[1]
        new_latent_vector[0][minLayerIdx:maxLayerIdx] = (latent_vector[0] + coeff*direction)[minLayerIdx:maxLayerIdx]
        if hasAttrChanged:
            self.w_src = new_latent_vector
        images = self.Gs.components.synthesis.run(new_latent_vector, **self.Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg = resImg.resize((self.img_size,self.img_size),PIL.Image.LANCZOS)
        resImg.save("resImg.jpg") 
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
        if isinstance(msg, EasyDict):
            self.call_func_names[msg.action](msg.params) 
        elif msg['action'] == 'initApp':
            self.initApp(msg['config'])
        elif msg['action'] == 'makeModel':
            self.makeModels()
        # elif msg['action'] == 'randomize':
        #     self.generateRandomSrcImg()

    ############### Main 
if __name__ == "__main__":
    sge = StyleGanEncoding()
    # sge.loadFaceAttributes()
    sge.makeModels()
    sge.loadAttributeLabelMapping()
    sge.sendSearchedImages()
    