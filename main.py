from gitCollector import gitCollector
import os
import pandas as pd


def main():
    token = os.getenv('STAR_GITHUB_TOKEN', '')
    if token == '':
        print("cannot get GITHUB token from, please declare STAR_GITHUB_TOKEN environment variable.")
        return

    lang = "python"
    min_star_count = 100
    max_star_count = 10000
    star_query = f"{min_star_count}..{max_star_count}"
    filename = f"{lang}_{min_star_count}_{max_star_count}.csv"
    gitC = gitCollector(lang, star_query, token)

    df = pd.DataFrame()
    for i in range(1,3):
        repos, err = gitC.getRepos(i)
        if err != None:
            print('failed to fetch repositories from GitHub, err: ', err)
            return

        for elem in repos['items']:
            df = df.append(gitC.getStatsOfRepo(elem), ignore_index=True)

    df.to_csv(filename)
    print(f"There are {len(repos['items'])} repos found")

if __name__ == "__main__":
    main()