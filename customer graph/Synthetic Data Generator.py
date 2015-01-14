from mongoengine import *

DB_NAME = 'mysite'

connect(DB_NAME)

# this is for the synthetic CRM data model
class Phone(EmbeddedDocument):
    number = IntField() #TODO: generate
    phone_type = StringField() #TODO: generate
    
class CustomerProfile(EmbeddedDocument):
    customer_id = IntField() #TODO: generate
    name = StringField() #Stuckey twitter match
    location = StringField() # Stuckey twitter match
    email = StringField() #TODO: generate
    phone = EmbeddedDocumentField(Phone) #TODO: generate
    twitter = StringField() #Stuckey twitter match
    dob = DateTimeField() #TODO: generate
    gender = StringField() #TODO: generate

class CustomerBehavior(EmbeddedDocument):
    mobile_app = BooleanField() #TODO: generate
    gift_card_balance = FloatField() #TODO: generate
    number_of_transactions = IntField() #TODO: generate

class Employment(EmbeddedDocument): # TODO: TBD
    linkedin_profile = StringField() 
    employer = StringField()
    job_title = StringField()
    salary_range_low = IntField()
    salary_range_mid = IntField()
    salary_range_high = IntField()

class CrmData(EmbeddedDocument):
    customer_profile = EmbeddedDocumentField(CustomerProfile)
    customer_behavior = EmbeddedDocumentField(CustomerBehavior)

class CollectedData(EmbeddedDocument):
    twitter = StringField() #TODO: update this to be an embedded doc
    employment = EmbeddedDocumentField(Employment) #TODO: update this to be an embedded doc for the matching algo
    
class MatchedData(EmbeddedDocument):
    sbi = StringField() #TODO: update this to be an embedded doc for the matching algo

class CustomerData(Document):
    crm_data = EmbeddedDocumentField(CrmData)
    collected_data = EmbeddedDocumentField(CollectedData)
    matched_data = EmbeddedDocumentField(MatchedData)



all_customers = CustomerData.objects.all()
print len(all_customers)



import uuid
def generate_customer_id():
    new_id = uuid.uuid4()
    return new_id
    

def generate_email(customer):
    if customer.crm_data.customer_profile.name:
        new_name = str(customer.crm_data.customer_profile.name).lower().replace(' ', '')
        new_email = new_name + '@email.com'
        return new_email
    else:
        #create generic email if there is no name
        pass



def generate_phone_number():
    number = '2125551212'
    return number



def generate_phone_type():
    phone_type = 'mobile'
    return phone_type



import datetime
from random import randrange
base = datetime.datetime.today()
def generate_dob():
    days_param = randrange(365*13,365*60)
    new_dob = base - datetime.timedelta(days=days_param)
    return new_dob.strftime('%m/%d/%Y')



import random
male_female_list = ['male', 'female']
def generate_gender():
    gender = random.choice(male_female_list)
    return gender



import random
mobile_app_probability = ['True'] * 3 + ['False'] * 7
def generate_mobile_app():
    return random.choice(mobile_app_probability)



import random
def generate_gift_card_balance():
    return random.uniform(0, 74.32)



def generate_number_of_transactions():
    #TODO: update this based on the parameters we need
    return 0



for customer in all_customers:
    customer.crm_data.customer_profile.customer_id = generate_customer_id()
    customer.crm_data.customer_profile.email = generate_email(customer)
    customer.crm_data.customer_profile.phone.number = generate_phone_number()
    customer.crm_data.customer_profile.phone.phone_type = generate_phone_type()
    customer.crm_data.customer_profile.dob = generate_dob()
    customer.crm_data.customer_profile.gender = generate_gender()
    customer.crm_data.customer_behavior.mobile_app = generate_mobile_app()
    customer.crm_data.customer_behavior.gift_card_balance = generate_gift_card_balance()
    customer.crm_data.customer_behavior.number_of_transactions = generate_number_of_transactions()




