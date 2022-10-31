# Database functions
from modules import *
globals().update(import_modules('home.database', globals()))


def db_create():
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command_0 = "DROP TABLE IF EXISTS signups, accounts, sessions, visitors, permissions CASCADE;"
    sql_command_1 = "CREATE TABLE IF NOT EXISTS signups (id SERIAL PRIMARY KEY, email VARCHAR(1000) UNIQUE, password VARCHAR(1000), url VARCHAR(1000) UNIQUE, timestamp NUMERIC(38, 10));"
    sql_command_2 = "CREATE TABLE IF NOT EXISTS accounts (id SERIAL PRIMARY KEY, email VARCHAR(1000) UNIQUE, password VARCHAR(1000), timestamp NUMERIC(38, 10));"
    sql_command_3 = "CREATE TABLE IF NOT EXISTS sessions (id SERIAL PRIMARY KEY, accounts_id INTEGER UNIQUE REFERENCES accounts(id), OTPP VARCHAR(1000), OTPP_session_id VARCHAR(1000) UNIQUE, OTPP_timestamp NUMERIC(38, 10), session_id VARCHAR(1000) UNIQUE, session_timestamp NUMERIC(38, 10), forgot_pass_url VARCHAR(1000) UNIQUE, forgot_pass_timestamp NUMERIC(38, 10));"
    sql_command_4 = "CREATE TABLE IF NOT EXISTS visitors (id SERIAL PRIMARY KEY, user_agent VARCHAR(1000), ip VARCHAR(1000), lang VARCHAR(1000), referer VARCHAR(1000), timestamp NUMERIC(38, 10), UNIQUE(user_agent, ip, lang, referer));"
    sql_command_5 = "CREATE TABLE IF NOT EXISTS permissions (id SERIAL PRIMARY KEY, accounts_id INTEGER UNIQUE REFERENCES accounts(id), admin VARCHAR(1000));"

    try:
        db.execute(sql_command_0)
        db.execute(sql_command_1)
        db.execute(sql_command_2)
        db.execute(sql_command_3)
        db.execute(sql_command_4)
        db.execute(sql_command_5)
        connection.commit()
    except:
        print('Could not reset the database.')
        connection.close()
        return

    connection.close()
    return


def db_sign_up(email, password, url):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    password = hashlib.sha256(password.encode()).hexdigest()
    timestamp = time.time()

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command = "INSERT INTO signups (email, password, url, timestamp) VALUES (%(email)s, %(password)s, %(url)s, %(timestamp)s);"
    parameters = {'email': email, 'password': password, 'url': url, 'timestamp': timestamp}

    try:
        db.execute(sql_command, parameters)
        connection.commit()
    except:
        print('Could not add email to database.')
        connection.close()
        return

    connection.close()
    return


def db_signed_up(email):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command = "SELECT COUNT(*) FROM signups WHERE email = %(email)s;"
    parameters = {'email': email}

    try:
        db.execute(sql_command, parameters)
        data = db.fetchall()
    except:
        print('Could not determine if email already exists.')
        connection.close()
        return False
    
    connection.close()

    if data[0][0] == 1:
        return True
    else:
        return False


def db_verify_email(url):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command_0 = "SELECT COUNT(*) FROM signups WHERE url = %(url)s;"
    parameters_0 = {'url': url}

    sql_command_1 = "SELECT email, password FROM signups WHERE url = %(url)s;"
    parameters_1 = {'url': url}

    try:
        db.execute(sql_command_0, parameters_0)
        data_0 = db.fetchall()
        if data_0[0][0] == 1:
            db.execute(sql_command_1, parameters_1)
            data = db.fetchall()
            email = data[0][0]
            password = data[0][1]
        else:
            connection.close()
            return
    except:
        print('Could not select email or password from url.')
        connection.close()
        return

    if db_account(email):
        connection.close()
        return

    timestamp = time.time()

    sql_command_2 = "INSERT INTO accounts (email, password, timestamp) VALUES (%(email)s, %(password)s, %(timestamp)s);"
    parameters_2 = {'email': email, 'password': password, 'timestamp': timestamp}

    sql_command_3 = "INSERT INTO sessions (accounts_id) SELECT id FROM accounts WHERE email = %(email)s;"
    parameters_3 = {'email': email}

    sql_command_4 = "INSERT INTO permissions (accounts_id) SELECT id FROM accounts WHERE email = %(email)s;"
    parameters_4 = {'email': email}

    try:
        db.execute(sql_command_2, parameters_2)
        connection.commit()
        db.execute(sql_command_3, parameters_3)
        connection.commit()
        db.execute(sql_command_4, parameters_4)
        connection.commit()
    except:
        print('Could not insert data into accounts and sessions tables.')
        connection.close()
        return
    
    connection.close()
    return


