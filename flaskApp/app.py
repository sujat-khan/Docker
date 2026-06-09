from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # This is our simple search box
    page_content = '''
        <h2>Multiplication Table</h2>
        <form method="POST">
            Enter a number: <input type="number" name="number" required>
            <input type="submit" value="Generate">
        </form>
        <hr>
    '''

    # If the user submitted a number, we generate the table
    if request.method == 'POST':
        number = int(request.form.get('number'))
        page_content += f"<h3>Table for {number}:</h3>"
        
        # Calculate and display 1 through 12
        for i in range(1, 13):
            page_content += f"{number} x {i} = {number * i} <br>"

    # Return everything directly to the browser
    return page_content

if __name__ == '__main__':
    app.run(debug=True)