# -*- coding: utf-8 -*-
"""
@author: Adam Eaton

Used to send notifications to the designated Slack channel regarding errors
that occur during runtime.

"""

from slackclient import SlackClient
import traceback
import sys

slack_token = "#"

def send_notification(msg):
    sc = SlackClient(slack_token)
    
    stack = traceback.format_exception_only(sys.last_type, sys.last_value)
    error = str(stack[len(stack)-1])
    message = msg + error
    
    sc.api_call(
            "chat.postMessage",
            channel = "#notifications",
            text = message)
    
    return