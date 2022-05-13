import os
import warnings
from re import I

from gitCollector import gitCollector

warnings.simplefilter(action='ignore', category=FutureWarning)
import os

import pandas as pd
from tqdm import tqdm


def main():
    token = os.getenv('STAR_GITHUB_TOKEN', '')
    if token == '':
        print("cannot get GITHUB token from, please declare STAR_GITHUB_TOKEN environment variable.")
        return
#denem
    lang = "python"
    min_star_count = 100
    max_star_count = 1000
    star_query = f"{min_star_count}..{max_star_count}"

    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, "data")):
        os.mkdir("data")
    
    gitC = gitCollector(lang, star_query, token)

    data_folder = os.path.join(cwd, "data")

    for i in range(2, 5):
        df = pd.DataFrame()
        repos, err = gitC.getRepos(i)
        filename = f"{lang}_{min_star_count}_{max_star_count}_{i}.csv"
        filename = os.path.join(data_folder, filename)
        if err != None:
            print('failed to fetch repositories from GitHub, err: ', err)
            return

        for elem in tqdm(repos['items']):
            df = df.append(gitC.getStatsOfRepo(elem), ignore_index=True)

        df.to_csv(filename)
    print(f"There are {len(repos['items'])} repos found")

if __name__ == "__main__":
    main()
