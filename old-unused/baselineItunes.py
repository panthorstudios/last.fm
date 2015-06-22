import win32com.client
from datetime import datetime
import time


iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")


mainLibrary = iTunes.LibraryPlaylist
tracks = mainLibrary.Tracks
numTracks = tracks.Count
print "number of tracks: " + str(numTracks)


fd=open("iTunesBaseline.txt","wb")

cnt=0
for track in tracks:
  track_converted =  win32com.client.CastTo(track, "IITFileOrCDTrack")
  ttype=track_converted.Kind
  tVideoKind=track_converted.VideoKind
  if ttype==1 and tVideoKind==0:  # i.e. type=file and videokind=0 (not a video)
    try:
      id=track_converted.TrackDatabaseID
      playCount=track_converted.PlayedCount
      tstr=str(id) + "\t" + str(playCount) + "\r\n"
      fd.write(tstr.encode("utf-8"))
    except Exception as inst:
      print "Failed: " + str(inst)

fd.close()

