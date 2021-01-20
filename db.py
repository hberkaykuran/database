import os
import sys
import copy

import psycopg2
import psycopg2.extras

import secret

from models.Artist import Artist
from models.ArtPiece import ArtPiece
from models.Comment import Comment
from models.FavArtist import FavArtist
from models.FavArtPiece import FavArtPiece
from models.FavMuseum import FavMuseum
from models.Museum import Museum
from models.User import User

from werkzeug.security import check_password_hash

class Database:
    def __init__(self): 
        self.url = os.getenv("DATABASE_URL")
        if not self.url:
            self.url = secret.dbUrl

    ########    User    ########
    
    #ADD USER
    def user_add(self,user):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = """INSERT INTO "USER" (username, password, age, sex, location, email, profilePicture, isModerator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                data = [user.username, user.password, user.age, user.sex, user.location, user.email, user.profilePicture, user.isModerator]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add user error: ",err)
        return None

    #UPDATE summary
    def user_update_summary(self, username, summary):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = """UPDATE "USER" SET summary = %s WHERE username = %s"""
                data = [summary, username]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update summary error: ",err)
        return None

    #UPDATE profilePicture
    def user_update_profilePicture(self, profilePicture, username):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = """UPDATE "USER" SET profilePicture = %s WHERE username = %s"""
                data = [profilePicture, username]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update profile picture error: ",err)
        return None

    #UPDATE password
    def user_update_password(self,username,password):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                #encrypt password
                statement = """UPDATE "USER" SET password = %s WHERE username = %s"""
                data = [password, username]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update password error: ",err)
        return None

    #SEARCH user
    def user_search(self,searchFilter,searchValue):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = f"SELECT username FROM \"USER\" WHERE {searchFilter} LIKE %s"
                data = ['%'+searchValue+'%']
                cursor.execute(statement, data)
                result = cursor.fetchall()
                cursor.close()
        except Exception as err:
            print("User search error: ",err)
        return result

    #GETINFO user
    def user_userinfo(self,username):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "SELECT username,age,sex,location,summary,profilePicture,isModerator FROM \"USER\" WHERE username=%s"
                data = [username]
                cursor.execute(statement, data)
                result = cursor.fetchone()
                cursor.close()
        except Exception as err:
            print("User search error: ",err)
        return result

    ########    Museum    ########

    #ADD MUSEUM
    def museum_add(self,museum):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "INSERT INTO MUSEUM (name, location, summary, museumPicture, userID) VALUES (%s, %s, %s, %s, %s)"
                data = [museum.name, museum.location, museum.summary, museum.museumPicture, museum.userID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add museum error: ",err)
        return None

    #UPDATE userID
    def museum_update_userID(self,museumID,userID):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE MUSEUM SET userID = %s WHERE museumID = %s"
                data = [userID, museumID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update moderator error: ",err)
        return None

    #UPDATE museumPicture
    def museum_update_museumPicture(self,museumID,museumPicture):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE MUSEUM SET museumPicture = %s WHERE museumID = %s"
                data = [museumPicture, museumID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update picture error: ",err)
        return None

    #UPDATE summary
    def museum_update_summary(self,museumID,summary):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE MUSEUM SET summary = %s WHERE museumID = %s"
                data = [summary, museumID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update summary error: ",err)
        return None

    ########    Artist    ########

    #ADD Artist
    def artist_add(self,artist):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "INSERT INTO ARTIST (name, summary, artistPicture) VALUES (%s, %s, %s)"
                data = [artist.name, artist.summary, artist.artistPicure]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add museum error: ",err)
        return None

    #UPDATE artistPicture
    def artist_update_artistPicture(self,artistID,artistPicture):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE ARTIST SET artistPicture = %s WHERE artistID = %s"
                data = [artistPicture, artistID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update picture error: ",err)
        return None

    #UPDATE summary
    def artist_update_summary(self,artistID,summary):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE ARTIST SET summary = %s WHERE artistID = %s"
                data = [summary, artistID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update summary error: ",err)
        return None
    ########    ArtPiece    ########

    #ADD ArtPiece
    def artpiece_add(self,artpiece):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "INSERT INTO ARTPIECE (name, era, summary, field, artPiecePicture, museumID, artistID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [artpiece.name, artpiece.era, artpiece.summary, artpiece.field, artpiece.artPiecePicture, artpiece.museumID, artpiece.artistID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add art piece error: ",err)
        return None

    #UPDATE summary
    def artpiece_update_summary(self,artPieceID,summary):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE ARTPIECE SET summary = %s WHERE artPieceID = %s"
                data = [summary, artPieceID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update summary error: ",err)
        return None

    #UPDATE artistPicture
    def artpiece_update_artPiecePicture(self,artPieceID,artPiecePicture):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = "UPDATE ARTPIECE SET artPiecePicture = %s WHERE artPieceID = %s"
                data = [artPiecePicture, artPieceID]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Update picture error: ",err)
        return None


    def login(self,un,password):
        try:
            with psycopg2.connect(self.url) as con:
                cursor = con.cursor()
                statement = """SELECT password FROM "USER" WHERE username=%s"""
                usr = [un]
                cursor.execute(statement,usr)
                data = cursor.fetchone()
                cursor.close()
                return  check_password_hash(data[0],password)
        except Exception as err:
            print("Login error: ",err)
        return None