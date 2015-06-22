import urllib
import socket
from xml.dom import minidom
import os, sys
import Image
import ImageDraw,ImageFont
from datetime import datetime,timedelta
from time import mktime


timeout = 5
socket.setdefaulttimeout(timeout)

class Artist:
  "store artist data"
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


userName="panthor7"
#userName="fredwilson"
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
    os.unlink(str(i)+".png")


artistList={}

##############################################################
# First get top artists XML
##############################################################
print "Getting artists..."

charturl="http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&period=7day&user="+userName+"&api_key=3ab0cd14f79b0c4e534f5834bb98a2a5"


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


#endDateString=int(xmldoc.documentElement.getElementsByTagName("weeklyartistchart")[0].attributes["to"].value)
#endDate=datetime.fromtimestamp(endDateString)
endDate=curday

for artist in artists:
  rank=int(artist.attributes["rank"].value)
  if rank<=5:
    name=artist.getElementsByTagName('name')[0].childNodes[0].data
    aurl=artist.getElementsByTagName('url')[0].childNodes[0].data
    plays=int(artist.getElementsByTagName('playcount')[0].childNodes[0].data)

    if plays>maxplays:
      maxplays=plays
    artst=Artist(name,aurl,rank,plays)
    artistList[rank]=artst

##############################################################
# Get the artist XML so we can find the image
##############################################################
    print "Getting image url for " + name + "..."
    encArtist=urllib.quote(name)
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
        imageurl=achild.childNodes[0].data
        artst.addImage(imageurl)
        fname=str(rank)+".png"
        urllib.urlretrieve(imageurl,fname)






html="<ol>"

for rank in artistList:
  artist=artistList[rank]
  html += "<li><a target=\"_blank\" href=\"" + artist.getUrl() + "\">" +artist.getName() +"</a></li>\n"

html+="</ol>"

f = open('lastfm.html', 'w')
f.write(html)
f.close()



imgwidth=540
imgheight=320

afile = "lfmlogo.png"
img=Image.new("RGBA",(imgwidth,imgheight),(227,227,227))
draw = ImageDraw.Draw(img)
draw.rectangle(((0,0),(imgwidth,42)),fill=(219,19,2))


ttfont = ImageFont.truetype("GIL_____.TTF", 15)
graphfont = ImageFont.truetype("GIL_____.TTF", 24)
txt="Patrick Joiner's top artists for the week ending " + endDate.strftime("%d %b %Y")

draw.text((140,12), txt, fill=(255,255,255),font=ttfont)

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
  fname=str(i)+".png"
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
  afile=str(artist.getRank()) + ".png"
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
  playsize=draw.textsize(txt,font=graphfont)
  txty=yoffset+(bheight/2)-(playsize[1]/2)
  txtx=imgwidth-padding-rtextpadding-playsize[0]
  draw.text((txtx,txty),txt,fill=(0,0,0),font=graphfont)



  yoffset += bheight+bvspace

img.save("lastfm.png")




