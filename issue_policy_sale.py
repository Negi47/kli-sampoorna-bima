import enum
import requests
import json
import variables
import logging

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()

def issue_policy_sale(jwt_token, policySaleReference,policy_details,seb_response):
    print("IPS PD", policy_details)
    amount = (len(policy_details)) * 200

    print(amount)
    try:
        url = f"{variables.BRISK_URL}{variables.ISSUE_POLICY_SALE_URL}"
        wso2_token = seb_response.get("wso2_token")
        headers = {
            'token': jwt_token,
            'Ocp-Apim-Subscription-Key': variables.OPM_KEY,
            'Content-Type': 'application/json',
            'Authorization' : f"Bearer {wso2_token}"
        }

        payload = {
            "policySaleReference": policySaleReference,
            "comment": "This is an issue comment",
            "policies": [
            {
                "policyReference": ""
            }
            ],
            "webhook": {
            "webhookUrl": "https://example.com/callMeBack",
            "headers": [
            ]
            }
        }

        payload["policies"] = [allocation.copy() for allocation in payload["policies"] * int(int(amount)/200)]
        for index_val,policy in enumerate(policy_details):
            print(index_val)
            print(policy)
            payload["policies"][index_val]["policyReference"] = policy_details.get(policy)

        print("Payload", payload)
        logger.info(f" [ISSUE POLICY SALE API] Payload : {payload}")
        
        response = requests.post(url, data = json.dumps(payload), headers = headers)
        print("IPS Response", response.text)
        logger.info(f" [ISSUE POLICY SALE API] Response : {response.text}")
        logger.info(f" [ISSUE POLICY SALE API] Response Status Code : {response.status_code}")
        print("Status", response.status_code)

        return response
    except requests.exceptions.Timeout as err:
            logger.info(f" [ISSUE POLICY SALE API] Timeout Occured : {err}")
            return "TIMEOUT"

    except Exception as e:
        logger.info(f" [ISSUE POLICY SALE API] Exception Occured : {e}")
        return "ERROR"