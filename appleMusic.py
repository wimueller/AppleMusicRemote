import appscript as aps
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='public/')
sio = SocketIO(app)

am = aps.app('Music')

lib = am.library_playlists['Library']
trackList = lib.tracks
playlists = am.playlists()
	
@sio.on('connect')
def connect():
	emit('server-status', 'Connected to Apple Music.')
	saveArtowrk()
	updateUI()

def updateUI():
	"""Emit UI changes to frontend"""
	
	songName = nowPlaying()
	songName = songName['artist'] + ' - ' + songName['title']
	
	status = am.player_state()
	if str(status).split('.')[1] == 'playing':
		pStatus = 1
	else:
		pStatus = 0
	
	sio.emit('current-track', songName)
	sio.emit('player-status', pStatus)
	sio.emit('shuffle-status', am.shuffle_enabled())
	sio.emit('mute-status', am.mute())

@app.route('/', methods=['GET'])
def root():
	return render_template('index.html', title='Apple Music')

@app.route('/api/search', methods=['GET'])
def searchTrack():
	"""Search track by string."""
	song = request.args.get('songname')

	try:
		trackList[aps.its.name.contains(song)].get()[0].play()
	except Exception as e:
		try:
			trackList[aps.its.artist.contains(song)].get()[0].play()
		except:
			return ('No song found',200)
	
	saveArtowrk()
	updateUI()

	return ('',200)

@app.route('/api/toggleshuffle', methods=['GET'])
def shuffleToggle():
	"""Toggle Shuffle."""
	isShuffle = am.shuffle_enabled()
	if isShuffle:
		am.shuffle_enabled.set(0)
	else:
		am.shuffle_enabled.set(1)
	updateUI()
	return('',200)

@app.route('/api/prev', methods=['GET'])
def prev():
	"""Soft previous track. Rewinds to current track's beginning.
		 Clicking it again immediately will play previous track."""
	am.back_track()
	updateUI()
	saveArtowrk()
	return ('',200)

@app.route('/api/playpause', methods=['GET'])
def playPause():
	"""Toggle Play/Pause player state."""
	am.playpause()
	updateUI()
	return ('',200)

@app.route('/api/next', methods=['GET'])	
def next():
	"""Plays next track."""
	am.next_track()
	updateUI()
	saveArtowrk()
	return ('',200)

@app.route('/api/mute', methods=['GET'])
def mute():
	"""Toggle Mute/Unmute."""
	isMute = am.mute()
	if isMute:
		am.mute.set(0)
	else:
		am.mute.set(1)
	updateUI()
	return ('',200)	

@app.route('/api/setvolume', methods=['PUT'])
def setVolume():
	"""Set application's volume."""
	value = int(request.args.get('value'))
	am.sound_volume.set(value)
	return ('',200)

@app.route('/api/stop', methods=['GET'])
def stop():
	"""Stop playback."""
	am.stop()
	return ('',200)

@app.route('/api/playlists', methods=['GET'])
def getPlaylists():
	"""Return list of avaliable playlists."""
	playlistNames = [_.name() for _ in playlists]

	return jsonify( { 'plists': playlistNames})

@app.route('/api/playplaylist', methods=['GET'])
def playPlaylist():
	"""Play specified playlist"""
	playlistName = request.args.get('playlistName')
	try:
		am.playlists[aps.its.name.contains(playlistName)].get()[0].play()
	except:
		return "No such playlist"
	
	saveArtowrk()
	
	updateUI()
	return ('',200)

def nowPlaying():
	"""Current track information"""
	track = am.current_track()
	title = track.name()
	artist = track.artist()
	album = track.album()

	return {'title':title, 'artist':artist, 'album':album}

def prev2():
	"""Force play previous track."""
	am.previous_track()
	updateUI()
	saveArtowrk()
	return ('',200)

def saveArtowrk():
	"""Write raw data to an image file"""
	try:
		imageData = am.current_track.artworks()[0].raw_data()
	except:
		return -1
	with open('./public/img/now_playing.png', 'wb') as file:
		file.write(imageData)
	sio.emit('update-art', '')

if __name__ == '__main__':
	print("")
	app.run(debug = False, host = '0.0.0.0', port=3000)
