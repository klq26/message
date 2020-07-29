# -*- coding: utf-8 -*-

import os
import sys
import json
import requests

value_dict = {"id":0,"name":"李淑云", "lat": 123.3321, "lng": 59.2923}

post_data={
    "data" : str(value_dict),
    "class_name": "location",
    "init":1
}
# res=requests.post(url="http://127.0.0.1:5000/message/api/dingtalk", data=post_data)
res=requests.post(url="https://www.klq26.site/message/api/all", data=post_data)
# res=requests.post(url="http://127.0.0.1:5000/message/api/email", data=post_data)
print(res.text)