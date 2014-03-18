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
# Update MySQL database
# ======

connection = mdb.connect('localhost', mysqlusername, mysqlpassword, 'python_test')

with connection:
    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute("UPDATE todo_list SET complete='0' WHERE Id='1'")

