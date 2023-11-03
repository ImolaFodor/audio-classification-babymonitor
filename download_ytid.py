import youtube_dl
import subprocess
import tempfile
import threading
from contextlib import contextmanager
import os
import pandas as pd

df = pd.read_csv("D:/units/deep learning/final_project/audioset/eval_segments.csv")
ytids = []

ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            #'progress_hooks': [my_hook],
        }

origwd = os.getcwd()

for index, row in df.iterrows():
    for val in row:
        if val == "/t/dd00002":
            if row[0]!='wVVBhbrnj9s' and row[0]!='-0p7hKXZ1ww':
                in_fname = os.getcwd() + '/' + row[0] + '.wav'
                ytids.append([row[0], in_fname, row[1], row[2]])

for ytid in ytids: 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        url = 'https://www.youtube.com/watch?v=' + str(ytid[0])
        print(url)
        ydl.download([url] )
        

for ytid in ytids: 
    # with tempfile.TemporaryDirectory(suffix=str(threading.get_ident())) as tmpdir:
    #     os.chdir(tmpdir)    
    start = ytid[2]
    stop = ytid[3]
    if isinstance(start, str): start = float(start)
    if isinstance(stop, str): stop= int(float(stop))

    ffmpeg_args = ['ffmpeg']
    ffmpeg_args += ['-y']
    ffmpeg_args += ['-i', ytid[1] ]
    ffmpeg_args += ['-ss', str(start)]

    if stop:
        ffmpeg_args += ['-t', str(stop - start)]
    
    out_fname = os.getcwd() + '/data/' + ytid[0] + '.wav'
    ffmpeg_args += [ out_fname ]

    process = subprocess.run(ffmpeg_args)
    #os.chdir(origwd)









    
