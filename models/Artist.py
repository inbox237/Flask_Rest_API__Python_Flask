from main import db

class Artist(db.Model):
    __tablename__ = "artists"
    
    id = db.Column(db.Integer, primary_key=True)
    artist_title = db.Column(db.String())