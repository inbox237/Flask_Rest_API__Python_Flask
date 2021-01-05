from models.Artist import Artist
from models.Album import Album
from main import db
from schemas.ArtistSchema import artist_schema, artists_schema
from schemas.AlbumSchema import album_schema, albums_schema
from flask import Blueprint, request, jsonify
from models.Album_Artist_Association import album_artist_association_table as aaat

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
    new_artist.artist_name = artist_fields["artist_name"]

    
    db.session.add(new_artist)
    db.session.commit()
    
    return jsonify(artist_schema.dump(new_artist))

@artists.route("/<int:id>", methods=["GET"])
def artist_show(id):
    #Return a single artist
    artist = Artist.query.get(id)

    return jsonify(artist_schema.dump(artist))

##### Ask Alex H to help me fix further later
@artists.route("/albums/<int:id>", methods=["GET"])
def artist_list_albums(id):
    #Return a single artist's album IDs

    albums = db.session.query(aaat).filter(aaat.c.artist_id == id)
    artist = Artist.query.get(id)
    #artist = db.session.query(Artist).join(Album).filter(Album.id == id).one()
    #artist = db.session.query(Artist).join(aaat).filter(aaat.c.artist_id == id)
    #artist = db.session.query(aaat).join(Artist).join(Album).filter(aaat.c.artist_id == id).one()
    #artist = db.session.query(Album).join(aaat).join(Artist).one()
    artist_list_new = []
    art_scheme = artist_schema.dump(artist)
    for album in albums:
        album_scheme = album_schema.dump(Album.query.get(album.album_id))
        artist_list_new.append((art_scheme, album_scheme))
    return jsonify(artist_list_new) 


@artists.route("/<int:id>", methods=["PUT", "PATCH"])
def artist_update(id):
    #Update a artist
    artists = Artist.query.filter_by(id=id)
    artist_fields = artist_schema.load(request.json)
    artists.update(artist_fields)
    db.session.commit()

    return jsonify(artist_schema.dump(artists[0]))

@artists.route("/<int:id>", methods=["DELETE"])
def artist_delete(id):
    #Delete a artist
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()

    return jsonify(artist_schema.dump(artist))