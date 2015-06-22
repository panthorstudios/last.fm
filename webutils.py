import urllib
import socket
import json
import logging

class WebUtils(object):
    """ Class to encapsulate web retrieval functions """ 
    RETRIES = 5
    DEFAULT_TIMEOUT = 5

    def __init__(self):
        self.retries=self.RETRIES
        socket.setdefaulttimeout(self.DEFAULT_TIMEOUT)

    def get_web_json(self, wurl):
        i=0
        result=None
        while i < self.retries:
            logging.debug("Getting data from last.fm: %s" % wurl)
            try:
                f = urllib.urlopen(wurl)
                result_text = f.read()
                i = self.retries
                try:
                    result = json.loads(result_text)
                except:
                    logging.error("Error loading result: %s" % result_text)
            except:
                logging.error("Error; retrying %d more times..." % (self.retries - i - 1))
            i += 1
        return result

    def get_web_xml(self, wurl):
        i=0
        result=None
        while i < self.retries:
          logging.info("Calling %s..." % wurl)
          try:
              f = urllib.urlopen(wurl)
              result=f.read()
              i = self.retries
          except:
              logging.error("Error with connection; retrying %d more times..." % (self.retries - i - 1))
          i += 1

        return result

    def encode(self,name):
        return urllib.quote(name.encode("utf-8"))

    def save_image(self,image_url,fname):
        urllib.urlretrieve(image_url,fname)

