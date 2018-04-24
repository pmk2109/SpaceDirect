VERSION_STR = 'v1.0.0'

import sys
import requests
import numpy as np
from error import Error
from flask import Blueprint, request, jsonify

sys.path.append('../')

from init_sql import PropertyDatabase

blueprint = Blueprint(VERSION_STR, __name__)
@blueprint.route('/return_space_matches', methods=['GET'])
def return_space_matches():
    '''
    Use this endpoint to give you a list of spaces in properties similar to the user surveyed need.
    ---
    tags:
     - v1.0.0

    responses:
     200:
       description: Returns a dictionary with 1 key (response) with a corresponding value as a list of dictionaries all containing keys (i.e. StreetAddress) and values corresponding
     default:
       description: Unexpected error
       schema:
         $ref: '#/definitions/Error'

    parameters:
     - name: locationPref
       in: query
       description: zipcode
       required: true
       type: string

     - name: size
       in: query
       description: Headcount
       required: true
       type: int

    consumes:
     - multipart/form-data
     - application/x-www-form-urlencoded
    '''

    user_locationPref = [request.args['locationPref']][0]
    user_size = 200*int([request.args['size']][0])


    pdb = PropertyDatabase()

    query = ("SELECT ListingType, StreetAddress, City, State,               \
                     ZipCode, SuiteNumber, AvailableSF, DateAvailable,      \
                     PropertyDescription                                    \
              FROM listingstemp_dt                                          \
              WHERE ZipCode = {}                                            \
                    AND  AvailableSF > {}*.75                               \
                    AND  AvailableSF < {}*1.25                              \
              ".format(user_locationPref, user_size, user_size))

    df = pdb.query_sql(query)
    results = df.to_dict(orient='records')

    

    d = {'results' : results}
    
    response = jsonify(d)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




from app import app
app.register_blueprint(blueprint, url_prefix='/'+VERSION_STR)
