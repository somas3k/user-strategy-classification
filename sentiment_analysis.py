import csv
import json

from monkeylearn import MonkeyLearn
import pandas as pd
import numpy as np



def calculate_sentiment(data):
    ml = MonkeyLearn('44f4b8a34bb91a70efb251025276838d7742795a')
    model_id = 'cl_pi3C7JiL'

    data = pd.read_json(data)
    result = []

    for i in range(0, data.shape[0]):
        res = extract_confidence(ml.classifiers.classify(model_id, [data['content'].values[i]]))
        result.append(np.asarray(res))

    result = np.asarray(result)
    data['tag'] = result[:, 0]
    data['confidence'] = result[:, 1]
    return data.to_json(orient='records')




def extract_confidence(results):
    res = results.body[0]['classifications'][0]
    return [res['tag_name'],res['confidence']]



def example_usage(file='./data/filtered_2.csv'):
    df = pd.read_csv(file)
    json_data=df.to_json(orient='records')
    calculate_sentiment(json_data)