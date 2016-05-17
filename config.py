# Credenciales de Mysql

MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'rootjf'
MYSQL_DATABASE_DB = 'inforuraldb'
MYSQL_DATABASE_HOST = 'localhost'

# Configuacion de sqlalchemy
SQLALCHEMY_DATABASE_URI = 'mysql://root:rootjf@localhost/inforuraldb'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "jf1002sdh90731"
SECRET_KEY = "jf1002sdh90731"
