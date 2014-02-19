'''
Example alert from Circonus:
{u’alerts’: [{u'metric_name': u'rtt', u'check_name': u'Google dns test', u'alert_value': u'9.64', u'alert_id': u'8347059', u'agent': u'Ashburn, VA, US', u'check_id': 77831, u'host': u'8.8.4.4', u'alert_time': u'Tue, 18 Feb 2014 19:19:07', u'alert_url': u'https://circonus.com/account/parlette/fault-detection?alert_id=8347059', u'metric_notes': u'Check dashboard, restart server', u'metric_link': u'', u'check_bundle_id': 57620, u'severity': u'2'}], u’account_name’: u’Parlette Demo’}

Corresponding chat message in HipChat
Circonus Alert (2:42 PM): SEVERITY 2 – Google dns test – 8.8.4.4 – rtt – Value = 9.64 – https://circonus.com/account/parlette/fault-detection?alert_id=8347059
'''

import requests
import json
import tornado.web

#Hipchat settings for the user to change
#HipChat V1 API key from https://yourcompany.hipchat.com/admin/api
auth_token = ""
#HipChat room API ID from https://yourcompany.hipchat.com/admin/rooms
room_id = ""

class HipChatHandler(tornado.web.RequestHandler):
	def post(self):
		#Check to make sure settings are in place
		if not auth_token:
			print "ERROR: auth_token not set in tornado_hipchat_plugin"
		elif not room_id:
			print "ERROR: room_id not set in tornado_hipchat_plugin"
		else:
			data = json.loads(self.request.body)
			print data
			payload = {'room_id':room_id, 'from':'Circonus Alert'}
			url = "https://api.hipchat.com/v1/rooms/message?auth_token="+auth_token+"&format=json"
			#Handle the message if someone clicked 'Send Message' from Circonus UI
			if data['alerts'][0]['metric_name'] == 'dummy_metric_name':
				payload['message'] = data['alerts'][0]['alert_value']
				r = requests.post(url, data=payload)
				r.raise_for_status()
			else:
				#Handle alerts that occur from ruleset thresholds
				for alert in data['alerts']:
					if 'clear_value' in alert:
						message = 'CLEARED - '+
									alert['check_name']+' - '+
									alert['host']+' - '+
									alert['metric_name']+' - '+
									'Clear Value = '+alert['clear_value']+' - '+
									alert['alert_url']
					else:
						message = 'SEVERITY '+alert['severity']+' - '+
									alert['check_name']+' - '+
									alert['host']+' - '+
									alert['metric_name']+' - '+
									'Value = '+alert['alert_value']+' - '+
									alert['alert_url']
					payload['message'] = message
					r = requests.post(url, data=payload)
					r.raise_for_status()

