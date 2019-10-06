from google.appengine.ext import ndb
from flask import Flask
from datetime import datetime
from app.services import link
from app.services import zuora_models
import json

response_str = '''{
  "basicInfo" : {
    "id" : "ff1e23e2211fb802b818d7c630fbc4f6",
    "name" : "Acme Inc.",
    "accountNumber" : "A00000485",
    "notes" : "",
    "status" : "Active",
    "crmId" : "",
    "batch" : "Batch5",
    "invoiceTemplateId" : "ff1e23e2ee5516d16eb5a28f95bc4eb4",
    "communicationProfileId" : "ff1e23e2ff482baa2ce91e228fddde1e",
    "CorporateRegion__h" : null,
    "Entity__c" : "EMEA",
    "InCollections__c" : "False",
    "salesRep" : "",
    "parentId" : null,
    "creditMemoTemplateId" : "ff1e23e2cd9d667a9f0128f56c454edd",
    "debitMemoTemplateId" : "ff1e23e2841a754fc0d846769febb215",
    "sequenceSetId" : null
  },
  "billingAndPayment" : {
    "billCycleDay" : 1,
    "currency" : "EUR",
    "paymentTerm" : "Net 30",
    "paymentGateway" : null,
    "invoiceDeliveryPrefsPrint" : false,
    "invoiceDeliveryPrefsEmail" : false,
    "additionalEmailAddresses" : [ "" ]
  },
  "metrics" : {
    "balance" : 8167.000000000,
    "totalInvoiceBalance" : 8167.000000000,
    "creditBalance" : 0E-9,
    "totalDebitMemoBalance" : 0E-9,
    "unappliedPaymentAmount" : 0E-9,
    "unappliedCreditMemoAmount" : 0E-9,
    "contractedMrr" : 3333.330000000
  },
  "billToContact" : {
    "address1" : "Maximilianstrasse 13",
    "address2" : "3rd Floor",
    "city" : "Munich",
    "country" : "Germany",
    "county" : "",
    "fax" : "",
    "firstName" : "Johnny",
    "homePhone" : "",
    "lastName" : "Bond",
    "mobilePhone" : "",
    "nickname" : "",
    "otherPhone" : "",
    "otherPhoneType" : null,
    "personalEmail" : "",
    "state" : "",
    "taxRegion" : "",
    "workEmail" : "",
    "workPhone" : "",
    "zipCode" : "80539",
    "contactDescription" : ""
  },
  "soldToContact" : {
    "address1" : "Maximilianstrasse 13",
    "address2" : "3rd Floor",
    "city" : "Munich",
    "country" : "Germany",
    "county" : "",
    "fax" : "",
    "firstName" : "Johnny",
    "homePhone" : "",
    "lastName" : "Bond",
    "mobilePhone" : "",
    "nickname" : "",
    "otherPhone" : "",
    "otherPhoneType" : null,
    "personalEmail" : "",
    "state" : "",
    "taxRegion" : "",
    "workEmail" : "",
    "workPhone" : "",
    "zipCode" : "80539",
    "contactDescription" : ""
  },
  "taxInfo" : {
    "exemptStatus" : "No",
    "exemptCertificateId" : "",
    "exemptCertificateType" : "",
    "exemptIssuingJurisdiction" : "",
    "exemptEffectiveDate" : null,
    "exemptExpirationDate" : null,
    "exemptDescription" : "",
    "exemptEntityUseCode" : "",
    "companyCode" : "",
    "VATId" : ""
  },
  "success" : true
}'''

response_str2 = '''{
  "payments": [
    {
      "id": "ff1e23e24eb0b0a19b74e8650d4b24ef",
      "accountId": "ff1e23e2211fb802b818d7c630fbc4f6",
      "accountNumber": "A00000485",
      "accountName": "Acme Inc.",
      "type": "External",
      "effectiveDate": "2018-03-22",
      "paymentNumber": "P-00002346",
      "paymentMethodId": "ff1e23e25f0e763009f4355bcd1614ed",
      "amount": 21833.000000000,
      "paidInvoices": [
        {
          "invoiceId": "ff1e23e27567f299059c440b7a755b3b",
          "invoiceNumber": "INV00002972",
          "appliedPaymentAmount": 21833.000000000
        }
      ],
      "gatewayTransactionNumber": null,
      "status": "Processed",
      "RetryNumber__c": null,
      "RetryStatus__c": "Complete"
    },
    {
      "id": "ff1e23e2843c08f6e909c3cbe9bf6f5d",
      "accountId": "ff1e23e2211fb802b818d7c630fbc4f6",
      "accountNumber": "A00000485",
      "accountName": "Acme Inc.",
      "type": "External",
      "effectiveDate": "2018-02-14",
      "paymentNumber": "P-00002345",
      "paymentMethodId": "ff1e23e25f0e763009f4355bcd1614ed",
      "amount": 10000.000000000,
      "paidInvoices": [
        {
          "invoiceId": "ff1e23e27567f299059c440b7a755b3b",
          "invoiceNumber": "INV00002972",
          "appliedPaymentAmount": 10000.000000000
        }
      ],
      "gatewayTransactionNumber": null,
      "status": "Processed",
      "RetryNumber__c": null,
      "RetryStatus__c": "Complete"
    }
  ],
  "success": true
}
'''

app = Flask(__name__)

@app.route('/service/add_account')
def add_account():

    response = json.loads(response_str)

    name = response['basicInfo']['name']
    account_number = response['basicInfo']['accountNumber']

    billToContact = response['billToContact']

    soldToContact = response['soldToContact']
    print(name, account_number, billToContact, soldToContact)
    #account_number_key = ndb.Key("Account", account_number)

    account = zuora_models.Account()
    account.account_number = ndb.Key("account",account_number)
    account.name = name
    #account.bill_to_contact = billToContact
    #account.sold_to_contact = soldToContact
    account.put()
    return {"account_number":account_number}


@app.route('/service/store')
def add_payments():
    response = json.loads(link.link())

    for i in response["payments"]:
        payment = zuora_models.Payment()
        payment.payment_id = ndb.Key("payment", i["id"])
        payment.account_id = i["accountId"]
        payment.account_number = i["accountNumber"]
        payment.account_name = i["accountName"]
        payment.type = i["type"]
        payment.effective_date = datetime.strptime(i["effectiveDate"], '%Y-%m-%d')
        payment.payment_number = i["paymentNumber"]
        payment.payment_method_id = i["paymentMethodId"]
        payment.amount = i["amount"]
        payment.put()

    return {"payment_number": "OK"}
