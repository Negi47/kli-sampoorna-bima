from distutils.log import debug
from email import policy
from imghdr import what
from flask import Flask, request, render_template
import logging
import flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import logging
from user_info import UserInfo
from submit_external_payment import submit_external_payment as SEP
from make_policy_sale_payment import make_policy_sale_payment as MPSP
from issue_policy_sale import issue_policy_sale as IPS
from whatsapp_consent_api import whatsapp_consent_api as WC
from send_push_notifications import send_push_notifcations as SPN

logging.basicConfig(filename='app_kli.log', filemode='w', format="%(asctime)s ----- %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["DEBUG"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://kli_sampoorna:kli_sampoorna@0.0.0.0:5432/user_info_kli'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://kli_sampoorna:kli_sampoorna@localhost/user_info_kli'
db = SQLAlchemy(app)

# @app.route('/', methods=["GET", "POST"])
# def index():
#     return "Hello Welcome to KLI"

@app.route("/save_user_info", methods=["GET", "POST"])
def save_user_info():
    phone_number = ""
    bus_transaction_id = ""
    policy_reference0 = ""
    policy_sale_reference = ""
    external_reference0 = ""
    payu_id = ""
    amount = ""
    if request.method == "GET":
        return "Get method is not allowed"
    elif request.method == "POST":
        if request.is_json:
            logger.info(f"[REQUEST BODY] {request}")
            data = request.json
            user_info = UserInfo( 
                phone_number = data.get("phone_number"), 
                bus_transaction_id = data.get("bus_txn_id"), 
                payu_id = data.get("payu_id"), 
                amount = data.get("amount"),
                policy_reference0= data.get("policy_reference0"),
                policy_reference1= data.get("policy_reference1"),
                policy_reference2= data.get("policy_reference2"), 
                policy_sale_reference = data.get("psr"), 
                external_reference0= data.get("external_reference0"),
                external_reference1= data.get("external_reference1"),
                external_reference2= data.get("external_reference2")
            )
            if phone_number is None:
                return ("Phone Number cannot be None", 406)
            if bus_transaction_id is None:
                return ("Bus Transaction ID cannot be None", 406)
            if policy_reference0 is None:
                return ("Policy Reference 0 cannot be None", 406)
            if policy_sale_reference is None:
                return ("Policy Sale Reference cannot be None", 406)
            if external_reference0 is None:
                return ("External Reference 0 cannot be None", 406)
            if payu_id is None:
                return ("PayU ID cannot be None", 406)
            if amount is None:
                return ("Amount cannot be None", 406)

            db.session.add(user_info)
            db.session.commit()
            db.session.refresh(user_info)
            return {'message': f'User Data with Phone_number {user_info.phone_number} saved successfully.'}
        else:
            return ("Invalid Payload",  401)

@app.route('/kli_sampoorna',methods=['GET'])
def get_method():
    data = request.data
    args = request.args

    logging.info('DATA %s',str(data))

    logger.info("GET method not accepted")
    return "Get method is not accepted"

@app.route('/kli_sampoorna',methods=['POST'])
def post_method():

    txn_id = ""
    data = request.data
    form_data = request.form
    logger.info('DATA %s',str(data))
    logger.info('FORM DATA %s',str(form_data))

    users = UserInfo.query.all()
    if not users:
        print("No users found. Database Empty")
    else:
        print("Users list found.",users)
        user_details = policy_details = {}
        try:
            for user in users:
                if str(form_data["reference_id"]) == str(user.payu_id):
                    logger.info(f"USER MATCHED {user}")

                    policySaleReference = user.policy_sale_reference
                    txn_id = user.bus_transaction_id
                    user_details["phone_number"] = str(user.phone_number)
                    user_details["txn_id"] = str(user.bus_transaction_id)
                    user_details["policy_reference0"] = user.policy_reference0

                    if user.policy_reference1 is not None:
                        user_details["policy_reference1"] = user.policy_reference1
                        
                        if user.policy_reference2 is not None:
                            user_details["policy_reference2"] = user.policy_reference2

                    print("Tax id", txn_id)
                    break;
            
            user_info = UserInfo( 
            status = form_data["txn_status"])

            db.session.add(user_info)
            db.session.commit()
            db.session.refresh(user_info)

            # if form_data["BusRes"] == "Success":
            if form_data["txn_status"] == "captured":
                        if not txn_id:
                            print("user details not matched. ")

                        else:
                            ## Call Sumit External Payment API
                            phonenumber = user_details.get("phone_number")
                            whatsapp_consent_response = WC(phonenumber)

                            # if (whatsapp_consent_response!="EXCEPTION") and (whatsapp_consent_response!="TIMEOUT"):
                            seb_response = SEP(user_details)
                            print("SEB Response", seb_response)
                            logger.info(f"[SEB RESPONSE] : {seb_response}")
                            
                            if (seb_response!="EXCEPTION") and (seb_response!="TIMEOUT"):
                                user_details.pop("txn_id")
                                user_details.pop("phone_number")
                                policy_details = user_details
                            
                                mpsp_response = MPSP(policy_details,seb_response,policySaleReference)
                                print("MPSP Response", mpsp_response)
                                logger.info(f"[MPSP RESPONSE] : {mpsp_response}")
                                
                                if (mpsp_response!="EXCEPTION") and (mpsp_response!="TIMEOUT"):
                                    jwt_token = seb_response.get("jwt_token")

                                    ips_response = IPS(jwt_token, policySaleReference,policy_details,seb_response)
                                    print("IPS Response", ips_response)
                                    logger.info(f"[IPS RESPONSE] : {ips_response}")
                                    
                                    if (ips_response!="EXCEPTION") and (ips_response!="TIMEOUT"):
                                    # if True:
                                        event_name = "Payment made"
                                        send_push_notification_response = SPN(phonenumber,event_name)
                                        print("SPN Response", send_push_notification_response)
                                        logger.info(f"[SPN RESPONSE] : {send_push_notification_response}")

                                        if (send_push_notification_response!="EXCEPTION") and (send_push_notification_response!="TIMEOUT"):
                                            data = "Please return to WhatsApp Bot for continuing journey"
                                            return render_template("index.html", data = data)
                                            
                                        else:
                                            return f"[~~~~~ SEND PUSH NOTIFCATIONS INTERAKT API] {send_push_notification_response}"
                                            
                                    else:
                                        return f"[~~~~~ ISSUE POLICY SALE API] {mpsp_response}"
                                    
                                else:
                                    return f"[~~~~~ MAKE POLICY SALE PAYMENT API] {mpsp_response}"

                            else:
                                return f"[~~~~~ SUBMIT EXTERNAL PAYMENT API] {seb_response}"

                            # else:
                            #     return f"[~~~~~ WHATSAPP CONSENT API] {whatsapp_consent_response}"
            else:
                print("Payment Failed")
                # if True:
                # phonenumber = user_details.get("phone_number")
                # event_name = "Payment Failed"
                # send_push_notification_response = SPN(phonenumber,event_name)
                # print("SPN Response", send_push_notification_response)
                # logger.info(f"[SPN RESPONSE] : {send_push_notification_response}")

                # if (send_push_notification_response=="EXCEPTION") and (send_push_notification_response=="TIMEOUT"):
                #     return f"[~~~~~ SEND PUSH NOTIFCATIONS INTERAKT API] {send_push_notification_response}"
                # return "Payment Failed.!!!"        
        
        except Exception as e:
            logger.error(f"Exception Occured {e}")   
    status = flask.Response(status = 200)
    # data = "Sorry, we weren’t able to complete your transaction due to some technical issue. Please click on below button to go back to WhatsApp and retry the payment."
    # return render_template("index.html", data = data)
    return status

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)


# ([('TranxID', '1000888386'), ('BusRes', 'Success'), ('SiStatus', '')])
