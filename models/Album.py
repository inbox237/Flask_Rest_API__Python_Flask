from main import db

class Album(db.Model):
    __tablename__ = "albums"
    
    id = db.Column(db.Integer, primary_key=True)
    album_title = db.Column(db.String())