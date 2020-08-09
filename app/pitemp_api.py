import settings
import pitemp_lib

#API stuff
from flask import Flask, abort, jsonify, request

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

api = settings.API

@application.route('/api/'+api+'/alive',methods=['POST'])
def get_alive():
    return jsonify({'data': 'Linux api is alive.'})

@application.route('/api/'+api+'/status',methods=['GET'])
def get_status():
    return jsonify(pitemp_lib.pitemp.db_read())

if __name__ == '__main__':
	application.run(host='0.0.0.0',port=10500, debug=True,ssl_context='adhoc')
