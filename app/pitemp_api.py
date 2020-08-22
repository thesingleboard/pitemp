import settings
from pitemp_lib import pitemp
import logging

#API stuff
from flask import Flask, abort, jsonify, request

#Set flask to output "pretty print"
application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

api = settings.API
pt = pitemp()

@application.route('/api/'+api+'/alive',methods=['POST'])
def get_alive():

    api_status = 'up'
    device_id = pt.get_cpu_id()
    if(device_id == '0000000000000000'):
        api_status = 'down'

    return jsonify({'DEVICEID': device_id,'STATUS':api_status})

@application.route('/api/'+api+'/status',methods=['GET'])
def get_status():

    try:
        system_status = pt.get_system_status()
    except Exception as e:
        logging.error("Sytem status: %s"%e)
        system_status = 'error'
    
    return jsonify({'status':system_status})
    
@application.route('/api/'+api+'/config',methods=['GET','PATCH'])
def config():
    
    #pull in the new config data
    newdata = request.get_json()
    if newdata is None:
        newdata = settings.CONFIG
    
    if request.method == 'GET':
        return jsonify({'STATUS':'OK','CONFIG':settings.CONFIG})
    
    if request.method == 'PATCH':

        current = settings.CONFIG

        for k,v in current.items():
            if(k == newdata[k]):
                v = newdata[v]

        return jsonify({'STATUS':'updated','CONFIG':current})

#@application.route('/api/'+api+'/data',methods=['GET'])
#def get_data():
#    return jsonify(pt.db_read())

if __name__ == '__main__':
	application.run(host='0.0.0.0',port=10500, debug=True,ssl_context='adhoc')
