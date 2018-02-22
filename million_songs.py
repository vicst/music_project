import os, glob
import hdf5_getters
from inspect import getmembers, isfunction

''' Posibble attributtes
['get_analysis_sample_rate', 'get_artist_7digitalid', 'get_artist_familiarity', 'get_artist_hotttnesss',
 'get_artist_id', 'get_artist_latitude', 'get_artist_location', 'get_artist_longitude', 'get_artist_mbid',
 'get_artist_mbtags', 'get_artist_mbtags_count', 'get_artist_name', 'get_artist_playmeid', 'get_artist_terms',
 'get_artist_terms_freq', 'get_artist_terms_weight', 'get_audio_md5', 'get_bars_confidence', 'get_bars_start',
 'get_beats_confidence', 'get_beats_start', 'get_danceability', 'get_duration', 'get_end_of_fade_in', 'get_energy',
 'get_key', 'get_key_confidence', 'get_loudness', 'get_mode', 'get_mode_confidence', 'get_num_songs', 'get_release',
 'get_release_7digitalid', 'get_sections_confidence', 'get_sections_start', 'get_segments_confidence',
 'get_segments_loudness_max', 'get_segments_loudness_max_time', 'get_segments_loudness_start',
 'get_segments_pitches', 'get_segments_start', 'get_segments_timbre', 'get_similar_artists', 'get_song_hotttnesss',
 'get_song_id', 'get_start_of_fade_out', 'get_tatums_confidence', 'get_tatums_start', 'get_tempo',
 'get_time_signature', 'get_time_signature_confidence', 'get_title', 'get_track_7digitalid', 'get_track_id',
 'get_year',open_h5_file_read]'''

#returns a list of the methods above, excluding the ones specified in not_desired parameter
def get_desired_mehods(not_desired=['get_analysis_sample_rate','get_key','get_key_confidence','get_audio_md5','open_h5_file_read','get_title','get_analysis_sample_rate', 'get_artist_7digitalid','get_release_7digitalid','get_artist_id','get_artist_mbid','get_sections_confidence', 'get_sections_start', 'get_segments_confidence',
 'get_segments_loudness_max', 'get_segments_loudness_max_time', 'get_segments_loudness_start','get_song_id', 'get_track_7digitalid', 'get_similar_artists','get_track_id','get_num_songs',
 'get_segments_pitches', 'get_segments_start', 'get_segments_timbre','get_beats_start','get_beats_confidence','get_bars_start','get_bars_confidence','get_artist_terms_weight','get_artist_terms_freq','get_artist_playmeid','get_tatums_start','get_tatums_confidence']):
    ## to add get_similar_artists
    desired = []
    #desired_names = []

    for field in getmembers(hdf5_getters):
        if isfunction(field[1]) and field[0] not in not_desired:
            desired.append(field[1])
            #desired_names.append(field[0])
    return desired




def get_all(basedir, ext = ".h5"):
    desired_mehods = get_desired_mehods()
    songs = {}
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*' + ext))
        for file in files:
            h5 = hdf5_getters.open_h5_file_read(file)
            attributes = []
            #print (type(h5))
            #print (h5.root)
            print(hdf5_getters.get_title(h5))
            for method in desired_mehods:
                attr = method(h5)
                print (method.__name__)
                print(attr)
                print(type(attr))
                attributes.append(attr)
            songs[hdf5_getters.get_title(h5)] = attributes
            h5.close()



print  (get_desired_mehods()[0])
get_all(r'C:\Users\victor.stanescu\Desktop\millionsongsubset_full.tar\MillionSongSubset\data\A\A')