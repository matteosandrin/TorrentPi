from tpb import TPB
from tpb import CATEGORIES, ORDERS
import requests, sys, json

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

	 	