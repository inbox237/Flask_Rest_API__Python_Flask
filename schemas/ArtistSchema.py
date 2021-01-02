from main import ma
from models.Artist import Artist

class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)