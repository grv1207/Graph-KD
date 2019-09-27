
from flask import Flask, request
import json
import re
import numpy as np

#import InferenceClass as Ic
import inference_class as Ic
import pickle
"""
with open(u'UIrelMapping.bin', 'rb') as wn:
    relDict = pickle.load(wn )
"""
regex = re.compile('[^a-zA-Z]')

app = Flask(__name__)


@app.route('/trans/', methods=['POST'])
def main():

    jsonString = request.get_json(force=True)
    edgeList = []
    holo_dict = {}

    if jsonString['inferenceType'] == 'trans':

        for count, pathDict in enumerate(jsonString["paths"]):
            tempDict = {}
            tempDict["pathIndex"] = count
            tempDict["edges"] = Ic.TransitiveInference(pathDict).trans_main()
            if bool(tempDict["edges"]):
                edgeList.append(tempDict)

    elif jsonString['inferenceType'] == 'holo':
        holo_dict["edges"] = Ic.HolographicInference(jsonString["paths"][0]).hole_main()
        if bool(holo_dict["edges"]):
            edgeList.append(holo_dict)

    #print(edgeList)
    return json.dumps(edgeList)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)

