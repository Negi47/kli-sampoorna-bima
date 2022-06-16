import requests
import logging

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()

esb_id = "IJ5zgGcMRa98dVFOvXie/4ncQyFAY1a0YrOVi0cmf+/0v4Dgnzxms2COh2mDm5Z5"
key = "123"

def whatsapp_consent_api(phone_number):
        try:
            print("WC", phone_number)

            url = f"https://klibusuat.mykotaklife.com/HTTPServices/WhatsAppMobileConsent/BTSHTTPReceive.dll?msg={phone_number}"
            print("WA Consent URL",url)
            payload = {}
            
            headers = {
            'Esb_ID': esb_id,
            'key': key,
            'Content-Type': 'application/json'
            }
            # return True

            logger.info(f"[WA CONSENT API] Payload : {payload}")
            response = requests.get(url, data = payload, headers = headers)
            logger.info(f"[WA CONSENT API] Response : {response.text}")
            
            if response.json().get("IsSuccess") == "true":
                return response
            logger.error(f"[WA CONSENT API] Error Occured : {response.text}")
            return "EXCEPTION"

        except requests.exceptions.Timeout as err:
            logger.error(f"[WA CONSENT API] Timeout : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.error(f"[WA CONSENT API] Exception Occured : {e}")
            return "EXCEPTION"