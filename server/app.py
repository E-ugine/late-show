#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Show, Guest, Appearance

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'successful'
class Shows(Resource):
    def get(self):
        shows = []
        for show in Show.query.all():
            show_dict = {
                "id": show.id,
                "name": show.name,
                "host": show.host,
                "air_date": show.air_date
            }
            shows.append(show_dict)
        return make_response(jsonify(shows), 200)

class ShowsId(Resource):
    def get(self, id):
        show = Show.query.filter(Show.id == id).first()
        
        if show:
            show_dict = {
                "id": show.id,
                "name": show.name,
                "host": show.host,
                "air_date": show.air_date,
                "appearances": []
            }

            for appearance in show.appearances:
                appearance_dict = {
                    "id": appearance.id,
                    "guest_name": appearance.guest.name,
                    "role": appearance.role
                }
                show_dict["appearances"].append(appearance_dict)

            return make_response(jsonify(show_dict), 200)
        else:
            return make_response(jsonify({"error": "Show not found"}), 404)

class Guests(Resource):
    def get(self):
        guests = []
        for guest in Guest.query.all():
            guest_dict = {
                "id": guest.id,
                "name": guest.name,
                "profession": guest.profession
            }
            guests.append(guest_dict)
        return make_response(jsonify(guests), 200)

    def post(self):
        data = request.get_json()

        if not all(key in data for key in ['name', 'profession']):
            return make_response(jsonify({"errors": ["Missing data fields"]}), 400)

        try:
            new_guest = Guest(
                name=data.get('name'),
                profession=data.get('profession')
            )
            db.session.add(new_guest)
            db.session.commit()

            return make_response(jsonify(new_guest.to_dict()), 201)

        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)

class GuestsId(Resource):
    def get(self, id):
        guest = Guest.query.filter(Guest.id == id).first()
        
        if guest:
            guest_dict = {
                "id": guest.id,
                "name": guest.name,
                "profession": guest.profession
            }
            return make_response(jsonify(guest_dict), 200)
        else:
            return make_response(jsonify({"error": "Guest not found"}), 404)

    def patch(self, id):
        guest = Guest.query.filter(Guest.id == id).first()
        
        if not guest:
            return make_response(jsonify({"error": "Guest not found"}), 404)

        try:
            data = request.get_json()
            for key, value in data.items():
                setattr(guest, key, value)
            db.session.add(guest)
            db.session.commit()

            return make_response(jsonify(guest.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)

class Appearances(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['role', 'guest_id', 'show_id']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"errors": [f"Missing field: {field}" for field in missing_fields]}, 400

        try:
            guest = db.session.get(Guest, data['guest_id'])
            show = db.session.get(Show, data['show_id'])

            if not guest or not show:
                return {"errors": ["Invalid 'guest_id' or 'show_id'"]}, 400

            new_appearance = Appearance(
                role=data['role'],
                guest_id=data['guest_id'],
                show_id=data['show_id']
            )
            db.session.add(new_appearance)
            db.session.commit()

            response_data = {
                'id': new_appearance.id,
                'role': new_appearance.role,
                'guest_id': new_appearance.guest_id,
                'show_id': new_appearance.show_id,
                'guest': guest.to_dict(rules=('-appearances.guest',)),
                'show': show.to_dict(rules=('-appearances.show',))
            }

            return make_response(jsonify(response_data), 201)

        except Exception as e:
            db.session.rollback()
            print("Error occurred:", e)
            return {"errors": ["An error occurred while creating Appearance"]}, 500

api.add_resource(Shows, '/shows')
api.add_resource(ShowsId, '/shows/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(GuestsId, '/guests/<int:id>', methods=['GET', 'PATCH'])
api.add_resource(Appearances, '/appearances', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=5555)
