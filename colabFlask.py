import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import numpy as np
import os
from easydict import EasyDict
from flask import Flask, request
import time
import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import tensorflow as tf
import threading
import queue
active_queues = []
active_threads = []
SG2_PKL_PATH = 'cache/generator_model-stylegan2-config-f.pkl'

app = Flask(__name__)


@app.route("/generateRandomImages", methods=['POST'])
def generateRandomImages():
    msg = EasyDict({'id': 0, 'action': 'generateRandomImages', 'params': {}})
    broadcast_event(EasyDict(msg))
    return ""


class Worker(threading.Thread):
    def __init__(self, id, modelCls=None):
        threading.Thread.__init__(self)
        print("active_count ", threading.active_count())
        self.mailbox = queue.Queue()
        self.id = id
        self.modelCls = modelCls
        # print("thread ", self.id)
        active_queues.append(self.mailbox)
        active_threads.append(self)

    def run(self):
        while True:
            data = self.mailbox.get()
            print("run ", data)
            if data == 'shutdown':
                return
            if 'action' in data.keys():
                if self.id == data['id']:
                    if 'params' in data.keys():
                        self.modelCls.doWork(data)
            elif 'close' in data.keys():
                if self.id == data['id']:
                    self.stop()

    def stop(self):
        print("stop ", self.id)
        self.mailbox.put("shutdown")
        # self.join()
        active_queues.remove(self.mailbox)
        active_threads.remove(self)
        print("active_queues ", len(active_queues), "active_threads", len(
            active_threads), "active_count ", threading.active_count())


def clear():
    active_queues = []
    for t in active_threads:
        t.stop()
    print("cleared all threads", active_threads)


def broadcast_event(data):
    print(data)
    for q in active_queues:
        q.put(data)


class StyleGanGen():
    def __init__(self):
        self.call_func_names = {
            'makeModels': self.makeModels,
            'generateRandomImages': self.generateRandomImages
        }
        self.Gs = None
        self.Gs_kwargs = dnnlib.EasyDict()
        self.Gs_kwargs.output_transform = dict(
            func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        self.Gs_kwargs.randomize_noise = False
        self.Gs_kwargs.minibatch_size = 1
        self.truncation_psi = 0.5

    def makeModels(self, params=None):
        print('making models')
        _G, _D, self.Gs = pretrained_networks.load_networks(SG2_PKL_PATH)
        self.w_avg = self.Gs.get_var('dlatent_avg')
        print("made models ", self.w_avg.shape)

    def generateImgFromWSrc(self, params=None):
        print("generateImgFromWSrc ", params.keys())
        w_src = params.w_src
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        print("G_imgs ", G_imgs.shape)
        return G_imgs

    def generateRandomImages(self, params=None):
        print("generateRandomImages ", params.keys())
        batch_size = 1
        z = np.random.randn(batch_size, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        G_imgs = self.Gs.components.synthesis.run(w_src, **self.Gs_kwargs)
        print("G_imgs ", G_imgs.shape)
        return G_imgs, w_src

    def generateRandom(self):
        z = np.random.randn(1, *self.Gs.input_shape[1:])
        w_src = self.Gs.components.mapping.run(z, None)
        w_src = self.w_avg + (w_src - self.w_avg) * self.truncation_psi
        # w_src = np.squeeze(w_src)
        images = self.generateImgFromWSrc(EasyDict({"w_src": w_src}))
        # save_images(images)

    def doWork(self, payload):
        assert(isinstance(payload, EasyDict))
        self.call_func_names[payload.action](payload.params)


sge = StyleGanGen()
threadMain = Worker(0, sge)
threadMain.setDaemon(True)
threadMain.start()
# time.sleep(1)
msg = EasyDict({'id': 0, 'action': 'makeModels', 'params': {}})
broadcast_event(EasyDict(msg))

app.run(threaded=True)
