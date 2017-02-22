from flask import Flask
from flask import render_template
from flask import request
from engine import get_data, add_torrent

app = Flask(__name__)
ip = "192.168.1.64"

@app.route('/')
def index():
    return render_template('index.html',ip=ip)

@app.route('/search',methods=["GET"])
def search():
	q = request.args.get('q')
	if len(q) > 0:
		return render_template('search.html', torrents=get_data(q),ip=ip)
	else:
		return render_template('search.html',ip=ip)

@app.route('/add',methods=["GET"])
def add():	
	magnet = request.args.get('m')
	print magnet
	success = add_torrent(magnet,ip)
	return render_template('add.html',success=success,ip=ip)

if __name__ == "__main__":
	app.run(host="0.0.0.0")