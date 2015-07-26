#!flask/bin/python
from flask import Flask, render_template, request, jsonify
import subprocess
import sys

app = Flask(__name__)
reload(sys)
sys.setdefaultencoding('utf8')
wu_adjs = []
wu_nouns = []

LINE_ONE = '%s from this day forward'
LINE_TWO = ' you will also be known as '


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/wuami/<name>', methods=['GET'])
def wu_am_i(name):
    wuname = get_wu_name(name)
    return common_return(wuname, '', '', wuname)


@app.route('/enterthewu/<name>', methods=['GET'])
def enter_the_wu(name):
    wuname = get_wu_name(name)
    message = LINE_ONE % name + LINE_TWO + wuname
    return common_return(message, LINE_ONE % name, LINE_TWO, wuname)


def common_return(message, l1, l2, l3):
    if request_wants_type('application/json'):
        return jsonify({'message': message})
    elif request_wants_type('text/plain'):
        return message
    elif request_wants_type('application/xml'):
        return render_template('response.xml', message=message)
    else:
        return render_template('response.html', l1=l1, l2=l2, l3=l3)


def get_wu_name(name):
    seed = 0
    for i, char in enumerate(name.lower()):
        seed += ord(char) * (i + 1)

    global wu_adjs
    if len(wu_adjs) == 0:
        wu_adjs = read_file('wu_adjs.txt')

    global wu_nouns
    if len(wu_nouns) == 0:
        wu_nouns = read_file('wu_nouns.txt')

    proc = subprocess.Popen("php random.php " + str(seed) + " " + str(len(wu_adjs)) + " " + str(len(wu_nouns)),
                            shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read().split(',')

    return wu_adjs[int(script_response[0])] + ' ' + wu_nouns[int(script_response[1])]


def read_file(fname):
    words = []
    with open(fname) as f:
        for i, word in enumerate(f):
            words.append(word.rstrip())
    return words


def request_wants_type(type):
    best = request.accept_mimetypes \
        .best_match([type, 'text/html'])
    return best == type and \
           request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']


if __name__ == '__main__':
    app.run()
