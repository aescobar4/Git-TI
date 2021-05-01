from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base64 import b64encode

import json

from ti.models import Album, Artist, Track

def index(request):
    response = json.dumps({})
    return HttpResponse(response, content_type='application/json')

# POST y GET de /artists
@csrf_exempt
def artists(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        name = payload['name']
        age = payload['age']
        id = b64encode(str(name).encode()).decode('utf-8')[:22]
        artist = Artist(id=id, name=name, age=age)
        try:
            artist.save()
            response = json.dumps({ 'id': id, 'name': name, 'age': age})
        except:
            response = json.dumps({ 'Error': 'Car could not be added!', 'tipoError': Exception})
    elif request.method == 'GET':
        artists = Artist.objects.all()
        return_list = []
        for artist in artists:
            self_ = 'https://localhost:8000/artists/' + artist.id
            artist_to_add = {
                'id': artist.id,
                'name': artist.name,
                'age': artist.age,
                'albums': self_ + '/albums',
                'tracks': self_ + '/tracks',
                'self': self_,
            }
            return_list.append(artist_to_add)
        response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# GET y DELETE de /artists/{artist_id}
@csrf_exempt
def artistsId(request, artist_id):
    if request.method == 'GET':
        artist = Artist.objects.get(id=artist_id)
        self_ = 'https://localhost:8000/artists/' + artist.id
        response = json.dumps({ 
            'id': artist.id,
            'name': artist.name,
            'age': artist.age,
            'albums': self_ + '/albums',
            'tracks': self_ + '/tracks',
            'self': self_,
        })
    elif request.method == 'DELETE':
        Artist.objects.get(id=artist_id).delete()
        response = json.dumps({'204': 'artista eliminado'})
    return HttpResponse(response, content_type='application/json')

# POST y GET de /artists/{artist_id}/albums
@csrf_exempt
def albumsPerArtist(request, artist_id):
    if request.method == 'POST':
        payload = json.loads(request.body)
        name = payload['name']
        genre = payload['genre']
        id = b64encode(str(name).encode()).decode('utf-8')[:22]
        album = Album(id=id, artist_id=artist_id, name=name, genre=genre)
        try:
            base = 'https://localhost:8000/'
            album.save()
            response = json.dumps({ 
                'id': id, 
                'artist_id': artist_id, 
                'name': name, 
                'genre': genre,
                'artist': base + 'artists/' + artist_id,
                'tracks': base + 'albums/' + id + '/tracks',
                'self': base + 'albums/' + id,
            })
        except:
            response = json.dumps({ 'Error': 'Car could not be added!', 'tipoError': Exception})
    elif request.method == 'GET':
        albums = Album.objects.filter(artist_id=artist_id).all()
        return_list = []
        base = 'https://localhost:8000/'
        for album in albums:
            return_list.append({
                'id': album.id, 
                'artist_id': artist_id, 
                'name': album.name, 
                'genre': album.genre,
                'artist': base + 'artists/' + artist_id,
                'tracks': base + 'albums/' + album.id + '/tracks',
                'self': base + 'albums/' + album.id,
            })
        response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# GET y DELETE de /albums/{album_id}
@csrf_exempt
def albumsId(request, album_id):
    if request.method == 'GET':
        album = Album.objects.get(id=album_id)
        base = 'https://localhost:8000/'
        response = json.dumps({ 
            'id': album_id, 
            'artist_id': album.artist_id, 
            'name': album.name, 
            'genre': album.genre,
            'artist': base + 'artists/' + album.artist_id,
            'tracks': base + 'albums/' + album_id + '/tracks',
            'self': base + 'albums/' + album_id,
        })
    elif request.method == 'DELETE':
        Album.objects.get(id=album_id).delete()
        response = json.dumps({204: 'album eliminado'})
    return HttpResponse(response, content_type='application/json')

# GET de /albums
def albums(request):
    albums = Album.objects.all()
    return_list = []
    for album in albums:
        self_ = 'https://localhost:8000/albums/' + album.id
        album_to_add = {
            'id': album.id,
            'artist_id': album.artist_id,
            'name': album.name,
            'genre': album.genre,
            'artist': 'https://localhost:8000/albums/' + album.artist_id,
            'tracks': self_ + '/tracks',
            'self': self_,
        }
        return_list.append(album_to_add)
    response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# GET y POST de /albums/{album_id}/tracks
@csrf_exempt
def tracksPerAlbum(request, album_id):
    if request.method == 'POST':
        payload = json.loads(request.body)
        name = payload['name']
        duration = payload['duration']
        id = b64encode(str(name).encode()).decode('utf-8')[:22]
        artist = Album.objects.get(id=album_id).artist_id
        track = Track(id=id, name=name, album_id=album_id, duration=duration)
        try:
            base = 'https://localhost:8000/'
            track.save()
            response = json.dumps({
                'id': id,
                'album_id': album_id,
                'duration': duration,
                'name': name,
                'times_played': 0,
                'artist': base + 'artists/' + artist,
                'album': base + 'albums/' + album_id,
                'self': base + 'tracks/' + id,
            })
        except:
            response = json.dumps({ 'Error': 'Car could not be added!', 'tipoError': Exception})
    elif request.method =='GET':
        tracks = Track.objects.filter(album_id=album_id).all()
        artist = Album.objects.get(id=album_id).artist_id
        return_list = []
        base = 'https://localhost:8000/'
        for track in tracks:
            return_list.append({
                'id': track.id,
                'album_id': track.album_id,
                'duration': track.duration,
                'name': track.name,
                'times_played': track.times_played,
                'artist': base + 'artists/' + artist,
                'album': base + 'albums/' + track.album_id,
                'self': base + 'tracks/' + track.id,
            })
        response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# GET y DELETE de /tracks/{track_id}
@csrf_exempt
def tracksId(request, track_id):
    if request.method == 'GET':
        track = Track.objects.get(id=track_id)
        artist = Album.objects.get(id=track.album_id).artist_id
        base = 'https://localhost:8000/'
        response = json.dumps({
            'id': track.id,
            'album_id': track.album_id,
            'duration': track.duration,
            'name': track.name,
            'times_played': track.times_played,
            'artist': base + 'artists/' + artist,
            'album': base + 'albums/' + track.album_id,
            'self': base + 'tracks/' + track.id,
        })
    elif request.method == 'DELETE':
        Track.objects.get(id=track_id).delete()
        response = json.dumps({204: 'cancion eliminada'})
    return HttpResponse(response, content_type='application/json')

# GET de /tracks
@csrf_exempt
def tracks(request):
    tracks = Track.objects.all()
    return_list = []
    base = 'https://localhost:8000/'
    for track in tracks:
        artist = Album.objects.get(id=track.album_id).artist_id
        return_list.append({
            'id': track.id,
            'album_id': track.album_id,
            'duration': track.duration,
            'name': track.name,
            'times_played': track.times_played,
            'artist': base + 'artists/' + artist,
            'album': base + 'albums/' + track.album_id,
            'self': base + 'tracks/' + track.id,
        })
    response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# GET de /artists/{artist_id}/tracks
def artistTracks(request, artist_id):
    albums = Album.objects.filter(artist_id=artist_id).all()
    return_list = []
    for album in albums:
        tracks = Track.objects.filter(album_id=album.id).all()
        artist = Album.objects.get(id=album.id).artist_id
        base = 'https://localhost:8000/'
        for track in tracks:
            return_list.append({
                'id': track.id,
                'album_id': track.album_id,
                'duration': track.duration,
                'name': track.name,
                'times_played': track.times_played,
                'artist': base + 'artists/' + artist,
                'album': base + 'albums/' + track.album_id,
                'self': base + 'tracks/' + track.id,
            })
        response = json.dumps(return_list)
    return HttpResponse(response, content_type='application/json')

# PUT de /artists/{artist_id}/albums/play
@csrf_exempt
def playArtist(request, artist_id):
    if request.method == 'PUT':
        albums = Album.objects.filter(artist_id=artist_id).all()
        for album in albums:
            tracks = Track.objects.filter(album_id=album.id).all()
            for track in tracks:
                print(track.times_played, track.name)
                track.times_played += 1
                print(track.times_played, track.name)
                track.save()
        response = json.dumps({200: 'todas reproducidas'})
    else:
        response = json.dumps({'error': 'metodo no sirve'}
    return HttpResponse(response, content_type='application/json')

# PUT de /albums/{album_id}/tracks/play
@csrf_exempt
def playAlbum(request, album_id):
    return null
