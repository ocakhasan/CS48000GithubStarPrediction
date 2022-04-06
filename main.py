from gitCollector import gitCollector


def main():

    gitC = gitCollector("go","10..1000")

    repos, err = gitC.getRepos()
    if err != None:
        print('failed to fetch repositories from GitHub, err: ', err)
        return

    
    #format of one repo
    print(repos['items'][0])

    #star counts to check if query works
    for elem in repos['items']:
        print(elem["stargazers_count"])

    print(len(repos['items']))

if __name__ == "__main__":
    main()