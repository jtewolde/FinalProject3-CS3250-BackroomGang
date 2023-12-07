'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 03- Video Playlist Manager Web Application
Description: This program is meant for conducting black box testing using Selenium
Group Name: Backroom Gang
Developed by: Joseph Tewolde
'''

# These are the imports for the program
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions

# Pre condition: an user with id = "jane" and password = "1" exists in the database
# Post condition: a playlist with name = "test", creation_date = "2021-10-10",
# creator_name = "jane", description = "this is a test", and quantity = 1 exists in the database
# Also, the user is redirected to the playlists page with the url "http://localhost:5000/playlists"


class TestCreatingPlaylist(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        # self.browser = webdriver.Edge()
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:5000/')

    def set_date_field(self, field_id, value):
        """Sets the value of a date field"""
        if field_id == "creation_date":
            # Assuming the date format is "mm/dd/yyyy"
            month, day, year = value.split('/')
            self.browser.find_element(By.ID, field_id).click()

            leftKey = Keys.ARROW_LEFT * 2  # 2 times to get to the month

            time.sleep(1)

            self.browser.find_element(By.ID, field_id).send_keys(leftKey)

            self.browser.find_element(By.ID, field_id).send_keys(month)

            time.sleep(1)

            self.browser.find_element(By.ID, field_id).send_keys(day)
            self.browser.find_element(By.ID, field_id).send_keys(year)

            self.assertIsNotNone(self.browser.find_element(By.ID, field_id))
            time.sleep(1)

    def testCreatingPlaylist(self):
        # Sign In
        self.browser.find_element(By.LINK_TEXT, "Sign In").click()
        self.browser.find_element(By.ID, "id").send_keys("jane")
        self.browser.find_element(By.ID, "passwd").send_keys("1")
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Navigate to Create Playlist
        self.browser.find_element(By.LINK_TEXT, "Create Playlist").click()

        # Form Input Values
        form_values = {
            "name": "test2",
            "creation_date": "12/7/2023",
            "creator_name": "bob",
            "description": "this is a test",
            "quantity": "3 "
        }

        # Fill Form
        for field_id, value in form_values.items():
            if field_id == "creation_date":
                self.set_date_field(field_id, value)
            else:
                element = self.browser.find_element(By.ID, field_id)
                element.click()
                element.send_keys(value)
                self.assertIsNotNone(
                    self.browser.find_element(By.ID, field_id))
                time.sleep(1)

        # Submit Form
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Check if the post condition is met
        playlist_page = self.browser.current_url
        self.assertEqual(playlist_page, "http://localhost:5000/playlists")


# Pre condition: an user with id = "jane" and password = "1" exists in the database
# Pre condition: a playlist with name = "test2" exists in the database and is associated with the user with id = "jane"
# Post condition: the user is redirected to the playlists page with the url "http://localhost:5000/playlists"
# Also, the playlist with name = "test2" is deleted from the database


    def testDeletingPlaylist(self):
        # Sign In
        self.browser.find_element(By.LINK_TEXT, "Sign In").click()
        self.browser.find_element(By.ID, "id").send_keys("jane")
        self.browser.find_element(By.ID, "passwd").send_keys("1")
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Delete Playlist
        # Locate the row associated with the playlist name "test2"
        playlist_row = self.browser.find_element(
            By.XPATH, "//td[text()='test2']/parent::tr")

        # Click on the "Delete Playlist" button in the same row
        delete_button = playlist_row.find_element(
            By.XPATH, ".//button[text()='Delete Playlist']")
        delete_button.click()

        self.browser.switch_to.alert.accept()  # Accept the alert

        time.sleep(1)

        # Check if the post condition is met
        playlist_page = self.browser.current_url
        self.assertEqual(playlist_page, "http://localhost:5000/playlists")

        # Check if the playlist is deleted from the database
        self.assertFalse(self.browser.find_elements(
            By.XPATH, "//td[text()='test2']/parent::tr"))

    # Pre condition: an user with id = "jane" and password = "1" exists in the database
    # Pre condition: a playlist with name = "THE PLAYLIST" exists in the database and is associated with the user with id = "jane"
    # Post condition: the user is redirected to the videos page with the url "http://localhost:5000/playlists/1/videos"

    def testViewingVideos(self):
        # Sign In
        self.browser.find_element(By.LINK_TEXT, "Sign In").click()
        self.browser.find_element(By.ID, "id").send_keys("jane")
        self.browser.find_element(By.ID, "passwd").send_keys("1")
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Locate the row associated with the playlist name "THE PLAYLIST"
        playlist_row = self.browser.find_element(
            By.XPATH, "//td[text()='THE PLAYLIST']/parent::tr")

        # Click on the "View Videos" button in the same row
        view_button = playlist_row.find_element(
            By.XPATH, ".//button[text()='View Videos']")
        view_button.click()

        time.sleep(1)

        # Check if the post condition is met
        videos_page = self.browser.current_url
        self.assertEqual(
            videos_page, "http://localhost:5000/playlists/1/videos")

    # Pre condition: an user with id = "jane" and password = "1" exists in the database
    # Pre condition: a playlist with name = "THE PLAYLIST" exists in the database with no videos
    # and is associated with the user with id = "jane"

    # Post condition: the user is redirected to the videos page with the url "http://localhost:5000/playlists/1/videos"
    # Also, a video with name = "test", url = "https://www.youtube.com/watch?v=9C_HReR_McQ", and length = 5 is added to the database

    def testAddingVideos(self):
        # Sign In
        self.browser.find_element(By.LINK_TEXT, "Sign In").click()
        self.browser.find_element(By.ID, "id").send_keys("jane")
        self.browser.find_element(By.ID, "passwd").send_keys("1")
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Locate the row associated with the playlist name "THE PLAYLIST"
        playlist_row = self.browser.find_element(
            By.XPATH, "//td[text()='THE PLAYLIST']/parent::tr")

        # Click on the "View Videos" button in the same row
        view_button = playlist_row.find_element(
            By.XPATH, ".//button[text()='View Videos']")

        view_button.click()

        time.sleep(1)

        # Click on the "Add Video" button

        self.browser.find_element(
            By.XPATH, "//button[text()='Add Video']").click()

        time.sleep(1)

        # Form Input Values
        form_values = {
            "name": "test",
            "url": "https://www.youtube.com/watch?v=9C_HReR_McQ",
            "length": "5"
        }

        # Fill Form
        for field_id, value in form_values.items():
            element = self.browser.find_element(By.ID, field_id)
            element.click()
            element.send_keys(value)
            time.sleep(1)
            self.assertIsNotNone(self.browser.find_element(By.ID, field_id))
            time.sleep(1)

        # Submit Form
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Check if the post condition is met
        videos_page = self.browser.current_url
        self.assertEqual(
            videos_page, "http://localhost:5000/playlists/1/videos")

    # Pre condition: an user with id = "jane" and password = "1" exists in the database
    # Pre condition: a playlist with name = "THE PLAYLIST" exists in the database with a video with name = "test"
    # and is associated with the user with id = "jane"

    # Post condition: the user is redirected to the videos page with the url "http://localhost:5000/playlists/1/videos"
    # Also, the video with name = "test" is deleted from the database

    def testDeletingVideos(self):
        # Sign In
        self.browser.find_element(By.LINK_TEXT, "Sign In").click()
        self.browser.find_element(By.ID, "id").send_keys("jane")
        self.browser.find_element(By.ID, "passwd").send_keys("1")
        self.browser.find_element(By.ID, "submit").click()
        time.sleep(1)

        # Locate the row associated with the playlist name "THE PLAYLIST"
        playlist_row = self.browser.find_element(
            By.XPATH, "//td[text()='THE PLAYLIST']/parent::tr")

        # Click on the "View Videos" button in the same row
        view_button = playlist_row.find_element(
            By.XPATH, ".//button[text()='View Videos']")

        view_button.click()

        time.sleep(1)

        # Locate the row associated with the video name "test"
        video_row = self.browser.find_element(
            By.XPATH, "//td[text()='test']/parent::tr")

        # Click on the "Delete Video" button in the same row
        delete_button = video_row.find_element(
            By.XPATH, ".//button[text()='Delete']")
        delete_button.click()

        self.browser.switch_to.alert.accept()  # Accept the alert

        time.sleep(1)

        # Check if the post condition is met
        videos_page = self.browser.current_url
        self.assertEqual(
            videos_page, "http://localhost:5000/playlists/1/videos?video_id=3")

        # Check if the video is deleted from the database
        self.assertFalse(self.browser.find_elements(
            By.XPATH, "//td[text()='test']/parent::tr"))


if __name__ == '__main__':
    unittest.main()
