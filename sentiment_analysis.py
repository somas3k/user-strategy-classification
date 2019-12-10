import json

from monkeylearn import MonkeyLearn
import pandas as pd
import numpy as np
from pandas import DataFrame


def calculate_sentiment(data):
    ml = MonkeyLearn('44f4b8a34bb91a70efb251025276838d7742795a')
    model_id = 'cl_pi3C7JiL'

    data = pd.read_json(data)
    result = []

    for i in range(0, data.size):
        res = extract_confidence(ml.classifiers.classify(model_id, [data[i]]))
        result.append(np.asarray(res))

    result = np.asarray(result)
    data['tag'] = result[:, 0]
    data['confidence'] = result[:, 1]
    return data.to_json(orient='records')




def extract_confidence(results):
    res = results.body[0]['classifications'][0]
    return [res['tag_name'],res['confidence']]






calculate_sentiment("")