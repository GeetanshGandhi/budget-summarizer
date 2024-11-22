from flask import Flask, request
from flask_cors import CORS, cross_origin
#define key-value for each financial year
valueToPdfMap = {
    "2024-25":"2024_25",
    "2023-24":"2023_24",
    "2022-23":"2022_23",
    "2021-22":"2021_22",
    "2020-21":"2020_21",
    "2019-20":"2019_20",
    "2018-19":"2018_19",
    "2017-18":"2017_18",
    "2016-17":"2016_17"
    }
#create Flask server and configure CORS for cross origin
app = Flask(__name__)
CORS(app)
#create api on flask server
@app.route('/fetchSummary', methods=['POST'])
@cross_origin()
def getSummary():
    return open("E:/coding/WEB DEV/Budget_Summarizer/backend/Summaries/summary"+valueToPdfMap[request.get_json()]+".txt", "r").read()
app.run(debug = False)
