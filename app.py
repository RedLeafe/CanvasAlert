from flask import Flask, render_template

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the homepage ("/")
@app.route('/')
def hello_world():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
