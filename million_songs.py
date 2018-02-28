import os, glob
import hdf5_getters
from inspect import getmembers, isfunction
import csv
import sqlite3
import numpy
import sys

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


conn =  sqlite3.connect(r"C:\Victor\python_sql\tracks.db")
cursor = conn.cursor()

methods_artist = [get_artist_familiarity,get_artist_hotttnesss,get_artist_latitude,get_artist_location,get_artist_longitude,get_artist_mbtags,get_artist_mbtags_count,get_artist_name,get_artist_terms]
methods_track = [get_danceability,get_duration,get_end_of_fade_in,get_energy,get_loudness,get_mode,get_mode_confidence,get_song_hotttnesss,get_start_of_fade_out,get_tempo,get_time_signature,get_time_signature_confidence,get_year,get_release]

#returns a list of the methods above, excluding the ones specified in not_desired parameter
def get_desired_mehods(not_desired=['get_analysis_sample_rate','get_key','get_key_confidence','get_audio_md5','open_h5_file_read','get_title','get_analysis_sample_rate', 'get_artist_7digitalid','get_release_7digitalid','get_artist_id','get_artist_mbid','get_sections_confidence', 'get_sections_start', 'get_segments_confidence',
 'get_segments_loudness_max', 'get_segments_loudness_max_time', 'get_segments_loudness_start','get_song_id', 'get_track_7digitalid', 'get_similar_artists','get_track_id','get_num_songs',
 'get_segments_pitches', 'get_segments_start', 'get_segments_timbre','get_beats_start','get_beats_confidence','get_bars_start','get_bars_confidence','get_artist_terms_weight','get_artist_terms_freq','get_artist_playmeid','get_tatums_start','get_tatums_confidence']):
    ## to add get_similar_artists
    desired = []
    for field in getmembers(hdf5_getters):
        if isfunction(field[1]) and field[0] not in not_desired:
            desired.append(field[1])
    return desired

#converts numpy element in python data type
def get_values(element):
    if isinstance(element, numpy.bytes_) or isinstance(element, numpy.unicode_):
        value = element.decode("utf-8")
    elif isinstance(element, numpy.int_):
        value = int(element)
    elif isinstance(element, numpy.float_) or  isinstance(element, numpy.cfloat):
        value = float(element)
    else:
        print (type(element))
    return [value, type(value)]


# creates a table for each list type attribute and populates the fields witin it
def create_and_populate(table_name, list_attr):
    column_name = "nume_" + table_name
    list_type = get_values(list_attr[0])
    if list_type[1] == str:
        column_type = "TEXT"
    elif list_type[1] == int:
        column_type = "INTEGER"
    elif list_type[1] == float:
        column_type = "REAL"
    sql_exp = "CREATE TABLE IF NOT EXISTS {0}({1} {2}, unique({1}));".format(table_name, column_name, column_type)
    print (sql_exp)
    cursor.execute(sql_exp)
    for attr in list_attr:
        value = get_values(attr)[0]
        sql_insert = r"""INSERT OR IGNORE INTO {0}({1}) VALUES ({2});""".format(table_name, column_name, repr(value))
        print (sql_insert)
        cursor.execute(sql_insert)
        conn.commit()



#executes create_and_populate if conditions are met
def tables_from_lists_func(met, list_attr):
    if len(list_attr) > 0:
        met_name = met.__name__
        table_name = met_name.replace("get_","")
        create_and_populate(table_name,list_attr)


def get_all(basedir, ext = ".h5", methods):
    if methods == "atist":
        methods = methods_artist
    elif methods == "tracks":
        methods = methods_track
    else:
        sys.exit("metode necunoscute")

    for method in methods:
        met_name = method.__name__
        print (met_name)
        column_name = met_name.replace("get","")
        #create_table_exp = "CREATE TABLE IF NOT EXISTS {0}({1} {2}, unique({1}));".format(table, column_name, column_type)
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*' + ext))
        for file in files:
            h5 = hdf5_getters.open_h5_file_read(file)
            print(hdf5_getters.get_title(h5))
            for method in desired_mehods:
                attr = method(h5)
                # daca atributul este o lista, se creaza un tabel cu denumirea atributului si valorile din lista
                if (isinstance(attr, numpy.ndarray)):
                    attr_list = list(attr)
                    tables_from_lists_func(method, attr_list)
                else:
                    table_name =
                    value = get_values(attr)
                    sql_ins_exp = "INSERT INTO {} VALUES (?)".format()
                #cursor.execute(sql_ins_exp, (value,))

            h5.close()

    # with open('Cantece.csv', 'w',newline='') as csv_file:
    #     writer = csv.DictWriter(csv_file, fieldnames=header)
    #     writer.writeheader()
    #     for root, dirs, files in os.walk(basedir):
    #         files = glob.glob(os.path.join(root,'*' + ext))
    #         for file in files:
    #             h5 = hdf5_getters.open_h5_file_read(file)
    #             #attributes = []
    #             #print (type(h5))
    #             #print (h5.root)
    #             print(hdf5_getters.get_title(h5))
    #             for method in desired_mehods:
    #                 attr = method(h5)
    #                 print (type(attr))
    #                 print (isinstance(attr,numpy.ndarray))
    #                 #daca atributul este o lista, se creaza un tabel cu denumirea atributului si valorile din lista
    #                 if (isinstance(attr,numpy.ndarray)):
    #                     attr_list = list(attr)
    #                     print (method)
    #                     tables_from_lists_func(method,attr_list)
    #                 attributes[method.__name__] = attr
    #             writer = csv.DictWriter(csv_file, fieldnames = header)
    #             writer.writerow(attributes)
    #             h5.close()
    print (attributes)



print  (get_desired_mehods()[0])
get_all(r'C:\Users\victor.stanescu\Desktop\millionsongsubset_full.tar\MillionSongSubset\data\A\A')