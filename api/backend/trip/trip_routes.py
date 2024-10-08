from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

trip = Blueprint('trip', __name__)

# Getting trips based on a user id
@trip.route('/trip/<user_id>', methods =['GET'])
def get_trip(user_id):
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    the_query = '''SELECT name, start_date, end_date, num_of_nights, city_name, 
        group_size
        FROM trip
        WHERE user_id = %s
    '''
    cursor.execute(the_query, (user_id))
    theData = cursor.fetchall()
 
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@trip.route('/trip_name/<user_id>', methods =['GET'])
def get_trip_name(user_id):
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    the_query = f'''SELECT id, name
        FROM trip
        WHERE user_id = {user_id}
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()

    trips_dict = {trip['name']: trip['id'] for trip in theData}

    return jsonify(trips_dict)

@trip.route('/trip', methods=['POST']) 
def add_new_trip():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    start_date = the_data['start_date']
    end_date = the_data['end_date']
    group_size = the_data['group_size']
    name = the_data['name']
    restaurant_budget = the_data['restaurant_budget']
    attraction_budget = the_data['attraction_budget']
    hotel_budget = the_data['hotel_budget']
    flight_budget = the_data['flight_budget']
    num_of_nights = the_data['num_of_nights']
    #city_id = the_data['city_id']
    city_name = the_data['city_name']

    # Constructing the query
    query = f'''
        insert into trip (start_date, end_date, group_size, name, hotel_budget, city_name, 
    restaurant_budget, attraction_budget, flight_budget, num_of_nights) values ( 
    "{start_date}", "{end_date}", {group_size}, "{name}", {hotel_budget}, "{city_name}", 
    {restaurant_budget}, {attraction_budget}, {flight_budget}, "{num_of_nights}")
    '''
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success'

@trip.route('/trip/<trip_name>', methods=['DELETE'])
def delete_trip(trip_name):
    current_app.logger.info('trip_routes.py: GET /trip')
    cursor = db.get_db().cursor()
    query = f'''
        delete from trip where name = "{trip_name}"
    '''
    cursor.execute(query)
    db.get_db().commit()
    return "Success!"

