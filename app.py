from flask import Flask
from flask import render_template
from flask import request
from engine import get_data, add_torrent
from os import listdir
from os.path import isdir
from os.path import join as path_join
import json

app = Flask(__name__)
ip = "192.168.1.64"
downloads_path = "/home/teo/Downloads/transmission/completed"


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

@app.route('/downloads',methods=["GET"])
def downloads():
	file_names = listdir(downloads_path)
	files = []
	for filename in file_names:
		if filename[0] != '$' and filename[0] != '.':
			files.append({'name': filename, 'isdir': isdir(path_join(downloads_path, filename))})
	files = sorted(files, key=lambda k: k['isdir'],reverse=True)
	return render_template('downloads.html', files=files, ip=ip, path=downloads_path)

if __name__ == "__main__":
	app.run(host="0.0.0.0")