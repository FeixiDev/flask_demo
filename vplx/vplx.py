# coding:utf-8

from flask import Flask, jsonify, make_response
import subprocess
import base64

app = Flask(__name__)


class Config(object):
    DEBUG = True


app.config.from_object(Config)


def read_flag_file():
    '''
    读取is_master文件
    :return: 0/1?None
    '''
    with open('is_master', 'r')as f:
        result = f.read()
    return result


def corss_domain(data):
    '''
    数据跨域
    :param data: 页面返回的数据
    :return: response
    '''
    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


@app.route('/is_master')
def is_master():
    '''
    数据路由，判断master ip
    :return: 0/1?None
    '''
    data = read_flag_file()
    return corss_domain(data)


global GLO_CMD_RESULT


@app.route('/data/<cmd>/', methods=['GET', 'POST'])
def cmd_result(cmd):
    '''
    数据路由，接收cmd返回执行结果
    :param cmd: 用户输入命令
    :return: 执行结果
    '''
    cmd_str = base64.b64decode(cmd)
    global GLO_CMD_RESULT

    if subprocess.getstatusoutput(cmd_str):
        cmd_result = subprocess.getoutput(cmd_str)
        data_value = base64.b64encode(cmd_result.encode('utf-8'))
        GLO_CMD_RESULT = data_value.decode()
        str_ok = "命令执行成功"
        return corss_domain(str_ok)
    else:
        str_err = "错误命令无法执行"
        return corss_domain(str_err)



@app.route('/cmd_result_data', methods=['GET', 'POST'])
def cmd_result_data():
    global GLO_CMD_RESULT
    '''
    数据路由
    :return: 执行结果`
    '''
    return corss_domain(GLO_CMD_RESULT)

ADD_DATA = None
TAKE_DATA = None
#后台处理函数
def add():
    a = 1 + 1
    return a 

def take():
    b = 1 * 1
    return b

#接收前端数据
@app.route('/add_result_data', methods=['GET', 'POST'])
def add_result_data():
    global ADD_DATA
    global TAKE_DATA
    ADD_DATA = add()
    TAKE_DATA = take()
    return "处理完成"

#发送后台数据去前端
@app.route('/result_data_show', methods=['GET', 'POST'])
def result_data_show():
    
    return  {"ADD_DATA":ADD_DATA,"TAKE_DATA":TAKE_DATA}




app.run(host='0.0.0.0', port=12122)
