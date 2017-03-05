from tpb import TPB
from tpb import CATEGORIES, ORDERS
import requests, sys, json
from os import listdir
from os.path import isdir
from os.path import join as path_join

def get_data(q):
	t = TPB('https://thepiratebay.org')
	search = t.search(q).order(ORDERS.SEEDERS.DES).page(0)
	return search



def add_torrent(magnet,ip):
	print 'Status: adding torrent'
	key = 'x-transmission-session-id'
	try:
		token = requests.get('http://'+ip+':9091/transmission/rpc').headers[key]
		add = requests.post('http://'+ip+':9091/transmission/rpc',
						  headers={key: token},
						  data=json.dumps({
						  	'method' : 'torrent-add',
						  	'arguments' : {
						  		'download-dir' : '/home/teo/Downloads/transmission/completed',
						  		'filename' : magnet,
						  		'paused' : False
						  	}
						  	}))
		result = json.loads(add.text)['result']
		print result
		if result == u'success':
			return True
		else:
			return False
	except requests.exceptions.ConnectionError:
		print "Error"
		return False

def list_files(base,path):
	full_path = path_join(base,path)
	file_names = listdir(full_path)
	files = []
	for filename in file_names:
		if filename[0] != '$' and filename[0] != '.':
			joint = path_join(full_path, filename)
			files.append({'name': filename, 'isdir': isdir(joint),'full_path': joint, 'rel_path': path_join(path,filename)})
	files = sorted(files, key=lambda k: k['name'])
	files = sorted(files, key=lambda k: k['isdir'],reverse=True)
	return files

	 	