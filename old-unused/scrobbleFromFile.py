import win32com.client
from datetime import datetime
import time
import scrobbler
import csv


scrobbler.login('panthor7','gambit')

fd=open("toscrobble.txt","rb")
freader = csv.reader(fd, delimiter='\t')
for row in freader:
  id=row[0]
  artist=row[1]
  track=row[2]
  playdate=row[3]
  playdateutc=int(row[4])
  songlen=int(row[5])
  print "Scrobbling " + artist + " - " + track + ", play date=" + str(playdate)
  try:
    scrobbler.submit(artist,track,playdateutc,length=songlen)
  except Exception as inst:
    print "Failed: " + str(inst)

fd.close()

scrobbler.flush()