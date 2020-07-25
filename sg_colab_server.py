import dynamo
import requests


class StyleGanColab():
    def __init__(self, local=False):
        if local:
            self.url = "http://localhost:5001"
        else:
            self.url = dynamo.get_bff_url()
        print("dynamo ", self.url)

    def sendMsgToColab(self, payload):
        url = self.url + "/msgFromMain"
        try:
            res = requests.post(url, json=payload)
            res = res.json()
        except:
            print("rest error")

    def generateRandomImages(self, threadId, batch_size=1, tag=""):
        self.sendMsgToColab(
            {"action": "generateRandomImages", "client_id": threadId, "batch_size": batch_size, "tag": tag})

    def generateImageFromWsrc(self, threadId, w_src, tag=""):
        self.sendMsgToColab({"action": "generateImgFromWSrc",
                             "client_id": threadId, "w_src": w_src.tolist(), "tag": tag})
