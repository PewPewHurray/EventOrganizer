from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Event:
    db = "eome_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.date_time = data["date_time"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.coordinator = data["coordinator"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.participants = []
        self.participants_ids = []

    @classmethod
    def add_event(cls, data):
        query = "INSERT INTO events (name, date_time, address, city, state, coordinator, created_at, updated_at) VALUES (%(name)s, %(date_time)s, %(address)s, %(city)s, %(state)s, %(coordinator)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_event_by_id(cls, data):
        query = "SELECT * FROM events LEFT JOIN users ON events.coordinator = users.id WHERE events.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        coordinator_data = {
            "id": results[0]["coordinator"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["users.created_at"],
            "updated_at": results[0]["users.updated_at"]
        }
        this_event = cls(results[0])
        this_event.coordinator = user.User(coordinator_data)
        return this_event

    @classmethod
    def get_event_by_id_with_participants(cls, data):
        query = "SELECT * FROM events LEFT JOIN participants ON events.id = event_id LEFT JOIN users AS participants_users ON user_id = participants_users.id LEFT JOIN users AS coordinators ON events.coordinator = coordinators.id WHERE events.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        coordinator_data = {
            "id": results[0]["coordinator"],
            "first_name": results[0]["coordinators.first_name"],
            "last_name": results[0]["coordinators.last_name"],
            "email": results[0]["coordinators.email"],
            "password": results[0]["coordinators.password"],
            "created_at": results[0]["coordinators.created_at"],
            "updated_at": results[0]["coordinators.updated_at"]
        }
        this_event = cls(results[0])
        this_event.coordinator = user.User(coordinator_data)
        for row in results:
            if row["participants_users.id"] != None:
                participant_data={
                "id": row["participants_users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["participants_users.created_at"],
                "updated_at": row["participants_users.updated_at"]
                }
                this_event.participants_ids.append(row["participants_users.id"])
                this_event.participants.append(user.User(participant_data))
        return this_event

    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events LEFT JOIN users ON events.coordinator = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        events_list = []
        for row in results:
            coordinator_data = {
            "id": row["coordinator"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["users.created_at"],
            "updated_at": row["users.updated_at"]
        }
            this_event = cls(row)
            this_event.date_time = this_event.date_time.strftime("%B %d, %Y at %I:%M %p")
            this_event.coordinator = user.User(coordinator_data)
            events_list.append(this_event)
        return events_list

    @classmethod
    def update_event(cls, data):
        query = "UPDATE events SET name = %(name)s, date_time = %(date_time)s, address = %(address)s, city = %(city)s, state = %(state)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy_event(cls, data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def add_particaipant(cls, data):
        query = "INSERT INTO participants (event_id, user_id) VALUES (%(event_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy_particaipant(cls, data):
        query = "DELETE FROM participants WHERE event_id = %(event_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_event(data):
        is_valid = True
        if len(data["name"])<2:
            flash("Event name must be at least 2 characters", "event")
            is_valid = False
        if not data["date_time"]:
            flash("Please select a date and time for the event", "event")
            is_valid = False
        if len(data["address"])<6:
            flash("Address must be at least 6 characters", "event")
            is_valid = False
        if len(data["city"])<2:
            flash("City must be at least 2 characters", "event")
            is_valid = False
        if len(data["state"])<2:
            flash("State must be at least 2 characters", "event")
            is_valid = False
        return is_valid