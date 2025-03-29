from flask import Flask, request, jsonify, render_template
from database import create_event, get_all_events, create_user, get_all_users, register_user_for_event
import sqlite3
import os

# For debugging - print working directory and check templates directory exists
print("Working directory:", os.getcwd())
templates_dir = os.path.join(os.getcwd(), "templates")
print("Templates directory exists:", os.path.exists(templates_dir))
if os.path.exists(templates_dir):
    print("Templates found:", os.listdir(templates_dir))

app = Flask(__name__)

# API routes
@app.route('/events', methods=['POST'])
def create_new_event():
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    place = data.get('place')
    owner_id = data.get('owner_id')
    if not all([name, date, place, owner_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        event = create_event(name, date, place, owner_id)
        # Serialize the event object to a dictionary
        event_dict = {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "place": event.place,
            "owner_id": event.owner_id
        }
        return jsonify(event_dict), 201
    except sqlite3.Error as e:
         return jsonify({'error': str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = get_all_events()
        # Serialize list of event objects to list of dictionaries
        serialized_events = [
            {
                "id": event.id,
                "name": event.name,
                "date": event.date,
                "place": event.place,
                "owner_id": event.owner_id
            } for event in events
        ]
        return jsonify(serialized_events), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def create_new_user():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Missing username'}), 400
    try:
        user = create_user(username)
        # Serialize the user object to JSON
        user_data = {"user_id": user.user_id, "username": user.user_name}
        print("Returning user data:", user_data)  # Add this line for debugging
        return jsonify(user_data), 201
    except (sqlite3.Error, AttributeError) as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = get_all_users()
        # Properly serialize user objects
        serialized_users = [{"id": user.user_id, "username": user.user_name} for user in users]
        return jsonify(serialized_users), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/events/<int:event_id>/register', methods=['POST'])
def register_user(event_id):
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    try:
        register_user_for_event(user_id, event_id)
        return jsonify({'message': 'User registered for event'}), 200
    except sqlite3.Error as e:
         return jsonify({'error': str(e)}), 500

# Page routes
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print("Error rendering index template:", str(e))
        return f"Error: {str(e)}", 500

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/users-page')
def users_page():
    return render_template('users.html')

@app.route('/events-page')
def events_page():
    return render_template('events.html')

if __name__ == '__main__':
    app.run(debug=True)