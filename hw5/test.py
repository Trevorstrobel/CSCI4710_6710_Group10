from string import Template

def getGroup(groupNum, country = None):
   
    
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
    if (country != None):
        countryStr = Template(" AND country = '$country'")
        SQL_QUERY = SQL_QUERY + countryStr.substitute(country = country)

    SQL_QUERY = SQL_QUERY + ";"

    #cur.execute(SQL_QUERY)
    
    print(SQL_QUERY)


getGroup(1, 'Guatemala')
