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
			#Handle the message if someone clicked 'Send Message' from Circonus UI
			if data['alerts'][0]['metric_name'] == 'dummy_metric_name':
				url = "https://api.hipchat.com/v1/rooms/message?auth_token="+auth_token+"&format=json"
				payload = {'room_id':room_id, 'from':'Circonus Alert', 'message':data['alerts'][0]['alert_value']}
				r = requests.post(url, data=payload)
				r.raise_for_status()
			else:
				#Handle alerts that occur from ruleset thresholds
				for alert in data['alerts']:
					if 'clear_value' in alert:
						message = 'CLEARED - '+alert['check_name']+' - '+alert['host']+' - '+alert['metric_name']+' - Clear Value = '+alert['clear_value']+' - '+alert['alert_url']
					else:
						message = 'SEVERITY '+alert['severity']+' - '+alert['check_name']+' - '+alert['host']+' - '+alert['metric_name']+' - Value = '+alert['alert_value']+' - '+alert['alert_url']
					url = "https://api.hipchat.com/v1/rooms/message?auth_token="+auth_token+"&format=json"
					payload = {'room_id':room_id, 'from':'Circonus Alert', 'message':message}
					r = requests.post(url, data=payload)
					r.raise_for_status()

