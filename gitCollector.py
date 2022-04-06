import sys
import os
import requests
from typing import List

#https://docs.github.com/en/rest/reference/search
class gitCollector ():

    def __init__(self, lang, stars):
        self.lang = lang
        self.stars = stars

    # gets page as parameter. returns page of search result.
    def getRepos(self,page=1):

        token = os.getenv('STAR_GITHUB_TOKEN', '')
        if token == '':
            return "cannot get GITHUB token from, please declare STAR_GITHUB_TOKEN environment variable."

        
        # url that is used in curl. per_page parameter max 100 no more is allowed.
        # more than 5 ANDs or ORs not allowed in github queries.
        URL = f"https://api.github.com/search/repositories"

        headers = {'Authorization': f'token {token}'}
        params = {'q': f'?q=language:{self.lang}+stars:{self.stars}&order=desc&per_page=100&page={page}'}
        try:
            r = requests.get(URL, headers=headers, params=params)

            if r.status_code != 200:
                return None, Exception(f"expected to get HTTP 200, got HTTP {r.status_code}, URL: {r.url}")

            return r.json(), None
        except Exception as e:
            return None, e
        
    def getStatsOfRepo(self,repoUrl):
        return "stats"