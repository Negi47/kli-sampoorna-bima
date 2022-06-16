import  json
import requests
import logging
import datetime
import base64
import uuid

logger = logging.getLogger()
logger.setLevel("INFO")

def main(event, context):
    """
   event['body'] is a string dict with the following keys:
   node, event, user, entities.
   Currently, we pass user_id, user_name, full_name, device_platform and language_code in the user dictionary.
   Args:
       event (dict): Data corresponding to this event
       context
   Returns
       (dict): response with statusCode and the response for the User
   """
    body = json.loads(event['body'])
    obj = ImageUpload(body = body)
    
    
    final_response = obj.get_final_response()
    logger.info(f" [FINAL RESPONSE] {final_response}")
    response = {'statusCode': 200, 'body': json.dumps(final_response), 'headers': {'Content-Type': 'application/json'}}
    return response

class ImageUpload:
    def __init__(self, body : dict):
        self.body = body
        self.entities = self.body.get("entities", {})
        logger.info(f"ENTITIES {self.entities}")
        self.user = self.body.get("user",{})
        self.conversation_details = self.body.get("conversation_details",{})
        self.env_variables = body.get("env_variables")
        self.user_details = self.body.get("user_details", {})

        self.brisk_url = self.env_variables.get("BRISK_API")
        self.image_upload_url = self.env_variables.get("UPLOAD_IMAGE")
        self.create_sale_policy_url = self.env_variables.get("CREATE_SALE_POLICY")

        logger.info(f" [CONVERSATION DETAILS] {self.conversation_details}")
        self.final_response = {}
    
    def create_sale_policy_api(self):
  
        try:
            policy_holder_name = self.conversation_details.get("name")
            policy_holder_name_split = policy_holder_name.split(" ",1)
            policy_holder_fname = policy_holder_name_split[0]
            policy_holder_lname = policy_holder_name_split[1]
            
            if "n_name" in self.conversation_details:
                # if len(self.conversation_details.get("n_name")) != 0:
                nominee_name = self.conversation_details.get("n_name")
            else:
                nominee_name = self.entities.get("nominee_name_kli")[0].get("entity_value").get("value")

            # nominee_name = self.conversation_details.get("n_name")
            nominee_name_split = nominee_name.split(" ",1)
            nominee_name_fname = nominee_name_split[0]
            nominee_name_lname = nominee_name_split[1]

            email = self.entities.get("kli_email")[0].get("entity_value").get("value")
            marital_status = self.entities.get("marital_status_kli")[0].get("entity_value")
            # marital_status = "married"
            
            # dd = self.entities.get("ph_date_of_birth", {})[0].get("entity_value").get("dd")
            # mm = self.entities.get("ph_date_of_birth", {})[0].get("entity_value").get("mm")
            # yy = self.entities.get("ph_date_of_birth", {})[0].get("entity_value").get("yy")
            # dob_str = f"{dd}/{mm}/{yy}"
            dob_str = self.conversation_details.get("dob")
            birth_date = datetime.datetime.strptime(dob_str,"%d/%m/%Y")
            
            # dd = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("dd")
            # mm = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("mm")
            # yy = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("yy")
            # nominee_dob_str = f"{dd}/{mm}/{yy}"

            if "n_dob" in self.conversation_details:
                nominee_dob_str = self.conversation_details.get("n_dob")
            else:
                dd = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("dd")
                mm = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("mm")
                yy = self.entities.get("nominee_dob_kli", {})[0].get("entity_value").get("yy")
                nominee_dob_str = f"{dd}/{mm}/{yy}"
            # nominee_dob_str = self.conversation_details.get("n_dob")
            # nominee_dob_kli
            nominee_dob_kli = datetime.datetime.strptime(nominee_dob_str,"%d/%m/%Y")

            completion_phone_number = self.conversation_details.get("phone")
            # nominee_phone_number_kli = self.entities.get("nominee_phone_number_kli")[0].get("entity_value").get("value")

            # if self.entities.get("gender_dict_kli")[0].get("entity_value") == "Male":
            #     gender = 1
            # else:
            #     gender = 0
            
            gender = self.conversation_details.get("gender")
            companyId = self.conversation_details.get("companyId")
            agentId = self.conversation_details.get("agentId")
            
            nominee_relationship = self.entities.get("nominee_relationship_kli")[0].get("entity_value")
            if nominee_relationship == "Husband":
                nominee_relationship_value = 2
                nominee_gender = 1
            elif nominee_relationship == "Son":
                nominee_relationship_value = 3
                nominee_gender = 1
            elif nominee_relationship == "Father":
                nominee_relationship_value = 4
                nominee_gender = 1
            elif nominee_relationship == "Brother":
                nominee_relationship_value = 5
                nominee_gender = 1
            elif nominee_relationship == "Wife":
                nominee_relationship_value = 6
                nominee_gender = 0
            elif nominee_relationship == "Daugther":
                nominee_relationship_value = 7
                nominee_gender = 0
            elif nominee_relationship == "Mother":
                nominee_relationship_value = 8
                nominee_gender = 0
            elif nominee_relationship == "Sister":
                nominee_relationship_value = 9
                nominee_gender = 0
            else: 
                nominee_relationship_value = 1
                nominee_gender = 2
            
            age = self.conversation_details.get("age")
            if (age>=18) or (age<=25):
                product_risk_reference = "d3226558-b5a7-4819-a9e4-5940b4c3d3d8"
            elif (age>=26) or (age<=40):
                product_risk_reference = "98c62308-9db4-5c54-b8d1-e779558597e7"
            elif (age>=41) or (age<=55):
                product_risk_reference = "f5aa4f8e-74d9-c058-024a-a0ce42dacd04"
    
            maturity = self.conversation_details.get("maturity")
            death_benifit = self.conversation_details.get("death_benifit")
            amount_base = 200
            amount = self.conversation_details.get("amount")
            guid = str(uuid.uuid4())

            state = self.conversation_details.get("state")
            city = self.conversation_details.get("city")
            hno = self.conversation_details.get("hno")
            address = self.conversation_details.get("full_address")
            full_address = hno + address
            pin = self.conversation_details.get("pincode")

            account_number = self.entities.get("account_number_kli")[0].get("entity_value")
            
            if len(self.entities.get("account_holders_name")) == 0:
                account_holders_name = policy_holder_name
            else:
                account_holders_name = self.entities.get("account_holders_name")[0].get("entity_value").get("value")
            
            bank_name = self.entities.get("bank_name_kli")[0].get("entity_value")

            url = f"{self.brisk_url}{self.create_sale_policy_url}"
        
            payload = {
                    "policies": [{
                    "currencyCode": "INR",
                    "members": [
                        {
                            "externalReference": "6e4342a8-02b0-fd4c-94f5-9b956b8a8a68", #new guid everytime.
                            "memberType": 1,
                            "title": "",
                            "firstName": policy_holder_fname,
                            "middleName": "",
                            "lastName": policy_holder_lname,
                            "eMail": email,
                            "nationalityId": "demo",
                            "birthDate": str(birth_date),
                            "mobilePhoneCode": "91",
                            "mobilePhone": completion_phone_number,
                            "landlinePhoneCode": None,
                            "landlinePhone": None,
                            "gender": gender,
                            "marriageStatus": marital_status,
                            "state": state,
                            "province": None,
                            "city": city,
                            "suburb": None,
                            "address": full_address,
                            "address1": None,
                            "address2": None,
                            "countryId": 194,
                            "stateCode": None,
                            "pin": pin,
                            "nationality": None,
                            "residency": None,
                            "alternateEMail": None,
                            "gpsCoordinate": None,
                            "postalAddress": full_address,
                            "postalCity": city,
                            "postalState": state,
                            "postalProvince": None,
                            "postalStateCode": None,
                            "postalGPSCoordinate": None,
                            "workAddress": None,
                            "workSuburb": None,
                            "workCity": None,
                            "workState": None,
                            "workProvince": None,
                            "workStateCode": None,
                            "workPhoneCode": None,
                            "workPhone": None,
                            "workCompany": None,
                            "workGPSCoordinate": None,
                            "trainingInstitution": None,
                            "studentID": None,
                            "customerIdentityType": 0,
                            "companyName": None,
                            "tradingAs": None,
                            "companyRegNo": None,
                            "vatNumber": None
                        }
                    ],
                    "beneficiaries": [
                        {
                            "externalReference": "ec37f14a-f026-05c4-7f27-c1493035ceeb", #new guid
                            "beneficiaryType": "nominee", #0,
                            "title": "",
                            "firstName": nominee_name_fname,
                            "middleName": "",
                            "lastName": nominee_name_lname,
                            "birthDate": str(nominee_dob_kli),
                            "eMail": "",
                            "mobilePhoneCode": "91",
                            "mobilePhone": "",
                            "landlinePhoneCode": None,
                            "landlinePhone": None,
                            "address": None,
                            "address1": None,
                            "address2": None,
                            "gender": nominee_gender,
                            "relationship": nominee_relationship_value,
                            "split": 1,
                            "customerIdentityType": 0,
                            "companyName": None,
                            "tradingAs": None,
                            "companyRegNo": None,
                            "vatNumber": None
                        }
                    ],
                    "attributes": [
                        {
                            "name": "Age",
                            "value": str(age)
                        }
                    ],
                    "risks": [
                        {
                            "externalReference": guid,
                            "attributes": [
                                {
                                    "name": "Age",
                                    "value": str(age)
                                }
                            ],
                            "valuations": [
                                {
                                    "name": "maturity",
                                    "value": float(maturity)
                                },
                                {
                                    "name": "deathBenefit",
                                    "value": float(death_benifit)
                                }
                            ],
                            "productRiskReference": "cbcb4dd3-e61f-791c-8c4b-2e215a512bbf", #difff for prod
                            "price": amount_base,
                            "discount": 0,
                            "tax": 0,
                            "total": amount_base
                        }
                    ],
                    "bankAccounts": [{
                        "bank" : bank_name,
                        "accountNumber": account_number,
                        "accountHolder": account_holders_name
                    }],
                    "productOptionReference": "4916ecad-fc89-9f90-b49d-cb05d5196350", #age check
                    "status": 15
                }
            ],
            "networkId": "D48911A5-820A-4A53-9E69-EE9B0E070372", #
            "companyId": companyId,
            "agentId": agentId
            }
    
            
            payload["policies"] = payload["policies"] * int(int(amount)/200)

            headers = {
                'token': self.conversation_details.get("jwtToken"),
                'Ocp-Apim-Subscription-Key': 'a00a7ff5c53f4c628979941833d63dc9',
                'Content-Type': 'application/json'
            }

            # logger.info(f"[CREATE POLICY SALE API] Payload :  {payload}")
            response = requests.post(url, data = json.dumps(payload), headers = headers, timeout = 9)
            if response.status_code != 202:
                logger.error(f"[CREATE POLICY SALE API] Error Occured : {response.text}")
                return "EXCEPTION"

            logger.info(f"[CREATE POLICY SALE API] Response :  {response.text}")
            return response

        except requests.exceptions.Timeout as err:
            logger.error(f"[CREATE POLICY SALE API] Timeout : {err}")
            return "TIMEOUT"

        except Exception as e:
            logger.error(f"[CREATE POLICY SALE API] Exception Occured : {e}")
            return "EXCEPTION"

    
    def upload_image_api(self):

        create_sale_policy_response = self.create_sale_policy_api()
        if (create_sale_policy_response != "EXCEPTION") and (create_sale_policy_response != "TIMEOUT"):
            try:
                policy_sale_reference = create_sale_policy_response.json().get("policySaleReference")
                self.conversation_details["psr"] = policy_sale_reference
                external_reference = create_sale_policy_response.json().get("externalReference") 
                policy_reference = create_sale_policy_response.json().get("policies")[0].get("policyReference")
                amount = self.conversation_details.get("amount")

                payload = {
                    "externalReference": external_reference,
                    "policySaleReference": policy_sale_reference,
                    "policyAttachments": [
                    {
                        "externalReference": "",
                        "policyReference": "",
                        "byteAttachments": [
                        {
                            "AttachmentByteArray": "",
                            "AttachmentInstanceId": "",

                            "FileExtension": "png",
                            "ProductAttachmentOptionInstanceId": ""
                        },
                        {
                            "AttachmentByteArray": "",
                            "AttachmentInstanceId": "",

                            "FileExtension": "png",
                            "ProductAttachmentOptionInstanceId": ""
                        },
                        {
                            "AttachmentByteArray": "",
                            "AttachmentInstanceId": "",

                            "FileExtension": "png",
                            "ProductAttachmentOptionInstanceId": ""
                        }
                        ]
                    }]
                }
                

                
                url = f"{self.brisk_url}{self.image_upload_url}"

                headers = {
                    'token' : self.conversation_details.get("jwtToken"),
                    'Ocp-Apim-Subscription-Key': 'a00a7ff5c53f4c628979941833d63dc9',
                    'Content-Type': 'application/json'
                }
                
                ###################### API CALL FOR CANCELLED CHEQUE IMAGE UPLOAD #####################
                cancelled_cheque_image_kli = self.entities.get("cancelled_cheque_image_kli")[0].get("entity_value")
                cancelled_cheque_image_call = requests.get(cancelled_cheque_image_kli)
                cancelled_cheque_encoded = base64.b64encode(cancelled_cheque_image_call.content)
                cancelled_cheque_base64 = cancelled_cheque_encoded.decode('utf-8')
                payload["policyAttachments"][0]["byteAttachments"][0]["AttachmentByteArray"] = cancelled_cheque_base64
                payload["policyAttachments"][0]["byteAttachments"][0]["AttachmentInstanceId"] = "4B264A91-CE6C-431F-8C57-0D9ACF5D3D46"
                payload["policyAttachments"][0]["byteAttachments"][0]["ProductAttachmentOptionInstanceId"] = "103B38F6-5138-BDF8-29CF-70DE411497E3"   
                
                ###################### API CALL FOR FRONT OF AADHAR CARD IMAGE UPLOAD #####################
                adhaar_image_kli = self.entities.get("aadhar_front_kli")[0].get("entity_value") # Front Image of Aadhar
                aadhar_image_call = requests.get(adhaar_image_kli)
                aadhar_image_encoded = base64.b64encode(aadhar_image_call.content)
                aadhar_image_base64 = aadhar_image_encoded.decode('utf-8')
                payload["policyAttachments"][0]["byteAttachments"][1]["AttachmentByteArray"] = aadhar_image_base64
                payload["policyAttachments"][0]["byteAttachments"][1]["AttachmentInstanceId"] = "AC5F90E9-CF24-474F-9CBC-B192B53A4B9B"
                payload["policyAttachments"][0]["byteAttachments"][1]["ProductAttachmentOptionInstanceId"] = "AECF6D6A-52E4-481A-BC13-7853AD1FA4E2"   
                
                ###################### API CALL FOR BACK OF AADHAR CARD IMAGE UPLOAD #####################
                address_proof_kli = self.entities.get("aadhar_card_back_kli")[0].get("entity_value") # Back Image of Aadhar
                address_proof_image_call = requests.get(address_proof_kli)
                address_proof_image_encoded = base64.b64encode(address_proof_image_call.content)
                address_proof_image_base64 = address_proof_image_encoded.decode('utf-8')
                payload["policyAttachments"][0]["byteAttachments"][2]["AttachmentByteArray"] = address_proof_image_base64
                payload["policyAttachments"][0]["byteAttachments"][2]["AttachmentInstanceId"] = "CF1F47A2-A0C8-4FE3-A497-D87EE13A9E21"
                payload["policyAttachments"][0]["byteAttachments"][2]["ProductAttachmentOptionInstanceId"] = "D93BABBC-D2B9-4852-9254-16F57BFC0B28"   

                # ###################### API CALL FOR NOMINEE'S FRONT OF AADHAR CARD IMAGE UPLOAD #####################
                # address_proof_kli = self.entities.get("aadhar_card_back_kli")[0].get("entity_value") # Back Image of Aadhar
                # address_proof_image_call = requests.get(address_proof_kli)
                # address_proof_image_encoded = base64.b64encode(address_proof_image_call.content)
                # address_proof_image_base64 = address_proof_image_encoded.decode('utf-8')
                # payload["policyAttachments"][0]["byteAttachments"][2]["AttachmentByteArray"] = address_proof_image_base64
                # payload["policyAttachments"][0]["byteAttachments"][2]["AttachmentInstanceId"] = "CF1F47A2-A0C8-4FE3-A497-D87EE13A9E21"
                # payload["policyAttachments"][0]["byteAttachments"][2]["ProductAttachmentOptionInstanceId"] = "D93BABBC-D2B9-4852-9254-16F57BFC0B28"   

                if (int(amount) / 2 ) == 1:
                    payload["policyAttachments"][0]["externalReference"] = create_sale_policy_response.json().get("policies")[0].get("externalReference")
                    payload["policyAttachments"][0]["policySaleReference"] = create_sale_policy_response.json().get("policies")[0].get("policyReference")

                elif (int(amount) / 2 ) == 2:
                    payload["policyAttachments"][0]["externalReference"] = create_sale_policy_response.json().get("policies")[0].get("externalReference")
                    payload["policyAttachments"][0]["policySaleReference"] = create_sale_policy_response.json().get("policies")[0].get("policyReference")

                    payload["policyAttachments"][0]["externalReference"] = create_sale_policy_response.json().get("policies")[0].get("externalReference")
                    payload["policyAttachments"][0]["policySaleReference"] = create_sale_policy_response.json().get("policies")[0].get("policyReference")
                
                payload["policyAttachments"] = [policy_attach.copy() for policy_attach in payload["policyAttachments"] * int(int(amount)/200)]

                self.policy_ref = []
                self.external_ref = []
                for index_val, policy in enumerate(create_sale_policy_response.json().get("policies")):
                    payload["policyAttachments"][index_val]["externalReference"] = create_sale_policy_response.json().get("policies")[index_val].get("externalReference")
                    payload["policyAttachments"][index_val]["policyReference"] = create_sale_policy_response.json().get("policies")[index_val].get("policyReference")
                    globals() [f"policy_reference{index_val}"] = create_sale_policy_response.json().get("policies")[index_val].get("policyReference")
                    globals() [f"external_reference{index_val}"] = create_sale_policy_response.json().get("policies")[index_val].get("externalReference")
    
                    self.policy_ref.append(globals() [f"policy_reference{index_val}"])
                    self.external_ref.append(globals() [f"external_reference{index_val}"])
                
                logger.info(f"Policy Reference {self.policy_ref}")
                logger.info(f"External Policy Reference {self.external_ref}")
                
                # logger.info(f"[UPLOAD IMAGE API] Payload : {json.dumps(payload)}")
                logger.info(f"[UPLOAD IMAGE API] Payload : {url}")
                response = requests.post(url, data = json.dumps(payload), headers = headers , timeout = 10)
                if response.status_code != 202:
                    logger.error(f"[UPLOAD IMAGE API] Exception Occured {response.text}")
                    return "EXCEPTION"
                logger.info(f"[UPLOAD IMAGE API] Response : {response.text}")
                return response

            except requests.exceptions.Timeout as err:
                logger.error(f"[UPLOAD IMAGE API] Timeout : {err}")
                return "TIMEOUT"

            except Exception as e:
                logger.error(f"[UPLOAD IMAGE API] Exception Occured {e}")
                return "EXCEPTION"
        else:
            return create_sale_policy_response

    def get_final_response(self):
        error_count = 0 if not self.conversation_details.get("cp_ui_error_count") else self.conversation_details.get('cp_ui_error_count')
        if error_count < 10:
            upload_image_api_response = self.upload_image_api()
            if (upload_image_api_response == "TIMEOUT") or (upload_image_api_response == "EXCEPTION"):                
                error_count = error_count + 1
                if error_count % 2 == 0:
                    even_odd = "even"
                else:
                    even_odd = "odd"
                self.conversation_details["cp_ui_error_count"] = error_count
                self.final_response["conversation_details"] = self.conversation_details
                self.final_response["error"] = "EXCEPTION/TIMEOUT"
                self.final_response["even_odd"] = even_odd
            else:
                self.conversation_details.pop("cp_ui_error_count", None)
                self.conversation_details.pop("resend_counter", None)
                self.conversation_details.pop("tc_counter", None)
                self.conversation_details.pop("tc_val_counter", None)
                self.conversation_details.pop("wrong_otp_counter", None)
                
                self.conversation_details["pf"] = self.policy_ref
                self.conversation_details["ef"] = self.external_ref
                self.final_response["pf"] = self.policy_ref
                self.final_response["ef"] = self.external_ref

                self.final_response["conversation_details"] = self.conversation_details
                self.final_response["error"] = False
        else:
            self.final_response["error"] = "MAX"
            self.final_response["hsl"] = "You have reached maximum limits to retry. Please try again later."
        
        return self.final_response