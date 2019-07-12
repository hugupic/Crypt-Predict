# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Used to send notifications to the designated Slack channel regarding errors
that occur during runtime.

"""

from slack import WebClient
import traceback
import sys

SLACK_TOKEN = open('SLACK_TOKEN.txt', 'r')

def send_notification(msg):
    client = WebClient(token=slack_token)
    
    stack = traceback.format_exception_only(sys.last_type, sys.last_value)
    error = str(stack[len(stack)-1])
    message = msg + error
    
    response = client.chat_postMessage(
        channel='#notifications',
        text=message)
    assert response["ok"]
    assert response["message"]["text"] == message
    
    return

    
