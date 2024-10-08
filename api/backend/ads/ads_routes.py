from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

ads = Blueprint('ads', __name__)

# Get all the ads informations from a marketing campaign 
@ads.route('/ads', methods =['GET'])
def get_ads():
    current_app.logger.info('ads_routes.py: GET /users')
    cursor = db.get_db().cursor()
    cursor.execute('select id, terms_and_conditions, description, type, marketing_campaign_id from ads')
    
    theData = cursor.fetchall()
    
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Adding a new ad 
@ads.route('/ads', methods=['POST'])
def add_new_ad():
    the_data = request.json
    current_app.logger.info(the_data)
    id = the_data['id']
    description = the_data['description']
    type = the_data['type']
    terms_and_conditions = the_data['terms_and_conditions']
    marketing_campaign_id = the_data['marketing_campaign_id']
    budget = the_data['budget']

    query = 'insert into ads (id, description, type, terms_and_conditions, marketing_campaign_id, budget) values("'
    query += id + '", "'
    query += description + '", "'
    query += type + '", "' 
    query += terms_and_conditions + '", "'
    query += marketing_campaign_id + '", "' 
    query += budget + ')'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db.commit()
    return 'Success'

# Updates ads information 
@ads.route ('/ads', methods = ['PUT'])
def update_ad():
    ads_info = request.json
    id = ads_info['id']
    description = ads_info['description']
    type = ads_info['type']
    terms_and_conditions = ads_info['terms_and_conditions']
    budget = ads_info['budget']
    marketing_campaign_id = ads_info['marketing_campaign_id']
    

    query = 'UPDATE ads SET description = %s, type %s, terms_and_conditions = %s, budget = %s, marketing_campaign_id = %s where id = %s'
    data = (description, type, terms_and_conditions, budget, marketing_campaign_id, id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Ad Updated '