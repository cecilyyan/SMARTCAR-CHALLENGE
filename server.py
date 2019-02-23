# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:21:40 2018

@author: Yijie Yan
"""
#in this project I use Flask as web framework
import os
import requests
from flask import Flask, render_template, jsonify, abort, url_for, Blueprint
from flask import request as flaskreq
import json


#use blueprint to organize a group of related views and manage URL routing
blueprint = Blueprint('endpoints', __name__)

#Make sure the id of vehical is integer
def checkID(id):
    try:
        id = int(id)
    except:
        abort(400, 'Non-int ID')

#send request to gm API. Minimize code repitition
def gmRequest(id, suffix, append={}):
    #id is the vehical id, suffix is used to distinguish different requests
    #append is used for Start/Stop Engine function since there are one more field in these json content

    #make a request
    head={'Content-Type':'application/json'}
    params={'id':id, 'responseType':'JSON'}
    params.update(append)
    response=requests.post(url='http://gmapi.azurewebsites.net'+suffix, json=params).json()

    #check the response status
    status = int(response['status'])
    if status == 404:
        abort(400, 'Can not found the key')
    elif status != 200:
        abort(500, 'GM server gives error code ' + str(status))
    return response

#Vehical Info
@blueprint.route('/vehicles/<id>', methods=['GET'])
def getVehicalInfo(id):
    #retrive imformation from GM
    checkID(id)

    response=gmRequest(id, '/getVehicleInfoService')

    #get data from request and parse it into Smartcar API form
    result={}
    data = ["vin","color","driveTrain"]
    for i in data:
        result[i]=response['data'][i]['value']

    four_door = response['data']['fourDoorSedan']['value']
    two_door = response['data']['twoDoorCoupe']['value']

    #check if door data is consistent
    if four_door == two_door:
        abort(500, 'GM gives inconsistent door responses')

    #assign the doorCount
    if four_door:
        result['doorCount']=4
    else:
        result['doorCount']=2

    return jsonify(result)

#Security
@blueprint.route('/vehicles/<id>/doors', methods=['GET'])
def getSecurityInfo(id):
    checkID(id)

    response=gmRequest(id, '/getSecurityStatusService')
    #extract security information from gm request and parse them into Smartcar API json format
    result=[]
    door_list=response['data']['doors']['values']
    for door in door_list:
        data = {}
        data["location"] = door["location"]["value"]
        data["locked"] = bool(door["location"]["value"])
        result.append(data)

    return jsonify(result)

#Fuel Range
@blueprint.route('/vehicles/<id>/fuel', methods=['GET'])
def getFuelRange(id):
    checkID(id)

    response = gmRequest(id, '/getEnergyService')
    #extract the fuel range
    if (response['data']['tankLevel']['type'] == "Null"):
        result = {
    		'percent': 0.0,
    	         }
    else:
        fuel = float(response['data']['tankLevel']['value'])
        result = {
		      'percent': fuel,
	             }
    return jsonify(result)

#Battery Range
@blueprint.route('/vehicles/<id>/battery', methods=['GET'])
def getBatteryRange(id):
    checkID(id)

    response=gmRequest(id, '/getEnergyService')
    if (response['data']['batteryLevel']['type'] == "Null"):
        result = {
    		'percent': 0.0,
    	         }
    else:
        battery = float(response['data']['batteryLevel']['value'])
        result = {
		      'percent': battery,
	             }
    return jsonify(result)

#Start/Stop Engine
@blueprint.route('/vehicles/<id>/engine', methods=['POST'])
def getStartorStop(id):
    checkID(id)
    #check POST request is json or not
    if not flaskreq.json:
        abort(400, 'Non-JSON POST request')
    #check it is start or stop engine
    command = ''
    if flaskreq.json['action'] == 'START':
        command = 'START_VEHICLE'
    elif flaskreq.json['action'] == 'STOP':
        command = 'STOP_VEHICLE'
    else:
        abort(400, 'Invalid commond. It should be START or STOP.')
     # send request to gm server and get the json as response
    response = gmRequest(id, '/actionEngineService', {'command': command})
    # Extracts outcome
    result = {}
    result["status"] = "success" if (response["actionResult"]["status"] == "EXECUTED") else "failure"
    return jsonify(result), 201


#404 error handler
@blueprint.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404

# def create_app():
# 	app = Flask(__name__)
# 	app.register_blueprint(blueprint)
# 	return app

if __name__ == '__main__':
    # app = create_app()
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.run(port=os.getenv('PORT', 5000))
