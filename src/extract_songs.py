import csv

def get_tracks(sp, tracks):
    """ get all track information to a list """
    song_lists = []
    for item in tracks['items']:
        track = item['track']
        track_info = []
        
        if track['name'] == '' and track['artists'][0]['name'] == '':
            track_info.append("Unknown")
            track_info.append("Unknown")
        else:
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

    
def write_to_csv(file_name, header, content):
    """ write list of track infor to csv file """  
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)
        writer.writerows(content)

