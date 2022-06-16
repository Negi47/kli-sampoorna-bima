import requests
import json
from login import login_api
import logging
import variables

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()

def submit_external_payment(user_details):
    logger.info(f"USER DETAILS -> {user_details}")
    print("############ User detailssss", user_details)
    amount = (len(user_details)-2) * 200
    print("Amount", amount)

    url = f"{variables.BRISK_URL}{variables.SUBMIT_EXTERNAL_PAYMENT_URL}"
    login_api_response = login_api()
    jwt_token = login_api_response.get("jwt_token")
    wso2_token = login_api_response.get("wso2_token")
    if jwt_token != "TIMEOUT" and jwt_token != "EXCEPTION":
        headers = {
        'token': jwt_token,
        'Ocp-Apim-Subscription-Key': variables.OPM_KEY,
        'Content-Type': 'application/json',
        'Authorization' : f"Bearer {wso2_token}"
        }
        payload = {
            "configurationKey": variables.SEP_CONFIG_KEY, 
            "external": {
                "providerReference": user_details.get("txn_id")
            },
            "payment": {
                "currency": " INR",
                "amount": str(amount)
            }   
        }
        logger.info(f" [SUBMIT EXTERNAL PAYMENT API] Payload : {payload}")

        try:
            seb_response = {"jwt_token" : jwt_token}
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            logger.info(f" [SUBMIT EXTERNAL PAYMENT API] Response : {response.text}")
            logger.info(f" [SUBMIT EXTERNAL PAYMENT API] Response Status Code : {response.status_code}")
            seb_response["paymentReference0"] =  response.json().get("paymentReference")
            seb_response["wso2_token"] = wso2_token
            return seb_response
            
        except requests.exceptions.Timeout as err:
            logger.info(f" [SUBMIT EXTERNAL PAYMENT API] Timeout Occured : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.info(f" [SUBMIT EXTERNAL PAYMENT API] Exception Occured : {e}")
            return "ERROR"
    else:
        return jwt_token