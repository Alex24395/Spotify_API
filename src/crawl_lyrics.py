import os
import configparser
import csv
import requests
import lyricwikia
    
if __name__ == '__main__':
    # Get current path
    dirpath = os.getcwd()
    main_dir = os.path.dirname(dirpath)
    
    songs_artists = []
    
    data = main_dir + "/generated_data/spotify_songs.csv"
    
    with open(data) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)
        for row in reader:
            songs_artists.append(row[:2])
    
    with open(main_dir + "/generated_data/lyrics.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['artist_name', 'song_name', 'lyrics'])
        for item in songs_artists:
            artist_name = item[0]
            song_name = item[1]
            try:
                lyric = lyricwikia.get_lyrics(artist_name, song_name)
                writer.writerow([artist_name, song_name, lyric])
            except Exception:
                pass

