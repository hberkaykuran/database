"""
This script runs the database application using a development server.
"""
import os
import sys

import psycopg2

INIT_STATEMENTS = [
        """CREATE TABLE IF NOT EXISTS "USER"(
	userID BIGSERIAL,
	username VARCHAR(20	) NOT NULL,
	password VARCHAR(20) NOT NULL,
	age INT NOT NULL,
	sex VARCHAR(255) NOT NULL,
	location VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	summary TEXT,
	profilePicture VARCHAR(255),
	isModerator BOOL NOT NULL,
	PRIMARY KEY (userID),
	UNIQUE(username),
	UNIQUE(email))""",

	"""CREATE TABLE IF NOT EXISTS Museum(	
	museumID BIGSERIAL,
	name VARCHAR(255) NOT NULL,
	location TEXT NOT NULL,
	summary TEXT NOT NULL,
	museumPicture VARCHAR(255),
	userID INT NOT NULL,
	PRIMARY KEY (museumID),
	FOREIGN KEY (userID) REFERENCES "USER"(userID))""",

	"""CREATE TABLE IF NOT EXISTS Artist(
	artistID BIGSERIAL,
	name VARCHAR(255) NOT NULL,
	summary TEXT NOT NULL,
	artistPicture VARCHAR(255),
	PRIMARY KEY (artistID))""",

	"""CREATE TABLE IF NOT EXISTS ArtPiece(
	artPieceID BIGSERIAL,
	name VARCHAR(255) NOT NULL,
	era VARCHAR(255) NOT NULL,
	summary TEXT NOT NULL,
	field VARCHAR(255) NOT NULL,
	artPiecePicture VARCHAR(255),
	museumID INT NOT NULL,
	artistID INT NOT NULL,
	PRIMARY KEY (artPieceID),
	FOREIGN KEY (museumID) REFERENCES Museum(museumID),
	FOREIGN KEY (artistID) REFERENCES Artist(artistID))""",


	"""CREATE TABLE IF NOT EXISTS FavMuseum(
	userID INT NOT NULL,
	museumID INT NOT NULL,
	FOREIGN KEY(userID) REFERENCES "USER"(userID),
	FOREIGN KEY(museumID) REFERENCES Museum(museumID),
	CONSTRAINT compKey_userID_museumID PRIMARY KEY(userID,museumID))""",

	"""CREATE TABLE IF NOT EXISTS FavArtPiece(
	userID INT NOT NULL,
	artPieceID INT NOT NULL,
	FOREIGN KEY(userID) REFERENCES "USER"(userID),
	FOREIGN KEY(artPieceID) REFERENCES ArtPiece(artPieceID ),
	CONSTRAINT compKey_userID_artPieceID PRIMARY KEY(userID,artPieceID))""",

	"""CREATE TABLE IF NOT EXISTS FavArtist(
	userID INT NOT NULL,
	artistID INT NOT NULL,
	FOREIGN KEY(userID) REFERENCES "USER"(userID),
	FOREIGN KEY(artistID) REFERENCES Artist(artistID ),
	CONSTRAINT compKey_userID_artistID PRIMARY KEY(userID,artistID))""",

	"""CREATE TABLE IF NOT EXISTS Comment(
	commentID BIGSERIAL,
	comment VARCHAR (255) NOT NULL,
	time TIMESTAMPTZ NOT NULL,
	userID INT NOT NULL,
	artPieceID INT NOT NULL,
	PRIMARY KEY(commentID),
	FOREIGN KEY(userID) REFERENCES "USER"(userID),
	FOREIGN KEY(artPieceID) REFERENCES ArtPiece(artPieceID))""",
]

def initialize(url):
    try:
        with psycopg2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
            cursor.close()
    except Exception as err:
        print("Error: ", err)


if __name__ == "__main__":
    url = "postgresql://postgres:24712015046b@localhost:8000/databaseproject"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        os._exit(1)
    initialize(url)