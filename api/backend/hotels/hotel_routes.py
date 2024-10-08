from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from urllib.parse import unquote

hotel = Blueprint('hotel', __name__)

# Getting hotels based on trip destination and hotel budget
@hotel.route('/hotel/<city_name>/<max_price>', methods =['GET'])
def get_hotel(city_name, max_price):
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    query = '''
        SELECT hotel.id, hotel.room_type, hotel.amenities, hotel.price_per_night,
               hotel.rating, hotel.city_id, hotel.email,
               (trip.group_size * hotel.price_per_night) AS total_price
        FROM hotel
        JOIN city ON hotel.city_id = city.id
        JOIN trip ON trip.city_id = hotel.city_id
        WHERE city.name = %s
        AND (trip.group_size * hotel.price_per_night) <= %s
        GROUP BY hotel.id, hotel.room_type, hotel.amenities, hotel.price_per_night,
                 hotel.rating, hotel.city_id, hotel.email
        ORDER BY hotel.rating, total_price DESC;
    '''
    data = (city_name, max_price)
    current_app.logger.info(f'query = {query}')
    cursor.execute(query, data)
    
    theData = cursor.fetchall()
    current_app.logger.info(f'retVal = {theData}')
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@hotel.route('/rating/<city>/<rating>', methods =['GET'])
def get_hotel_rating(city, rating):
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    query = f'''
        SELECT name, room_type, amenities, price_per_night, rating
        FROM hotel
        WHERE city_name = "{unquote(city)}" AND rating >= {rating}
        ORDER BY rating, price_per_night ASC;
    '''
    current_app.logger.info(f'query = {query}')
    cursor.execute(query)
    
    theData = cursor.fetchall()
    current_app.logger.info(f'retVal = {theData}')
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@hotel.route('/email/<name>', methods =['GET'])
def get_hotel_email(name):
    current_app.logger.info('hotel_routes.py: GET /hotel')
    cursor = db.get_db().cursor()
    query = f'''
        SELECT email
        FROM hotel
        WHERE name = "{unquote(name)}"
    '''
    current_app.logger.info(f'query = {query}')
    cursor.execute(query)
    
    theData = cursor.fetchall()
    current_app.logger.info(f'retVal = {theData}')
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@hotel.route('/hotel', methods=['POST'])
def add_new_hotel_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    rating = the_data['rating']


    # Constructing the query
    query = 'insert your rating for the hotel ("'
    query += rating + '", "'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

    