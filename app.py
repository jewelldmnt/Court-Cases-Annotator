from flask import Flask, render_template, request, redirect, url_for

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
        # For now, just print the data to the console
        print(f"Annotator: {annotator_name}")
        print(f"Court Case Link: {court_case_link}")
        print(f"Title: {title}")
        print(f"Court Case Text: {court_case_text}")
        print(f"Facts: {facts}")
        print(f"Issues: {issues}")
        print(f"Rulings: {rulings}")

        return redirect(url_for('index'))  # Redirect after submitting

    # Display the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
