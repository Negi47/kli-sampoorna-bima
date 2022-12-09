from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://kli_sampoorna:kli_sampoorna@localhost/user_info_kli'
db = SQLAlchemy(app)

class UserInfo(db.Model):
    id = db.Column(db.Integer, autoincrement = True, nullable = False, primary_key = True)
    phone_number = db.Column(db.Numeric(10,0), nullable = False)
    bus_transaction_id = db.Column(db.Numeric(10,0), nullable = False)
    payu_id = db.Column(db.String(40), nullable = False)
    amount = db.Column(db.String(40), nullable = False)
    policy_reference0 =  db.Column(db.String(14), nullable = False)
    policy_reference1 =  db.Column(db.String(14), nullable = True)
    policy_reference2 =  db.Column(db.String(14), nullable = True)
    policy_sale_reference = db.Column(db.String(40), nullable = False)
    external_reference0 =  db.Column(db.String(40), nullable = False)
    external_reference1 =  db.Column(db.String(40), nullable = True)
    external_reference2 =  db.Column(db.String(40), nullable = True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, phone_number, bus_transaction_id, payu_id, amount, policy_reference0,policy_reference1, policy_reference2, policy_sale_reference,external_reference0, external_reference1, external_reference2):
        self.phone_number = phone_number
        self.bus_transaction_id = bus_transaction_id
        self.payu_id = payu_id
        self.amount = amount
        self.policy_reference0 = policy_reference0
        self.policy_reference1 = policy_reference1
        self.policy_reference2 = policy_reference2
        self.policy_sale_reference = policy_sale_reference,
        self.external_reference0 = external_reference0
        self.external_reference1 = external_reference1
        self.external_reference2 = external_reference2
    
    def __repr__(self):
        return f'{self.phone_number} {self.bus_transaction_id} {self.policy_reference0} {self.policy_reference1} {self.policy_reference2} {self.policy_sale_reference}  {self.amount} {self.payu_id}'
