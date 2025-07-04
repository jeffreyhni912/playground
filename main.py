from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/') #Sets up the default root, with temporary http link returning "home"
def home():
    return "Home" # => Return json response with the data


if __name__ == "__main__":
    app.run(debug=True)

    ## Application test goals:
    ## 1) Create and manage a database of successful/failed application runs
    ## 2) Create an API endpoint which can run scripts which will "do" something
    ## 3) Add an authentication system (either SSO or another) to restrict connections to people allowed
