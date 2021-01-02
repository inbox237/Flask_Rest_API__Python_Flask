from main import db

class Album(db.Model):
    __tablename__ = "albums"
    
    album_id = db.Column(db.Integer, primary_key=True)
    album_title = db.Column(db.String())