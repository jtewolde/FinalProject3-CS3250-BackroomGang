'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 03- Video Playlist Manager Web Application
Description: This program is meant for testing the data model
Group Name: Backroom Gang
Developed by: Joseph Tewolde
'''
# These are the imports for the program
from sqlalchemy import *
from sqlalchemy.engine import *
from sqlalchemy.orm import *

# This is the base class for the program


class Base(DeclarativeBase):
    pass

# This is the class for the user table


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # user id
    email = Column(String, unique=False, nullable=False)  # email address
    passwd = Column(String)  # password
    creation_date = Column(String)  # date of creation

    # playlists created by user, cascade deletes all playlists created by user when user is deleted
    playlists = relationship(
        'Playlist', cascade="all,delete", backref='user', lazy=True)

# This is the class for the playlist table


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True)  # playlist id
    name = Column(String, unique=False, nullable=False)  # playlist name
    creation_date = Column(String)  # date of creation
    creator_name = Column(String)  # creator id
    quantity = Column(Integer)  # number of videos in playlist

    users_id = Column(String, ForeignKey('users.id'),
                      nullable=False)  # user id
    # videos in playlist, cascade deletes all videos in playlist when playlist is deleted
    videos = relationship('Video', cascade="all,delete",
                          backref='playlist', lazy=True)

# This is the class for the video table


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True)  # video id
    name = Column(String, unique=False, nullable=False)  # video name
    url = Column(String)  # url of video

    playlist_id = Column(String, ForeignKey(
        'playlists.id'), nullable=False)  # playlist id


# This is the main function for the program
if __name__ == "__main__":
    # This is the engine for the program
    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(engine)

    # This is the session for the program
    Session = sessionmaker(bind=engine)
    session = Session()

    # This is the user for the program
    user1 = User(id="jotewolde", email="jotewolde@aol.com",
                 passwd="password", creation_date="10/10/2021")
    user2 = User(id="JMurray", email="Jmurray@gmail.com",
                 passwd="123456", creation_date="09/10/2024")
    user3 = User(id="Bsolz", email="BSolz@yahoo.com",
                 passwd="password", creation_date="07/24/2021")

    session.add(user1)  # add user to session
    session.add(user2)  # add user to session
    session.add(user3)  # add user to session

    # This is the playlist for the program
    playlist1 = Playlist(id="1", name="Playlist", creation_date="10/10/2021",
                         creator_name="Jamal", quantity=1, users_id="jotewolde")
    playlist2 = Playlist(id="2", name="Playlist2", creation_date="10/31/2023",
                         creator_name="Michael", quantity=1, users_id="jotewolde")

    playlist3 = Playlist(id="3", name="Playlist3", creation_date="10/10/2021",
                         creator_name="Jamal", quantity=1, users_id="JMurray")
    playlist4 = Playlist(id="4", name="Playlist4", creation_date="10/31/2023",
                         creator_name="Michael", quantity=1, users_id="JMurray")

    playlist5 = Playlist(id="5", name="Playlist5", creation_date="10/10/2021",
                         creator_name="Jamal", quantity=1, users_id="Bsolz")
    playlist6 = Playlist(id="6", name="Playlist6", creation_date="10/31/2023",
                         creator_name="Michael", quantity=1, users_id="Bsolz")

    session.add(playlist1)  # add playlist to session
    session.add(playlist2)  # add playlist to session
    session.add(playlist3)  # add playlist to session
    session.add(playlist4)  # add playlist to session
    session.add(playlist5)  # add playlist to session
    session.add(playlist6)  # add playlist to session

    # This is the video for the program
    video = Video(id="1", name="Video", url="www.youtube.com", playlist_id="1")
    video2 = Video(id="2", name="Video2",
                   url="www.youtube.com", playlist_id="1")
    video3 = Video(id="3", name="Video3",
                   url="www.youtube.com", playlist_id="1")

    video4 = Video(id="4", name="Video4",
                   url="www.youtube.com", playlist_id="2")
    video5 = Video(id="5", name="Video5",
                   url="www.youtube.com", playlist_id="2")
    video6 = Video(id="6", name="Video6",
                   url="www.youtube.com", playlist_id="2")

    video7 = Video(id="7", name="Video7",
                   url="www.youtube.com", playlist_id="3")
    video8 = Video(id="8", name="Video8",
                   url="www.youtube.com", playlist_id="3")

    video9 = Video(id="9", name="Video9",
                   url="www.youtube.com", playlist_id="4")
    video10 = Video(id="10", name="Video10",
                    url="www.youtube.com", playlist_id="4")

    video11 = Video(id="11", name="Video11",
                    url="www.youtube.com", playlist_id="5")
    video12 = Video(id="12", name="Video12",
                    url="www.youtube.com", playlist_id="5")

    session.add(video)  # add video to session
    session.add(video2)  # add video to session
    session.add(video3)  # add video to session
    session.add(video4)  # add video to session
    session.add(video5)  # add video to session
    session.add(video6)  # add video to session
    session.add(video7)  # add video to session
    session.add(video8)  # add video to session
    session.add(video9)  # add video to session
    session.add(video10)  # add video to session
    session.add(video11)  # add video to session
    session.add(video12)  # add video to session
    session.commit()  # commit session

    # This is the query for the program
    query = session.query(User).all()
    for user in query:
        print(user.id, user.email, user.passwd,
              user.creation_date)  # print query

    # This is the query for the program
    query = session.query(Playlist).all()
    for playlist in query:
        print(playlist.id, playlist.name, playlist.creation_date,
              playlist.creator_name, playlist.quantity, playlist.users_id)  # print query

    # This is the query for the program
    query = session.query(Video).all()
    for video in query:
        print(video.id, video.name, video.url,
              video.playlist_id)  # print query

    # Testing the delete cascade
    session.delete(playlist6)  # delete playlist
    session.delete(playlist4)
    session.commit()  # commit session

    # See if playlist2 is deleted and all videos in playlist2 are deleted
    query = session.query(Playlist).all()
    for playlist in query:
        print(playlist.id, playlist.name, playlist.creation_date,
              playlist.creator_name, playlist.quantity, playlist.users_id)  # print query

    query = session.query(Video).all()
    for video in query:
        print(video.id, video.name, video.url,
              video.playlist_id)  # print query

    # Testing the delete cascade for user
    session.delete(user1)  # delete user
    session.commit()  # commit session

    # See if user1 is deleted and all playlists created by user1 are deleted
    query = session.query(User).all()
    for user in query:
        print(user.id, user.email, user.passwd,
              user.creation_date)  # print query
