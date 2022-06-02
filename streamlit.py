import streamlit as st
import pandas as pd
import pickle
import os
import requests, re
import numpy as np

filename = "finalized_model.sav"
k_best_filename = "k_best_file.sav"


def getContributorCountOfRepo(token, reponame):
        headers = {
            'Authorization': f'token {token}',
            'accept': 'application/vnd.github.v3+json'
        }

        try:
            url = f'https://api.github.com/repos/{reponame}/contributors?per_page=1&anon=true'
            r = requests.get(url, headers=headers)

            if r.status_code != 200:
                return None, Exception(f"expected to get HTTP 200, got HTTP {r.status_code}, URL: {r.url}")

            conts = r.json()[0] 
            conts['number'] = re.search('\d+$', r.links['last']['url']).group()
            return conts['number'], None
        except Exception as e:
            return None, e


def getTotalIssueCount(token, reponame):
    try:

        headers = {
            'Authorization': f'token {token}',
            'accept': 'application/vnd.github.v3+json'
        }

        url = f'https://api.github.com/search/issues?q=repo:{reponame}+type:issue' 

        response = requests.get(url, headers=headers)

        return response.json()['total_count'], None
    except Exception as e:
        return 0, e

def getCommitCount(token, reponame):
    try:
        headers = {
            'Authorization': f'token {token}',
            'accept': 'application/vnd.github.v3+json'
        }


        url = f'https://api.github.com/repos/{reponame}/commits?per_page=1' 
        response = requests.get(url, headers=headers)

        
        
        commit = response.json()[0] 
        commit['number'] = re.search('\d+$', response.links['last']['url']).group()
        return commit['number'], None
    except Exception as e:
        return 0, e

def getStatsOfRepo(token, repoObj):
        stats = {}
        stats["name"] = repoObj["full_name"]
        stats["url"] = repoObj["html_url"]
        stats["star_count"] = repoObj["stargazers_count"]
        if repoObj["license"] is None:
            stats["license"] = "Not Found"
        else:
            stats["license"] = repoObj["license"]["name"]
        contributorCount, err = getContributorCountOfRepo(token, repoObj["full_name"])
        if err == None:
            stats["contributor_count"] = contributorCount
        stats["size"] = repoObj["size"]
        stats["watchers_count"] = repoObj["watchers_count"]

        stats["forks"] = repoObj["forks_count"]
        stats["github_pages"] = repoObj["has_pages"]
        stats["open_issues"] = repoObj["open_issues"]
        stats["topics_count"] = len(repoObj["topics"])
        stats["created_at"] = repoObj["created_at"]
        stats["updated_at"] = repoObj["updated_at"]
        stats["allow_forking"]= repoObj["allow_forking"]
        issue_count, err = getTotalIssueCount(token, repoObj["full_name"])
        if err != None:    
            stats['total_issue_count'] = 0
        else:
            stats["total_issue_count"] = issue_count
        
        commit_count, err = getCommitCount(token, repoObj['full_name'])
        if err != None:
            stats['commit_count'] = 0
        else:
            stats["commit_count"] = commit_count

        return stats

def getTotalInfoofRepo(token, reponame):
    URL = f"https://api.github.com/repos/{reponame}"

    headers = {
        'Authorization': f'token {token}',
        'accept': 'application/vnd.github.v3+json'
    }

    try:
            
            r = requests.get(URL, headers=headers)

            if r.status_code != 200:
                return None, Exception(f"expected to get HTTP 200, got HTTP {r.status_code}, URL: {r.url}")

            result = getStatsOfRepo(token, r.json())
            return result, None
    except Exception as e:
            return None, e







@st.cache
def load_data():
    df =pd.read_csv("total_scraped_data_v3.csv")
    df = df.drop(columns=['Unnamed: 0'])
    model = pickle.load(open(filename, 'rb'))
    k_best = pickle.load(open(k_best_filename, 'rb'))
    token = os.getenv("STAR_GITHUB_TOKEN")
    return df, model, token, k_best

st.title("CS 48000 Demo")

data_load_state = st.text('Loading data...')

data, model, token, k_best = load_data()

data_load_state.text('Loading data...done!')



st.subheader('Github Repository Data')
st.write(data.head(10))

st.header("Interactive Prediction Demo")

repo_name = st.text_input("enter repo name for example (peak/s5cmd)")
prediction = None
stats = None

def prepare_df(df):
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    df["years"] = (df["updated_at"] - df["created_at"]) / np.timedelta64(1, 'Y')
    df["years"] = df["years"].astype(np.int32)

    df["closed_issue"] = df["total_issue_count"] - df["open_issues"]
    df["issue_close_rate"] = df["closed_issue"] / df["total_issue_count"]
    df["issue_close_rate"] = df["issue_close_rate"].fillna(0)

    df["github_pages"] = df["github_pages"].astype(np.int32)
    df["allow_forking"] = df["allow_forking"].astype(np.int32)
    df["size"] = df["size"] / 1024.0


    
    return df

if repo_name:
    stats, err =getTotalInfoofRepo(token, repo_name)
    data_df = pd.DataFrame([stats])
    data_df = prepare_df(data_df)
    dropped_columns_df = data_df.drop(columns=["created_at", "license", "name", "updated_at", "url", "watchers_count", "star_count"])
    dropped_columns_df = k_best.transform(dropped_columns_df)
    prediction = model.predict(dropped_columns_df)
    st.write("model predicted", prediction, repo_name)

if stats:
    st.subheader("The data we collected from github api")
    st.write(stats)

if prediction:
    st.title(f"Prediction for {repo_name}")
    st.subheader(f"{np.int(1000*(prediction[0] - 1))} - {np.int(1000 * prediction[0])}")

