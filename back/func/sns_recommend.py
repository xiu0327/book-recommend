#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(keyword, title_to_index, key, cosine_sim):

    idx = title_to_index[keyword]
    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [idx[0] for idx in sim_scores]

    result = []

    for i in movie_indices:
        try: result.append(key[i])
        except IndexError: continue

    return result

def sns_recommend(keywords):

    with open('/home/ubuntu/data/yes24_미대출도서(new_category).json', 'r', encoding="utf-8") as f:
        bookinfo = json.load(f)

    f.close()


    keywords = keywords.split("_")

    result = []

    for keyword in keywords:
        tfidf = TfidfVectorizer()
        # data = list(corpus.values()) #키워드 추가
        data = [bookinfo[key]["bookToken"] for key in bookinfo.keys()]
        data.append(keyword)
        tfidf_matrix = tfidf.fit_transform(data)
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        title_to_index = dict(zip(data, [n for n in range(len(data))]))
        result.extend(get_recommendations(keyword, title_to_index, list(bookinfo.keys()), cosine_sim))
        # result.append([bookinfo[item] for item in get_recommendations(keyword, title_to_index, list(bookinfo.keys()), cosine_sim)])

    return [bookinfo[item] for item in list(set(result))]
