from bottle import run
from bottle import route
from bottle import HTTPError
from bottle import request


import album

@route('/albums/<artist>')
def albums(artist):
	albums_count, albums_list = album.find(artist)
	album_names = [album.album for album in albums_list]
	print(album_names)
	result1 = "<h1>По исполнителю {} найдено {} альбом(-ов)</h1>\n".format(artist, albums_count)
	result2 = "".join(map(lambda item:"<li>{}</li>\n".format(item), album_names))
	result2 = "<div><ol>"+result2+"</ol>\n</div>\n"
	return result1 + result2

@route('/albums/', method = 'POST')
def albums_post():
	album_data = {'album': request.forms.get('album'),
		'year': request.forms.get('year'),
		'artist': request.forms.get('artist'),
		'genre': request.forms.get('genre')}
		
	#выполняем необходимые проверки	
	result,message = album.validate(album_data)
	if not result:
		res_html = "<h1>{}</h1>\n".format(message)
		return res_html

	album_data['artist'] = album.capitalize_name(album_data['artist'])
	album_data['album'] = album.capitalize_name(album_data['album'])
	if album_data['genre']:
		album_data['genre'] = album.capitalize_name(album_data['genre'])

	print(album_data) #для теста

	result = album.album_create(album_data)
	if result:
		res_html = "<h1>Успех!</h1>\n<h2>Альбом исполнителя {} добавлен в базу данных:</h2>\n".format(album_data["artist"])
		return res_html



if __name__ == "__main__":
	run(host='localhost', port=8080, debug=True)