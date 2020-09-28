import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
	__tablename__ = "album"

	id = sa.Column(sa.INTEGER, primary_key = True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def find(artist):
	session = connect_db()
	albums_count = session.query(Album).filter(Album.artist == artist).count()
	albums_list = session.query(Album).filter(Album.artist == artist).all()
	return albums_count, albums_list

def capitalize_name(s):
	s_capitalized = ' '.join([s_part.capitalize() for s_part in s.split(' ')])
	return s_capitalized

def title_name(s):
	if s:
		s_parts = [s_part.lower() for s_part in s.split(' ')]
		s_parts[0].capitalize()
		s_titled = ' '.join(s_parts)
		return s_titled
	else:
		return ''

#проверяет заполненность полей: artist, album
#проверяет корректность формата: year
def validate(album_data):
	result = True
	message=""

	if not album_data["artist"]:
		result = False
		message = "Не указан исполнитель"
	elif not album_data["album"]:
		result = False
		message = "Не указано название альбома"
	elif album_data["year"]:
		if len(album_data["year"])!=4 or not album_data["year"].isnumeric():
			result = False
			message = "Год выпуска альома указан в неверном формате"

	return result, message


def album_create(album_data):
	try:
		session = connect_db()
		album_record = session.query(Album).filter(sa.and_(Album.artist == album_data["artist"], Album.album == album_data["album"])).first()
		if album_record is None:
			album_record = Album(
				artist = album_data["artist"],
				album = album_data["album"],
				genre = album_data["genre"],
				year = album_data["year"])
		else:
			album_record.artist = album_data["artist"]
			album_record.album = album_data["album"]
			album_record.genre = album_data["genre"]
			album_record.year = album_data["year"]
		session.add(album_record)
		session.commit()
		print("commit OK")
	except Exception as err:
		print("commit NOK")
		result = False
		print(err)
		return result
	else:
		result = True
		return result
	finally:
		pass
	
	