def db_forgot_pass(email):
    if db_account(email) == False:
        return

    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command = "SELECT forgot_pass_timestamp FROM sessions WHERE accounts_id = (SELECT id FROM accounts WHERE email = %(email)s);"
    parameters = {'email': email}

    try:
        db.execute(sql_command, parameters)
        data = db.fetchall()
    except:
        print('Could not get the forgot_pass_timestamp.')
        connection.close()
        return
    
    connection.close()

    if data[0][0] == None or Decimal(time.time()) - data[0][0] >= 86400:
        url = secret_url()
        timestamp = time.time()
        if send_reset_pass(email, url):
            DATABASE_URL = os.environ.get('DATABASE_URL')

            try:
                connection = psycopg2.connect(DATABASE_URL, sslmode='require')
                db = connection.cursor()
            except:
                print('Could not connect to database.')
                return

            sql_command = "UPDATE sessions SET forgot_pass_url = %(url)s, forgot_pass_timestamp = %(timestamp)s WHERE accounts_id = (SELECT id FROM accounts WHERE email = %(email)s);"
            parameters = {'url': url, 'timestamp': timestamp, 'email': email}

            try:
                db.execute(sql_command, parameters)
                connection.commit()
            except:
                print('Could not insert forgot_pass_url into database.')
                connection.close()
                return
            
            connection.close()

    return


def db_account(email):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command = "SELECT COUNT(*) FROM accounts WHERE email = %(email)s;"
    parameters = {'email': email}

    try:
        db.execute(sql_command, parameters)
        data = db.fetchall()
    except:
        print('Could not check if account exists.')
        connection.close()
        return False
    
    connection.close()

    if data[0][0] == 1:
        return True
    else:
        return False


def db_login(email, password):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    password = hashlib.sha256(password.encode()).hexdigest()

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command = "SELECT COUNT(*) FROM accounts WHERE email = %(email)s AND password = %(password)s;"
    parameters = {'email': email, 'password': password}

    try:
        db.execute(sql_command, parameters)
        data = db.fetchall()
    except:
        print('Could not login the user.')
        connection.close()
        return False
    
    connection.close()

    if data[0][0] == 1:
        return True
    else:
        return False


def db_send_OTPP(email):
    OTPP_session_id = secret_url()
    alphabet = (ascii_letters + digits + punctuation).replace(' ', '')
    OTPP = ''.join(choice(alphabet) for i in range(9))

    if send_OTPP_email(email, OTPP):
        DATABASE_URL = os.environ.get('DATABASE_URL')
        timestamp = time.time()

        try:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            db = connection.cursor()
        except:
            print('Could not connect to database.')
            return ''

        sql_command = "UPDATE sessions SET OTPP = %(OTPP)s, OTPP_session_id = %(OTPP_session_id)s, OTPP_timestamp = %(timestamp)s WHERE accounts_id = (SELECT id FROM accounts WHERE email = %(email)s);"
        parameters = {'OTPP': OTPP, 'OTPP_session_id': OTPP_session_id, 'timestamp': timestamp, 'email': email}

        try:
            db.execute(sql_command, parameters)
            connection.commit()
        except:
            print('Could not insert OTPP to database.')
            connection.close()
            return ''

        connection.close()
        return OTPP_session_id

    return ''


