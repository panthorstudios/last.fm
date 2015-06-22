import win32com.client
from datetime import datetime
import time
import csv


fd=open("lastscrobble.txt","rb")
sdatestr=fd.readline()
fd.close()

startdate=datetime.strptime(sdatestr,"%Y-%m-%d %H:%M:%S")
newdate=datetime.now()
newdatestr=newdate.strftime("%Y-%m-%d %H:%M:%S")

iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")


mainLibrary = iTunes.LibraryPlaylist
tracks = mainLibrary.Tracks
numTracks = tracks.Count
print "number of tracks: " + str(numTracks)

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
      playdiff=playdate-startdate
      diffdays=playdiff.days + (playdiff.seconds / 86400.0)
      if diffdays>0:
        playdateutc=int(time.mktime(playdate.timetuple()))
        tstr=str(id) + "\t" + artist + "\t" + name + "\t"  + str(playdate)  + "\t" + str(playdateutc) + "\t" + str(songlen) + "\r\n"
        fd.write(tstr.encode("utf-8"))
    except Exception as inst:
      print "Failed: " + str(inst)

fd.close()

fd=open("lastscrobble.txt","wb")
fd.write(newdatestr)
fd.close()


