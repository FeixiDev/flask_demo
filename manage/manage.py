# coding: utf-8

from flask import Flask, render_template, request, jsonify

import urllib3

IP_LIST = ['10.203.1.223', '10.203.1.224']

app = Flask(__name__)


class Config(object):
    DEBUG = True


app.config.from_object(Config)


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
    '''
    http = urllib3.PoolManager()
    for ip in IP_LIST:
        is_master_url = f'http://{ip}:12122/is_master'
        response = http.request('GET', is_master_url)
        if response.status == 200:
            if "1" in response.data.decode():
                return jsonify(ip)
    print('Can not get master IP')
    return jsonify('0.0.0.0')


# if __name__ == '__name__' :
app.run()
