from flask import Blueprint, request, jsonify, render_template

from flask import Flask, request, jsonify
from .utils.fetch_comments import fetch_comments
from .utils.analyze_sentiment import analyze_sentiment

import numpy as np
import pandas as pd

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/analyze_comments', methods=['GET'])
def analyze_comments():
    subfeddit = request.args.get('subfeddit')
    time_range = request.args.get('time_range', None)
    sort_by = request.args.get('sort_by', None)
    
    comments = fetch_comments(subfeddit)
    for comment in comments:
        polarity, classification = analyze_sentiment(comment['text'])
        comment['polarity'] = polarity
        comment['classification'] = classification
    
    if sort_by == 'polarity':
        comments.sort(key=lambda x: x['polarity'])
    
    return jsonify(comments)

'''
@bp.route('/results')
def show_results():
    # Sample data to pass to the template
    placement_prediction = 'Placement Prediction'
    container_prediction = 'Container Template Prediction'

    return render_template('result.html', placement_prediction=placement_prediction, container_prediction=container_prediction)


@bp.route('/predict_next_placement', methods=['POST'])
def predict_next_placement():
    # Get JSON data from POST request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request. Please provide input data.'}), 400
    
    # List of required fields in the data
    required_fields = ['pageContainers', 'pageWidth', 'pageHeight', 'replicaId', 'instance', 'getNextPlacementOnly', 'pageLeftTitle', 'pageRightTitle']

    # Check if each required field is in data
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Invalid request. Please provide {field} attribute.'}), 400      

    # TBD. check if the model is in the cache.
    # If not, load the model from disk and add it to the cache. Optionally, implement a cache eviction policy (like LRU) to remove least recently used models when the cache is full.
    # consider using a library like cachetools in Python to implement an LRU cache easily.

    placement_model, label_to_rectangle_mapping, rectangles_editable, env_model, env_canvas_orig  = load_placement_model(data)    
    container_model, container_model_category_encoder = load_container_model(data)
    
    container_category_page_left_encoded = container_model_category_encoder.transform([[data['pageLeftTitle']]])
    container_category_page_right_encoded = container_model_category_encoder.transform([[data['pageRightTitle']]])

    container_category_page_left_encoded_df = pd.DataFrame(container_category_page_left_encoded, columns=container_model_category_encoder.get_feature_names_out(['category']))
    container_category_page_right_encoded_df = pd.DataFrame(container_category_page_right_encoded, columns=container_model_category_encoder.get_feature_names_out(['category']))
    
    # Preprocess data
    env_model, env_canvas_orig = preprocess_input_placement(data, env_model, env_canvas_orig)    

    output = []
    make_single_prediction = int(float(data['getNextPlacementOnly'])) > 0
    page_width = int(float(data['pageWidth']))

    make_prediction = True    
    while make_prediction:
        # Make prediction
        model_input = env_model.canvas.flatten()[np.newaxis, :] 
        prediction = placement_model.predict([model_input])    

        # Postprocess prediction
        prediction, env_model, env_canvas_orig = postprocess_output_placement(prediction, label_to_rectangle_mapping, rectangles_editable, env_model, env_canvas_orig, make_single_prediction)

        # walk through prediction and add lyout_id key,value to each item
        for item in prediction:
            if item['x'] >= page_width:
                item_category = container_category_page_right_encoded_df
            else:
                item_category = container_category_page_left_encoded_df

            rect = [item['x'], item['y'], item['width'], item['height']]
            rect_df = pd.DataFrame([rect], columns=['x', 'y', 'width', 'height'])
            model_container_input = pd.concat([rect_df, item_category], axis=1)            

            # Get the probability of each class for each sample
            probabilities = container_model.predict_proba(model_container_input)

            # For the first sample, get the indices that would sort the probabilities
            sorted_indices = np.argsort(probabilities[0])[::-1] # [::-1] is used to sort in descending order

            # Get the top 5 class indices with highest probability
            top_5_indices = sorted_indices[:5]

            # Construct the list with dictionaries containing 'label' and 'prob'
            top_5_predictions = []
            for index in top_5_indices:
                # Getting the label
                if hasattr(container_model, 'classes_'):
                    label = container_model.classes_[index]
                else:
                    label = index

                # Getting the probability
                prob = probabilities[0, index]

                # Appending the dictionary to the list
                top_5_predictions.append({"id": str(label), "prob": f"{prob:.2f}"})           

            item['layout'] = top_5_predictions
        
        # Solange weitere Container platziert werden können, wird die Schleife fortgesetzt
        if len(prediction) > 0:        
            output.extend(prediction)
        else:
            make_prediction = False

        if make_single_prediction:
            break
   

    #print(output)

    return jsonify(output)
'''