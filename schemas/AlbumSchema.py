from main import ma
from models.Album import Album

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)