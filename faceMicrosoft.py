
import requests
import numpy as np
from matplotlib import pyplot as plt
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import os
import pickle
import time

subscription_key = "dc6cd846e6394578aa43a2a1e713626b"
assert subscription_key

face_api_url = 'https://westus2.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://how-old.net/Images/faces2/main007.jpg'
network_pkl = 'cache/generator_model-stylegan2-config-f.pkl'

headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

Gs_kwargs = dnnlib.EasyDict()
Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
Gs_kwargs.randomize_noise = False
Gs_kwargs.minibatch_size = 1

truncation_psi = 0.9

def openSavedAttr():
    _G, _D, Gs = pretrained_networks.load_networks(network_pkl)
    pkl_file = open('results/savedAttr.pkl', 'rb')
    mydictlist = pickle.load(pkl_file)
    pkl_file.close()
    # print(mydictlist)
    idx = 10
    w_src = mydictlist[idx]['wlatent']
    print(w_src.shape)
    print(mydictlist[idx]['facesAttr'])
    images = Gs.components.synthesis.run(w_src, **Gs_kwargs)
    resImg = PIL.Image.fromarray(images[0], 'RGB')
    resImg.save("resImg2.jpg")

def saveAttrtoPkl():
    _G, _D, Gs = pretrained_networks.load_networks(network_pkl)
    w_avg = Gs.get_var('dlatent_avg')
    randomLatentsSize = 5000
    headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    savedDicts = []
    for i in range(randomLatentsSize):
        print("Saving ", i)
        if i%50 == 0:
            time.sleep(2.4)
            output = open('results/savedAttr.pkl', 'wb')
            pickle.dump(savedDicts,output)
            output.close()
            print("Saved pickle")
        z = np.random.randn(1, *Gs.input_shape[1:])
        w_src = Gs.components.mapping.run(z, None)
        w_src = w_avg + (w_src - w_avg) * truncation_psi
        images = Gs.components.synthesis.run(w_src, **Gs_kwargs)
        resImg = PIL.Image.fromarray(images[0], 'RGB')
        resImg.save("resImg.jpg")
        image_data = open("resImg.jpg", "rb")
        response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
        response.raise_for_status()
        facesAttr = response.json()
        mydict = {'facesAttr': facesAttr, 'wlatent': w_src}
        savedDicts.append(mydict)
    output = open('results/savedAttr.pkl', 'wb')
    pickle.dump(savedDicts,output)
    output.close()
    print("Saved Faces Attr")

# openSavedAttr()
saveAttrtoPkl()