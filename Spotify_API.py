import sys
import os
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import csv

def get_tracks(tracks):
    """ get all track information to a list """
    song_lists = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_info = []
        track_info.append(i)
        track_info.append(track['artists'][0]['name'])
        track_info.append(track['name'])
        track_info.append(track['popularity'])
        track_info.append(track['duration_ms'])
        
        # Add features
        get_feature = sp.audio_features([track['id']])
        feature = get_feature[0]
        track_info.append(feature['danceability'])
        track_info.append(feature['energy'])
        track_info.append(feature['key'])
        track_info.append(feature['loudness'])
        track_info.append(feature['mode'])
        track_info.append(feature['speechiness'])
        track_info.append(feature['acousticness'])
        track_info.append(feature['instrumentalness'])
        track_info.append(feature['liveness'])
        track_info.append(feature['valence'])
        track_info.append(feature['tempo'])
        track_info.append(feature['time_signature'])

        song_lists.append(track_info)
    return song_lists


def write_to_csv(tracks_info):
    """ write list of track infor to csv file """
    with open("spotify_songs.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['id', 'artist_name', 'song_name', 'popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 
                            'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'])
        writer.writerows(tracks_info)
        writer.writerow("\n")
            

if __name__ == '__main__':
    
    # Get credential info
    config = configparser.ConfigParser()
    config.read('local_config.ini')
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
                songs_info = get_tracks(tracks)
                for i in range(len(songs_info)):
                    all_songs.append(songs_info[i])

                # get the next 100s tracks
                while tracks['next']:
                    tracks = sp.next(tracks)
                    songs_info = get_tracks(tracks)
                    for i in range(len(songs_info)):
                        all_songs.append(songs_info[i])
        
        # Write song info to csv
        write_to_csv(all_songs)
                
    else:
        print ("Can't get token for", username)