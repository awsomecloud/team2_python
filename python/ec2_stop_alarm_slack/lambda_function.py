#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function
import boto3
import json
import logging
import time
import re
import instance_state, instance_auto
from base64 import b64decode
from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlencode

#KMS로 암호화된 url
ENCRYPTED_HOOK_URL = "kms 사용시 사용"
#복호화
HOOK_URL = ""
#"https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext']
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    
    
    #종료 function = stopped 시작 function = running
    if event['type'] == "stopped" :
        instance_auto.instances_stop()
    else:
        instance_auto.instances_start()
    
    #상태 변경까지 대기
    time.sleep(30)
    result_text = instance_state.print_info(event['type'])
    

    slack_message = {
        "username": "BIMO",
        "icon_url" : "https://ca.slack-edge.com/T0ADM364S-UHC8WDMLP-5c50791074b2-48",
        "text" : "\n" + result_text,
        "channel": "#test01"
    }
    #json.dumps(slack_message)
    #req = Request(HOOK_URL, data=urlencode(slack_message))
    req = Request(HOOK_URL, json.dumps(slack_message).encode(encoding='UTF8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)