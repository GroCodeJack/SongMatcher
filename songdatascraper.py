import requests
from bs4 import BeautifulSoup

def printSongs(playlist):
	for song in playlist:
		print("Title: ", song[0])
		print("Artist: ", song[1])
		print("Key: ", song[2])
		print("Camelot: ", song[3])
		print("BPM: ", song[4])
		print("\n\n")

def printTitleAndArtist(playlist):
	count = 1
	for song in playlist:
		print(count)
		print("Title: ", song[0])
		print("Artist: ", song[1])
		print("\n")
		count+=1


def findMatchesInKeyAndRange(bpm_lb, bpm_ub, camelot_value, playlist):
	matches = []
	camelot_neighbors = getCamelotNeighbors(camelot_value)


	for song in playlist: 
		if((int(song[4]) >= bpm_lb and int(song[4]) <= bpm_ub) and 
			(song[3] == camelot_value or 
				song[3] == camelot_neighbors[1] or 
				song[3] == camelot_neighbors[2] or 
				song[3] == camelot_neighbors[3])):
			matches.append(song)
	return matches

def findMatchesInRange(bpm_lb, bpm_ub, playlist):
	matches = []
	for song in playlist: 
		if((int(song[4]) >= bpm_lb and int(song[4]) <= bpm_ub)):
			matches.append(song)
	return matches

def doubleBPM(playlist):
	new_playlist = playlist
	# print(new_playlist)
	for song in new_playlist: 
		if int(song[4]) >= 75 and int(song[4]) < 100:
			doubletime = int(song[4]) * 2
			print(doubletime)
			song[4] = str(doubletime)
	return new_playlist

def getCamelotNeighbors(camelot_value):

	camelot_neighbors = []
	camelot_neighbors.append(camelot_value)

	cam_num = camelot_value[0:len(camelot_value)-1]
	cam_letter = camelot_value[len(camelot_value)-1]
	print(cam_letter)

	for x in range(0, 3):
		if cam_num == "1":
			cam_up = int(cam_num) + 1
			cam_down = "12"
			if cam_letter == "A":
				cam_letter_switch = "B"
			else:
				cam_letter_switch = "A"
			camelot_neighbors.append(str(cam_up) + cam_letter)
			camelot_neighbors.append(cam_down + cam_letter)
			camelot_neighbors.append(cam_num + cam_letter_switch)
			return camelot_neighbors

		elif cam_num == "12":
			cam_up = "1"
			cam_down = int(cam_num) - 1
			if cam_letter == "A":
				cam_letter_switch = "B"
			else:
				cam_letter_switch = "A"
			camelot_neighbors.append(cam_up + cam_letter)
			camelot_neighbors.append(str(cam_down) + cam_letter)
			camelot_neighbors.append(cam_num + cam_letter_switch)
			return camelot_neighbors
		else:
			cam_up = int(cam_num) + 1
			cam_down = int(cam_num) - 1
			if cam_letter == "A":
				cam_letter_switch = "B"
			else:
				cam_letter_switch = "A"
			camelot_neighbors.append(str(cam_up) + cam_letter)
			camelot_neighbors.append(str(cam_down) + cam_letter)
			camelot_neighbors.append(cam_num + cam_letter_switch)
			return camelot_neighbors


def scrapeData(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')

	playlist_data=[]
	song_table = soup.find('table', class_='table')

	for body in song_table.find_all('tbody'):
		rows = body.find_all('tr')
		for row in rows:
			song_data=[]

			song_data.append(row.find_all('td')[2].text)
			song_data.append(row.find_all('td')[3].text)
			song_data.append(row.find_all('td')[4].text)
			song_data.append(row.find_all('td')[6].text)
			song_data.append(row.find_all('td')[7].text)

			playlist_data.append(song_data)

	return playlist_data


spotify_url="https://open.spotify.com/playlist/35uBGymzei5xVL6GVUknrZ?si=d6d575a0d3524402"

playlist_key=spotify_url[34:56]

url = 'https://songdata.io/spotify-playlist-analysis?id=' + playlist_key

raw_playlist = scrapeData(url)
playlist = doubleBPM(raw_playlist)
mix_suggestions = []

mix_suggestions = findMatchesInKeyAndRange(115, 130, "1A", playlist)
printSongs(mix_suggestions)

