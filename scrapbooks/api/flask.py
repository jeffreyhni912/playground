from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.route('/') #Sets up the default root, with temporary http link returning "home"
# def home():
#     return "Home" # => Return json response with the data

#=================================== MOST BASIC TUTORIAL ===============================#
##=============================== CREATING A GET ROUTE ===========================##
@app.route("/get-user/<user_id>") #user_id is path parameter that is a dynamic variable to pass into the url
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name":"John Doe",
        "email": "John.doe@example.com"
    }

    extra = request.args.get("extra") #Query parameter supported by get-user/123?{QUERY_PARAMETER}

    if extra: 
        user_data["extra"] = extra #Pass through "?extra=Hello" to return k -> extra, v-> Hello
        return jsonify(user_data), 200 #200 is default success code
    else:
        #In flask, create a dictionary and jsonify it to return the data
        return jsonify(user_data), 200 

## CONNECTION RETURNS
# http://{gateway}:{port}/get-user/123?extra=%22hello%22 
# {
#   "email": "John.doe@example.com",
#   "extra": "\"hello\"",
#   "name": "John Doe",
#   "user_id": "123"
# }
#================================ CREATING A POST ROUTE ============================ #
@app.route("/create-user", methods=["POST"]) #Specify the accepted methods, could technically add get as a potential request type
def create_user():
    #if request.method == "POST": #Could use filters like this to create paths, probably better practice to separate functions
    data = request.get_json()
    print('Successfully received post')
    print(data)
    return jsonify(data), 201 #201 default post success

## CONNECTION RETURNS
# http://{gateway}:{port}/create_user
# data returned -> {'email': 'Jane.doe@example.com', 'name': 'Jane Doe', 'user_id': '124'}

if __name__ == "__main__":
    app.run(debug=True)


