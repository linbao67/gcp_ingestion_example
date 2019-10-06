from datetime import datetime

from google.appengine.ext import ndb


class Account(ndb.Model):
    account_number = ndb.KeyProperty()
    name = ndb.StringProperty()
   # bill_to_contact = ndb.StringProperty()
    #sold_to_contact = ndb.StringProperty()

class SoldToContact(ndb.Model):
    pass


class BillToContact(ndb.Model):
    pass


class Payment(ndb.Model):
    payment_id = ndb.KeyProperty()
    account_id = ndb.StringProperty()
    account_number = ndb.StringProperty()
    account_name = ndb.StringProperty()
    type = ndb.StringProperty()
    effective_date = ndb.DateTimeProperty()
    payment_number = ndb.StringProperty()
    payment_method_id = ndb.StringProperty()
    amount = ndb.FloatProperty()




