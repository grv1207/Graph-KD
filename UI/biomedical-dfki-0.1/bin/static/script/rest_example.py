import requests
import json


url_syntax = "http://www.dfki.de/mEx/syntax"
url_semantic = "http://www.dfki.de/mEx/semantic"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

text2process='Heute kein Fieber, kein Infekt, keine Beschwerden bei Miktion.'


print ("Semantic Processing of:", text2process)

data = {'text': text2process}
####################################
#some variations can be found here
#data = {'text': text2process, "ner":{"lstm":["medical_condition","process","time_information"]},"re":{"cnn":["has_time_info","hasState"]},"neg":{"negex":["Medical_condition"]},"norm":{"norm":["candidate","wsd"]}}
#data = {'text': text2process, "ner":{"lstm":["medical_condition","process"]},"re":{"cnn":["has_time_info","hasState"]},"neg":{"negex":["Medical_condition"]}}
res = requests.post(url_semantic, data=json.dumps(data), headers=headers)
if res.ok and res.json:
    print (res.json())
else:
    print (">>", res)



print ("")
print ("Syntactic Processing of:", text2process)

data = {'text': text2process}
res = requests.post(url_syntax, data=json.dumps(data), headers=headers)
if res.ok and res.json:
    print (res.json())
else:
    print (">>", res)




