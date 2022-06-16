import requests
import json
import logging
import variables

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()

def make_policy_sale_payment(policy_details, seb_response,policySaleReference):
    try:

        print(policy_details)
        url = f"{variables.BRISK_URL}{variables.MAKE_SALE_POLICY_URL}"
    
        amount = (len(policy_details)) * 200

        print(amount)
        wso2_token = seb_response.get("wso2_token")
        headers = {
            'token': seb_response.get("jwt_token"),
            'Ocp-Apim-Subscription-Key': variables.OPM_KEY,
            'Content-Type': 'application/json',
            'Authorization' : f"Bearer {wso2_token}"
            }
        
        
        payload ={
            "paymentReference": str(seb_response.get(f"paymentReference{0}")),
            "policySaleReference": policySaleReference, 
            "paymentType": "External",
            "transactionType": "debit",
            "paymentStatus": "success",
            "amount": int(amount),
            "discount": 0,
            "tax": 0,
            "total": int(amount),
            "currencyCode": "INR",
            "allocations": [
                {   
                    "policyReference": "",
                    "amount": 200,
                    "discount": 0,
                    "tax":0,
                    "total": 200
                }

            ]
            }

        payload["allocations"] = [allocation.copy() for allocation in payload["allocations"] * int(int(amount)/200)]
    
        print("MPSP Payload before", json.dumps(payload))
        for index_val,policy in enumerate(policy_details):
            print("Index Val",index_val)
            print("polictyyy", policy)
            payload["allocations"][index_val]["policyReference"] = policy_details.get(policy)
            

        print("MPSP Payload", json.dumps(payload))
        logger.info(f" [MAKE POLICY SALE PAYMENT API] Payload : {payload}")

        response = requests.post(url, data = json.dumps(payload), headers = headers)
        print("MPSP Response",response.text)
        logger.info(f" [MAKE POLICY SALE PAYMENT API] Response : {response.text}")
        logger.info(f" [MAKE POLICY SALE PAYMENT API] Response Status Code : {response.status_code}")
        print("Status", response.status_code)
        return response
    
    except requests.exceptions.Timeout as err:
            logger.info(f" [MAKE POLICY SALE PAYMENT API] Timeout Occured : {err}")
            return "TIMEOUT"

    except Exception as e:
        logger.info(f" [MAKE POLICY SALE PAYMENT API] Exception Occured : {e}")
        return "ERROR"
    
