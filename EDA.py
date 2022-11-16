import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import sklearn
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


df_x = pd.read_csv('C:\\Users\\15147\\PycharmProjects\\pythonProject\\Airbnb\\beer_final.csv')
df_x[df_x.Beer_name==""] = np.NaN
df = df_x.fillna(method='ffill')
df.describe()
print(df.describe())

# df['U_id'] = df.groupby('User').ngroup()
# df.sort_values(by='U_id',ascending=False,inplace=True)
# df.reset_index(inplace=True)
# df.drop(['index'],axis=1,inplace=True)


# we use this step to get how many time beer has been rated
reviews_count_analyze = df.groupby('Beer_name').Rating.count().to_frame('Reviews_count').sort_values(by='Reviews_count', ascending=False)
reviews_count_analyze.reset_index(inplace=True)
# we use this step to gey how many reviews have been given by user
reviews_user = df.groupby('User').Rating.count().to_frame('User_count').sort_values(by='User_count', ascending=False)
reviews_user.reset_index(inplace=True)
# We will keep beer which recived more than 15 reviews and user who gave more than 10 reviews
beer_id_grt_thn_15 = reviews_count_analyze.loc[reviews_count_analyze['Reviews_count'] >= 15].Beer_name.to_frame('id1')
beer_user_grt_thn_10 = reviews_user.loc[reviews_user['User_count']>=10].User.to_frame('id1')
# we will join that 2 result
df_2= df.merge(beer_id_grt_thn_15 ,how = 'inner', left_on = 'Beer_name', right_on = 'id1').drop(['id1'], axis=1)
df_final = pd.merge(df_2,beer_user_grt_thn_10,how = 'inner', left_on = 'User', right_on= 'id1').drop(['id1'], axis=1)
df_beer_features = df_final.pivot_table(index='User',columns='Beer_name',values='Rating').fillna(0)
df_beer_features_cosine = df_final.pivot_table(index='Beer_name',columns='User',values='Rating').fillna(0)
# This step we use to transpose matrix
T = df_beer_features.values.T
list_beers = list(df_beer_features.columns)

def exp_variance (list_):
    out = []
    for num in list_:
        SVD = TruncatedSVD(n_components=num,random_state=num)
        SVD.fit(T)
        var_explained = np.sum(SVD.explained_variance_ratio_)
        combination = (num,var_explained)
        out.append(combination)
    return out

list_ = [5, 10, 20, 50, 100, 150, 200, 250]
experiment = exp_variance(list_)
# we will go with 100 based on 80/20 principal as 100 covers 80 percent of variance.

SVD100 = TruncatedSVD(n_components=100,random_state=100)
final100 = SVD100.fit_transform(T)
similar100 = np.corrcoef(final100)

def get_beer_svd(Beer_name, n):
    get_index = list_beers.index(Beer_name)
    similarity = similar100[get_index]
    nearest= []
    for idx, coeff in enumerate(similarity):
       nearest.append((list_beers[idx],coeff))
       nearest.sort(key=lambda x:x[1],reverse=True)

    final_result=[]
    for i in range(1,n):
         final_result.append(nearest[i][0])
    return final_result

df_beer_features_cosine.fillna(0, inplace=True)
similarity_score = cosine_similarity(df_beer_features_cosine)

def get_beer_cosine(Beer_name,n):
    index = np.where(df_beer_features_cosine.index== Beer_name)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key =lambda x:x[1],reverse = True)[1:n]
    my_beer = []
    for i in similar_item:
        my_beer.append(df_beer_features_cosine.index[i[0]])
    return my_beer

## To get the common beer from 2 diffrent methods


A = set(get_beer_svd('La ButeuseLe Trou Du Diable', 10))
B = set(get_beer_cosine('La ButeuseLe Trou Du Diable',10))
print('common beers: {}'.format(A.intersection(B)))
print('number of common beers: {}'.format(len(A.intersection(B))))


# # df_image = (df_final[['Beer_name', 'Image']]).drop_duplicates()
# # pickle.dump(df_image,open('Image.pkl','wb'))
# #

# # #

    # for i in similar_item:
    #     item= []
    #     temp_df = df_image[df_image['Beer_name'] == df_beer_features.index[i[0]]]
    #     item.extend(temp_df['Beer_name'])
    #     item.extend(temp_df['Image'])
    #     data.append(item)
# #

# #
# # # pickle.dump(df_beer_features,open('df_beer_features.pkl','wb'))
# # # pickle.dump(similarity_score,open('similarity_score.pkl','wb'))
# #
#
#



