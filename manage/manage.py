# coding: utf-8

from flask import Flask, render_template, request, jsonify

import urllib3

IP_LIST = ['10.203.1.223', '10.203.1.224']

app = Flask(__name__)


class Config(object):
    DEBUG = True


app.config.from_object(Config)

# @app.route('/login')
# def login():
#     return render_template('login.html')
#
# @app.route('/index')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/data_request', methods=['GET', 'POST'])
# def data_request():
#     if request.method == 'GET':
#         data_interface_ip=request.args.get('ip')
#         data_dic['login_ip']=data_interface_ip
#         str_login_url=f'http://{data_interface_ip}:12122/login'
#
#         #通过urllib3爬取网络资源
#         http = urllib3.PoolManager()
#         response = http.request('GET', str_login_url)
#
#         #将数据存放在data
#         if response.status == 200:
#             data_dic['login_text']=response.data.decode()[1:8]
#             data_dic['login_status']=response.status
#         else:
#             data_dic['login_status']=response.status
#         print(data_dic)
#     return 'data'
#
# @app.route('/data_response', methods=['GET', 'POST'])
# def data_response():
#     return jsonify(data_dic)


@app.route('/index')
def index():
    '''
    index页面路由
    :return: index.html
    '''
    return render_template('index.html')


@app.route('/master_ip', methods=['GET', 'POST'])
def master_ip():
    '''
    master_ip数据路由
    :return: T:master ip, F:列表中第一个ip
    '''
    http = urllib3.PoolManager()
    for ip in IP_LIS:
        str_login_url = f'http://{ip}:12122/is_master'
        response = http.request('GET', str_login_url)
        if response.status == 200:
            if "1" in response.data.decode():
                return jsonify(ip)
    print('Can not get master IP')
    return jsonify('0.0.0.0')


# if __name__ == '__name__' :
app.run()
