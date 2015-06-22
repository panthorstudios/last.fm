import urllib
import socket
import shutil
from xml.dom import minidom
import os, sys
import re
from datetime import datetime,timedelta
from time import mktime


timeout = 5
socket.setdefaulttimeout(timeout)

def download(url,fname):
  """Copy the contents of a file from a given URL to a local file."""
  retries=5
  i=0
  while i<retries:
    print "Retrieving " + url + "..."
    try:
      urllib.urlretrieve(url,fname)
      i=retries
    except:
      print "Timeout; retrying "+str(retries-i-1)+" more times..."
    i += 1

	
##############################################################
# Get XML from a URL with retries
##############################################################
def getWebContent(wurl):
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

f = open('blastwave.txt', 'r')
templ=f.read()
f.close()


comicbase="http://www.blastwave-comic.com"
 
for i in range(1,2):
  comicurl=comicbase + "/index.php?p=comic&nro=" + str(i)
# <img src="./comics/20060503.jpg"  alt="#3. Orders?" > 
  whtml=getWebContent(comicurl)
#  print whtml
  m=re.search('img src="(.+.jpg)"  alt="([^"]+)"',whtml)
  if m:
    imgraw=m.group(1)
    imgname=imgraw[1:len(imgraw)]
    img=comicbase + imgname
    txt=m.group(2)
  else:
    print 'not matched for #' + str(i)

  chapter=templ
  chapter=chapter.replace('__TITLE__', 'Chapter %d' % i)

  print chapter

  chapter=chapter.replace("__CHAPTER__", txt)
  chapter=chapter.replace("__IMAGE__", imgname)

  fname="blastwave%02d.jpg" % i
  txtfname="Text/chapter%02d.xhtml" % i

#  download(img,fname)
  f=open(txtfname,'w')
  f.write(chapter)
  f.close()


  