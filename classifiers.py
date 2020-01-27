from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import random
import csv
import matplotlib.pyplot as plt

def check_stability(X, Y,file='resultsByQuarter.csv'):
    with open(file, newline='') as samples:
        Xs = []
        Ys = []
        user = None
        date = []
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)
        reader = csv.DictReader(samples)
        for row in reader:
            if user is None:
                user = row['user_id']
            elif user != row['user_id']:
                labels = clf.predict(Xs)
                dates = date
                plt.plot(dates, labels, 'ro')
                plt.ylabel('labels')
                plt.xlabel('dates')
                plt.title(user)
                plt.show()
                Xs = []
                Ys = []
                date = []
                user = row['user_id']

            date.append(row['date'].split(" ")[0])
            Xs.append([row[field_name] for field_name in field_names])
            Ys.append(row['label'])

X = []
Y = []
field_names = ['tweets', 'retweets', 'average_hashtags', 'average_urls', 'average_followers', 'right_partiality',
               'left_partiality', 'polarity', 'subjectivity', 'average_tweet_size']
with open('results2.csv', newline='') as results:
    reader = csv.DictReader(results)
    
    for row in reader:
        X.append([row[field_name] for field_name in field_names])
        Y.append(row['label'])

Ys = []
Xs = []
TEST_PERCENT_OF_SAMPLES = 0.1
for i in range(int(len(X)*TEST_PERCENT_OF_SAMPLES)):
    rand_index = random.randint(0, len(X) - 1)
    Xs.append(X.pop(rand_index))
    Ys.append(Y.pop(rand_index))

check_stability(X,Y)

classifiers = {'decision tree': tree.DecisionTreeClassifier(), 'random forest': RandomForestClassifier(n_estimators=10)}
accuracy = {}
for clf_name in classifiers.keys():
    clf = classifiers[clf_name].fit(X, Y)
    classifiers[clf_name] = clf
    predictions = clf.predict(Xs)
    accurate = 0
    for i in range(len(predictions)):
        if predictions[i] == Ys[i]:
            accurate += 1
    accuracy[clf_name] = accurate/len(predictions)
    print('accuracy of',"'" + clf_name + "'", ":", accuracy[clf_name])

draw_decision_tree = False
if draw_decision_tree:
    import graphviz
    import os
    os.environ["PATH"] += os.pathsep + 'D:/Programs/Graphviz2.38/bin/'
    dot_data = tree.export_graphviz(classifiers['decision tree'], out_file=None, feature_names=field_names, class_names=['RightTroll', 'LeftTroll', 'Fearmonger', 'HashtagGamer', 'NewsFeed'], filled=True, rounded=True)
    graph = graphviz.Source(dot_data)
    graph.render('res2')
