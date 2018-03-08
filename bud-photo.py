#!/usr/bin/python

import sys
import time
from picamera import PiCamera
import datetime
import RPi.GPIO as GPIO
import os
import logging

logging.basicConfig(format='%(asctime)s %(message)s',filename='budscanner.log',level=logging.DEBUG)

GPIO.setmode(GPIO.BCM)

####################################################################################
def getdatedirname():
	return(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()))

####################################################################################  
def takephoto(camera,mainshotdir,photonumber):
	#camera.resolution=( 2592, 1944 )
	#camera.start_preview()
	#sleep(3)
	nowdatetime=getdatedirname()
	filename=mainshotdir+"/%03d_%s.jpg" % (photonumber,nowdatetime)
	camera.capture(filename,quality=95)	
	logging.debug("photo taken: "+filename)
	print("photo taken: "+filename)
	os.chmod(filename,0o777)
	#camera.stop_preview()

####################################################################################
def getfreediskspacemegabytes(pathname):
	stat = os.statvfs(pathname)
	return ((stat.f_bfree*stat.f_bsize)/(1024*1024))

####################################################################################
def main():

	for i in range(5,0,-1):	
		print("BudScanner Startup in "+str(i)+" seconds...")
		time.sleep(1)

	freediskspacemegabytes=getfreediskspacemegabytes("/home/pi/budscanner/")
	logging.debug("*****************************************************")
	logging.debug("Free disk space: "+str(freediskspacemegabytes)+" megabytes")

	mindiskspacerequired=250
	if freediskspacemegabytes<=mindiskspacerequired:
		errormsg="ERROR: Not enough free disk space: "+str(mindiskspacerequired)+" Mbyte required! Exiting program!"
		print(errormsg)
		logging.error(errormsg)
		sys.exit()

	mainshotdir="/home/pi/budscanner/shots/"+getdatedirname()
	if not os.path.exists(mainshotdir):
		logging.debug("Creating folder: "+mainshotdir)
		os.makedirs(mainshotdir)
		os.chmod(mainshotdir,0o777)

	camera = PiCamera()
	time.sleep(4)
	camera.resolution=( 2592, 1944 )
	takephoto(camera,mainshotdir,0)

	logging.debug("Program end.")

	for i in range(5,0,-1):	
		print("System shutting down in "+str(i)+" seconds...")
		time.sleep(1)
	logging.debug("Shutting down...")
	os.system("sudo shutdown -h now")	#shutdown
	#os.system("sudo shutdown -r now")	#reboot


####################################################################################
main()

