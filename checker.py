# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:22:35 2018

@author: Yijie Yan
"""

import os
import requests
from flask import Flask, render_template, jsonify, abort, url_for, Blueprint
from flask import request as flaskreq
import json

# make sure the id of vehical is integer
def checkID(id):
    try:
        id = int(id)
    except:
        abort(400, 'Non-int ID')
