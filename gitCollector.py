import os
import re
import sys
from typing import List

import requests


#https://docs.github.com/en/rest/reference/search
class gitCollector ():

    def __init__(self, lang, stars, token):
        self.lang = lang
        self.stars = stars
        self.token = token

    # gets page as parameter. returns page of search result.
    def getRepos(self,page=1):

        
        # url that is used in curl. per_page parameter max 100 no more is allowed.
        # more than 5 ANDs or ORs not allowed in github queries.
        URL = f"https://api.github.com/search/repositories"

        headers = {
            'Authorization': f'token {self.token}',
            'accept': 'application/vnd.github.v3+json'
        }
        #params = {'q': f'=language:{self.lang}+stars:{self.stars}&order=desc&per_page=100&page={page}'}

        query = f'stars:{self.stars}'
        if self.lang != "":
            query = f'language:{self.lang}+stars:{self.stars}'

        params = {
            'q': query,
            'per_page': 100,
            'page': page,
        }

        payload_str = "&".join("%s=%s" % (k, v) for k, v in params.items())
        print("currently scraping", URL + "?" + payload_str)
        try:
            r = requests.get(URL, headers=headers, params=payload_str)
            print()

            if r.status_code != 200:
                return None, Exception(f"expected to get HTTP 200, got HTTP {r.status_code}, URL: {r.url}")

            return r.json(), None
        except Exception as e:
            return None, e
    
    def getStatsOfRepo(self, repoObj):
        stats = {}
        stats["name"] = repoObj["full_name"]
        stats["url"] = repoObj["html_url"]
        stats["star_count"] = repoObj["stargazers_count"]
        if repoObj["license"] is None:
            stats["license"] = "Not Found"
        else:
            stats["license"] = repoObj["license"]["name"]
        contributorCount, err = self.getContributorCountOfRepo(repoObj["full_name"])
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
        issue_count, err = self.getTotalIssueCount(repoObj["full_name"])
        if err != None:    
            stats['total_issue_count'] = 0
        else:
            stats["total_issue_count"] = issue_count
        
        commit_count, err = self.getCommitCount(repoObj['full_name'])
        if err != None:
            stats['commit_count'] = 0
        else:
            stats["commit_count"] = commit_count

        return stats

    def getContributorCountOfRepo(self, reponame):
        headers = {
            'Authorization': f'token {self.token}',
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

    def getTotalIssueCount(self, reponame):
        try:

            headers = {
                'Authorization': f'token {self.token}',
                'accept': 'application/vnd.github.v3+json'
            }

            url = f'https://api.github.com/search/issues?q=repo:{reponame}+type:issue' 

            response = requests.get(url, headers=headers)

            return response.json()['total_count'], None
        except Exception as e:
            return 0, e

    def getCommitCount(self, reponame):
        try:
            headers = {
                'Authorization': f'token {self.token}',
                'accept': 'application/vnd.github.v3+json'
            }


            url = f'https://api.github.com/repos/{reponame}/commits?per_page=1' 
            response = requests.get(url, headers=headers)

            
            
            commit = response.json()[0] 
            commit['number'] = re.search('\d+$', response.links['last']['url']).group()
            return commit['number'], None
        except Exception as e:
            return 0, e
