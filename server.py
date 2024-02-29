from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from router import Router  
from database.database import Database
import json
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '2WVVDhxz5k%$29f#4^4c4VtP65BvC4t8'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=240) 
jwt = JWTManager(app)

contact_points = ['localhost']
keyspace = 'colab'
database = Database(contact_points, keyspace)
router = Router(database)
    
@app.route('/add_brand', methods=['POST']) #brand
def add_brand():
    try:
        data = request.json
        email = data['email']
        phone = data['phone']
        brand_name = data['brand_name']
        username = data['username']
        password = data['password']
        description = data['description']
        response = router.add_brand(email, phone, brand_name, username, password, description)
        return {"STATUS": 402, "DESCRIPTION": "succesfully registered brand", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e),"RESPONSE": "FAILED"}
    
@app.route('/add_influencer', methods=['POST']) 
def add_influencer():
    try:
        data = request.json
        email = data['email']
        phone = data['phone']
        username = data['username']
        password = data['password']
        bio = data['bio']
        dob = data['dob']
        location = data['location']
        professional_description = data['professional_description']
        response = router.add_influencer(email, phone, username, password, bio, location, dob, professional_description)
        return {"STATUS": 402, "DESCRIPTION": "succesfully registered influencer", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e),"RESPONSE": "FAILED"}
    
@app.route('/verify_email', methods=['GET']) 
def verify_email():
    try:
        token = request.args.get('token')
        router.verify_email(token)
        return {"STATUS": 402, "DESCRIPTION": "succesfully veified email"}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e),"RESPONSE": "could not verify email"}


@app.route('/login', methods=['POST']) #brand and influencer
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        is_brand = router.is_brand(email)
        if (router.login(email, password, is_brand)):
            access_token = create_access_token(identity=email)
            return {"STATUS": 402, "RESPONSE": "Logged in Successfully", "ACCESS_TOKEN": access_token, "is_brand": is_brand}
        raise Exception()
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
        # return {"STATUS": 302, "DESCRIPTION": "Invalid Credentials", "RESPONSE": "FAILED"}

# @app.route('/modify_user', methods=['PUT'])
# @jwt_required()
# def modify_user():
#     data = request.get_json()
#     email = get_jwt_identity()
#     result = router.modify_user(data)
#     return jsonify(result)

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        email = get_jwt_identity()
        response = router.logout(email)
        unset_jwt_cookies(jsonify({"STATUS": 402, "DESCRIPTION": "successfully logged out"}))
        return jsonify({"STATUS": 402, "DESCRIPTION": "successfully logged out"})
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

@app.route('/add_handle', methods=['POST']) 
@jwt_required()
def add_handle():
    try:
        data = request.json
        handle = data.get('handle')
        username = data.get('username')
        email = get_jwt_identity()
        if router.is_brand(email):
            raise Exception("Brands dont have handles as of yet")
        response = router.add_handle(email, handle, username)
        return {"STATUS": 402, "DESCRIPTION": "succesfully added handle", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e),"RESPONSE": "FAILED"}

