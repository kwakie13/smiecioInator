import matplotlib.pyplot as plt
import pandas
from sklearn import tree
from sklearn.externals import joblib

attributes = ["distance_to_bin", "distance_to_trash", "filling_mass", "filling_space", "trash_mass", "trash_space"]
decisions = ["decision"]


def learning_tree():
    dataset = pandas.read_csv('tree_dataset.csv')

    x = dataset[attributes]
    y = dataset[decisions]

    decision_tree = tree.DecisionTreeClassifier()
    decision_tree = decision_tree.fit(x, y)

    return decision_tree


def making_decision(tree, distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space):
    decision = tree.predict([[distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space]])

    return decision


def save_tree_to_txt(tree):
    with open("tree.txt", "w") as file:
        file.write(tree.export_text(tree))


def save_tree_to_png(tree):
    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(tree, feature_names=attributes, filled=True)
    fig.savefig("decision_tree.png")


def save_tree_to_structure(tree):
    joblib.dump(tree, 'tree_model')


def load_tree_from_structure(file):
    return joblib.load(file)
