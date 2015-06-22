#!/usr/bin/env python

import urllib
import socket
import shutil
from xml.dom import minidom
import os, sys
from PIL import Image
from PIL import ImageDraw,ImageFont
from datetime import datetime,timedelta
from time import mktime

timeout = 5
socket.setdefaulttimeout(timeout)

class Artist:
  """store artist data"""
  def __init__(self, nameIn,urlIn,rankIn,playsIn):
    self.name=nameIn  
    self.url=urlIn
    self.rank=rankIn
    self.imageurl=""
    self.playcount=playsIn

  def addImage(self,imgIn):
    self.imageurl=imgIn

  def getName(self):
    return self.name


  def getRank(self):
    return self.rank
  def getPlayCount(self):
    return self.playcount


  def getUrl(self):
    return self.url
  def getImageUrl(self):
    return self.imageurl


##############################################################
# Get XML from a URL with retries
##############################################################
def getWebXML(wurl):
  retries=5
  i=0
  result=None
  while i<retries:
    print "Calling " + wurl + "..."
    try:
      f = urllib.urlopen(wurl)
      result=f.read()
      i=retries
    except:
      print "Timeout; retrying "+str(retries-i-1)+" more times..."
    i += 1

  return result


lfm_user_name='panthor7'
api_key='3ab0cd14f79b0c4e534f5834bb98a2a5'
weekoffset=0


##############################################################
#Apparently if you don't use Sunday 12:00 GMT then it won't return anything
##############################################################

curdate=datetime.today()
curday=datetime(curdate.year,curdate.month,curdate.day,21,0,0) 
print "weekday=" + str(curday.weekday())

dayspastsunday=curday.weekday()+1
if (dayspastsunday!=7):
  curday=curday-timedelta(days=dayspastsunday)

if weekoffset>0:
  curday=curday-timedelta(days=(weekoffset*7))

etime=int(mktime(curday.timetuple()))
prevsun=curday-timedelta(days=7)
stime=int(mktime(prevsun.timetuple()))

print prevsun.strftime("%d %b %Y %H %M")
print curday.strftime("%d %b %Y %H %M")
for i in range(1,6):
  fname=str(i)+".png"
  if os.path.exists(fname):
    os.unlink("images/temp/" + str(i)+".png")

artistList={}

##############################################################
# First get top artists XML
##############################################################
print "Getting artists..."

chart_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=%s&api_key=%s&from=%s&to=%s' % (lfm_user_name,api_key,str(stime),str(etime))

chart=getWebXML(chart_url)
if chart==None:
  print "Couldn't get chart; exiting..."
  sys.exit(1)


##############################################################
# Parse XML, then get each artist node
##############################################################
xmldoc = minidom.parseString(chart)
artists = xmldoc.getElementsByTagName('artist')
maxplays=0


endDateString=int(xmldoc.documentElement.getElementsByTagName("weeklyartistchart")[0].attributes["to"].value)


endDate=datetime.fromtimestamp(endDateString)

titletxt="Top artists for the week ending " + endDate.strftime("%d %b %Y")


maxrank=5

for artist in artists:
  rank=int(artist.attributes["rank"].value)
  if rank<=maxrank:
    name=artist.getElementsByTagName('name')[0].childNodes[0].data
    if name=="Philip Glass" or name=="Michael Riesman":
      maxrank += 1
    else:
      aurl=artist.getElementsByTagName('url')[0].childNodes[0].data
      plays=int(artist.getElementsByTagName('playcount')[0].childNodes[0].data)
#    name=name.encode("utf-8")
#    aurl=aurl.encode("utf-8")
      if plays>maxplays:
        maxplays=plays
      artst=Artist(name,aurl,rank,plays)
      artistList[rank]=artst

##############################################################
# Get the artist XML so we can find the image
##############################################################
#    fixname=name.replace("\xf8","o")
      print "Getting image url for " + repr(name) + "..."
      encArtist=urllib.quote(name.encode("utf-8"))
      aurl="http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=" + encArtist + "&api_key=3ab0cd14f79b0c4e534f5834bb98a2a5"
      artistInfo=getWebXML(aurl)
      if artistInfo==None:
        print "Couldn't get artist info for "+name+". Exiting..."
        sys.exit(1)

      adoc = minidom.parseString(artistInfo)
      artist = adoc.getElementsByTagName('artist')[0]
