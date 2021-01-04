from main import ma
from models.Album import Album
from marshmallow.validate import Length

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
    
    album_title = ma.String(required=True, validate=Length(min=1))

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)