VERSION_STR = 'v1.0.0'

import sys
import requests
import numpy as np
from error import Error
from flask import Blueprint, request, jsonify

sys.path.append('../')

# run build model on a weekly basis so that patents can be stored
# in a compressed format (this part is the time consuming part)
# After this, run use_model to unload pickles/msgpacks and run
# scoring function to return the appropriate object.

# import use_model
from init_sql import PropertyDatabase

# total_tfidf, tfidf = use_model.unpickle()
# user_text -- how to generate/store this?
 #-- think about how this may be implemented (NOT NECESSARY AT THE MOMENT)



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


    print "location: ", user_locationPref, type(user_locationPref)
    print "size: ", user_size, type(user_size)




    # num_results = 50
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
    # print results

    # results = use_model.assemble_results(pdb, user_text, num_results, tfidf,
                                    #  total_tfidf)

    '''
    EXAMPLE RESULTS:
    d = {'results' : [  {'doc_number': '123456',
                    'date' : '20160713',
                    'title' : 'toilet seat light',
                    'abstract' : 'a paragraph of text will go here',
                    'description' : 'many paragraphs of text will go here',
                    'claims' : 'a couple paragraphs of text will go here',
                    'scores' : [decimal point number]
                    },
                    {'doc_number': '123457',
                    'date' : '20160714',
                    'title' : 'toilet seat cushion',
                    'abstract' : 'a paragraph of text will go here',
                    'description' : 'many paragraphs of text will go here',
                    'claims' : 'a couple paragraphs of text will go here'
                    'scores' : [decimal point number]
                    },
                    {'doc_number': '123458',
                    'date' : '20160715',
                    'title' : 'under seat light',
                    'abstract' : 'a paragraph of text will go here',
                    'description' : 'many paragraphs of text will go here',
                    'claims' : 'a couple paragraphs of text will go here'
                    'scores' : [decimal point number]
                    },
                    {'doc_number': '123459',
                    'date' : '20160716',
                    'title' : 'toilet light',
                    'abstract' : 'a paragraph of text will go here',
                    'description' : 'many paragraphs of text will go here',
                    'claims' : 'a couple paragraphs of text will go here'
                    'scores' : [decimal point number]
                    },
                    { 'doc_number': '123460',
                    'date' : '20160717',
                    'title' : 'under sink light',
                    'abstract' : 'a paragraph of text will go here',
                    'description' : 'many paragraphs of text will go here',
                    'claims' : 'a couple paragraphs of text will go here'
                    'scores' : [decimal point number]
                    }
                ]
        }
        '''

    d = {'results' : results}


    # lst = []
    # for e in d.values():
    #     for f in e:
    #         if float(f['score']) > 0.1:
    #             lst.append(f)
    #
    # d = {'results' : lst}
    #
    # for elem in d.values():
    #     for item in elem:
    #         if item['doc_number'][0] == 'D':
    #             doc_num = item['doc_number'][0] + item['doc_number'][2:]
    #         else:
    #             doc_num = item['doc_number'][1:]
            # item['link'] = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1={0}.PN.&OS=PN/{0}&RS=PN/{0}".format(doc_num)

    response = jsonify(d)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




from app import app
app.register_blueprint(blueprint, url_prefix='/'+VERSION_STR)