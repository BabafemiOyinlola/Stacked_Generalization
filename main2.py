import math
import random
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier

from experiments2 import cross_validate_clfs, cross_validate_clfs_noise, cross_validate_kappa, q_statistic
from stacked2 import StackedGeneralization

def split_data(filepath, lbl_pos=-1):
    data = pd.read_csv(filepath, header=None)
    data = np.array(data)
    X, y = None, None
    if lbl_pos == -1:
        y = data[:, -1]
        X = data[:, 0:data.shape[1]-1]
    elif lbl_pos == 0:
        y = data[:, 0]
        X = data[:, 1:data.shape[1]]
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    return (X_train, X_test, y_train, y_test) 

if __name__ == "__main__":
    knn, dt, svm, lr, nb, stk, stk_prob = KNeighborsClassifier(n_neighbors=1, leaf_size=1, p=1), DecisionTreeClassifier(max_depth=1, splitter="random", random_state=1),\
                                    SVC(max_iter=1), LogisticRegression(), GaussianNB(), StackedGeneralization(), StackedGeneralization()
    mlp = MLPClassifier(hidden_layer_sizes=(5, 1))

    classifiers_cv = [svm, dt, mlp, stk, stk_prob]
    classifiers_cv_names = ["svm", "dt", "mlp", "stacked", "stacked_prob"]

    # data = pd.read_csv('data/waveform/waveform.txt', header=None)
    # data = pd.read_csv('data/glass/glass.csv', header=None)
    data = pd.read_csv('data/hepatitis/hepatitis.csv', header=None)

    #non numeric label
    # data = pd.read_csv('data/avila/avila.csv', header=None)
    
    #binary 
    # data = pd.read_csv('data/sonar/sonar.csv', header=None)
    # data = pd.read_csv('data/ionosphere/ionosphere.csv', header=None)
    # data = pd.read_csv('data/breast_cancer/breast_cancer.csv', header=None)
    # data = pd.read_csv('data/iris/iris.csv', header=None)
    

    data = data.sample(frac=1).reset_index(drop=True) #shuffle


    cv_results = cross_validate_clfs(data, classifiers_cv, classifiers_cv_names, meta_clf=LogisticRegression(), encode=False)
    print("\nCROSS VALIDATION NOISELESS \n")
    for clf, acc in cv_results:
        print(clf + " : " + str(round(acc, 3)) + " \t\t\tError: " + str(round(1 - acc, 3)))
    
    # print("\nCROSS VALIDATION NOISE \n")
    # for i in range(5, 30, 5):
    #     print("\n")
    #     print("Noise level: ", i)
    #     cv_results_noise = cross_validate_clfs_noise(data, classifiers_cv, classifiers_cv_names, meta_clf=LogisticRegression, level=i, encode=True)
    #     for clf, acc in cv_results_noise:
    #         print(clf + " : " + str(round(acc, 3)) + " \t\t\tError: " + str(round(1 - acc, 3)))

    # kappa_scores = cross_validate_clfs(data, classifiers_cv, classifiers_cv_names, meta_clf=SVC, encode=True)
    # print("\nKAPPA SCORES\n")
    # for clf, k in kappa_scores:
    #     print(clf + " : " + str(round(k, 3)))



    print("\nDone")