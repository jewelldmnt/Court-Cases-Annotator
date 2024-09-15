from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        annotator_name = request.form['annotator_name']
        court_case_link = request.form['court_case_link']
        title = request.form['title']
        court_case_text = request.form['court_case_text']
        facts = request.form['facts']
        issues = request.form['issues']
        rulings = request.form['rulings']

        # Process or save the form data
        court_case_data = {
            'annotator':annotator_name,
            'link':court_case_link,
            'title':title,
            'whole text':court_case_text,
            'facts':facts,
            'issues':issues,
            'rulings':rulings
        }

        store_data(court_case_data)

        return redirect(url_for('index'))  # Redirect after submitting

    # Display the form
    return render_template('index.html', count=annotator_count())

def annotator_count():
    create_table_if_not_exists()

    # create connection
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()

    print("connection made")

    court_query = cursor.execute("SELECT COUNT(annotator), annotator FROM CourtCases GROUP BY annotator")
    court_data = court_query.fetchall()

    print("fetching done")

    # commit changes and close database connect
    conn.commit()
    conn.close()

    return court_data

def create_table_if_not_exists():
    # create connection
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    
    # create table if not exists
    cursor.execute("""CREATE TABLE IF NOT EXISTS CourtCases (
    court_id INT NOT NULL,
    annotator VARCHAR(30),
    link TEXT,
    title TEXT, 
    whole_text TEXT,
    facts TEXT,
    issues TEXT,
    ruling TEXT,
    PRIMARY KEY(court_id)
    )""")

    # commit changes and close database connect
    conn.commit()
    conn.close()

def store_data(court_case_data):
    # create connection
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()

    court_query = cursor.execute("SELECT MAX(court_id) FROM CourtCases")
    court_data = court_query.fetchone()

    if not court_data[0]:
        court_id = 1
    else:
        print(court_data)
        court_id = court_data[0] + 1


    # store values to database
    cursor.execute("""INSERT INTO CourtCases (court_id, annotator, link, title, whole_text, facts, issues, ruling) 
              VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (court_id, court_case_data['annotator'], court_case_data['link'], court_case_data['title'], 
                                 court_case_data['whole text'], court_case_data['facts'], court_case_data['issues'], 
                                 court_case_data['rulings']))

    # commit changes and close database connect
    conn.commit()
    conn.close()

# Route for viewing cases
@app.route('/view_cases', methods=['GET', 'POST'])
def view_cases():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        court_cases = search_cases(search_term)
    else:
        court_cases = get_all_cases()

    return render_template('view_cases.html', court_cases=court_cases)

# Route for editing a case
@app.route('/edit_case/<int:case_id>', methods=['GET', 'POST'])
def edit_case(case_id):
    if request.method == 'POST':
        annotator_name = request.form['annotator_name']
        court_case_link = request.form['court_case_link']
        title = request.form['title']
        court_case_text = request.form['court_case_text']
        facts = request.form['facts']
        issues = request.form['issues']
        rulings = request.form['rulings']

        update_case(case_id, annotator_name, court_case_link, title, court_case_text, facts, issues, rulings)
        return redirect(url_for('view_cases'))

    case = get_case_by_id(case_id)
    return render_template('edit_case.html', case=case)

# Route for deleting a case
@app.route('/delete_case/<int:case_id>', methods=['POST'])
def delete_case(case_id):
    delete_case_by_id(case_id)
    return redirect(url_for('view_cases'))

# Function to get all cases
def get_all_cases():
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CourtCases")
    cases = cursor.fetchall()
    conn.close()
    return cases

# Function to search cases
def search_cases(search_term):
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CourtCases WHERE title LIKE ? OR whole_text LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    cases = cursor.fetchall()
    conn.close()
    return cases

# Function to get a case by ID
def get_case_by_id(case_id):
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CourtCases WHERE court_id = ?", (case_id,))
    case = cursor.fetchone()
    conn.close()
    return case

# Function to update a case
def update_case(case_id, annotator_name, court_case_link, title, court_case_text, facts, issues, rulings):
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CourtCases
        SET annotator = ?, link = ?, title = ?, whole_text = ?, facts = ?, issues = ?, ruling = ?
        WHERE court_id = ?
    """, (annotator_name, court_case_link, title, court_case_text, facts, issues, rulings, case_id))
    conn.commit()
    conn.close()

# Function to delete a case by ID
def delete_case_by_id(case_id):
    conn = sqlite3.connect('court_cases.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CourtCases WHERE court_id = ?", (case_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
