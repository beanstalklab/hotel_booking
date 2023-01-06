import pandas as pd
import numpy as np
import pymysql
from sklearn.metrics.pairwise import cosine_similarity

def connect_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='quanlykhachsan'
    )
    return conn

def get_cursor(conn):
    conn.begin()
    cur = conn.cursor()
    return cur

def importData():
    conn = connect_db()
    query = "select * from danhgia;"
    rating_data = pd.read_sql(query, conn)

    hotel_rating_user =rating_data.pivot_table(index='account_id', columns='room_id', values='rating')
    return hotel_rating_user.values

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

def predict(u_index, i_index, k):
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
    return np.round(r_hat, 3)


def predict_top_k_items_of_user(u_index, k_users):
    items = []
    for i_index in range(ratings_matrix.shape[1]):
        if np.isnan(ratings_matrix[u_index][i_index]):
            rating = predict(u_index, i_index, k_users)
            items.append((i_index, rating))
    items = sorted(items, key=lambda tup: tup[1])
    items = list(reversed(items))
    return items


ratings_matrix = importData()
mean_centered_ratings_matrix = get_mean_centered_ratings_matrix(ratings_matrix)
mean_centered_ratings_matrix[np.isnan(mean_centered_ratings_matrix)] = 0
user_similarity_matrix = cosine_similarity(mean_centered_ratings_matrix)

def get_result(user_id):
    result_predict  = predict_top_k_items_of_user(user_id, 2)
    return result_predict
# print(get_result(1))