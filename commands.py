from main import db
from flask import Blueprint
import click
from click import pass_context

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.Album import Album
    from models.Artist import Artist
    from models.User import User
    from models.Playlist import Playlist
    from models.Album_Artist_Association import album_artist_association_table as aaat
    from models.User_Playlist_Association import user_playlist_association_table as upat
    
    from main import bcrypt
    from faker import Faker
    import random
    faker = Faker()

    users = []

    art_alb_association_pairs = []
    usr_pla_association_pairs = []
    count_art_alb = [0]*10
    count_alb_art = [0]*10
    count_usr_pla = [0]*10
    count_pla_usr = [0]*10

#Users/Playlists
    for i in range(1,11):
        user = User()
        playlist = Playlist()

        playlist.playlist_title = faker.unique.name()

        user.email = f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.user_season = random.randint(1,4)
    
        #User/Playlist - Link Pairs
        usr_int = random.randint(1,10)
        pla_int = random.randint(1,10)

        #Append Association List - Users and Playlists - don't enter duplicates
        while (usr_int,pla_int) in usr_pla_association_pairs:
            usr_int = random.randint(1,10)
            pla_int = random.randint(1,10)

        #Add count both directions
        count_usr_pla[usr_int-1]+=1
        count_pla_usr[pla_int-1]+=1

        usr_pla_association_pairs.append((usr_int,pla_int))

        db.session.add(user)
        db.session.add(playlist)
        users.append(user)

    db.session.commit()
    

#Artists/Albums
    for i in range(1,11):
        artist = Artist()
        album = Album()
        artist.user_id = random.choice(users).id
        artist.artist_name = faker.unique.name()
        album.album_title = faker.unique.catch_phrase()
        
        #Artist/Album - Link Pairs
        art_int = random.randint(1,10)
        alb_int = random.randint(1,10)
       
        #Append Association List - Albums and Artists - don't enter duplicates
        while (art_int,alb_int) in art_alb_association_pairs:
            art_int = random.randint(1,10)
            alb_int = random.randint(1,10)

        #Add count both directions
        count_art_alb[art_int-1]+=1
        count_alb_art[alb_int-1]+=1

        art_alb_association_pairs.append((art_int,alb_int))

        db.session.add(artist)
        db.session.add(album)
  
    #create main tables   
    db.session.commit()

#COUNTS
    #Count Artist's Albums
    print(f'art_count: {count_art_alb}')
    for i,val in enumerate(count_art_alb):
        print(f'ind: {i} val: {val}')
        artist = db.session.query(Artist).filter(Artist.id==i+1).one()
        artist.artist_s_albums_count = val
        db.session.commit()

    #Count Album's Artists
    print(f'alb_count: {count_alb_art}')
    for i,val in enumerate(count_alb_art):
        print(f'ind: {i} val: {val}')
        album = db.session.query(Album).filter(Album.id==i+1).one()
        album.album_s_artists_count = val
        db.session.commit()

    #Count User's playlists
    print(f'usr_count: {count_usr_pla}')
    for i,val in enumerate(count_usr_pla):
        print(f'ind: {i} val: {val}')
        user = db.session.query(User).filter(User.id==i+1).one()
        user.user_s_playlists_count = val
        db.session.commit()

    #Count Playlist's Users
    print(f'pla_count: {count_pla_usr}')
    for i,val in enumerate(count_pla_usr):
        print(f'ind: {i} val: {val}')
        playlist = db.session.query(Playlist).filter(Playlist.id==i+1).one()
        playlist.playlist_s_users_count = val
        db.session.commit()


    #create association tables
    db.session.execute(aaat.insert().values(art_alb_association_pairs))
    db.session.execute(upat.insert().values(usr_pla_association_pairs))
    db.session.commit()

    print("Tables seeded")

@db_commands.cli.command("refresh")
@pass_context
def refresh_db(ctx):
    drop_db.invoke(ctx)
    create_db.invoke(ctx)
    seed_db.invoke(ctx)
    print("Done!")