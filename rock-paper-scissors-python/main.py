from os import environ
import logging
import requests
from util import str2hex, hex2str
from challenge import Challenge, Move
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def add_notice(data):
    logger.info(f"Adding notice {data}")
    notice = {"payload": str2hex(data)}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")

def add_report(output = ""):
    logger.info("Adding report: " + output)
    report = {"payload": str2hex(output)}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

def handle_advance(data):
    try:
        logger.info(f"Received advance request data {data}")
        payload = data["payload"]
        # {'metadata': 
        #   {'msg_sender': '0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266', 
        #    'epoch_index': 0, 
        #    'input_index': 0, 
        #    'block_number': 66, 
        #    'timestamp': 1729633582
        #   }, 
        #   'payload': '0x227b5c226d6574686f645c223a205c226372656174655f6368616c6c656e67655c227d22'}
        converted2String = hex2str(payload)

        logger.info(f"converted2String {converted2String}")
        payload = json.loads(converted2String)
        logger.info(f"payload1 {payload}")
        payload = json.loads(payload)
        logger.info(f"payload2{payload}")
    except:
        return "reject"
    
    method = payload.get("method")
    sender = data["metadata"]["msg_sender"]
    logger.info(f"Received advance request payload {payload} method {method} sender {sender}")

    handler = advance_method_handlers.get(method)
    if not handler:
        add_report("Invalid method")
        return "reject"
    
    return handler(payload, sender)

def handle_inspect(data):
    try:
        payload = json.loads(hex2str(data["payload"]))
    except:
        return "reject"
    
    method = payload.get("method")

    logger.info(f"Received inpect request data {datapayload} method {method}")

    handler = inspect_method_handlers.get(method)
    if not handler:
        add_report("Invalid method")
        return "reject"
    
    return handler()

# Advance state
# create challenge
def create_challnge(payload, sender):
    add_report("Create challenge")
    return "accept"
# accept challenge
def accept_challenge(payload, sender):
    add_report("Accept challenge")
    return "accept"
# reveal
def reveal(payload, sender):
    add_report("Reveal challenge")
    return "accept"


# Inpect state
# get challenges
def get_challenges(payload):
    add_report("Get challenges")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

advance_method_handlers = {
    "create_challenge": create_challnge,
    "accept_challenge": accept_challenge,
    "reveal": reveal,
}

inspect_method_handlers = {
    "get_challenges": get_challenges,
}


finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
