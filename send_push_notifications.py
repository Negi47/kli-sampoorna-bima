import json
import requests
import datetime
import logging 

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()


def send_push_notifcations(phone_number,event_name):
    create_user_response = create_user(phone_number)
    if (create_user_response!="EXCEPTION") and (create_user_response!="TIMEOUT"):
        try:
            url = "https://api.interakt.ai/v1/public/track/events/"

            payload = json.dumps({
            "userId": "12035448-36a0-3aa24",
            "phoneNumber": phone_number,
            "countryCode": "+91",
            "event": event_name,
            "traits": {
                "Success": "true"
            },
            "createdAt": str(datetime.datetime.now())
            })

            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic QlpGaXpSQUpfMFY4aVVWWThrQWJiUG1fNkdPLXg4Zm5OTWJOT09nclNHSTo=',
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            logger.info(f"**Push Notification API** URL={url} Headers={headers} Payload={payload} ResponseCode={response.status_code} Response={response.text}")

            if response.status_code == 201:
                logger.info(f" [PUSH NOTIFICATION INTERAKT API] Response : {response.text}")
                return response
            else:
                logger.info(f" [PUSH NOTIFICATION INTERAKT API] Error Occured : {response.text}")
                return "ERROR"

        except requests.exceptions.Timeout as err:
            logger.info(f" [PUSH NOTIFICATION INTERAKT API] Timeout Occured : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.info(f" [PUSH NOTIFICATION INTERAKT API] Exception Occured : {e}")
            return "ERROR"
    else:
        return create_user_response

def create_user(phone_number):
    
    url = "https://api.interakt.ai/v1/public/track/users/"
    try:

        payload = json.dumps({
        "userId": phone_number,
        "phoneNumber": phone_number,
        "countryCode": "+91",
        "traits": {},
        "createdAt": str(datetime.datetime.now())
        })

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic QlpGaXpSQUpfMFY4aVVWWThrQWJiUG1fNkdPLXg4Zm5OTWJOT09nclNHSTo='
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info(f"** Create User in Interakt ** URL={url} Headers={headers} Payload={payload} ResponseCode={response.status_code} Response={response.text}")
        if response.status_code == 202:
            logger.info(f" [CREATE USER INTERAKT API] Response : {response.text}")
            return response
        else:
            logger.info(f" [CREATE USER INTERAKT API] Error Occured : {response.text}")
            return "ERROR"
    
    except requests.exceptions.Timeout as err:
        logger.info(f" [CREATE USER INTERAKT API] Timeout Occured : {err}")
        return "TIMEOUT"

    except Exception as e:
        logger.info(f" [CREATE USER INTERAKT API] Exception Occured : {e}")
        return "ERROR"
