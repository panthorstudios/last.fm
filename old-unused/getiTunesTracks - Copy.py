import win32com.client
from datetime import datetime
import time
import csv

playCounts={}
fd=open("iTunesBaseline.txt","rb")
freader = csv.reader(fd, delimiter='\t')
for row in freader:
  id=row[0]
  plays=row[5]
  playCounts[id]=plays

iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")


mainLibrary = iTunes.LibraryPlaylist
tracks = mainLibrary.Tracks
numTracks = tracks.Count
print "number of tracks: " + str(numTracks)

startdate=datetime(2010,12,7,23,40,00)

fd=open("toscrobble.txt","wb")

cnt=0
for track in tracks:
  track_converted =  win32com.client.CastTo(track, "IITFileOrCDTrack")
  ttype=track_converted.Kind
  if ttype==1:  # i.e. file
    try:
      id=track_converted.TrackDatabaseID
      songlen=track_converted.Duration
      artist=track_converted.Artist
      name=track_converted.Name
      album=track_converted.Album
      albumArtist=track_converted.AlbumArtist
      playCount=track_converted.PlayedCount
      pd=track_converted.PlayedDate
      playdate=datetime(pd.year,pd.month,pd.day,pd.hour,pd.minute,pd.second)
      oldCount=-1
      if playCounts.has_key(str(id)):
        oldCount=playCounts[id]
      print id + ":" + str(oldCount) + ":" + str(playCount-oldCount)
      if oldCount!=-1:
        if playCount>oldCount:
          playdateutc=int(time.mktime(playdate.timetuple()))
          tstr=str(id) + "\t" + artist + "\t" + albumArtist + "\t" + album + "\t" + name + "\t"  + str(playCount) + "\t" + str(playdate)  + "\t" + str(playdays) + "\r\n"
          fd.write(tstr.encode("utf-8"))
    except Exception as inst:
      print "Failed: " + str(inst)

fd.close()

