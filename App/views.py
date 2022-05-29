# import libraries
import pandas as pd
from django.shortcuts import render,redirect
from django.conf import settings
import pickle

import os
from .DataSets import *
from django.http import HttpResponse
import requests
import json

# function for homepage
def home(request):
    if(request.method == "POST"):
        title= request.POST.get("movie")
        print(title)
        return redirect(f"http://127.0.0.1:8000/recommend/{title}")
    return render(request,"App/index.html")

def fetchImageUrl(id):
    reqUrl = f"https://api.themoviedb.org/3/movie/{id}?api_key=64a496e8ea028722359a95ad858ba389&language=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    print(id)
    payload = ""
    response = requests.request("GET", reqUrl, data=payload, headers=headers)
    path = json.loads(response.text).get("poster_path")
    final_path = f"https://image.tmdb.org/t/p/w500/{path}"

    return final_path




def recommendations(request, param):
    path_to_csv = str(settings.BASE_DIR) +'\\App\\DataSets\\tmdb_5000_movies.csv'
    path_to_nm = str(settings.BASE_DIR) +'\\App\\DataSets\\movies.csv'
    df = pd.read_csv(path_to_csv)

    res = df[df['original_title'].str.contains(f"{param}")]
    search_results = []
    for key, values in res.to_dict()["title"].items():
        search_results.append({"id":key,"title":values})

    index = df.original_title[df.original_title == res.iloc[0].original_title].index.tolist()
    print("Index is",index)
    #Get Insights from trained model

    # first_movie = res.iloc[0].index
    # print("Index is",first_movie)
    path_to_pickel = str(settings.BASE_DIR) + '\\App\\TrainedModel\\model_pickel'
    with open(path_to_pickel, "rb") as f:
        mp = pickle.load(f)
    distance = mp[index[0]]

    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:9]
    recom = []
    for i in movie_list:
        dict = {}
        dict["id"] = i[0]
        try:
            dict["title"] = df.iloc[i[0]].title
            dict["image"] = fetchImageUrl(df.iloc[i[0]].id)
        except Exception as e:
            pass
        # append dictionary to list
        recom.append(dict)



    return render(request,"App/recommendations.html",{"related":search_results,"recom":recom})

