import sys
import os
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from extract_songs import *

if __name__ == '__main__':
    # Get current path
    dirpath = os.getcwd()
    main_dir = os.path.dirname(dirpath)

    # Get credential info
    config = configparser.ConfigParser()
    config.read(main_dir + '/config/config.ini')
    cid = config['DEFAULT']['cid']
    secret = config['DEFAULT']['secret']
    username = config['DEFAULT']['username']

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Define scope for the access to your account
    scope = 'user-library-read playlist-read-private'
    token = util.prompt_for_user_token(username, scope, client_id=cid,client_secret=secret, redirect_uri='http://localhost/')

    # Using token to retrieve data
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        all_songs = []
        for playlist in playlists['items']:
            if playlist['name'] == 'All Songs':
                print('Total tracks: {0}'.format(playlist['tracks']['total']))
                results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                songs_info = get_tracks(sp, tracks)
                for i in range(len(songs_info)):
                    all_songs.append(songs_info[i])

                # get the next 100s tracks
                while tracks['next']:
                    tracks = sp.next(tracks)
                    songs_info = get_tracks(sp, tracks)
                    for i in range(len(songs_info)):
                        all_songs.append(songs_info[i])
        
        # Write song info to csv
        songs_file_name = main_dir + "/generated_data/spotify_songs.csv"
        songs_file_header = ['artist_name', 'song_name', 'popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 
                    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
        write_to_csv(songs_file_name, all_songs, songs_file_header)
        
        # Get genres of artists
        artist_genres = []
        artist_names = []
        with open(main_dir + "/generated_data/spotify_songs.csv") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader, None) #skip the header
            for row in reader:
                artist_names.append(row[0])
        
        # remove duplicate names
        distinct_artist_names = list(set(artist_names))

        print(len(distinct_artist_names))
        # search genres for artist
        for name in distinct_artist_names:
            genres = []
            artists = sp.search(q='artist:' + name, type='artist')
            genres.append(name)
            for i in range(len(artists['artists']['items'])):
                genre = artists['artists']['items'][i]['genres']
                if genre:
                    genres.append(genre)
            
            artist_genres.append(genres)
        # print(artist_genres[0])
        # Write genres to csv
        genres_file_name = main_dir + "/generated_data/genres.csv"
        genres_file_header = ['artist_name', 'genres']
        write_to_csv(genres_file_name, genres_file_header, artist_genres)

        # artists = sp.search(q='artist:' + 'Spencer Kane', type='artist')
        # print(not artists['artists']['items'])
    else:
        print ("Can't get token for", username)