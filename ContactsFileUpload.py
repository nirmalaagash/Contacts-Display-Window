import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    passwd="",
    database="contact_details",
)
my_database = db_connection.cursor()

import csv

with open('Contacts.csv', "r") as theFile:
    reader = csv.DictReader(theFile)
    for line in reader:
        # line is { 'workers': 'w0', 'constant': 7.334, 'age': -1.406, ... }
        # e.g. print( line[ 'workers' ] ) yields 'w0'
        print("heyyyy")
        print(line)
        my_database = db_connection.cursor()
        sql_statement = "INSERT INTO contact (contact_id,fname,mname,lname) values(%s,%s,%s,%s)"
        values = (line['contact_id'], line['first_name'], line['middle_name'] , line['last_name'])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO address (contact_id,address_type,address,city,state,zip) values(%s,%s,%s,%s,%s,%s)"
        values = (line['contact_id'], 'Home Address', line['home_address'], line['home_city'], line['home_state'], line['home_zip'])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO address (contact_id,address_type,address,city,state,zip) values(%s,%s,%s,%s,%s,%s)"
        values = (line['contact_id'], 'Work Address',line['work_address'], line['work_city'], line['work_state'], line['work_zip'])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO phone (contact_id,phone_type,area_code,number) values(%s,%s,%s,%s)"
        values = (line['contact_id'], 'Home Phone', line['home_phone'][:3], line['home_phone'][4:7]+line['home_phone'][8:])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO phone (contact_id,phone_type,area_code,number) values(%s,%s,%s,%s)"
        values = (line['contact_id'], 'Cell Phone', line['cell_phone'][:3], line['cell_phone'][4:7]+line['cell_phone'][8:])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO phone (contact_id,phone_type,area_code,number) values(%s,%s,%s,%s)"
        values = (line['contact_id'], 'Work Phone', line['work_phone'][:3], line['work_phone'][4:7]+line['work_phone'][8:])
        my_database.execute(sql_statement, values)
        sql_statement = "INSERT INTO date (contact_id,date_type,date) values(%s,%s,%s)"
        values = (line['contact_id'], 'DOB', line['birth_date'])
        my_database.execute(sql_statement, values)
        db_connection.commit()
