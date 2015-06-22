#!/usr/bin/env python

import shutil
import os, sys
from datetime import datetime,timedelta, date
from time import mktime
import logging

from artist import Artist
from webutils import WebUtils
from imageutils import LastFMImage

LFM_USER_NAME = os.environ['LASTFM_USER_NAME']
API_KEY = os.environ['LASTFM_API_KEY']


def get_top_artists():
    """ Get the top 5 artists from last.fm """

    weekoffset=0

    ##############################################################
    # Apparently if you don't use Sunday 12:00 GMT then 
    # last.fm won't return anything
    ##############################################################

    curdate=datetime.today()
    curday=datetime(curdate.year,curdate.month,curdate.day,21,0,0) 
    logging.info("Today is weekday #" + str(curday.weekday()))

    dayspastsunday=curday.weekday()+1
    if (dayspastsunday!=7):
      curday=curday-timedelta(days=dayspastsunday)

    if weekoffset>0:
      curday=curday-timedelta(days=(weekoffset*7))

    etime=int(mktime(curday.timetuple()))
    prevsun=curday-timedelta(days=7)
    stime=int(mktime(prevsun.timetuple()))

    logging.info("Most recent Sunday in GMT = %s" % curday.strftime("%d %b %Y %H %M"))
    logging.info("Sunday before most recent Sunday in GMT = %s" % prevsun.strftime("%d %b %Y %H %M"))

    for i in range(1,6):
      fname=str(i)+".png"
      if os.path.exists(fname):
        os.unlink("images/temp/" + str(i)+".png")

    ##############################################################
    # First get top artists data
    ##############################################################
    logging.info("Getting top artists from last.fm...")

    chart_type='user.getweeklyartistchart&from=%s&to=%s' % (str(stime),str(etime))
    chart_type='user.gettopartists&period=6month'
    #title_text="Top artists for the week ending " + endDate.strftime("%d %b %Y")
    title_text = 'Top artists (last 6 months)'


    webutils=WebUtils()

    chart_url = 'http://ws.audioscrobbler.com/2.0/?user=%s&api_key=%s&format=json&method=%s' % (LFM_USER_NAME,API_KEY,chart_type)

    chart = webutils.get_web_json(chart_url)

    if chart==None:
        logging.error("Couldn't get chart; exiting...")
        exit(1)

    artists = chart['topartists']['artist']

    #end_date_string=int(xmldoc.documentElement.getElementsByTagName("weeklyartistchart")[0].attributes["to"].value)
    #end_date=datetime.fromtimestamp(end_date_string)

    maxrank=5
    artist_list={}
    for a in artists:
        rank=int(a['@attr']['rank'])
        if rank<=maxrank:
            name=a['name']
            url=a['url']
            plays=int(a['playcount'])

            artist=Artist(name, rank, url, plays)
            artist_list[rank]=artist

            logging.info('Getting image url from last.fm for %s...'  % name)
            enc_artist=webutils.encode(name)
            aurl = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=%s&api_key=%s&format=json' % (enc_artist,API_KEY)

            artist_info_obj=webutils.get_web_json(aurl)

            if artist_info_obj==None:
                logging.error("Couldn't get artist info for "+name+". Exiting...")
                exit(1)

            artist_info = artist_info_obj['artist']

    ##############################################################
    # Find the medium size image (width=45)
    ##############################################################
            a_images = artist_info['image']
            for img in a_images:
                if img['size'] == 'medium':
                    image_url = img['#text']
                    artist.image_url = image_url
                    fname = "images/temp/" + str(rank) + ".png"
                    webutils.save_image(image_url,fname)


    #dte_str=end_date.strftime("%Y%m%d")
    dte_str=date.today().strftime("%Y%m%d")

    logging.info("Creating image...")
    img=LastFMImage(artist_list,title_text)

    logging.info("Saving image...")
    img.save('results/lastfm-%s.png',dte_str)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level = logging.INFO)
    get_top_artists()



