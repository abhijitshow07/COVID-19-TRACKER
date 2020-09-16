# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:21:30 2020

@author: ABHIJIT SHOW
"""


from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, json, jsonify
import twitter
import get_news
import world
import time_series

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
@app.route('/home')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/india')
@cross_origin()
def india():
    return render_template('india.html')

@app.route('/index_graph')
@cross_origin()
def index_graph():
    return render_template('index_graph.html')

@app.route('/india_graph')
@cross_origin()
def india_graphs():
    return render_template('india_graph.html')

@app.route('/index_sentiment')
@cross_origin()
def global_sentiment():
    return render_template('index_sentiment.html')

@app.route('/india_sentiment')
@cross_origin()
def india_sentiment():
    return render_template('india_sentiment.html')

@app.route('/index_historical')
@cross_origin()
def index_historical():
    return render_template('index_historical.html')

@app.route('/index_predictions')
@cross_origin()
def index_predictions():
    return render_template('index_predictions.html')

@app.route('/india_predictions')
@cross_origin()
def india_predictions():
    return render_template('india_predictions.html')

@app.route('/get_tweets')
@cross_origin()
def get_tweets():
    return jsonify(twitter.tweet())

@app.route('/get_india_tweets')
@cross_origin()
def get_india_tweets():
    return jsonify(twitter.india_tweet())

@app.route('/get_index_news')
@cross_origin()
def fun_global_news():
    return jsonify(get_news.global_news())

@app.route('/get_india_news')
@cross_origin()
def fun_india_news():
    return jsonify(get_news.india_news())

@app.route('/index_news')
@cross_origin()
def index_news():
    return render_template('index_news.html')

@app.route('/india_news')
@cross_origin()
def india_news():
    return render_template('india_news.html')

@app.route('/about')
@cross_origin()
def about():
    return render_template('about.html')

@app.route('/get_country_list')
@cross_origin()
def get_country_list():
    return jsonify(world.read_country_list())

@app.route('/get_country_data',methods=["POST"])
@cross_origin()
def get_country_data():
    data=request.get_json(force = True)
    return jsonify(world.read_country_data(int(data["index"])))

@app.route('/get_world_original')
@cross_origin()
def get_world_original():
    return jsonify(world.world_original())

@app.route('/get_india_original',methods=["GET"])
@cross_origin()
def get_india_original():
    return jsonify(world.india_original())

@app.route('/get_world_predictions')
@cross_origin()
def get_world_predictions():
    return jsonify(world.world_fitted())

@app.route('/get_india_predictions')
@cross_origin()
def get_india_predictions():
    return jsonify(world.india_fitted())

@app.route('/update_india_world_pred')
@cross_origin()
def update_india_world_pred():
    world.india_world_pred()
    return jsonify("UPDATED")
    
@app.route('/update')
@cross_origin()
def update():
    world.country_wise()
    world.india_daily_cumulative()
    time_series.get_time_series()
    return jsonify("UPDATED")

@app.route('/update_news')
@cross_origin()
def update_news():
    get_news.news_audio_save()
    return jsonify("UPDATED")

@app.route('/read_world_time_series')
@cross_origin()
def read_world_time_series():
    with open('json_data/world_time_series.json') as file:
        world_time_series = json.load(file)
    return jsonify(world_time_series)

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000 ,threaded=True)
    #app.run(debug=True, port=5000 , use_reloader=False)  