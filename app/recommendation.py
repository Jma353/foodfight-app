import os
import base64
import json
import urllib2
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import defaultdict
from collections import Counter
from numpy import linalg as LA
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import operator
from operator import itemgetter
import io
import math

def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.

    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct


# EVERYTHING ELSE FOR NOW WILL BE IN LOCAL MODE... PLEASE PUSH TO S3 WHEN YOU CAN 
file1 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_name_to_id.json')
file2 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_bus_index_to_name.json')
file3 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_bus_name_to_index.json')
file4 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_bus_compressed.json')
file5 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_features_compressed.json')
file6 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/index_to_vocab_arizona.json')
file7 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/vocab_to_index_arizona.json')
file8 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/inv_index_arizona.json')
file9 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/cat_inv_index_arizona.json')
file10 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_bus_location.json')
file11 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_categories.json')
file12 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_features.json')


bus_name_to_id = json.load(file1,encoding='utf8')
bus_index_to_name = json.load(file2,encoding='utf8')
bus_name_to_index = json.load(file3,encoding='utf8')
bus_compressed = json.load(file4, object_hook=json_numpy_obj_hook, encoding='utf8')
features_compressed = json.load(file5, object_hook=json_numpy_obj_hook, encoding='utf8') ## 11mb
index_to_vocab = json.load(file6,encoding='utf8')
vocab_to_index = json.load(file7,encoding='utf8')
inv_index = json.load(file8, object_hook=json_numpy_obj_hook, encoding='utf8')
cat_inv_index = json.load(file9, object_hook=json_numpy_obj_hook, encoding='utf8')
bus_location = json.load(file10,encoding='utf8')
arizona_categories = json.load(file11,encoding='utf8')
arizona_features = json.load(file12,encoding='utf8')

def rocchio(q, relevant,irrelevant,a=.3, b=.3, c=.8, clip = True):
    '''
    Arguments:
        query: a string representing the name of the beer being queried for
        
        relevant: a list of strings representing the names of relevant beers for query
        
        irrelevant: a list of strings representing the names of irrelevant beers for query
        
        a,b,c: floats, corresponding to the weighting of the original query, relevant queries,
        and irrelevant queries, respectively.
        
        clip: boolean, whether or not to clip all returned negative values to 0
        
    Returns:
        q_mod: a vector representing the modified query vector. this vector should have no negatve
        weights in it!
    '''
    bus_vector = bus_compressed[bus_name_to_index[q],:]
    relevant_vectors = [bus_compressed[bus_name_to_index[x],:] for x in relevant] 
    relevant_vector = sum(x for x in relevant_vectors)
    irrelevant_vectors =[bus_compressed[bus_name_to_index[x],:] for x in irrelevant]  
    irrelevant_vector = sum(x for x in irrelevant_vectors)
    first_term = (a*bus_vector)
    if not relevant:
        second_term = 0
    else:
        second_term = ((b*relevant_vector)/(len(set(relevant))))
    if not irrelevant:
        third_term = 0
    else:
        third_term = ((c*irrelevant_vector)/(len(set(irrelevant))))

    if clip:
        final = (first_term + second_term - third_term).clip(min=0)
    else:
        final = (first_term + second_term - third_term)
    return final

def bus_recommender(q, releveant, disliked):
    query_vector = rocchio(q,releveant,disliked)
    sims = (np.dot(bus_compressed,query_vector))/(LA.norm(bus_compressed)* LA.norm(query_vector))
    asort = np.argsort(-sims)
    result = []
    for i in asort[1:]:
        if bus_index_to_name[i] == q:
            continue
        result.append((bus_index_to_name[i],sims[i]/sims[asort[0]]))
    return result



def closest_features(feature_index_in, k = 5):
    f_compressed = normalize(features_compressed.T, axis = 1)
    feature_vector = f_compressed[feature_index_in,:]
    sims = (np.dot(f_compressed,feature_vector))/(LA.norm(f_compressed)* LA.norm(feature_vector))
    asort = np.argsort(-sims)
    result = []
    for i in asort[1:]:
        if i == feature_index_in:
            continue
        result.append((index_to_vocab[str(i)],sims[i]/sims[asort[0]]))
    return result[0:k]

def find_cat_resteraunts(cat_tup, weight):
    key,value  = cat_tup
    cat_ids = []
    for bus_ids in cat_inv_index[key]:
        cat_ids.append((bus_ids,value*weight))
    return cat_ids

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def find_similar(input_weights,liked,disliked,latitude,longitude):
    ## OUR ALGORITHM: cat_weights*0.15 + tfidf*0.15 + distance*0.6
    algo_cat = 15
    algo_flav = 15
    algo_tfidf = 15
    algo_distance = 60
    result_list = defaultdict(list)
    for k,v in input_weights.iteritems():
        if k in arizona_categories:
            for bus_id, score in find_cat_resteraunts((k,v), algo_cat):
                result_list[bus_id].append(score)
        elif k in arizona_features:
            for flav in closest_features(vocab_to_index[k])[0:2]:
                sorted_inv_index = sorted(inv_index[flav[0]], key=itemgetter(1), reverse=True)
                for bus_tup in sorted_inv_index[0:5]:
                    result_list[bus_tup[0]].append((bus_tup[1]/sorted_inv_index[0][1])*algo_flav)
    if len(liked)!=0:
        for indx in range(0,len(liked)):
            relevant = [i for i in liked if i!=liked[indx]]
            for elem in bus_recommender(liked[indx],liked,disliked):
                result_list[elem[0]].append(elem[1]*30)
    # dist = {}
    # for key, value in bus_location.iteritems():
    #     dist[key] = distance((latitude,longitude), value)
    # sorted_result = sorted(dist.items(), key=operator.itemgetter(1), reverse=True)
    
    # for dist_tup in sorted_result:
    #     result_list[dist_tup[0]].append(((dist_tup[1]-sorted_result[-1][1])/sorted_result[0][1])*algo_distance)
    final_result = {}
    for k,v in result_list.iteritems():
        final_result[k] = sum(v)
    return sorted(final_result.items(), key=operator.itemgetter(1), reverse=True)[0:5]
