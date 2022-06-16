
from flask import Flask, request, render_template
import logging 
import atexit
import io
import json
import flask
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

# @app.route('/digilockers',methods=['GET'])
# def get_method():
#     data = request.data
#     print("Data",data)
    
#     args = request.args
#     print("Args",args)
    
#     logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG)
#     logging.debug('DATA %s',str(data))
#     status = flask.Response(status = 200)
#     if len(data):
#         return status
#     else:
#         print("No data received")
#         return status

# @app.route('/digilockers',methods=['POST'])
# def post_method():
#     logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG)
#     data = request.data
#     logging.debug('DATA %s',str(data))
#     status = flask.Response(status = 200)

    # mobile_number = "9999999999"

    # if "event" in data:
    # if data.get('event') == "documents.pulled.successfully":
        # logging.debug('DATA %s',str(data))
        # mobile_number = data['payload']['digilocker_request']['customer_identifier'] 
        # push_eventnotfication(mobile_number)

    # return status

def push_eventnotfication(mobile_number):
    url = "https://api.interakt.ai/v1/public/track/events/"

    payload = {
        "userId": mobile_number,
        "phoneNumber": mobile_number,
        "countryCode": "+91",
        "event": "Create certificate",
        "traits": {
            "URL": "https://www.interakt.shop/resource-center/api-doc"
        },
        "createdAt": "2020-11-05T13:26:52.926Z"
    }
    headers = {
    'Authorization': 'Basic cDdTTUEyeFdBYmR0NWV1SjRWWmcxUF80YkUwUEJ2WWc2N1FiNUU5c2RNbzo=',
    'Content-Type': 'application/json',
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        logging.debug('Response Push Notification %s',str(response.text))
        status = True

    except Exception as err:
        status = True

    return status

@app.route('/kli_sampoorna',methods=['GET'])
def get_method():
    data = request.data
    print("Data",data)
    
    args = request.args
    print("Args",args)
    
    logging.basicConfig(filename='app_kli.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG)
    logging.debug('DATA %s',str(data))
    status = flask.Response(status = 200)
    if len(data):
        return "Get Method is not accepted"
    else:
        print("No data received")
        return "Get method is not accepted"

@app.route('/kli_sampoorna',methods=['POST'])
def post_method():
    logging.basicConfig(filename='app_kli.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG)
    data = request.data
    form_data = request.form
    logging.debug('DATA %s',str(data))
    logging.debug('FORM DATA %s',str(form_data))

    status = flask.Response(status = 200)

#    return "<html><style>  .center-screen {  display: flex;  flex-direction: column;  justify-content: center;  align-items: center;  text-align: center;  min-height: 100vh;</style> <head> </head> <body> <div class="center-screen"> <img src="https://www.kotaklife.com/assets/images/fb-share.png" alt="Kotak Logo" width="250" height="150"> <b style="color:rgb(30,70,121);">Please return to WhatsApp Bot for continuing journey</b> &nbsp; <a href="https://api.whatsapp.com/send?phone=3197010240285" style="display: inline-block; padding:8px; border-radius: 8px; background-color: #25D366; color: #fff; text-decoration: none; font-family: sans-serif; font-size: 16px;">Return to WhatsApp</a> </div> </body> </html>"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)

