from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hire_my_lawyer'
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def home_page():
    return render_template('lawyer_hiring.html')

@app.route('/clientRegistration', methods=['GET', 'POST'])
def client_registration():
    if request.method == 'POST':
        # Collect data from form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_no = request.form['contact_no']
        alternate_contact_no = request.form['alternate_contact_no']
        registration_date = request.form['registration_date']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert into users table
        cursor.execute('''
            INSERT INTO users (username, password, email, first_name, last_name, contact_no, alternate_contact_no, registration_date, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'client')
        ''', (username, password, email, first_name, last_name, contact_no, alternate_contact_no, registration_date))
        
        # Get the user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Insert into clients table
        cursor.execute('''
            INSERT INTO clients (user_id)
            VALUES (%s)
        ''', (user_id,))

        conn.commit()
        cursor.close()
        conn.close()

    return render_template('lawyer_hiring_Site_client_registration.html')

@app.route('/lawyerRegistration', methods=['GET', 'POST'])
def lawyer_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_no = request.form['contact_no']
        alternate_contact_no = request.form['alternate_contact_no']
        registration_date = request.form['registration_date']
        specialization = request.form['specialization']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert into users table
        cursor.execute('''
            INSERT INTO users (username, password, email, first_name, last_name, contact_no, alternate_contact_no, registration_date, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'lawyer')
        ''', (username, password, email, first_name, last_name, contact_no, alternate_contact_no, registration_date))
        
        # Get the user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Insert into lawyers table
        cursor.execute('''
            INSERT INTO lawyers (user_id, specialization)
            VALUES (%s, %s)
        ''', (user_id, specialization))

        conn.commit()
        cursor.close()
        conn.close()

    return render_template('lawyer_hiring_Site_lawyer_registration.html')

@app.route('/searchLawyer', methods=['GET'])
def search_lawyer():
    location = request.args.get('location')
    language = request.args.get('language')
    experience = request.args.get('experience')
    practice_area = request.args.get('practice_area')
    sort_by = request.args.get('sort_by')
    
    query = 'SELECT * FROM lawyers WHERE 1=1'
    params = []
    
    if location:
        query += ' AND location = %s'
        params.append(location)
    if language:
        query += ' AND languages_spoken LIKE %s'
        params.append(f'%{language}%')
    if experience:
        query += ' AND experience >= %s'
        params.append(experience)
    if practice_area:
        query += ' AND practice_area = %s'
        params.append(practice_area)
    
    if sort_by:
        query += ' ORDER BY ' + sort_by
    
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    lawyers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('searchLawyer.html', lawyers=lawyers)

if __name__ == "_main_":
    app.run(debug=True, port=8000)