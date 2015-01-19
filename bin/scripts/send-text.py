#!/usr/bin/python
# Splunk Perimeter Security - Twilio-Powered Alert Script
#
# This script sends a text message alert when certain events are triggered
# within the Splunk Perimeter Security app. Since the script has a dependecy
# on the Twilio Python packages, we call this script via a wrapper shell
# script to avoid Splunk using its internal python binary.

# =Variable Definitions=
Twilio_From = "<your Twilio phone number>"
Twilio_SID = "<your Twilio SID>"
Twilio_Auth = "<your Twilio Auth key - keep this secret!>"
# /=Variable Definitions=

import sys
import csv
import gzip
import datetime
from twilio.rest import TwilioRestClient 

SplunkAlert = sys.argv[1]
SplunkResults = sys.argv[2]
client = TwilioRestClient(Twilio_SID, Twilio_Auth) 

with gzip.open(SplunkResults) as ResultsFile:
	reader = csv.DictReader(ResultsFile)
	for row in reader:
		if not "alert_phone" in row:
			print "ERROR: Missing alert_phone field"

		# The alert text can be overriden by the alert_text field
		if "alert_text" in row:
			SplunkAlert = row["alert_text"]

		alertOutput = {
			'app': 'Splunk Perimeter Security',
			'body': SplunkAlert,
			'dest': 'Splunk Perimeter Secuitry',
			'dest_category': 'Splunk Alerts',
			'severity': 'critical',
			'src': row["zone_name"],
			'src_category': 'Alarm Zone',
			'subject': 'Zone Access Violation',
			'type': 'alarm'
		}
	
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		for k, v in alertOutput.iteritems():
			print "%s=\"%s\"" % (k,v),
		print ""


		# Generate a text message alert per line in the file, per alert phone
		for alert_phone in row["alert_phone"].split(","):
			
			alertOutput = {
				'app': 'Splunk Perimeter Security',
				'body': SplunkAlert,
				'dest': alert_phone,
				'dest_category': 'Text Message',
				'severity': 'critical',
				'src': row["zone_name"],
				'src_category': 'Alarm Zone',
				'subject': 'Zone Access Violation - Text Message Alert',
				'type': 'alarm'
			}
		
			print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			for k, v in alertOutput.iteritems():
				print "%s=\"%s\"" % (k,v),
			print ""

			client.messages.create(
				to=alert_phone,
				from_=Twilio_From,
				body="%s: %s" % ( row["zone_name"], SplunkAlert ), 
			)
