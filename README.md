# Github Star Prediction - CS 48000 Project

This is a simple classification problem which tries to predict the Github Star Count of Github repositories. 

To handle the task we collected the data via [Github Api](https://docs.github.com/en). You can see the data in [here](total_scraped_data_v3.csv).

## Collected Fields from Github Api

We collected the below features from Github Api.

| Feature  | Description |
| ------------- | ------------- |
| name  | name of the github repo (i.e ocakhasan/cmd)  |
| url  | url of the github repo  |
| star count | |
| licence  |   |
| contributor count  |   |
| size  | size of the repository  |
| forks  | fork count of the repo  |
| github pages  | boolean which shows if the repo has github pages  |
| topics count  | number of counts used to describe repo  |
| open issues  | open issue count of the repo  |
| created at  |  date the repo is created |
| updated at  |  date the repo is last updated  |
| allow forking  | bool which shows if repo allows forking  |
| total issue count  |   |
| commit count  |  |

Total number of collected data is 6142 with 80% as training and 20% as testing.

## Model cleaning and training

There were some data cleaning and processing in the [final.ipynb](final.ipynb). 



### Results

- we have achieved 40 percent accuracy. 


### Feature Engineering

We added new features based on the the fields we collected.

- `how many years the repo has been developed` with the fields from `created_at` an `updated_at`. 
- `issue_close_rate` based on number of closed issues and total issue counts  

### Training

We trained several classification algorithms

- [Decision Tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
- [KNN](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
- [SVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
- [Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [SGD](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)

The best performed one is `DecisionTreeClassifer` with the accuracy of 40%.

## How to run the repo

First clone the repo

```
> git clone https://github.com/ocakhasan/CS48000GithubStarPrediction
> cd CS48000GithubStarPrediction
```

install the below packages via `pip`.
```
pandas
numpy
sklearn
streamlit
```

Then you can run the cells in [final.ipynb](final.ipynb) to achieve the results or you can see the output of the each cell.

## Demo

We have a demo website, where you can simply enter repository name and get a result, but for that you need an Github Api Token and you need to set an environment variable called `STAR_GITHUB_TOKEN` which allows us to send more requests to Github Api.

To run the demo, please install [streamlit](https://streamlit.io/). 

```
streamlit run streamlit.py
```