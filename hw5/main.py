# Authors:          Trevor Strobel, Malcolm Flaherty
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

@app.route('/')
def index():
    conn = connect()
    cur = conn.cursor()
    
    COUNTRIES = "SELECT DISTINCT country FROM not_alone;"
    cur.execute(COUNTRIES)
    countries = cur.fetchall()

    subGroups = []

    #Split data into 4 groups based on age and gender
    #group 1
    GROUP_1 = "CREATE TABLE group_1 AS (SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Male');"
    
    cur.execute(GROUP_1)

    #group 2
    GROUP_2 = "CREATE TABLE group_2 AS (SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Male');"

    cur.execute(GROUP_2)

    #group 3
    GROUP_3 = "CREATE TABLE group_3 AS (SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Female');"

    cur.execute(GROUP_3)

    #group 4
    GROUP_4 = "CREATE TABLE group_4 AS (SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Female');"

    cur.execute(GROUP_4)
    
    #split each group into smaller groups based on country and size
    for x in range(1,5):
        for row in countries:
            #drop TEMP table from pervious loop cycle
            cur.execute("DROP TABLE IF EXISTS TEMP;")

            #create table to store current subgroup in
            group = "GROUP_" + str(x)
            country = row[0]
            TEMP = "CREATE TABLE TEMP AS (SELECT * FROM " + group + " WHERE country = '" + country + "');"
            TEMPROWS = "SELECT * FROM TEMP;"
            cur.execute(TEMP)

            #get number of rows in table, to make sure subgroup is not empty
            cur.execute("SELECT COUNT(*) FROM TEMP;")
            rowCount = cur.fetchone()[0]

            #check if subgroup is empty
            if rowCount > 0:
                #if current country has more than 10 entries, split using kmeans
                cur.execute(TEMPROWS)
                subGroup = cur.fetchall()
                if rowCount >= 10:
                    labels = util.cluster_user_data(subGroup)
        
                    splitGroup = util.split_user_data(subGroup, labels)

                    for y in splitGroup:
                         subGroups.append(y)
                else:
                    subGroups.append(subGroup)

    #pass groups to index.html
    return render_template('index.html', subGroups = subGroups, countries = countries, column_html = column_names)

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



