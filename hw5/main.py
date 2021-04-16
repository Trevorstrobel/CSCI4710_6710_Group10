# Author:           Trevor Strobel
# Date:             4/9/2021
# Assn:             Hw 5

from flask import Flask, request, render_template
import psycopg2
import csv
from string import Template
import util

# create a Flask instance
app = Flask(__name__)

#Database Variables
connInfo = "host=localhost dbname=hw5db user=admin5 password='web_apps'"

#SQL Strings
SQL_TABLE_CREATE = "CREATE TABLE not_alone (	Index INT ,	Country VARCHAR(20) ,	Age INT ,	Gender VARCHAR(30) ,	Fear INT ,	Anxiety INT , Angry INT, Happy INT , Sad INT , Which_Emotion TEXT , Feel TEXT , Most_Meaning TEXT , Occupation TEXT ,  	PRIMARY KEY (Index));"

column_names = ["index","What country do you live in?","How old are you?","What is your gender?","To what extent do you feel FEAR due to the coronavirus?","To what extent do you feel ANXIOUS due to the coronavirus?","To what extent do you feel ANGRY due to the coronavirus?","To what extent do you feel HAPPY due to the coronavirus?","To what extent do you feel SAD due to the coronavirus?","Which emotion is having the biggest impact on you?","What makes you feel that way?","What brings you the most meaning during the coronavirus outbreak?","What is your occupation?"]

#database connection
def connect():
    c = psycopg2.connect(connInfo)
    return c

#create database table
def createTable():
    #creates a connection to the database
    conn = connect()
    #creates a cursor for the db
    cur = conn.cursor()

    #drops table if it exists
    cur.execute("DROP TABLE IF EXISTS not_alone;")
    print("table dropped")
    conn.commit()

    #creates the table
    cur.execute(SQL_TABLE_CREATE)
    conn.commit()

    #read info from csv and insert into database

    with open('we_are_not_alone_no_nan.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) #skips first row of csv file
        
        for row in reader:
            cur.execute("INSERT INTO not_alone VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
            #if(len(row) > 13):
            #    print(row)


    #commit changes to the db
    conn.commit()
    conn.close()



#This route returns all unique countries in the DB.
@app.route('/getCountries')
def getCountries():
    conn = connect()
    cur = conn.cursor()

    SQL_QUERY = "SELECT DISTINCT country FROM not_alone;"

    cur.execute(SQL_QUERY)
    return cur.fetchall()

#this one route is able to take care of all needed requests. 
# specify the group number and optionally, a country. 
@app.route('/getGroup/<int:groupNum>/<string:country>')
def getGroup(groupNum, country = ""):
    conn = connect()
    cur = conn.cursor()
    
    #chooses the correct variables for SQL query
    
    age = None
    gender = None
    opsList = [">= 36", "<= 35", "Male", "Female"]

    if(groupNum % 2 == 0):
        age = opsList[0]
    else:
        age = opsList[1]

    if(groupNum < 3 ):
        gender = opsList[2]
    else:
        gender = opsList[3]

    SQL_QUERY = Template("SELECT * FROM not_alone WHERE age $age AND gender = '$gender'")
    

    SQL_QUERY = SQL_QUERY.substitute(age = age, gender = gender)

    #if country is specified, add that qualifier to the string
    if (country != ""):
        countryStr = Template(" AND country LIKE '$country'")
        SQL_QUERY = SQL_QUERY + countryStr.substitute(country = country)

    #add the line terminator
    SQL_QUERY = SQL_QUERY + ";"

    #execute and return the query results
    cur.execute(SQL_QUERY)
    data = cur.fetchall()
    
    #if data returned is greater than 10 entries, split it into 3 groups using the 
    # functions from util
    if(len(data) > 10):
        labels = util.cluster_user_data(data)
        
        data = util.split_user_data(data, labels)
        
    return data



        
        

@app.route('/')
def index():
    conn = connect()
    cur = conn.cursor()
    
    COUNTRIES = "SELECT DISTINCT country FROM not_alone";
    subGroups = []

    #Split data into 4 groups based on age and gender
    #group 1
    GROUP_1 = Template("SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Male'") 

    GROUP_1 = GROUP_1.substitute()
    GROUP_1 = GROUP_1 + ";"

    cur.execute(GROUP_1)
    group1 = cur.fetchall()

    #group 2
    GROUP_2 = Template("SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Male'") 

    GROUP_2 = GROUP_2.substitute()
    GROUP_2 = GROUP_2 + ";"

    cur.execute(GROUP_2)
    group2 = cur.fetchall()

    #group 3
    GROUP_3 = Template("SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Female'") 

    GROUP_3 = GROUP_3.substitute()
    GROUP_3 = GROUP_3 + ";"

    cur.execute(GROUP_3)
    group3 = cur.fetchall()

    #group 4
    GROUP_4 = Template("SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Female'") 

    GROUP_4 = GROUP_4.substitute()
    GROUP_4 = GROUP_4 + ";"

    cur.execute(GROUP_4)
    group4 = cur.fetchall()
    
    #split each group into smaller groups based on country and size
    for x in range(1,4):
        for row in COUNTRIES:
            #Getting a "relation GROUP_1 does not exist" error here... not sure why
            group = "GROUP_" + str(x)
            TEMP = "SELECT * FROM " + group + " WHERE country = '$country';"

            #TODO: check if current country has more than 10 entries and split using kmeans functions if it does.

            cur.execute(TEMP)
            subGroup = cur.fetchall()
            subGroups.append(subGroup)


    #pass groups to index.html
    return render_template('index.html', subGroups = subGroups, column_html = column_names)

# default page for 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404_error.html'), 404

# default page for 500 error
@app.errorhandler(500)
def server_error(e):
	print(e)
	return render_template('500_error.html'), 500

@app.route('/test_500')
def fake_function():
	'''
	Need to test this when debug mode is off
	'''
	a = v * 5
	return a

if __name__ == '__main__':
# app.debug = True
    #create and populate table
    createTable()
    ip = '127.0.0.1'
    app.run(host=ip)


