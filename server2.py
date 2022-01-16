import os
from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import jsonify
import numpy as np
import pandas as pd
import pickle
import io

app = Flask(__name__)
@app.route('/')
def hello():
    return render_template("index.html")

@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Crop Recommendation'
    return render_template('crop.html', title=title)
 
@ app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'Fertilizer Suggestion'

    return render_template('fertilizer.html', title=title) 

crop_recommendation_model_path = 'models/Stacking_crop_model.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

fertilizer_recommendation_model_path = 'models/Stacking_fertilizer_model.pkl'
fertilizer_recommendation_model = pickle.load(open(fertilizer_recommendation_model_path, 'rb'))
  
@ app.route('/fert-predict', methods=['POST'])
def fertilizer_prediction():
    title = 'Fertilizer Recommendation'
    #s_t={0: 'Black', 1: 'Clayey', 2: 'Loamy', 3: 'Red', 4: 'Sandy'}
    #c_t={0: 'Barley', 1: 'Cotton', 2: 'Ground Nuts', 3: 'Maize', 4: 'Millets',5: 'Oil seeds', 6: 'Paddy', 7: 'Pulses', 8: 'Sugarcane', 9: 'Tobacco', 10: 'Wheat'}
    f_t={0: '10-26-26', 1: '14-35-14', 2: '17-17-17', 3: '20-20', 4: '28-28', 5: 'DAP', 6: 'Urea'}
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        moisture = float(request.form['moisture'])
        temperature = float(request.form['temperature'])
        humidity= float(request.form['humidity'])
        soil_type=int(request.form['soiltype'])
        crop_type=int(request.form['croptype'])
        data = np.array([[temperature, humidity,moisture,soil_type,crop_type, N,K,P]])
        my_prediction = fertilizer_recommendation_model.predict(data)
        final_prediction = f_t[int(my_prediction)]
        return render_template('fert-result.html', prediction=final_prediction, title=title)


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Crop Recommendation'
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        humidity= float(request.form['humidity'])
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction
        return render_template('crop-result.html', prediction=final_prediction, title=title)

        
if __name__ == "__main__":
    app.run(debug=True)