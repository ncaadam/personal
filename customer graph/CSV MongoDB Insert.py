import csv
from pymongo import MongoClient
import sys


def insert_csv_to_db(path):
    client = MongoClient()
    db = client.mysite
    if 'SBI_profiles' in db.collection_names():
            print "This database already exists"
            coll = db.SBI_profiles
            print "There are", coll.count(), "customers in the database."
    else:
        print "Creating database..."
        coll = db.create_collection('SBI_profiles')
        print "Database created..."

    if coll.count() == 0:
        try:
            with open(path,'rU') as cust_data:
                print "Opening csv file..."
                try:
                    print "Uploading data..."
                    cust_data_reader = csv.DictReader(cust_data)
                    coll.insert(cust_data_reader)
                    print "There were",coll.count(),"customers inserted."
                except Exception,e:
                    print "There was an error when reading or uploading your CSV file -", str(e)
        except Exception,e:
            print "There was an error opening your CSV file -", str(e)
    else:
        print "There is already data in the customer table. Remove it first."


def main(input_var):
    insert_csv_to_db(input_var)

if __name__ == "__main__":
    main(sys.argv[1])