##############################################################
# Find the medium size image (width=45)
##############################################################
      for achild in artist.childNodes:
        if achild.nodeName=="image" and achild.attributes["size"].value=="medium":
          if achild.childNodes.length > 0:
            imageurl=achild.childNodes[0].data
            artst.addImage(imageurl)
            fname="images/temp/" + str(rank)+".png"
            urllib.urlretrieve(imageurl,fname)
          else:
            if name=="Essential Resophonics":
              shutil.copyfile("images/essreso.png", "images/" + str(rank)+".png")



html=""

html += "<p><b>" + titletxt + "</b></p>\n"

html += "<p>Commentary goes here.</p>\n"

html += "<ol>" + "\n"

for rank in artistList:
  artist=artistList[rank]
  html += "<li><a target=\"_blank\" href=\"" + artist.getUrl().encode("utf-8") + "\">" +artist.getName().encode("utf-8") +"</a></li>\n"

html+="</ol>"

f = open('results/lastfm.txt', 'w')
f.write(html)
f.close()



imgwidth=540
imgheight=320

afile = "images/lfmlogo.png"
img=Image.new("RGBA",(imgwidth,imgheight),(227,227,227))
draw = ImageDraw.Draw(img)
draw.rectangle(((0,0),(imgwidth,42)),fill=(219,19,2))

tt_font_name='fonts/gillsans.ttf'

textfont = ImageFont.truetype(tt_font_name, 15)
graphfont = ImageFont.truetype(tt_font_name, 24)

draw.text((140,12), titletxt, fill=(255,255,255),font=textfont)

aimg=Image.open(afile)
img.paste(aimg,(20,0))
bheight=45

yoffset=60
maxbarwidth=400
imgspace=10
playcountspace=10
bvspace=5
rtextpadding=4
padding=20
imgspacing=4

xmax=0
for i in range(1,6):
  fname="images/temp/" + str(i)+".png"
  aimg=Image.open(fname)
  sze=aimg.size
  xval=sze[0]
  yval=sze[1]
  newx=int(xval*float(bheight)/yval)
  if newx>xmax:
    xmax=newx

print xmax


for rank in artistList:
  artist=artistList[rank]
  plays=artist.getPlayCount()

#################################
# First paste artist image
#################################
  afile="images/" + str(artist.getRank()) + ".png"
  aimg=Image.open(afile)
  sze=aimg.size
  xval=sze[0]
  yval=sze[1]

  newx=int(xval*float(bheight)/yval)
  aimg=aimg.resize((newx,bheight),Image.ANTIALIAS)

  img.paste(aimg,(padding+(xmax-newx),yoffset))

#################################
# Next draw bar chart
#################################
  maxbarwidth=imgwidth-(2*padding)-xmax-imgspacing
  bwidth=plays/float(maxplays)*maxbarwidth
  barleft=padding+xmax+imgspacing
  draw.rectangle(((barleft,yoffset),(barleft+bwidth,yoffset+bheight)),fill=(160,160,160))

#################################
# Write play count
#################################
  txt=str(plays)
  playsize=draw.textsize(txt,font=graphfont)
  txty=yoffset+(bheight/2)-(playsize[1]/2)
  txtx=barleft + playcountspace
  draw.text((txtx,txty),txt,fill=(0,0,0),font=graphfont)

#################################
# Write artist name
#################################
  txt=artist.getName()
  if len(txt)>35:
     txt=txt[0:35]
  playsize=draw.textsize(txt,font=graphfont)
  txty=yoffset+(bheight/2)-(playsize[1]/2)
  txtx=imgwidth-padding-rtextpadding-playsize[0]
  draw.text((txtx,txty),txt,fill=(0,0,0),font=graphfont)



  yoffset += bheight+bvspace
dtestr=endDate.strftime("%Y%m%d")
img.save("results/lastfm-" + dtestr + ".png")




