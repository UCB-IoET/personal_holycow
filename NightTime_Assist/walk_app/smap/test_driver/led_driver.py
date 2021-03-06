import time
import urllib2
import sys
import msgpack
import socket
from smap.archiver.client import RepublishClient
from smap import driver, util


class ledDriver(driver.SmapDriver):
    
    def setup(self, opts):
        self.rate = float(opts.get('rate', 1))
        self.add_timeseries('/index', 'unit', data_type='double')
	self.add_timeseries('/rgb', 'unit', data_type='double')

#        self.set_metadata('/led_app', {
#                          'Metadata/Description' : 'Application to link PIR to LED',
#                         })

	self.archiverurl = opts.get('archiverurl','http://shell.storm.pm:8079')                                                
        self.subscription_index = opts.get('subscription','Path= "/led_app/1/index"')
	self.subscription_rgb = opts.get('subscription','Path= "/led_app/1/rgb"')
        self.r1 = RepublishClient(self.archiverurl, self.cb_index, restrict=self.subscription_index) 
	self.r2 = RepublishClient(self.archiverurl, self.cb_rgb, restrict=self.subscription_rgb)  
	self.table = {} 

	self.UDP_IP = "2001:470:4956:2:212:6d02::304f" #all IPs
	self.UDP_PORT = 1444 
 
	# Note we are creating an INET6 (IPv6) socket
	self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def cb_index(self, points, led_index ):
        print "Points: ",points
	print "\nData" , led_index

	print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	print self.table
#	index = led_index[0][0][-1] + 0.0
	index = led_index[0][0][-1] + 0.0
	
	curr_time = time.time()
#	self.add('/index',curr_time, index)
	self.add('/index', curr_time, index)
	if (led_index[0][0][-2] not in self.table.keys()):
		self.table[led_index[0][0][-2]] = {}
	self.table[led_index[0][0][-2]][0] = index

    def cb_rgb(self, points, led_rgb ):
        print "Points: ",points
	print "\nData" , led_rgb

	print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
#	index = led_index[0][0][-1] + 0.0
	rgb = led_rgb[0][0][-1] + 0.0
	
	curr_time = time.time()
#	self.add('/index',curr_time, index)
	self.add('/rgb', curr_time, rgb)
	if (led_rgb[0][0][-2] not in self.table.keys()):
		self.table[led_rgb[0][0][-2]] = {}
	self.table[led_rgb[0][0][-2]][1] = rgb

    def send_rgb(self):
	print "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
	print "Sending data to led strip"
	if (len(self.table.keys()) > 0):
		earliest_time = min(self.table, key=self.table.get)
		index = self.table[earliest_time][0]
		rgb = self.table[earliest_time][1]
		del self.table[earliest_time]
		msg = {}
		msg["index"] = index
		msg["rgb"] = rgb
		print msg
		msg_pack = msgpack.packb(msg)
		self.sock.sendto(msg_pack, (self.UDP_IP, self.UDP_PORT))
	

    def start(self):
	self.r1.connect()
	self.r2.connect()
	util.periodicSequentialCall(self.send_rgb).start(1)

    def stop(self):
     print "Quit"
     self.stopping = True














