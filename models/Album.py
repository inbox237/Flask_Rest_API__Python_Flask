from main import db
from models.Album_Artist_Association import album_artist_association_table
from models.Artist import Artist

class Album(db.Model):
    __tablename__ = "albums"
    
    id = db.Column(db.Integer, primary_key=True)
    album_title = db.Column(db.String())
    album_s_artists = db.relationship("Artist",
                        secondary=album_artist_association_table,
                        back_populates="artist_s_albums")

    def __repr__(self):
        return f"<Album {self.album_title}>"
