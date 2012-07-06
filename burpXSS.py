#!/usr/bin/python
import gds.pub.burp
import os,sys
from optparse import OptionParser
from pprint import pprint
import subprocess
import signal

sqlmapPath="/pentest/web/fimap-read-only/src/fimap.py"

cookie=""
filename=""
urls={}

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Burp proxy logfile", metavar="burpProxyFile")
parser.add_option("-c", "--cookie", dest="cookie",
                  help="Cookie to use", metavar="cookieString")
parser.add_option("--domain", dest="domain",
                  help="Domain name", metavar="domainName")

(options, args) = parser.parse_args()

if options.filename==None:
	print "[!] Please use -f or --filename and select a burp proxy file"
	sys.exit(0)

try:
   with open(options.filename) as f: pass
except IOError as e:
   print '[!] Problem opening burp proxy logfile: '+str(e)	
   sys.exit(0)
except NameError as e:
   print '[!] Problem opening burp proxy logfile: '+str(e)	
   sys.exit(0)

proxylog = gds.pub.burp.parse(options.filename)
for i in proxylog:
	if(i.get_request_method()=='GET'):
		if options.domain!=None:
			if str(options.domain.lower()) in str(i.host.lower()):
				url = i.host+i.get_request_path()
				if "?" in i.get_request_path():
					if options.cookie==None:
						cookie=i.get_request_header('Cookie')
					else:
						cmd = "/usr/bin/python "+sqlmapPath+" -s -4 -u '"+url+"' --user-agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1' --cookie='"+cookie+"'"
						print cmd
						subprocess.call(cmd,shell=True)

		else:
			if "?" in i.get_request_path():
				if options.cookie==None:
					cookie=i.get_request_header('Cookie')
				else:
					cookie=options.cookie
				url = i.host+i.get_request_path()
				cmd = "/usr/bin/python "+sqlmapPath+" -s -4 -u '"+url+"' --user-agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1' --cookie='"+cookie+"'"
				print cmd
				subprocess.call(cmd,shell=True)		

	if(i.get_request_method()=='POST'):	
		if options.domain!=None:
			if str(options.domain.lower()) in str(i.host.lower()):
				if options.cookie==None:
					cookie=i.get_request_header('Cookie')
				else:
					cookie=options.cookie
				url = i.host+i.get_request_path()
				if(len(i.get_request_body())>0):
					if i.get_request_body() not in urls:
						urls[i.get_request_body()]=cookie
						cmd = "/usr/bin/python "+sqlmapPath+" -s -4 -u \""+url+"\""+" --post=\""+i.get_request_body()+"\" --user-agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1' --cookie=\""+cookie+"\""
						print cmd
						subprocess.call(cmd,shell=True)
		else:
			if options.cookie==None:
				cookie=i.get_request_header('Cookie')
			else:
				cookie=options.cookie
			url = i.host+i.get_request_path()
			if(len(i.get_request_body())>0):
				if i.get_request_body() not in urls:
					urls[i.get_request_body()]=cookie
					cmd = "/usr/bin/python "+sqlmapPath+" -s -4 -u \""+url+"\""+" --post=\""+i.get_request_body()+"\" --user-agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1' --cookie=\""+cookie+"\""
					print cmd
					subprocess.call(cmd,shell=True)


