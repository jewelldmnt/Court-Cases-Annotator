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
    

if __name__ == '__main__':
    app.run(debug=True)
