from controllers.albums_controller import albums
from controllers.artists_controller import artists
from controllers.auth_controller import auth

registerable_controllers = [
    auth,
    albums,
    artists
]