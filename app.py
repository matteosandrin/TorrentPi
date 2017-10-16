from flask import Flask
from flask import render_template
from flask import request
from engine import get_data, add_torrent, list_files


app = Flask(__name__)
ip = "192.168.1.64"
downloads_path = "/home/teo/Downloads/transmission/completed"
ftp_user = 'teo'


@app.route('/')
def index():
    return render_template('index.html',ip=ip)

@app.route('/search',methods=["GET"])
def search():
	q = request.args.get('q')
	if len(q) > 0:
		return render_template('search.html', torrents=get_data(q),ip=ip,query=q)
	else:
		return render_template('search.html',ip=ip)

@app.route('/add',methods=["GET"])
def add():	
	magnet = request.args.get('m')
	print magnet
	success = add_torrent(magnet,ip)
	return render_template('add.html',success=success,ip=ip)

@app.route('/files/',methods=["GET"])
@app.route('/files/<path:path>',methods=["GET"])
def files(path=''):
	files = list_files(ftp_user, downloads_path, path)
	return render_template('downloads.html', files=files, ip=ip, path=path)

if __name__ == "__main__":
	app.run(host="0.0.0.0")







