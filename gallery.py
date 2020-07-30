from easydict import EasyDict
import pickle
import numpy as np

SAVED_GALLERY_LATENTS_PATH = 'results/savedAttrFromClient.pkl'


def loadGallery(max_images):
    pkl_file = open(SAVED_GALLERY_LATENTS_PATH, 'rb')
    savedAttrs = pickle.load(pkl_file)
    pkl_file.close()

    w_srsc = []

    for i in range(len(savedAttrs)):
        w_srsc.append(savedAttrs[i]['wlatent'])
    if len(w_srsc) == 0:
        print("No gallry found")
    if len(w_srsc) > 0:
        w_srsc.reverse()
        w_srsc = w_srsc[:max_images]
        w_srsc = np.asarray(w_srsc)
        w_srsc = np.squeeze(w_srsc, axis=1)
    # load metadata for selected attrs
    return w_srsc
    # f_results = [executor.submit(
    #     main_generator.getCachedGallery, w_src=w_srsc)]
    # futures.wait(f_results)
    # gen_images = f_results[0].result()
    # print("Gallery ", gen_images.shape)

    # gen_images = self.processGeneratedImages(gen_images)
    # metadata = self.getMetadataFromSaved(savedAttrs)
    # self.broadcastGalleryToClient(
    #     gen_images, metadata=metadata, tag='gallery')


def saveLatent(dictEntry):
    pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
    savedAttrs = pickle.load(pkl_file)
    pkl_file.close()

    print("Total gallery ", len(savedAttrs))

    savedAttrs.append(dictEntry)
    output = open('results/savedAttrFromClient.pkl', 'wb')
    pickle.dump(savedAttrs, output)
    output.close()


def getMetadataFromSaved(max_images, curr_user):
    metadata = []
    pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
    savedAttrs = pickle.load(pkl_file)
    pkl_file.close()
    attrs = savedAttrs.copy()
    attrs.reverse()
    attrs = attrs[:max_images]
    for i in range(len(attrs)):
        md = EasyDict({})
        md.idx = attrs[i]["idx"]
        if attrs[i].get("username"):
            md.username = attrs[i]["username"]
        else:
            md.username = "unknown"
        md.isCurrUserLoved = False
        if attrs[i].get("usersWhoLoved"):
            users = attrs[i]["usersWhoLoved"]
            md.totalLoved = len(users)
            if curr_user in users:
                md.isCurrUserLoved = True
        else:
            md.totalLoved = 0
        metadata.append(md)
    return metadata


def love(params, curr_user):
    pkl_file = open('results/savedAttrFromClient.pkl', 'rb')
    savedAttrs = pickle.load(pkl_file)
    pkl_file.close()
    idx = params.idx
    matches = [x for x in savedAttrs if x['idx'] == idx]
    isLoved = params.isLoved
    if isLoved:
        if matches[0].get('usersWhoLoved'):
            if curr_user not in matches[0]['usersWhoLoved']:
                matches[0]['usersWhoLoved'].append(curr_user)
                print(idx, matches[0]['usersWhoLoved'])
        else:
            matches[0]['usersWhoLoved'] = [curr_user]
    else:
        if curr_user in matches[0]['usersWhoLoved']:
            matches[0]['usersWhoLoved'].remove(curr_user)
    output = open('results/savedAttrFromClient.pkl', 'wb')
    pickle.dump(savedAttrs, output)
    output.close()
###################


def resetSavedGallery():
    savedAttrs = []
    with open('results/savedAttrFromClient.pkl', 'wb') as handle:
        # output = open('results/savedAttrFromClient.pkl', 'wb')
        pickle.dump(savedAttrs, handle)
    # output.close()


# resetSavedGallery()
