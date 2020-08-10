import dynamo
import requests
import mysocket
import json


class StyleGanColab():
    def __init__(self, local=False):
        if local:
            self.url = "http://localhost:5001"
        else:
            self.url = dynamo.get_bff_url()
        print("dynamo ", self.url)
        # self.pingColab()

    def update_url(self):
        # Dynamo should be updated with the latest colab url
        self.url = dynamo.get_bff_url()
        print("url updated ", self.url)
        self.pingColab()

    def pingColab(self):
        url = self.url + "/ping"
        try:
            res = requests.get(url, json={})
            res = res.json()
        except requests.ConnectionError as e:
            print("connection error ", e)
            mysocket.main.emailError(e)
            return 0
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError error ", e)
            # mysocket.main.emailError(e)
            return 0
        except Exception as e:
            print("Other error ", e)
            mysocket.main.emailError(e)
            return 0
        return 1

    def sendMsgToColab(self, payload):
        url = self.url + "/msgFromMain"
        try:
            res = requests.post(url, json=payload)
            res = res.json()
            return 1
        except:
            print("rest error")
            return 0

    def generateRandomImages(self, threadId, batch_size=1, tag=""):
        return self.sendMsgToColab(
            {"action": "generateRandomImages", "client_id": threadId, "batch_size": batch_size, "tag": tag})

    def generateImageFromWsrc(self, threadId, w_src, tag=""):
        return self.sendMsgToColab({"action": "generateImgFromWSrc",
                                    "client_id": threadId, "w_src": w_src.tolist(), "tag": tag})
