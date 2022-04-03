import os
import random, string, subprocess, json
#https://docs.github.com/en/rest/reference/search
class gitCollector ():

    def __init__(self, lang, stars):
        self.lang = lang
        self.stars = stars

    # gets page as parameter. returns page of search result.
    def getRepos(self,page=1):
        # url that is used in curl. per_page parameter max 100 no more is allowed.
        # more than 5 ANDs or ORs not allowed in github queries.
        url = f"https://api.github.com/search/repositories?q=language:{self.lang}+stars:{self.stars}&order=desc&per_page=100&page={page}"
        proc = subprocess.Popen(["curl", "-H", "Accept: application/vnd.github.preview.text-match+json", url],
                                stdout=subprocess.PIPE)
        print("CMD: {}".format(' '.join(proc.args)))
        output = proc.communicate()[0].decode("UTF-8")
        jsonout = json.loads(output)
        return jsonout

    def getStatsOfRepo(self,repoUrl):
        return "stats"