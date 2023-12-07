'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 03- Video Playlist Manager Web Application
Description: This program is meant for doing white box testing on the models.py file
Group Name: Backroom Gang
Developed by: Joseph Tewolde
'''

# These are the imports for the program
import unittest
from sqlalchemy import *
from sqlalchemy.engine import *
from sqlalchemy.orm import *
from testing_models import *

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


class TestModels(unittest.TestCase):
    """ This class is meant for testing the models.py file """

    def setUp(self):
        """ This function is meant for setting up the testing environment """
        # This is the engine for the program
        self.engine = create_engine('sqlite:///test.db', echo=True)
        Base.metadata.create_all(self.engine)

        # This is the session for the program
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """ This function is meant for tearing down the testing environment """
        self.session.close()  # Close the session

    def test_user_creation(self):
        """ This function is meant for testing the user table """
        # This is the user for the program
        user = User(id="test", email="test@gmail.com",
                    passwd="password", creation_date="10/10/2021")

        self.session.add(user)  # add user to session
        self.session.commit()
        self.assertEqual(user.id, "test")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.passwd, "password")
        self.assertEqual(user.creation_date, "10/10/2021")

    def test_playlist_creation(self):
        """ This function is meant for testing the playlist table """
        # This is the playlist for the program
        playlist = Playlist(id="testPlaylist", name="playlist1", creation_date="07/13/2023",
                            creator_name="creator", quantity=2, users_id="test")

        self.session.add(playlist)
        self.session.commit()
        self.assertEqual(playlist.id, "testPlaylist")
        self.assertEqual(playlist.name, "playlist1")
        self.assertEqual(playlist.creation_date, "07/13/2023")
        self.assertEqual(playlist.creator_name, "creator")
        self.assertEqual(playlist.quantity, 2)
        self.assertEqual(playlist.users_id, "test")

    def test_video_creation(self):
        """ This function is meant for testing the video table """
        # This is the video for the program
        video = Video(id="testVideo", name="video1",
                      url="www.youtube.com", playlist_id="testPlaylist")

        self.session.add(video)
        self.session.commit()
        self.assertEqual(video.id, "testVideo")
        self.assertEqual(video.name, "video1")
        self.assertEqual(video.url, "www.youtube.com")
        self.assertEqual(video.playlist_id, "testPlaylist")

    def test_add_user(self):
        """ This function is meant for testing adding a user to the database """
        # This is the user for the program
        user2 = User(id="test2", email="jtewolde@gmail.com",
                     passwd="1234", creation_date="08/10/2021")

        # Get the number of users in the database
        num_users = self.session.query(User).count()

        self.session.add(user2)
        self.session.commit()
        self.assertEqual(user2.id, "test2")
        self.assertEqual(user2.email, "jtewolde@gmail.com")
        self.assertEqual(user2.passwd, "1234")
        self.assertEqual(user2.creation_date, "08/10/2021")
        self.assertEqual(user2, self.session.query(
            User).filter_by(id="test2").first())
        self.assertEqual(self.session.query(User).count(), num_users + 1)

    def test_add_playlist(self):
        """ This function is meant for testing adding a playlist to the database """
        # This is the playlist for the program
        playlist2 = Playlist(id="testPlaylist2", name="playlist2", creation_date="07/13/2023",
                             creator_name="creator", quantity=2, users_id="test2")

        # Get the number of playlists in the database
        num_playlists = self.session.query(Playlist).count()

        self.session.add(playlist2)
        self.session.commit()
        self.assertEqual(playlist2.id, "testPlaylist2")
        self.assertEqual(playlist2.name, "playlist2")
        self.assertEqual(playlist2.creation_date, "07/13/2023")
        self.assertEqual(playlist2.creator_name, "creator")
        self.assertEqual(playlist2.quantity, 2)
        self.assertEqual(playlist2.users_id, "test2")
        self.assertEqual(playlist2, self.session.query(
            Playlist).filter_by(id="testPlaylist2").first())
        self.assertEqual(self.session.query(
            Playlist).count(), num_playlists + 1)

    def test_add_video(self):
        """ This function is meant for testing adding a video to the database """
        # This is the video for the program
        video2 = Video(id="testVideo2", name="video2",
                       url="www.youtube.com", playlist_id="testPlaylist2")

        num_videos = self.session.query(Video).count()

        self.session.add(video2)
        self.session.commit()

        self.assertEqual(video2.id, "testVideo2")
        self.assertEqual(video2.name, "video2")
        self.assertEqual(video2.url, "www.youtube.com")
        self.assertEqual(video2.playlist_id, "testPlaylist2")
        self.assertEqual(video2, self.session.query(
            Video).filter_by(id="testVideo2").first())
        self.assertEqual(self.session.query(Video).count(), num_videos + 1)

    def test_delete_video(self):
        """ This function is meant for testing deleting a video from the database """
        # This is the video for the program
        video3 = Video(id="testVideo3", name="video3",
                       url="www.youtube.com", playlist_id="testPlaylist2")

        numVideos = self.session.query(Video).count()

        self.session.add(video3)
        self.session.commit()

        self.assertEqual(self.session.query(Video).filter_by(
            id="testVideo3").first(), video3)
        self.assertEqual(self.session.query(Video).count(), numVideos + 1)

        self.session.delete(video3)
        self.session.commit()

        self.assertEqual(self.session.query(
            Video).filter_by(id="testVideo3").first(), None)
        self.assertEqual(self.session.query(Video).count(), numVideos)

    def test_delete_playlist(self):
        """ This function is meant for testing deleting a playlist from the database and all videos in the playlist """
        # This is the playlist for the program
        playlist3 = Playlist(id="testPlaylist3", name="playlist3", creation_date="07/13/2023",
                             creator_name="creator", quantity=2, users_id="test2")

        numPlaylists = self.session.query(Playlist).count()
        numSongsInPlaylist = self.session.query(
            Video).filter_by(playlist_id="testPlaylist3").count()

        self.session.add(playlist3)
        self.session.commit()

        self.assertEqual(self.session.query(Playlist).filter_by(
            id="testPlaylist3").first(), playlist3)
        self.assertEqual(self.session.query(
            Playlist).count(), numPlaylists + 1)
        self.assertEqual(self.session.query(Video).filter_by(
            playlist_id="testPlaylist3").count(), numSongsInPlaylist)

        self.session.delete(playlist3)
        self.session.commit()

        self.assertEqual(self.session.query(Playlist).filter_by(
            id="testPlaylist3").first(), None)
        self.assertEqual(self.session.query(Playlist).count(), numPlaylists)
        self.assertEqual(self.session.query(Video).filter_by(
            playlist_id="testPlaylist3").count(), 0)


if __name__ == "__main__":
    unittest.main()  # Run the tests
