import joblib
import matplotlib.pyplot as plt
import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

attributes = ["distance_to_bin", "distance_to_trash", "filling_mass", "filling_space", "trash_mass", "trash_space"]
decisions = ["decision"]


def learning_tree():
    dataset = pandas.read_csv('./DecisionTree/tree_dataset.csv')

    x = dataset[attributes]
    y = dataset[decisions]

    decision_tree = DecisionTreeClassifier()
    decision_tree = decision_tree.fit(x, y)

    return decision_tree


def making_decision(decision_tree, distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass,
                    trash_space):
    decision = decision_tree.predict(
        [[distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space]])

    return decision


def save_tree_to_txt(decision_tree):
    with open('./DecisionTree/tree_in_txt.txt', "w") as file:
        file.write(tree.export_text(decision_tree))


def save_tree_to_png(decision_tree):
    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(decision_tree, feature_names=attributes, filled=True)
    fig.savefig('./DecisionTree/decision_tree.png')


def save_tree_to_structure(decision_tree):
    joblib.dump(decision_tree, './DecisionTree/tree_model')


def load_tree_from_structure(file):
    return joblib.load(file)
