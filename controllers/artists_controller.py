from models.Artist import Artist
from main import db
from schemas.ArtistSchema import artist_schema, artists_schema
from flask import Blueprint, request, jsonify
artists = Blueprint('artists', __name__, url_prefix="/artists")

@artists.route("/", methods=["GET"])
def artist_index():
    #Retrieve all artists
    artists = Artist.query.all()
    return jsonify(artists_schema.dump(artists))

@artists.route("/", methods=["POST"])
def artist_create():
    #Create a new artist
    artist_fields = artist_schema.load(request.json)

    new_artist = Artist()
    new_artist.artist_title = artist_fields["artist_title"]
    
    db.session.add(new_artist)
    db.session.commit()
    
    return jsonify(artist_schema.dump(new_artist))

@artists.route("/<int:artist_id>", methods=["GET"])
def artist_show(artist_id):
    #Return a single artist
    artist = Artist.query.get(artist_id)
    return jsonify(artist_schema.dump(artist))

@artists.route("/<int:artist_id>", methods=["PUT", "PATCH"])
def artist_update(artist_id):
    #Update a artist
    artists = Artist.query.filter_by(artist_id=artist_id)
    artist_fields = artist_schema.load(request.json)
    artists.update(artist_fields)
    db.session.commit()

    return jsonify(artist_schema.dump(artists[0]))

@artists.route("/<int:artist_id>", methods=["DELETE"])
def artist_delete(artist_id):
    #Delete a artist
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()

    return jsonify(artist_schema.dump(artist))