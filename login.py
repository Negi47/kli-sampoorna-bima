import json
import requests
import logging
import variables
from http.client import HTTPSConnection
from base64 import b64encode
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def login_api():

    wso2_token_response = wso2_token_generation_api()
    if (wso2_token_response != "ERROR") and (wso2_token_response != "TIMEOUT"):
        wso2_token =  wso2_token_response.json().get("access_token")

        url = f"{variables.BRISK_URL}{variables.LOGIN_API_URL}"
        payload = json.dumps({
            "environment": "dev",
            "eMail": variables.LOGIN_EMAIL,
            "password": variables.LOGIN_PASSWORD
        })
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': variables.OPM_KEY,
            'Authorization' : f"Bearer {wso2_token}"
        }

        try:
            response = requests.post(url = url, headers=headers, data = payload, timeout=17)
            logger.info(f" [LOGIN API] Response : {response.text}")
            logger.info(f" [LOGIN API] Response : {response.status_code}")
            jwt_token = response.json().get("jwtToken") 
            login_response = {
                "jwt_token" : jwt_token,
                "wso2_token" : wso2_token
            }
            return login_response
            
        except requests.exceptions.Timeout as err:
            logger.info(f" [LOGIN API] Timeout Occured : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.info(f" [LOGIN API] Exception Occured : {e}")
            return "ERROR"
    else:
        return wso2_token_response

def wso2_token_generation_api():
        url = variables.WSO2_TOKEN_API

        payload='grant_type=client_credentials'

        userAndPass = b64encode(b"3KRs7inl37kd3PlRJ2MfxLPZrHAa:xeyItfqciMGIWkNftOIvHzimXa4a").decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass }
        
        # userAndPass = "UG90VF9JdkduTXNSX19TdmVXN1FBNko3eW1JYTpqWmRLRG90ZlhiVzRMVlpSS1dpQ2JfYVF0ZThh"
        headers = { 
        'Authorization': f'Basic {userAndPass}',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout = 4)
            logger.info(f" [WSO2 TOKEN GENERATION API] Response : {response.text}")
            logger.info(f" [WSO2 TOKEN GENERATION API] Response : {response.status_code}")
            return response

        except requests.exceptions.Timeout as err:
            logger.info(f" [WSO2 TOKEN GENERATION API] Timeout Occured : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.info(f" [WSO2 TOKEN GENERATION API] Exception Occured : {e}")
            return "ERROR"

