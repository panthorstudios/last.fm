#!/usr/bin/env python

import os, sys
from PIL import Image
from PIL import ImageDraw, ImageFont
from datetime import datetime, date
from artist import Artist

class LastFMImage(object):

    IMAGE_WIDTH = 540
    IMAGE_HEIGHT  = 320
    BACKGROUND_IMAGE = 'images/lfmlogo.png'
    TT_FONT = 'fonts/gillsans.ttf'
    TITLE_FONT_SIZE = 24
    GRAPH_FONT_SIZE = 24
    Y_OFFSET = 60
    MAX_BAR_WIDTH = 400
    IMAGE_SPACING = 10
    PLAY_COUNT_SPACING = 10
    BV_SPACING = 5
    RTEXT_PADDING = 4
    PADDING = 20
    IMAGE_SPACING2 = 4
    BG_GRAY_COLOR = (227,227,227)
    BG_RED_COLOR = (219,19,2)
    WHITE = (255,255,255)
    BLACK = (0, 0, 0)
    BHEIGHT = 45

    def __init__(self,artists,title_text):
        self.artist_list=artists
        self.title_text = title_text
        self.text_font = ImageFont.truetype(self.TT_FONT, self.TITLE_FONT_SIZE)
        self.graph_font = ImageFont.truetype(self.TT_FONT, self.GRAPH_FONT_SIZE)
        self.img = Image.new("RGBA",(self.IMAGE_WIDTH, self.IMAGE_HEIGHT),self.BG_GRAY_COLOR)
        self.create_image()

    def create_image(self):
# first create template with title
        self.img = Image.new("RGBA",(self.IMAGE_WIDTH, self.IMAGE_HEIGHT),self.BG_GRAY_COLOR)
        draw = ImageDraw.Draw(self.img)
        draw.rectangle(((0,0),(self.IMAGE_WIDTH,42)),fill=self.BG_RED_COLOR)
        draw.text((140,12), self.title_text, fill=self.WHITE,font=self.text_font)
        bimg=Image.open(self.BACKGROUND_IMAGE)
        self.img.paste(bimg,(20,0))

        yoffset=self.Y_OFFSET

# Find max image width 
        xmax=0
        maxplays=0
        for i in range(5):
            fname = 'images/temp/' + str(i+1) + '.png'
            aimg = Image.open(fname)
            sze = aimg.size
            xval = sze[0]
            yval = sze[1]
            newx = int(xval*float(self.BHEIGHT)/yval)
            if newx > xmax:
                xmax = newx
            
        for rank in self.artist_list:
            artist=self.artist_list[rank]
            if artist.play_count > maxplays:
                maxplays = artist.play_count

        for rank in self.artist_list:
            artist=self.artist_list[rank]
            plays=artist.play_count

        #################################
        # First paste artist image
        #################################
            afile="images/temp/%d.png" % artist.rank
            aimg=Image.open(afile)
            sze=aimg.size
            xval=sze[0]
            yval=sze[1]

            newx=int(xval*float(self.BHEIGHT)/yval)
            aimg=aimg.resize((newx,self.BHEIGHT),Image.ANTIALIAS)

            self.img.paste(aimg,(self.PADDING+(xmax-newx),yoffset))

        #################################
        # Next draw bar chart
        #################################
            maxbarwidth = self.IMAGE_WIDTH - (2 * self.PADDING) - xmax - self.IMAGE_SPACING
            bwidth=plays / float(maxplays) * maxbarwidth
            barleft=self.PADDING + xmax + self.IMAGE_SPACING
            draw.rectangle(((barleft,yoffset),(barleft+bwidth,yoffset+self.BHEIGHT)),fill=(160,160,160))

        #################################
        # Write play count
        #################################
            txt=str(plays)
            playsize = draw.textsize(txt,font=self.graph_font)
            txty=yoffset+(self.BHEIGHT/2)-(playsize[1]/2)
            txtx=barleft + self.PLAY_COUNT_SPACING
            draw.text((txtx,txty),txt,fill=self.BLACK,font=self.graph_font)

        #################################
        # Write artist name
        #################################
            txt=artist.name
            if len(txt)>35:
                txt=txt[0:35]
            playsize=draw.textsize(txt,font=self.graph_font)
            txty=yoffset+(self.BHEIGHT/2)-(playsize[1]/2)
            txtx=self.IMAGE_WIDTH - self.PADDING - self.RTEXT_PADDING - playsize[0]
            draw.text((txtx,txty),txt,fill=self.BLACK,font=self.graph_font)

            yoffset += self.BHEIGHT + self.BV_SPACING

    def get_as_html(self):
        html=""
        html += "<p><b>" + title_text + "</b></p>\n"
        html += "<p>Commentary goes here.</p>\n"
        html += "<ol>" + "\n"
        for rank in self.artist_list:
            artist=self.artist_list[rank]
            html += "<li><a target=\"_blank\" href=\"" + artist.url.encode("utf-8") + "\">" +artist.name.encode("utf-8") +"</a></li>\n"

        html+="</ol>"
        f = open('results/lastfm.txt', 'w')
        f.write(html)
        f.close()
        return html

    def save(self,fname,file_date=None):
        if file_date==None:
            file_date = date.today()
        self.img.save(fname % file_date)