@app.route('/get_user_profile_details', methods=['GET'])
@jwt_required()
def get_user_profile_details():
    try:
        email = get_jwt_identity()
        if router.is_brand(email):
            raise Exception("Brands dont have user profile details as of yet")
        response = router.get_user_profile_details(email)
        return {"STATUS": 402, "DESCRIPTION": "succesfully fetched profile", "RESPONSE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
    
#######################################################################################
#######################################################################################

@app.route('/cash_in', methods=['POST'])
@jwt_required()
def cash_in():
    try:
        data = request.get_json()
        amount = data.get('amount')
        email = get_jwt_identity()
        assert(amount > 0)
        response = router.cash_in(email, amount)
        return {"STATUS": 402, "DESCRIPTION": "succesfully cashed in", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
    
@app.route('/add_payment_gateway', methods=['POST'])
@jwt_required()
def add_payment_gateway():
    try:
        data = request.get_json()
        gate_way_type = data.get('gate_way_type')
        account_number = data.get('account_number')
        account_holder_name = data.get('account_holder_name')
        mobile_number = data.get('mobile_number')
        email = get_jwt_identity()
        response = router.add_payment_gateway(email, gate_way_type, account_number, account_holder_name, mobile_number)
        return {"STATUS": 402, "DESCRIPTION": "succesfully added gateway", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
    
@app.route('/cash_out', methods=['POST'])
@jwt_required()
def cash_out():
    try:
        data = request.get_json()
        amount = data.get('amount')
        assert(amount > 0)
        email = get_jwt_identity()
        response = router.cash_out(email, amount)
        return {"STATUS": 402, "DESCRIPTION": "succesfully cashed out", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

@app.route('/check_balance', methods=['GET'])
@jwt_required()
def check_balance():
    try:
        email = get_jwt_identity()
        response = router.check_balance(email)
        return {"STATUS": 402, "DESCRIPTION": "succesfully fetched balance", "RESPONSE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
    
#######################################################################################
#######################################################################################

@app.route('/add_job', methods=['POST'])
@jwt_required()
def add_job():
    try:
        data = request.get_json()
        title = data.get('title')
        minimum_followers = data.get('minimum_followers')
        influence_threshold = data.get('influence_threshold')
        keywords = data.get('keywords')
        count = data.get('count')
        deadline = data.get('deadline')
        location = data.get('location')
        bid = data.get('bid')
        job_code = data.get('job_code')
        email = get_jwt_identity()
        if not router.is_brand(email):
            raise Exception("Influencers cannot add jobs")
        response = router.add_job(email, title, minimum_followers, influence_threshold, keywords, count, deadline, location, bid, job_code)
        return {"STATUS": 402, "DESCRIPTION": "succesfully added campaign", "RESPONSE": str(response)}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

@app.route('/get_jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    try:
        email = get_jwt_identity()
        if router.is_brand(email):
            raise Exception("Sign in as influencer to get jobs")
        response = router.get_jobs(email)
        return {"STATUS": 402, "DESCRIPTION": "succesfully fetched eligible campaigns", "RESPONSE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

@app.route('/get_all_jobs', methods=['GET'])
def get_all_jobs():
    try:
        response = router.get_all_jobs()
        return {"STATUS": 402, "DESCRIPTION": "succesfully fetched all campaigns", "RESPONSE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

@app.route('/test_eligibility', methods=['POST'])
@jwt_required()
def test_eligibility():
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        caption = data.get('caption')
        image = data.get('image')
        email = get_jwt_identity()
        if router.is_brand(email):
            raise Exception("Brands cannot test for eligibility")
        response = router.test_eligibility(job_id, caption, image)
        return {"STATUS": 402, "DESCRIPTION": "PASSED FOR ELIGIBILITY", "RESPONSE": "SUCCESS", "MAGNITUDE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}
    
@app.route('/apply_job', methods=['POST'])
@jwt_required()
def apply_job():
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        email = get_jwt_identity()
        if router.is_brand(email):
            raise Exception("Brands cannot apply for jobs")
        response = router.apply_job(email, job_id)
        return {"STATUS": 402, "DESCRIPTION": "succesfully completed job", "RESPONSE": response}
    except Exception as e:
        return {"STATUS": 302, "DESCRIPTION": str(e), "RESPONSE": "FAILED"}

# @app.route('/check_status', methods=['GET'])
# def check_status():
#     user_id = request.args.get('user_id')
#     result = router.check_status(user_id)
#     return jsonify(result)

# @app.route('/get_brands', methods=['GET'])
# def get_brands():
#     result = router.get_brands()
#     return jsonify(result)

# @app.route('/get_influencers', methods=['GET'])
# def get_influencers():
#     result = router.get_influencers()
#     return jsonify(result)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, threaded=True)
    app.run(host='0.0.0.0', port=5000)
