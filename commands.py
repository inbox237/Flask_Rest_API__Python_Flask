from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.Album import Album
    from models.Artist import Artist
    from models.Album_Artist_Association import album_artist_association_table as aaat
    from faker import Faker
    import random
    faker = Faker()

    association_pairs = []
    
    count = [0]*10
    for i in range(1,11):
        artist = Artist()
        album = Album()

        artist.artist_name = faker.unique.name()
        album.album_title = faker.unique.catch_phrase()
        
       
        #Link pairs
        art_int = random.randint(1,10)
        alb_int = random.randint(1,10)
        #don't enter duplicates
        while (art_int,alb_int) in association_pairs:
            art_int = random.randint(1,10)
            alb_int = random.randint(1,10)
        count[art_int-1]+=1
        association_pairs.append((art_int,alb_int))

        db.session.add(artist)
        db.session.add(album)

    
  
    #create main tables   
    db.session.commit()
    #Count Artist's Albums
    print(f'art_count: {count}')
    for i,val in enumerate(count):
        print(f'ind: {i} val: {val}')
        artist = db.session.query(Artist).filter(Artist.id==i+1).one()
        artist.artist_s_albums_count = val
        db.session.commit()
    #create association table
    db.session.execute(aaat.insert().values(association_pairs))
    db.session.commit()

    print("Tables seeded")

