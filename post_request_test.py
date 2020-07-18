# -*- coding: utf-8 -*-

import os
import sys
import json
import requests

value_dict = {"id":0,"name":"李淑云", "lat": 123.3321, "lng": 59.2923}

post_data={
    "data" : str(value_dict),
    "class_name": "location",
}
# post_data = json.dumps(data,indent=4,ensure_ascii=False)
# post_data = data
# print(post_data)
res=requests.post(url="http://127.0.0.1:5000/message/api/dingtalk", data=post_data)
# res=requests.post(url="http://112.125.25.230/gohome/api/location", data=post_data)
# print(res.text)