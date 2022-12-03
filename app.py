from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re
from io import BytesIO
import base64
from matplotlib.figure import Figure

df_Image = pickle.load(open('df_Image.pkl','rb'))
df_beer_features_cosine = pickle.load(open('df_beer_features_cosine.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
df_comment = pickle.load(open('df_comment.pkl','rb'))
similar100 = pickle.load(open('similar100.pkl','rb'))
list_beers = pickle.load(open('list_beers.pkl','rb'))



app = Flask(__name__, template_folder='template')


@app.route('/')
def index():
    return render_template('index.html',
                           beer_name = list(df_Image['Beer_name'].values),
                           image     =list(df_Image['Image'].values),
                           province  =list(df_Image['province'].values)
                           )

@ app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@ app.route('/recommend_beer', methods =['POST'])
def recommend():
    user_input = request.form.get('user_input')
    get_index = list_beers.index(user_input)
    similarity = similar100[get_index]
    index = np.where(df_beer_features_cosine.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:10]
    df_new = df_comment[df_comment['Beer_name'] == user_input ]
    clean_review = df_new['Comment']
    clean_review.dropna()
    p = Counter(" ".join(list(map(str, clean_review))).split()).most_common(5)
    rslt = pd.DataFrame(p, columns=['Word', 'Frequency'], index=None)
    rslt['Word'] = rslt['Word'].apply(lambda x: re.sub(r'[^A-Za-z\s]', '', x))
    graph = rslt.plot(y="Frequency", x="Word", kind="barh", legend=False)
    graph.set(ylabel =None)
    plt.savefig('static/style/graph.png')

    nearest = []
    for idx, coeff in enumerate(similarity):
        nearest.append((list_beers[idx], coeff))
        nearest.sort(key=lambda x: x[1], reverse=True)
    data_svd = []
    for i in range(1,10):
         data_svd.append(nearest[i][0])
    data_cosine = []
    for i in similar_item:
        data_cosine.append(df_beer_features_cosine.index[i[0]])
    my_beer = list(set(data_cosine) & set(data_svd))
    data = []
    # for i in similar_item:
    for i in  my_beer:
        item = []
        temp_df = df_Image[df_Image['Beer_name'] == i]
        #temp_df = df_Image[df_Image['Beer_name'] == df_beer_features_cosine.index[i[0]]]
        item.extend(temp_df['Beer_name'])
        item.extend(temp_df['Image'])
        item.extend(temp_df['province'])
        #data.append(item)
        data.append(item)
   # print(data)
    return render_template('recommend.html',data=data, url= '/static/style/graph.png')
if __name__=='__main__':
    app.run(debug=True)