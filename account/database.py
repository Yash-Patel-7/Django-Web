# Database functions
from modules import *
globals().update(import_modules('account.database', globals()))


def db_session_id(session_id):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command_1 = "SELECT COUNT(*) FROM sessions WHERE session_id = %(session_id)s;"
    parameters_1 = {'session_id': session_id}

    sql_command_2 = "SELECT session_timestamp FROM sessions WHERE session_id = %(session_id)s;"
    parameters_2 = {'session_id': session_id}

    try:
        db.execute(sql_command_1, parameters_1)
        data_1 = db.fetchall()
        if data_1[0][0] == 1:
            db.execute(sql_command_2, parameters_2)
            data_2 = db.fetchall()
    except:
        print('Could not check Session ID.')
        connection.close()
        return False
    
    connection.close()

    if data_1[0][0] == 1:
        if Decimal(time.time()) - data_2[0][0] <= 3600:
            return True
        return False
    else:
        return False


def allowed_reset_pass_url(url):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return False

    sql_command_1 = "SELECT COUNT(*) FROM sessions WHERE forgot_pass_url = %(url)s;"
    parameters_1 = {'url': url}

    sql_command_2 = "SELECT forgot_pass_timestamp FROM sessions WHERE forgot_pass_url = %(url)s;"
    parameters_2 = {'url': url}

    try:
        db.execute(sql_command_1, parameters_1)
        data_1 = db.fetchall()
        if data_1[0][0] == 1:
            db.execute(sql_command_2, parameters_2)
            data_2 = db.fetchall()
    except:
        print('Could not check allowed reset password urls.')
        connection.close()
        return False
    
    connection.close()

    if data_1[0][0] == 1:
        if Decimal(time.time()) - data_2[0][0] <= 86400:
            return True
        return False
    else:
        return False


def update_password(url, password):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    password = hashlib.sha256(password.encode()).hexdigest()
    temp_url = secret_url()

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command_1 = "UPDATE accounts SET password = %(password)s WHERE id = (SELECT accounts_id FROM sessions WHERE forgot_pass_url = %(url)s);"
    parameters_1 = {'password': password, 'url': url}

    sql_command_2 = "UPDATE sessions SET forgot_pass_url = %(temp_url)s WHERE forgot_pass_url = %(url)s;"
    parameters_2 = {'temp_url': temp_url, 'url': url}

    try:
        db.execute(sql_command_1, parameters_1)
        connection.commit()
        db.execute(sql_command_2, parameters_2)
        connection.commit()
    except:
        print('Could not update the password.')
        connection.close()
        return
    
    connection.close()
    return


def db_log_out(session_id):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    temp_session_id = secret_url()

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command = "UPDATE sessions SET session_id = %(temp_session_id)s WHERE session_id = %(session_id)s;"
    parameters = {'temp_session_id': temp_session_id, 'session_id': session_id}

    try:
        db.execute(sql_command, parameters)
        connection.commit()
    except:
        print('Could not log out.')
        connection.close()
        return
    
    connection.close()
    return


def db_admin(email, give_or_revoke):
    if type(email) is not str:
        return
    if type(give_or_revoke) is not bool:
        return
    
    if give_or_revoke == True:
        value = 'True'
    else:
        value = None

    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return

    sql_command = "UPDATE permissions SET admin = %(value)s WHERE accounts_id = (SELECT id FROM accounts WHERE email = %(email)s);"
    parameters = {'value': value, 'email': email}

    try:
        db.execute(sql_command, parameters)
        connection.commit()
    except:
        print('Could not give admin permissions.')
        connection.close()
        return
    
    connection.close()
    return


def db_permissions(session_id):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        db = connection.cursor()
    except:
        print('Could not connect to database.')
        return {}

    sql_command = "SELECT admin FROM permissions WHERE accounts_id = (SELECT accounts_id FROM sessions WHERE session_id = %(session_id)s);"
    parameters = {'session_id': session_id}

    try:
        db.execute(sql_command, parameters)
        permissions = db.fetchall()
    except:
        print('Could not get permissions for account.')
        connection.close()
        return {}
    
    connection.close()

    return {
        'admin': permissions[0][0],
    }

