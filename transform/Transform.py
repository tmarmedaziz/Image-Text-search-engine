import pickle
import requests
from io import BytesIO, StringIO
from PIL import Image
from feature_extractor import FeatureExtractor
import sys
sys.path.insert(0, r'C:\Users\moham\AIM\RTb\search-engine\transform')

source_no_vecs = ["ImageID", "Title", "AuthorID", "Tags", "OriginalURL"]

loaded_model = pickle.load(
    open(r"C:\Users\moham\AIM\RTb\search-engine\indexing\data\pca_model.pkl", 'rb'))

fe = FeatureExtractor()


def transform_image(img):
    return loaded_model.transform(fe.extract(img).reshape(1, -1))


def search_by_text_query(text):

    body = {
        "query": {
            "multi_match": {
                "fields":  ["Title", "Tags"],
                "query":     text,
                "fuzziness": "AUTO"
            }
        }
    }
# {"query" : {
#         "multi_match": {
#           "query": text,
#           "fields": ["Title", "Tags"]
#         }
#       }}

    r = requests.post('http://localhost:9200/open-images/_search', json=body)
    print(r)
    return r


def search_by_image_query(img, size=5):
    feature_vector = transform_image(img)
    query = {"query": {
        "elastiknn_nearest_neighbors": {
            "field": "featureVec",
            "vec": {"values": feature_vector[0].tolist()},

            "model": "exact",
            "similarity": "l2",
            "candidates": 150
        }
    }
    }
    r = requests.post('http://localhost:9200/open-images/_search', json=query)
    return r
