import json

class ObjectLike(dict):
    __getattr__ = dict.get
 
x = json.loads( open("out2.json").read(), object_hook=ObjectLike)

import pdb; pdb.set_trace()

