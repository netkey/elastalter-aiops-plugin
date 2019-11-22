#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: netkey
@contact: 54netkey@gmail.com
@date: 2019-11-22 17:35
@version: 0.0.0
@license:
@copyright:

"""
import json
import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from requests.exceptions import RequestException
from elastalert.util import EAException


class AIOpsAlerter(Alerter):
    
    required_options = frozenset(['aiops_webhook', 'aiops_appid'])

    def __init__(self, rule):
        super(AIOpsAlerter, self).__init__(rule)
        self.aiops_webhook_url = self.rule['aiops_webhook']
        self.aiops_app_key = self.rule['aiops_appid']
        self.aiops_priority = self.rule.get('aiops_priority', 1)

    def format_body(self, body):
        return body.encode('utf8')
    
    def alert(self, matches):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=utf-8"
        }
        body = self.create_alert_body(matches)
        payload = {
            "app": self.aiops_app_key,
	    "eventType": "trigger",
	    "eventId": "12345",
	    "alarmName": self.create_title(matches),
            "alarmContent": body,
	    "priority": self.aiops_priority
        }
        try:
            response = requests.post(self.aiops_webhook_url, 
                        data=json.dumps(payload, cls=DateTimeEncoder),
                        headers=headers)
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error request to aiops: {0}".format(str(e)))

    def get_info(self):
        return {
            "type": "aiops",
            "aiops_webhook": self.aiops_webhook_url
        }
        pass
