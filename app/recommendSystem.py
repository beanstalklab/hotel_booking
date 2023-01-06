import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import math
from numpy.linalg import norm
import sys
import pymysql
sys.path.append("D:\\dulieuD\\Program Language\\Python_2021\\final_exam\\hotel_booking\\app")
from flask import Flask, render_template

# indices for vector (lấy ra chỉ số đc rating của các vector)
def specified_rating_indices(u):
    return list(map(list, np.where(np.isfinite(u))))

def mean(u):
    specified_ratings = u[np.isfinite(u)] # specified_ratings = u[specified_rating_indices(u)] 
    m = np.sum(specified_ratings)/np.shape(specified_ratings)[0]
    return m

def all_user_mean_ratings(ratings_matrix):
    return np.array([mean(ratings_matrix[u, :]) for u in range(ratings_matrix.shape[0])])

def get_mean_centered_ratings_matrix(ratings_matrix):
    users_mean_rating = all_user_mean_ratings(ratings_matrix)
    mean_centered_ratings_matrix = np.around(ratings_matrix - np.reshape(users_mean_rating, (-1, 1)), 3)
    return mean_centered_ratings_matrix


def similarity(u, v):
    cosine = np.dot(u, v) / (norm(u) * norm(v) + 1e-8)
    return np.around(cosine, 5)

def get_user_similarity_value_for(u_index, mean_centered_ratings_matrix):
    user_ratings = mean_centered_ratings_matrix[u_index, :]
    similarity_value = np.array([similarity(mean_centered_ratings_matrix[i, :], user_ratings) for i in range(mean_centered_ratings_matrix.shape[0])])
    return similarity_value

def get_user_similarity_matrix(mean_centered_ratings_matrix):
    similarity_matrix = []
    for u_index in range(mean_centered_ratings_matrix.shape[0]):
        similarity_value = get_user_similarity_value_for(u_index, mean_centered_ratings_matrix)
        similarity_matrix.append(similarity_value)
    return np.array(similarity_matrix)


def predict(u_index, i_index, k,ratings_matrix,user_similarity_matrix,mean_centered_ratings_matrix):
    # k là số lượng người dùng giống với người dùng cần dự đoán
    # ta có thể tùy chọn giá trị k này
    users_mean_rating = all_user_mean_ratings(ratings_matrix)
    
    similarity_value = user_similarity_matrix[u_index]
    sorted_users_similar = np.argsort(similarity_value)
    sorted_users_similar = np.flip(sorted_users_similar, axis=0)
        
    users_rated_item = specified_rating_indices(ratings_matrix[:, i_index])[0]
    
    ranked_similar_user_rated_item = [u for u in sorted_users_similar if u in users_rated_item]
    
    if k < len(ranked_similar_user_rated_item):
        top_k_similar_user = ranked_similar_user_rated_item[0:k]   
    else:
        top_k_similar_user = np.array(ranked_similar_user_rated_item)
            
    ratings_in_item = mean_centered_ratings_matrix[:, i_index]
    top_k_ratings = ratings_in_item[top_k_similar_user]
    
    top_k_similarity_value = similarity_value[top_k_similar_user]
    
    r_hat = users_mean_rating[u_index] + np.sum(top_k_ratings * top_k_similarity_value)/np.sum(np.abs(top_k_similarity_value))
    return r_hat


def predict_top_k_items_of_user(u_index, k_users,ratings_matrix,user_similarity_matrix,mean_centered_ratings_matrix):
    items = []
    for i_index in range(ratings_matrix.shape[1]):
        if np.isnan(ratings_matrix[u_index][i_index]):
            rating = predict(u_index, i_index, k_users,ratings_matrix,user_similarity_matrix,mean_centered_ratings_matrix)
            items.append((i_index, rating))
    items = sorted(items, key=lambda tup: tup[1])
    items = list(reversed(items))
    return items

