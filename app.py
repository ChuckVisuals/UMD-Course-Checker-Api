from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

#base route to check if the API is online
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'API ONLINE!'})


#Gets the seat count for any class 
#Params1 class_name: the class name (e.g. CMSC131)
#Prams2 section_id: the section id (e.g. 0101)
@app.route('/getSeatCount', methods=['GET'])
def get_seats():
    class_name = request.args.get('class_name')
    section_id = request.args.get('section_id')
    
    if not class_name or not section_id:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    url = f'https://app.testudo.umd.edu/soc/search?courseId={class_name.upper()}&sectionId=&termId=202408&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on'

    result = requests.get(url)
    filtered_divs = []

    doc = BeautifulSoup(result.text ,"html.parser")
    #print(doc.prettify())
    divs = doc.find_all('div', class_=['section delivery-f2f','section delivery-online','section delivery-blended'])

    for div in divs:
        span = div.find('span', class_='section-id')
        if span and span.text.strip() == section_id:
            filtered_divs.append(div)
            seat_span = div.find('span', class_='open-seats-count')
            if seat_span:
                return jsonify({'open_seats': int(seat_span.text.strip())})
            
    return jsonify({'error': 'Section not found'}), 404


@app.route('/sendEmailOnRegistar', methods=['POST'])
def sendEmailOnRegistar():
    email = request.args.get('email')
    name = request.args.get('name')
    
    if not email or not name:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    #testing getting data from the request
    print(email, name)
    return 200
    