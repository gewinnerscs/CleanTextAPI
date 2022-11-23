import os
import re
import sqlite3 as sql
import pandas as pd
from flasgger import LazyJSONEncoder, LazyString, Swagger, swag_from
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API for Data Cleansing of Hate Speech created by Gewinner Sinaga'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'API Documentation for Data Cleaning of Hate Speech taken from both text and file'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)


@swag_from("docs/home.yml", methods=['GET'])
@app.route('/', methods=['GET'])
#Function for showing home page
def home():
     json_response = {
         'status_code': 200,
         'description': "API Text and File Cleansing",
     }
     response_data = jsonify(json_response)
     return response_data

@swag_from("docs/all_data.yml", methods=['GET'])
@app.route('/all_data', methods=['GET'])
#Function for showing all data from database
def database():
    connection = sql.connect('main.db')
    all_data = pd.read_sql('SELECT * from Tweet',connection)
    all_data = all_data.T.to_dict()
    return jsonify(
        all_data = all_data,
        status_code=200

    )

@swag_from("docs/text_clean.yml", methods=['POST'])
@app.route('/text_clean', methods=['POST'])
#Function for text cleaning from input text
def text_clean():
    text = request.form['raw_text']
    connection = sql.connect('main.db')
    #Clean text based on the abusive list
    #All abusive words in the text is cencored
    #abusive = pd.read_csv('abusive.csv')                              #read abusive.csv
    cursor = connection.cursor()
    abusive = pd.read_sql('select * from Abusive', connection)
    list_abusive = abusive['ABUSIVE'].to_list()                       #convert abusive.csv to list
    data_text = text.split()                                          #convert input text to list
    for dat_text in range(len(data_text)):                            #looping thorough input text list
        for abusive in range(len(list_abusive)):                      #looping thorough list_abusive to find matche words
            if list_abusive[abusive] == data_text[dat_text]:          #find match words between input text list and abusive list
                data_text[dat_text] = '*'*len(data_text[dat_text])    #subsitute matched words with * 
    cleaned_data = ' '.join(data_text)                                #convert to string

    #Clean text again based on kamusalaya.csv
    alay = pd.read_sql('select * from Kamus_alay', connection)        #read kamusalay from databse
    dict_alay = dict(alay.values)                                     #convert dataframe to dict
    cleaned_data = ' '.join(dict_alay.get(alay_word,alay_word) for alay_word in cleaned_data.split())   #find matched word from key, subsitute with values of dict and covert to string

    #Capitalize the text
    cleaned_data = cleaned_data.capitalize()
    #Remove character non-alphanumerical
    cleaned_data = re.sub(r'\\x[A-Za-z0-9./]+', '', cleaned_data)
    #Remove non-ASCII
    cleaned_data = re.sub(r'[^\x00-\x7F]+','', cleaned_data)
    #Remove new line from text in between 
    cleaned_data = re.sub(r'\\t|\\n|\\r|\t|\r|\n', '', cleaned_data)
    #Clean puctuation 
    cleaned_data = re.sub(r'[?:!;.,]','', cleaned_data)
    #Remove white space in the leading
    cleaned_data = cleaned_data.lstrip()
    #Remove white space in the trailing
    cleaned_data = cleaned_data.rstrip()
    #Remove multiple white space
    cleaned_data = re.sub(r'^\s+ | \s+$','', cleaned_data)

    raw_text = ''.join(text)
    clean_text = ''.join(cleaned_data)
    query = f"INSERT INTO Tweet (Raw_text, Clean_text) VALUES ('{text}','{cleaned_data}')"
    cursor.execute(query)
    connection.commit()

    #Return cleaned_data to jsonify
    return jsonify(
        raw_text=text,
        clean_text=cleaned_data,
        status_code=200
    )

@swag_from("docs/file_clean.yml", methods=['POST'])
@app.route('/file_clean', methods=['POST'])
#Function for file cleaning from file
def file_clean():
    connection = sql.connect('main.db')
    file      = request.files['data_file']                                                #Request data file from uploaded file
    file      = pd.read_csv(file, encoding='latin-1')
    #df_tweet = pd.read_sql('select * from Tweet', connection)                            #Read table from database (main.db)
    # Remove new line from text in between 
    re_tweet = file['Tweet'].str.replace(r'\\t|\\n|\\r|\t|\r|\n', '', regex=True)
    # Replace the number in the first sentence
    re_tweet = re_tweet.str.replace(r'^[0-9].','', regex=True)
    # Remove character non-alphanumerical
    re_tweet = re_tweet.str.replace(r'\\x[A-Za-z0-9./]+', '', regex=True)
    # Remove punctuation
    re_tweet = re_tweet.str.replace(r'[^\w\s]','', regex=True)
    # Remove link 
    re_tweet = re_tweet.str.replace('http[^\s]+|www.[^\s]+|@[^\s]+', '', regex=True)
    # Remove non-ASCII
    re_tweet = re_tweet.str.replace(r'[^\x00-\x7F]+','', regex=True)
    # Remove URL 
    re_tweet = re_tweet.str.replace(r'RT|URL',' ', regex=True)
    # Remove white space in the leading 
    re_tweet = re_tweet.str.lstrip()
    # Remove white space in the trailing
    re_tweet = re_tweet.str.rstrip()
    # Capitalize the text
    re_tweet = re_tweet.str.capitalize()
    # Remove multiple white space
    re_tweet = re_tweet.str.replace(r'^\s+ | \s+$','', regex=True)
    file_regex = re_tweet.to_frame('Raw_text')

    alay  = pd.read_sql('select * from Kamus_alay', connection)                             #Read kamusalay file using pandas format
    dict_alay = dict(alay.values)                                                           #Convert DataFrame format do dictionary

    raw_tweet = [file_regex['Raw_text'][raw].split() for raw in range(len(file_regex))]     #Convert each row to list
    abusive = pd.read_sql('select * from Abusive', connection)
    list_abusive = abusive['ABUSIVE'].to_list() 

    substitute_text =[]                                                                     #Make a list for substitute_text
    for tweet in range(len(raw_tweet)):                                                     #Looping thorough raw_text
        substitute_text.append([' '.join([dict_alay.get(item,item)for item in raw_tweet[tweet]])]) #Subsitute match word from dict_alay to the new_list and append to the list
    
    #Subsitute the matched words from abusive to the subsitute text
    cencored_text= []
    for text in range(len(substitute_text)):
        my_list = substitute_text[text][0].split()
        text_list = ' '.join(my_list)
        for tag in list_abusive:
            text_list = text_list.replace(tag, '*'*len(tag))
        cencored_text.append(text_list)

    #Convert list to the string
    tweet_dict = {"Raw_text":[],"Clean_text":[]}
    # tweet_dict_clean = {"Clean_text":[]}
    tweet_initial = file['Tweet']
    #Append the data to tweet_dict
    for i in range(len(cencored_text)):
        tweet_dict["Raw_text"].append(tweet_initial[i])
        tweet_dict["Clean_text"].append(''.join(cencored_text[i]))
    tweet_dict = pd.DataFrame(tweet_dict)
    tweet_dict.to_sql('Tweet', connection, if_exists='append', index=False)         #Append the data to database
    tweet_dict_final = tweet_dict.T.to_dict()

    return jsonify(
        clean_file=tweet_dict_final,
        status_code=200
    )


if __name__ == '__main__':
    app.run(debug=True)
