import sys
import os
import requests
from typing import List
import re
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
        params = {
            'q': f'language:{self.lang}+stars:{self.stars}',
            'sort': 'stars',
            'per_page': 100,
            'page': {page}
        }

        payload_str = "&".join("%s=%s" % (k, v) for k, v in params.items())
        try:
            r = requests.get(URL, headers=headers, params=payload_str)

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
            stats["licence"] = "Not Found"
        else:
            stats["license"] = repoObj["license"]["name"]
        contributorCount, err = self.getContributorCountOfRepo(repoObj["contributors_url"])
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
        stats['total_issue_count'] = self.getTotalIssueCount(repoObj["full_name"])
        stats['commit_count'] = self.getCommitCount(repoObj['full_name'])

        return stats

    def getContributorCountOfRepo(self, contUrl):
        headers = {
            'Authorization': f'token {self.token}',
            'accept': 'application/vnd.github.v3+json'
        }

        try:
            r = requests.get(contUrl, headers=headers)

            if r.status_code != 200:
                return None, Exception(f"expected to get HTTP 200, got HTTP {r.status_code}, URL: {r.url}")

            return len(r.json()), None
        except Exception as e:
            return None, e

    def getTotalIssueCount(self, reponame):
        headers = {
            'Authorization': f'token {self.token}',
            'accept': 'application/vnd.github.v3+json'
        }

        url = f'https://api.github.com/search/issues?q=repo:{reponame}+type:issue' 

        response = requests.get(url, headers=headers)

        return response.json()['total_count']

    def getCommitCount(self, reponame):
        headers = {
            'Authorization': f'token {self.token}',
            'accept': 'application/vnd.github.v3+json'
        }


        url = f'https://api.github.com/repos/{reponame}/commits?per_page=1' 
        response = requests.get(url, headers=headers)

        
        
        commit = response.json()[0] 
        commit['number'] = re.search('\d+$', response.links['last']['url']).group()
        return commit['number'] 
        
