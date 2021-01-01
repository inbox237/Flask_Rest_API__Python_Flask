from models.Album import Album
from main import db
from schemas.AlbumSchema import album_schema, albums_schema
from flask import Blueprint, request, jsonify
albums = Blueprint('albums', __name__, url_prefix="/albums")

@albums.route("/", methods=["GET"])
def album_index():
    #Retrieve all albums
    albums = Album.query.all()
    return jsonify(albums_schema.dump(albums))

@albums.route("/", methods=["POST"])
def album_create():
    #Create a new album
    album_fields = album_schema.load(request.json)

    new_album = Album()
    new_album.title = album_fields["title"]
    
    db.session.add(new_album)
    db.session.commit()
    
    return jsonify(album_schema.dump(new_album))

@albums.route("/<int:album_id>", methods=["GET"])
def album_show(album_id):
    #Return a single album
    album = Album.query.get(album_id)
    return jsonify(album_schema.dump(album))

@albums.route("/<int:album_id>", methods=["PUT", "PATCH"])
def album_update(album_id):
    #Update a album
    albums = Album.query.filter_by(album_id=album_id)
    album_fields = album_schema.load(request.json)
    albums.update(album_fields)
    db.session.commit()

    return jsonify(album_schema.dump(albums[0]))

@albums.route("/<int:album_id>", methods=["DELETE"])
def album_delete(album_id):
    #Delete a album
    album = Album.query.get(album_id)
    db.session.delete(album)
    db.session.commit()

    return jsonify(album_schema.dump(album))