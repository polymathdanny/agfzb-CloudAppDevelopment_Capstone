from __future__ import annotations
import requests
import json
# import related models here
from .models import CarDealer, DealerReview

#from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions



from requests.auth import HTTPBasicAuth

NLU_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/49b9c00d-0b2b-46f5-8fa7-eab33eb68c49'
NLU_API_KEY = 'ZIC1bWqSG8J_C3sr3ma1CDB5SSeNKxVu0CeB5nQuvEIv'

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print('GET from {} '.format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
        params=kwargs)
    except:
        # If any error occurs
        print('Network exception occurred')
    status_code = response.status_code
    print('With status {} '.format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    return requests.post(url, params=kwargs, json=json_payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    if 'dealerId' in kwargs or 'state' in kwargs:
        if 'dealerId' in kwargs:
            param = {'dealerId': kwargs['dealerId']}
        elif 'state' in kwargs:
            param = {'state': kwargs['state']} 
        json_result = get_request(url, **param)
    else:
        json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['body']['data']['docs']
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc.get('address'),
                                   city=dealer_doc.get('city'),
                                   full_name=dealer_doc.get('full_name'),
                                   id=dealer_doc.get('id'),
                                   lat=dealer_doc.get('lat'),
                                   long=dealer_doc.get('long'),
                                   short_name=dealer_doc.get('short_name'),
                                   st=dealer_doc.get('st'),
                                   state=dealer_doc.get('state'),
                                   zip=dealer_doc.get('zip'))
            results.append(dealer_obj)
    return results


# get_dealer_by_id
def get_dealer_by_id(url, dealerId):
    return get_dealers_from_cf(url, dealerId=dealerId)[0]


#get_dealers_by_state
def get_dealers_by_state(url, st):
    return get_dealers_from_cf(url, state=st)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        if 'error' in json_result['body']:
            return results
        # Get the row list in JSON as reviews
        reviews = json_result['body']['data']['docs']
        # For each review object
        for review_doc in reviews:
            review_text = review_doc['review']

            if review_text:
                sentiment = analyze_review_sentiments(review_doc['review'])
            else:
                sentiment = ''

            review_obj = DealerReview(car_make=review_doc.get('car_make'),
                                      car_model=review_doc.get('car_model'),
                                      car_year=review_doc.get('car_year'),
                                      dealership=review_doc.get('dealership'),
                                      id=review_doc.get('id'),
                                      name=review_doc.get('name'),
                                      purchase=review_doc.get('purchase'),
                                      purchase_date=review_doc.get('purchase_date'),
                                      review=review_doc.get('review'),
                                      sentiment=sentiment)
            results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator(NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    
    try:
        response = natural_language_understanding.analyze(text=text,
                                                        features=Features(sentiment=SentimentOptions(targets=[text]))
        ).get_result()
    
        label = json.dumps(response)
        label = response['sentiment']['document']['label']
    except:
        label = ''
        
    return(label)

