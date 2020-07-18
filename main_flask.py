# -*- coding: utf-8 -*-

import os
import sys
import json

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import select, func

from flask import Flask
from flask import request
from flask import Response
# 跨域
from flask_cors import *

from account import account
from datetimeManager import datetimeManager
from dingdingMessager import dingdingMessager
from emailMessager import emailMessager

folder = os.path.abspath(os.path.dirname(__file__))
dm = datetimeManager()
account = account()
# 创建数据库引擎
engine = create_engine(f'mysql+pymysql://{account.mysqlUser}:{account.mysqlPassword}@112.125.25.230:3306/message')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

# 发钉钉
# host/message/api/dingtalk
# 发邮件
# host/message/api/email
# 所有方式
# host/message/api/all
# 参数
# {"data": {}, "class": "...", "subject": "标题"}

# 添加公共返回值
def packDataWithCommonInfo(isCache = False, isSuccess = True, msg = "success", duration = '0', data = {}):
    code = 0
    if not isSuccess:
        code = -1
    result = {'code' : code, 'msg' : msg, 'isCache' : False, 'aliyun_date' : dm.getDateTimeString(), 'data' : data, 'duration' : duration}
    return json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)

@app.route('/message/api/dingtalk', methods=['POST'])
def send_msg_by_dingtalk():
    start_ts = dm.getTimeStamp()
    # data = json.dumps(records, ensure_ascii=False, indent=4)
    data = {}
    if request.method=='POST':
        class_name = request.form['class_name']
        # eval 是从字符串字典转回 dict
        obj = eval(request.form['data'])
        if obj != None and len(class_name) > 0:
            # 入数据库（确定 id）
            newId = 1
            # ★ 如果是初次创建数据库，select 会失败，此时应该注释下面 4 行代码，不做判断了，场景不多
            sql = f"""SELECT * FROM {class_name} order by id DESC LIMIT 1"""
            latest = pd.read_sql(sql, engine)
            if len(latest.id.values) > 0:
                newId = latest.id.values[0] + 1
            obj['id'] = int(newId)
            obj['aliyun_date'] = dm.getDateTimeString()
            df = pd.DataFrame(obj, index=[newId])
            df.to_sql(f'{class_name}', engine, if_exists='append', index=True)
            # 发钉钉
            dingdingMessager().send(f'{class_name}\n\n{json.dumps(obj,indent=4,sort_keys=False,ensure_ascii=False)}')
            # # 发邮件
            emailMessager().send(subject=f'{class_name}', msg=json.dumps(obj,indent=4,sort_keys=False, ensure_ascii=False))

    end_ts = dm.getTimeStamp()
    duration = dm.getDuration(start_ts, end_ts)
    data = packDataWithCommonInfo(duration = duration, data = data)
    return Response(data, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=5000, debug=True)