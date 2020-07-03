import xmltodict
import json
import os

all_data = []


for root, dirs, files in os.walk('all-xml'):
    for fname in files:
        path = 'all-xml/'+fname
        print (fname)
        f = open(path, "r")
        xml = f.read()

        my_dict=xmltodict.parse(xml)
        json_data=json.dumps(my_dict)

        all_data.append(json_data)

print(all_data)