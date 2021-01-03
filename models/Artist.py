from main import db
from models.Album_Artist_Association import album_artist_association_table

class Artist(db.Model):
    __tablename__ = "artists"
    
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String())
    artist_s_albums = db.relationship("Album",
                        secondary=album_artist_association_table,
                        back_populates="album_s_artists")