import xmltodict
import json
import os
from tqdm import tqdm
result = []

path = r'D:\xml_info'

i = 0

for file in tqdm(os.listdir(path)):

    filename = path + '/' + file
    with open(filename, 'r', encoding='utf-8') as f:
        xml_data = f.read()

    data_dict = xmltodict.parse(xml_data)

    item = data_dict['ns2:institutionInfo']['ns2:body']['ns2:position']
    inn = item['placer']['inn']
    fullname = item['initiator']['fullName']
    result.append({'id': i + 1, 'inn': inn, 'fullname': fullname})
    i += 1

json_data = json.dumps(result, ensure_ascii=False)


with open(r'D:\data\data.json', 'w') as f:
    json.dump(result,f)