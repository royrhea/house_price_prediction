from flask import Flask,request,jsonify
import util
app=Flask(__name__)
import datetime
from flask_cors import CORS

# ✅ Enable CORS globally
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200

@app.route("/")
def home():
    return "App is running"

@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response=jsonify({
        'locations':util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/predict_home_price',methods=['GET','post'])
def predict_home_price():
    total_sqft=float(request.form['total_sqft'])
    location=request.form['location']
    bhk=int(request.form['bhk'])
    bath=int(request.form['bath'])
    response=jsonify({
        'estimated_price': util.get_estimated_price(sqft=total_sqft, location=location,bhk=bhk,bath=bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__=="__main__":
    print("starting python flask server for home price prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)