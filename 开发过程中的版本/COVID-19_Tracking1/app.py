from flask import Flask
from flask import render_template
from flask import jsonify
import utils


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/c1')
def get_c1_data():
	data = utils.get_c1_data()
	return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})


@app.route('/time')
def gettime():
	return utils.get_time()


@app.route('/tem')
def hello_world3():
    return render_template("index.html")

@app.route('/ajax', methods=["get","post"])
def hello_world4():
    return '10000'

if __name__ == '__main__':
    app.run()
