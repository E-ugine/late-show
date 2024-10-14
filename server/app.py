#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Episode as EpisodeModel, Guest, Appearance

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'LATESHOW API SUCCESSFULLY CREATED!'

class Episode(Resource):
    def get(self):
        shows = []
        for show in EpisodeModel.query.all():
            show_dict = {
                "id": show.id,
                "date": show.date,
                "number": show.number
            }
            shows.append(show_dict)
        return make_response(jsonify(shows), 200)

class EpisodesId(Resource):
    def get(self, id):
        show = EpisodeModel.query.filter(EpisodeModel.id == id).first()
        
        if show:
            show_dict = {
                "id": show.id,
                "name": show.number,
                "appearances": []
            }

            for appearance in show.appearances:
                appearance_dict = {
                    "id": appearance.id,
                    "guest_name": appearance.guest.name,
                }
                show_dict["appearances"].append(appearance_dict)

            return make_response(jsonify(show_dict), 200)
        else:
            return make_response(jsonify({"error": "Show not found"}), 404)

    def delete(self, id):
        show = EpisodeModel.query.filter(EpisodeModel.id == id).first()
        
        if show:
            db.session.delete(show)
            db.session.commit()
            return make_response(jsonify({"message": "Show deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Show not found"}), 404)

class Guests(Resource):
    def get(self):
        guests = []
        for guest in Guest.query.all():
            guest_dict = {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
            guests.append(guest_dict)
        return make_response(jsonify(guests), 200)

class Appearances(Resource):
    def post(self):
        # Extracting data from the request
        guest_id = request.form.get("guest_id")
        episode_id = request.form.get("episode_id")

        if not guest_id or not episode_id:
            missing_fields = []
            if not guest_id:
                missing_fields.append("guest_id")
            if not episode_id:
                missing_fields.append("episode_id")
            return jsonify({"errors": [f"Missing field: {field}" for field in missing_fields]}), 400

        # Fetching the Guest and Episode from the database
        guest = Guest.query.get(guest_id)
        episode = EpisodeModel.query.get(episode_id)

        if not guest:
            return jsonify({"errors": "Guest not found"}), 404
        if not episode:
            return jsonify({"errors": "Episode not found"}), 404

        # Creating a new Appearance object and adding it to the database
        try:
            new_appearance = Appearance(
                guest_id=guest_id,
                episode_id=episode_id
            )

            db.session.add(new_appearance)
            db.session.commit()

            # Returning the newly created Appearance object as JSON response
            appearance_dict = {
                "id": new_appearance.id,
                "guest_id": new_appearance.guest_id,
                "episode_id": new_appearance.episode_id,
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                },
                "episode": {
                    "id": episode.id,
                    "number": episode.number,
                    "date": episode.date
                }
            }
            return jsonify(appearance_dict), 201

       
        except Exception as e:
            db.session.rollback()  
            print("Error occurred:", e)
            return jsonify({"errors": ["An error occurred while creating Appearance"]}), 500


api.add_resource(Episode, '/episodes')
api.add_resource(EpisodesId, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=5555)
