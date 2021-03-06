import requests
import json
import tornado.web

#Hipchat settings for the user to change
#HipChat V1 API key from https://yourcompany.hipchat.com/admin/api
auth_token = ""
#HipChat room API ID from https://yourcompany.hipchat.com/admin/rooms
room_id = ""

#Circonus API Information
circonus_api_name = ""
circonus_api_key = ""

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
					#If Circonus API details were provided, get the check information from the alert
					check_bundle = None
					if circonus_api_name and circonus_api_key:
						check_bundle = requests.get(
							"https://api.circonus.com/check_bundle?f__checks_has=/check/"+str(alert['check_id']),
							auth=(circonus_api_name,circonus_api_key),
							headers={"Accept": "application/json"}
						).json()
					if 'clear_value' in alert:
						message = 'CLEARED - '+alert['check_name']+' - '+alert['host']+' - '+alert['metric_name']+' - '+'Clear Value = '+alert['clear_value']+' - '+alert['alert_url']
					else:
						message = 'SEVERITY '+alert['severity']+' - '+alert['check_name']+' - '+alert['host']+' - '+alert['metric_name']+' - '+'Value = '+alert['alert_value']+' - '+alert['alert_url']
					#Append tag information to message if we looked up the check_bundle
					if check_bundle:
						if check_bundle[0]['tags']:
							message += ' - TAGS = '
							for tag in check_bundle[0]['tags']:
								message += tag+', '
							#Remove trailing comma
							if message[-2:] == ', ':
								message = message[:-2]
					payload['message'] = message
					r = requests.post(url, data=payload)
					r.raise_for_status()

