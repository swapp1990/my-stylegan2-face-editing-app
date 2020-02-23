from easydict import EasyDict

dir_mapping = [
    EasyDict({"name": "gender", 
                "mapping": "gender",
                "condition": [],
                "coeff_mapping":[{"male": 13.5, "female": -4.5}]
            }), 
    EasyDict({"name": "race_black", 
                "mapping": "race_basic", 
                "condition": ["black", "brown", "white"], 
                "coeff_mapping": [{"black": 3.5, "brown": 2.5, "white": -2.5}]
            }),
    EasyDict({"name": "race_yellow", 
                "mapping": "race_asian", 
                "condition": ["asian"], 
                "coeff_mapping": [{"asian": 6.0}]
            }),
    EasyDict({"name": "age", 
                "mapping": "age", 
                "condition": [], 
                "coeff_mapping": [{"young": 5.5, "old": -11.5}]
            }),
    EasyDict({"name": "smile", 
                "mapping": "smile", 
                "condition": ["smile", "laugh","sad", "neutral"], 
                "coeff_mapping": [{"smile": -4.2, "laugh": -7, "sad": 4.5, "neutral": 0.0}]
            })
]

AttrToSearchMapping = [
    EasyDict({"name": "gender", "syns": ["gender", "sex"], "values": [["male", "boy",  "man"], ["female", "girl","woman"]]}),
    EasyDict({"name": "race_basic", "syns": ["race", "skin"], "values": [["white"], ["black"], ["brown"], ["yellow"]]}),
    EasyDict({"name": "race_asian", "syns": ["race", "skin"], "values": [["asian", "chinese"]]}),
    EasyDict({"name": "age", "syns": ["age"], "values": [["old", "older"], ["young", "younger"]]}),
    EasyDict({"name": "smile", "syns": ["smile"], "values": [["smile", "smiling"], ["laugh", "laughing"], ["sad"], ["neutral"]]})
]

def getDirListfromSearchTxt(txt):
        searchTxt = txt.lower()
        attr_dict = getAttributesFromSearchtxt(searchTxt)
        dir_list = []
        for i,k in enumerate(attr_dict.keys()):
            dir_dict = {}
            foundMapping = False
            v = attr_dict[k]
            for dm in dir_mapping:
                if dm.mapping == k:
                    dir_dict['name'] = dm.name
                    dir_coeff_mapping = dm.coeff_mapping[0]
                    for coeff_k in dir_coeff_mapping.keys():
                        if v == coeff_k:
                            dir_dict['coeff'] = dir_coeff_mapping[coeff_k]
                    foundMapping = True
            if foundMapping:
                dir_dict['order'] = i
                dir_list.append(dir_dict)
        print(dir_list)
        return dir_list
    
def getAttributesFromSearchtxt(searchTxt):
    searchTxtList = searchTxt.split()
    
    matchingAttrs = []
    matchingAttrsNames = []
    matchingAttrsVals = []
    for a in AttrToSearchMapping:
        matchedSyns = [s for s in a.syns if s in searchTxtList]
        for vl in a.values:
            matchedSyns = matchedSyns + [s for s in vl if s in searchTxtList]
        if len(matchedSyns) > 0:
            matchingAttrs.append(a)
            matchingAttrsNames.append(a.name)
    for ma in matchingAttrs:
        for vl in ma.values:
            if any(x in searchTxtList for x in vl):
                matchingAttrsVals = matchingAttrsVals + [vl[0]]
    attr_dict = {}
    for key, val in zip(matchingAttrsNames, matchingAttrsVals):
        attr_dict[key] = val
    print(attr_dict)
    attr_dict = EasyDict(attr_dict)
    return attr_dict

