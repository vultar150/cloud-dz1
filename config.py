from flaskext.mysql import MySQL
from flask import Flask

app = Flask(__name__)
app.secret_key = "secret key"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'foo'
app.config['MYSQL_DATABASE_PASSWORD'] = '4060'
app.config['MYSQL_DATABASE_DB'] = 'StudentList'
app.config['MYSQL_DATABASE_HOST'] = '10.66.66.1'
mysql.init_app(app)
