from gitCollector import gitCollector
import os
import pandas as pd


def main():
    token = os.getenv('STAR_GITHUB_TOKEN', '')
    if token == '':
        print("cannot get GITHUB token from, please declare STAR_GITHUB_TOKEN environment variable.")
        return

    lang = "go"
    min_star_count = 10
    max_star_count = 1000
    star_query = f"{min_star_count}..{max_star_count}"
    filename = f"{lang}_{min_star_count}_{max_star_count}.csv"
    gitC = gitCollector(lang, star_query, token)
    df = pd.DataFrame()

    repos, err = gitC.getRepos()
    if err != None:
        print('failed to fetch repositories from GitHub, err: ', err)
        return

    
    #format of one repo
    print(repos['items'][0])

    #star counts to check if query works
    for elem in repos['items']:
        df = df.append(gitC.getStatsOfRepo(elem), ignore_index=True)

    df.to_csv(filename)
    print(f"There are {len(repos['items'])} repos found")

if __name__ == "__main__":
    main()