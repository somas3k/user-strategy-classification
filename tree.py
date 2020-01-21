from sklearn import tree
import csv
import matplotlib.pyplot as plt
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'D:/Programs/Graphviz2.38/bin/'
X = []
Y = []
field_names = ['tweets', 'retweets', 'average_hashtags', 'average_urls', 'average_followers', 'right_partiality',
               'left_partiality', 'polarity', 'subjectivity', 'average_tweet_size']
with open('results2.csv', newline='') as results:
    reader = csv.DictReader(results)
    for row in reader:
        X.append([row[field_name] for field_name in field_names])
        Y.append(row['label'])

Xs = []
with open('samples.csv', newline='') as samples:
    reader = csv.DictReader(samples)
    for row in reader:
        Xs.append([row[field_name] for field_name in field_names])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
print(clf.predict(Xs))
print(clf.predict_proba(Xs))

dot_data = tree.export_graphviz(clf, out_file=None, feature_names=field_names, class_names=['RightTroll', 'LeftTroll', 'Fearmonger', 'HashtagGamer', 'NewsFeed'], filled=True, rounded=True)
graph = graphviz.Source(dot_data)
graph.render('res2')