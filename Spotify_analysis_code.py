import pandas as pd
from pandas import testing as tm
import numpy as np
import matplotlib.pyplot as plt
import json
import csv


def date_format(release_dates: str) -> str:
  ''' 
  The function accepts a date of type str.  
  The pandas library's to_datetime method converts the date to a single YYYY-MM-DD format. 
  The date in str type returnes to the user.
  '''
  
  only_date = pd.to_datetime(pd.Series(release_dates)).dt.normalize()
  without_time = only_date.dt.date
  return str(*without_time)


def df_analysis(csv_name: str):
  ''' 
  The function accepts a file name in the str format.
  Next, the corresponding calculations are carried out with the data from the file.
  The results are written to a file format json.
  '''
  df = pd.read_csv(csv_name)
  df_date = df['Release Date']
  #all songs by Ed Sheeran
  songs_by_ES = []
  for e in df['Artist']:
    if 'Ed Sheeran' in e:
      ED_song = str(df.loc[df.Artist == e, 'Song'])
      if ED_song not in songs_by_ES:
        songs_by_ES.append(ED_song)
  with open('analysis_spotify_top_songs.json', 'w') as f:
    json.dump('All songs by Ed Sheeran: ', f)
    f.write('\n')
    json.dump(songs_by_ES, f, indent=2)
    f.write('\n')
    
  #top 3 earliest songs
  with open('analysis_spotify_top_songs.json', 'a') as f:
              json.dump('Top 3 earliest songs: ', f)
              f.write('\n')

  list_for_dates = []
  for e in df_date:
    list_for_dates.append(date_format(e))
  sorted_list_for_dates = sorted(list_for_dates)
  top3_early_dates = [sorted_list_for_dates[0], sorted_list_for_dates[1], sorted_list_for_dates[2]] 

  for e in df_date:
    e_new = date_format(e)
    if e_new in top3_early_dates:
      per_date = df.loc[df['Release Date'] == e]
      song_per_date = per_date['Song']
      song_per_date = song_per_date.to_json()
      with open('analysis_spotify_top_songs.json', 'a') as f:
          json.dump(song_per_date, f, indent=2, separators=('\n', ': '))
          f.write('\n') 
          
  #total number of streams per artist 
  streams_per_artist = df.groupby('Artist')['Streams (Billions)'].sum()
  streams_per_artist = streams_per_artist.to_json(orient = 'index', indent = 3)
  with open('analysis_spotify_top_songs.json', 'a') as f:
          f.write('\n')
          json.dump('Total number of streams per artist: ', f)
          f.write('\n') 
          json.dump(streams_per_artist, f) 


def make_histogram(csv_name: str):
  ''' 
  The function accepts a file name in the str format.
  The necessary data from the file is iterated to build a histogram 
  of the dependence of listening to music on Spotify from the year.
  Upon completion of the function, the histogram is displayed on the user's
  screen and saved in the png file.
  '''
  dict_streams_years = {}

  with open(csv_name) as f:
      reader = csv.reader(f)
      headers = next(reader)
      
      for row in reader:
        date = row[4]
        streams = row[2]    
                        
        if '.' in date:    
          only_year = '20' + date[-2:]
        else:
          only_year = date[-4:]
        
        if ',' in streams:
          streams = float(streams.replace(',', '.'))
          
        
        if only_year not in dict_streams_years:
          dict_streams_years[only_year] = [streams]
        else:
          dict_streams_years[only_year] += [streams]        


  dict_streams_years = sorted(dict_streams_years.items())
  dates = []
  total_streams = []
  sorted_total_streams = []
  for e in dict_streams_years:
    dates.append(e[0])
    total_streams.append(e[1])

  for e in total_streams:
    e = sum(e)
    sorted_total_streams.append(e)

  fig, ax = plt.subplots()
  ax.bar(dates, sorted_total_streams)
  ax.set_facecolor('seashell')
  fig.set_facecolor('floralwhite')
  fig.set_figwidth(12)    
  fig.set_figheight(6)
  fig.suptitle('Streams on Spotify per release year (billions)', fontsize=20)
  plt.xlabel('Years', fontsize=18)
  plt.ylabel('Streams', fontsize=18)
  plt.savefig('Histogram Streams per Years.png')


date_format('29 November 2019')
df_analysis('spotify_songs_top_100.csv')
make_histogram('spotify_songs_top_100.csv')

