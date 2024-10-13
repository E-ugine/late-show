from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255))  # Set a max length for the date string
    number = db.Column(db.String(255))  # Set a max length for the episode number

    # Relationship mapping Episode to related Appearance
    appearances = db.relationship('Appearance', backref='episode', lazy='joined')

    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.id}: {self.number}>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Ensure name is not null
    occupation = db.Column(db.String(255))  # Set a max length for the occupation string

    # Relationship mapping Guest to Appearance
    appearances = db.relationship('Appearance', backref='guest', lazy='joined')

    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.id}: {self.name}; {self.occupation}>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5')
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id,
            'episode': self.episode.to_dict() if self.episode else None,  # Avoids errors if episode is None
            'guest': self.guest.to_dict() if self.guest else None  # Avoids errors if guest is None
        }

    def __repr__(self):
        return f'<Appearance {self.id}: Episode {self.episode_id}, Guest {self.guest_id}, Rating {self.rating}>'
