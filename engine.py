from tpb import TPB
from tpb import CATEGORIES, ORDERS
import requests, sys, json
from os import listdir
from os.path import isdir
from os.path import join as path_join
from os.path import expanduser
from unidecode import unidecode

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

def list_files(user, base, path):
	full_path = path_join(base,path)
	file_names = listdir(full_path)
	files = []
	for filename in file_names:
		if filename[0] != '$' and filename[0] != '.':
			joint = path_join(full_path, filename)
			home = expanduser('~'+user)
			filename = ''.join(i for i in filename if ord(i)<128)
			files.append({'name': unidecode(unicode(filename)), 'isdir': isdir(joint),'ftp_path': joint.replace(home,""), 'rel_path': path_join(path,filename)})
	files = sorted(files, key=lambda k: k['name'])
	files = sorted(files, key=lambda k: k['isdir'],reverse=True)
	return files

	 	
