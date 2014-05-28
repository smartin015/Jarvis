#import threading
import urllib2
import sys
import time
import traceback

#TODO: Extend threading.Thread
class KaicongDevice():
    
    def __init__(self, callback, domain, uri_format, packet_size, user="admin", pwd="123456"):
        """ domain:   Camera IP address or web domain 
                      (e.g. 385345.kaicong.info)
        """
        self.callback = callback
        self.running = False
        self.packet_size = packet_size
        self.uri = uri_format % (domain, user, pwd)
    
    def handle(self, data):
        pass
        
    def shutdown(self):
        self.running = False
                
    def run(self):
        self.running = True
        while self.running:
            stream = None
            
            try:
                
                print "Opening url: %s" % self.uri
                stream = urllib2.urlopen(self.uri)
                
                if not stream:
                    print "Could not connect to audio stream! Exiting..."
                    return
                
                while self.running:
                    self.handle(stream.read(self.packet_size))
            
            except:
                print "Stream capture error:", traceback.print_exc()
                print "Retrying in 5 seconds..."
                time.sleep(5.0)
            finally: 
                stream.close()