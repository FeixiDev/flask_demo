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

@app.route('/ex_cmd/<cmd>/', methods=['GET', 'POST'])
def oprt_ex_cmd(cmd):
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

@app.route('/ex_cmd_result', methods=['GET', 'POST'])
def ex_cmd_result():
    '''
    数据路由
    :return: 执行结果`
    '''
    return corss_domain(GLO_CMD_RESULT)

global CALCULATE_RESULT

#后台处理函数
def calculate(A,B):
    return {"add":A+B,"subtract":A-B,"multiply":A*B,"divided":A/B}

#接收前端数据
@app.route('/calc/<A>/<B>/', methods=['GET', 'POST'])
def oprt_calculate(A,B):
    global CALCULATE_RESULT 
    CALCULATE_RESULT = calculate(int(A),int(B))
    if CALCULATE_RESULT:
        str_ok = "数据处理成功"
        return corss_domain(str_ok)
    else:
        str_err = "数据处理失败"
        return corss_domain(str_err)
#返回前端
@app.route('/calculate_result', methods=['GET', 'POST'])
def provide_calculate_result():
    return  corss_domain(CALCULATE_RESULT)



app.run(host='0.0.0.0', port=12122)
