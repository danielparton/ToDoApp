import MySQLdb as mdb
import yaml

# ======
# Read MySQL user credentials from a configuration file
# ======

with open('config.yaml', 'r') as configfile:
    config_settings = yaml.load(configfile)
mysqlusername = config_settings['mysqlusername']
mysqlpassword = config_settings['mysqlpassword']


# ======
# Retrieve data
# ======

connection = mdb.connect('localhost', mysqlusername, mysqlpassword, 'python_test')

with connection:
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM todo_list")

    # column headers
    column_headers = cursor.description
    #print column_headers

    # fetch all rows
    rows = cursor.fetchall()
    for row in rows:
        #print row
        pass

    # may be unfeasible to fetch all rows
    # instead can fetch one row at a time
    #for i in range(cursor.rowcount):
    #    row = cursor.fetchone()
    #    print row[0], row[1]

    # the cursor class implements the iterator protocol, so this is another approach
    for row in cursor:
        #print row
        pass

    # this cursor returns rows as dicts
    cursor2 = connection.cursor(mdb.cursors.DictCursor)
    cursor2.execute("SELECT * FROM todo_list LIMIT 2") # use LIMIT to limit range of rows returned
    for row in cursor2:
        print row