def db_OTPP_session_id(OTPP_session_id):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command_1 = "SELECT COUNT(*) FROM sessions WHERE OTPP_session_id = %(OTPP_session_id)s;"
    parameters_1 = {'OTPP_session_id': OTPP_session_id}

    sql_command_2 = "SELECT OTPP_timestamp FROM sessions WHERE OTPP_session_id = %(OTPP_session_id)s;"
    parameters_2 = {'OTPP_session_id': OTPP_session_id}

    try:
        db.execute(sql_command_1, parameters_1)
        data_1 = db.fetchall()
        if data_1[0][0] == 1:
            db.execute(sql_command_2, parameters_2)
            data_2 = db.fetchall()
    except:
        print('Could not check OTPP Session ID.')
        connection.close()
        return False
    
    connection.close()

    if data_1[0][0] == 1:
        if Decimal(time.time()) - data_2[0][0] <= 60:
            return True
        return False
    else:
        return False


def db_verify_OTPP(OTPP_session_id, OTPP, update = False, unverified = False):
    session_id = secret_url()
    timestamp = time.time()
    temp_OTPP_session_id = secret_url()
    alphabet = (ascii_letters + digits + punctuation).replace(' ', '')
    temp_OTPP = ''.join(choice(alphabet) for i in range(9))

    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return ''

    sql_command_1 = "SELECT COUNT(*) FROM sessions WHERE OTPP_session_id = %(OTPP_session_id)s AND OTPP = %(OTPP)s;"
    parameters_1 = {'OTPP_session_id': OTPP_session_id, 'OTPP': OTPP}

    sql_command_2 = "UPDATE sessions SET session_id = %(session_id)s, session_timestamp = %(timestamp)s WHERE OTPP_session_id = %(OTPP_session_id)s;"
    parameters_2 = {'session_id': session_id, 'timestamp': timestamp, 'OTPP_session_id': OTPP_session_id}

    sql_command_3 = "UPDATE sessions SET OTPP = %(temp_OTPP)s, OTPP_session_id = %(temp_OTPP_session_id)s WHERE OTPP_session_id = %(OTPP_session_id)s;"
    parameters_3 = {'temp_OTPP': temp_OTPP, 'temp_OTPP_session_id': temp_OTPP_session_id, 'OTPP_session_id': OTPP_session_id}

    try:
        if unverified:
            db.execute(sql_command_3, parameters_3)
            connection.commit()
            connection.close()
            return
        db.execute(sql_command_1, parameters_1)
        data = db.fetchall()
        if data[0][0] == 1 and update:
            db.execute(sql_command_2, parameters_2)
            connection.commit()
            db.execute(sql_command_3, parameters_3)
            connection.commit()
    except:
        print('Could not verify OTPP or insert new Session ID into database.')
        connection.close()
        return ''
    
    connection.close()

    if data[0][0] == 1:
        return session_id
    else:
        return ''


def db_pre_process(request):
    timestamp = time.time()
    SessionStore.clear_expired()

    user_agent = request.headers.get('User-Agent', '')
    ip = "{}:{}".format(request.headers.get('X-Forwarded-For', ''), request.headers.get('X-Forwarded-Port', ''))
    lang = request.headers.get('Accept-Language', '')
    referer = request.headers.get('Referer', os.environ.get('ORIGIN'))

    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command_0 = "SELECT COUNT(*) FROM visitors WHERE user_agent = %(user_agent)s AND ip = %(ip)s AND lang = %(lang)s AND referer = %(referer)s;"
    parameters_0 = {'user_agent': user_agent, 'ip': ip, 'lang': lang, 'referer': referer}

    sql_command_1 = "INSERT INTO visitors (user_agent, ip, lang, referer, timestamp) VALUES (%(user_agent)s, %(ip)s, %(lang)s, %(referer)s, %(timestamp)s);"
    parameters_1 = {'user_agent': user_agent, 'ip': ip, 'lang': lang, 'referer': referer, 'timestamp': timestamp}

    try:
        db.execute(sql_command_0, parameters_0)
        data = db.fetchall()
        if data[0][0] == 0:
            db.execute(sql_command_1, parameters_1)
            connection.commit()
    except:
        print('Could not insert visitor into database.')
        connection.close()
        return

    connection.close()
    return


def db_query():
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command = ""
    parameters = {}

    try:
        db.execute(sql_command, parameters)
        data = db.fetchall()
    except:
        print('Could not execute query.')
        connection.close()
        return

    connection.close()

    print(data)
    return


# db_create()


# db_query()

