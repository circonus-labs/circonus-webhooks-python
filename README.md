circonus-webhooks-python
========================

##Generic Circonus Webhook Notification Handlers in Python

While our dev team is investigating the idea of making HipChat and Slack as options for a contact group, we’ve come up with a simple way to push alerts into your HipChat/Slack rooms using our webhook feature in rules. 

The first step is have an HTTP server set up that can accept POST requests from Circonus alerts, use that data, then form an API call to HipChat or Slack. The files in this repo are an example of this, in Python, using the Tornado library. You’ll need to modify the file and enter your auth_token and room_id, plus you can change the port. 

To start the server, you’ll need to install Pip (if necessary), the ‘requests’ Python library, and the ‘tornado’ Python library. Here’s the commands to do that:
```
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py
pip install requests
pip install tornado
python example_tornado_http_server.py
```

###HipChat specifics
You'll need to get a V1 API key from the HipChat Group Admin page, located at https://yourcompany.hipchat.com/admin/api. You’ll also need to know the API ID of the room you want to message, which can be found by clicking on the room in https://yourcompany.hipchat.com/admin/rooms.  This information should be entered into the proper sections near the top of tornado_hipchat_plugin.py.

Once the main Tornado server is running (meaning it’s sitting with a blank line), you can set up a contact group with a new member set to:

http://IPOFTORNADOSERVER:8080/hipchat/?format=json

The Tornado server then captures the alert data, grabs the fields, figures out if it’s a clear event or a new event, and then posts a detailed message to the HipChat room. Here’s an example of the event details, along with the corresponding HipChat message:
```
{u’alerts’: [{u'metric_name': u'rtt', u'check_name': u'Google dns test', u'alert_value': u'9.64', u'alert_id': 
u'8347059', u'agent': u'Ashburn, VA, US', u'check_id': 77831, u'host': u'8.8.4.4', u'alert_time': u'
Tue, 18 Feb 2014 19:19:07', u'alert_url': u'https://circonus.com/account/parlette/fault-detection?alert_id=8347059', 
u'metric_notes': u'Check dashboard, restart server', u'metric_link': u'', u'check_bundle_id': 57620, u'severity':
u'2'}], u’account_name’: u’Parlette Demo’}

Circonus Alert (2:42 PM): SEVERITY 2 – Google dns test – 8.8.4.4 – rtt – Value = 9.64 – 
https://circonus.com/account/parlette/fault-detection?alert_id=8347059
```
The fields used in the message can be easily modified based on what is useful to you.

###Slack specifics

You'll want to visit https://YOURSITE.slack.com/services/new/incoming-webhook to set up a new webhook for the Tornado server to connect to.  Once you set the proper variables in tornado_slack_plugin.py, you can run the Tornado server and set the Circonus contact group to:

http://IPOFTORNADOSERVER:8080/slack/?format=json
