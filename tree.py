from sklearn import tree
import csv
import matplotlib.pyplot as plt

X = []
Y = []
field_names = ['tweets', 'retweets', 'average_hashtags', 'average_urls', 'average_followers', 'right_partiality',
               'left_partiality', 'polarity', 'subjectivity', 'average_tweet_size']
with open('results.csv', newline='') as results:
    reader = csv.DictReader(results)
    for row in reader:
        X.append([row[field_name] for field_name in field_names])
        Y.append(row['label'])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

plot = tree.plot_tree(clf, fontsize=3, proportion=True)
plt.show()
print()
