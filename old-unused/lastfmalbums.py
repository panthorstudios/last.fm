import csv
import urllib
import socket
import shutil
from xml.dom import minidom
import os, sys
import Image
import ImageDraw,ImageFont
from datetime import datetime,timedelta
from time import mktime


##############################################################
# Get XML from a URL with retries
##############################################################
def getWebXML(wurl):
  retries=5
  i=0
  result=None
  while i<retries:
 #   print "Calling " + wurl + "..."
    try:
      f = urllib.urlopen(wurl)
      result=f.read()
      i=retries
    except:
      print "Timeout; retrying "+str(retries-i-1)+" more times..."
    i += 1

  return result
  

timeout = 5
socket.setdefaulttimeout(timeout)

spamReader = csv.reader(open('zunealbums.txt', 'rb'), delimiter='\t', quotechar='\"')
for row in spamReader:
  artistName=row[0]
  albumName=row[1]

  albumEnc=urllib.quote_plus(albumName)
  charturl="http://ws.audioscrobbler.com/2.0/?method=album.search&album="+albumEnc+"&api_key=3ab0cd14f79b0c4e534f5834bb98a2a5"

  chart=getWebXML(charturl)


  if chart==None:
    print "Couldn't get chart; exiting..."
    sys.exit(1)


##############################################################
# Parse XML, then get each artist node
##############################################################
  xmldoc = minidom.parseString(chart)
  artists = xmldoc.getElementsByTagName('artist')
  maxplays=0


  isFound=False
  for album in xmldoc.documentElement.getElementsByTagName("album"):
    albumNameFound= album.getElementsByTagName("name")[0].firstChild.nodeValue 
    artistNameFound= album.getElementsByTagName("artist")[0].firstChild.nodeValue 
    idFound= album.getElementsByTagName("id")[0].firstChild.nodeValue 
    urlFound= album.getElementsByTagName("url")[0].firstChild.nodeValue 
    if albumNameFound==albumName and artistNameFound==artistName:
      for coverImg in album.getElementsByTagName("image"):
        if coverImg.attributes["size"].value=="large":
	      if coverImg.firstChild != None:
	        cImg=coverImg.firstChild.nodeValue

      print albumNameFound + "\t" + artistNameFound  + "\t" + idFound+"\t"+cImg
      isFound=True
	  
  if not isFound:
    print albumName + "\t" + artistName +"\t\t"
	  