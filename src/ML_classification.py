import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import ML_helpers
import shap
from sklearn import decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib

matplotlib.rcParams["figure.dpi"] = 200
size = 11
ticksize = 11
legendsize = 11
plt.rc('font', size=size)  # controls default text size
plt.rc('axes', titlesize=size)  # fontsize of the title
plt.rc('axes', labelsize=size)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=ticksize)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=ticksize)  # fontsize of the y tick labels
plt.rc('legend', fontsize=legendsize)  # fontsize of the legend

dataframe_dir_ml = r'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\dataframes\ML'
dataframe_dir_results = rf"M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\results"
dataframe_dir_ml_labeled = f'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\dataframes\ML\labled_data'
dataframe_dir_ml_labeled_selected = f'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\dataframes\ML\labled_data\labled'
dataframe_dir_ml_labeled_all = f'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\dataframes\ML\labled_data\labled_all'
dataframe_dir_ml_labeled_m = f'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\dataframes\ML\labled_data\labled_first_more'


def svm_classifier(x, y, filename, report_df):
    print("***SVM***")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    # svclassifier = SVC(kernel='rbf')
    svclassifier = SVC(kernel='sigmoid')
    svclassifier.fit(x_train, y_train)

    y_predict = svclassifier.predict(x_test)

    print("-----report----------")
    print(metrics.classification_report(y_test, y_predict))  # output_dict=True))
    report = pd.DataFrame.from_dict(metrics.classification_report(y_test, y_predict, output_dict=True))
    report['target'] = filename
    report['algorithm'] = "SVM"

    print("-----score----------")
    score = metrics.accuracy_score(y_test, y_predict)
    print(score)
    report['score'] = score

    print("---------confusion matrix--------")
    cm = confusion_matrix(y_test, y_predict)
    print(cm)

    return pd.concat([report_df, report])


def naive_bayes_classifier(x, y, filename, report_df):
    print("naive bayes")
    labels = y.unique()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    NB = GaussianNB()
    NB.fit(x_train, y_train)

    # Predict Output
    y_predict = NB.predict(x_test)

    print("-----report----------")
    print(metrics.classification_report(y_test, y_predict))  # output_dict=True))
    report = pd.DataFrame.from_dict(metrics.classification_report(y_test, y_predict, output_dict=True))
    report['target'] = filename
    report['algorithm'] = "naive_bayes"

    print("-----score----------")
    score = metrics.accuracy_score(y_test, y_predict)
    print(score)
    report['score'] = score

    print("---------confusion matrix--------")
    cm = confusion_matrix(y_test, y_predict)
    print(cm)

    return pd.concat([report_df, report])


def kNeighbors_classifier(x, y, filename, report_df):
    print('***KNeighborsClassifier***')
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    KNN = KNeighborsClassifier(n_neighbors=3)
    # fit the model
    KNN.fit(x_train, y_train)

    # Predict Output
    y_predict = KNN.predict(x_test)

    print("-----report----------")
    print(metrics.classification_report(y_test, y_predict))  # output_dict=True))
    report = pd.DataFrame.from_dict(metrics.classification_report(y_test, y_predict, output_dict=True))
    report['target'] = filename
    report['algorithm'] = "KNN"

    print("-----score----------")
    score = metrics.accuracy_score(y_test, y_predict)
    print(score)
    report['score'] = score

    print("---------confusion matrix--------")
    cm = confusion_matrix(y_test, y_predict)
    print(cm)

    return pd.concat([report_df, report])


def random_forest_classifier(x, y, filename, report_df):
    print('***Random Forest***')

    feature_list = x.columns  # list(x_features.columns)
    print('feature length:', len(feature_list))

    x_train_features, x_test_features, y_train_labels, y_test_labels = train_test_split(x, y, test_size=0.25, random_state=42)

    forest = RandomForestClassifier(criterion='gini', n_estimators=5, random_state=42, n_jobs=2)
    # BalancedRandomForestClassifier(n_estimators=10)
    forest.fit(x_train_features, y_train_labels)

    print(forest.classes_)

    y_predict = forest.predict(x_test_features)

    print("-----report----------")
    print(metrics.classification_report(y_test_labels, y_predict))  # output_dict=True))
    report = pd.DataFrame.from_dict(metrics.classification_report(y_test_labels, y_predict, output_dict=True))
    report['target'] = filename
    report['algorithm'] = "random_forest"

    print("-----score----------")
    score = metrics.accuracy_score(y_test_labels, y_predict)
    print(score)
    report['score'] = score

    print("---------confusion matrix--------")
    cm = confusion_matrix(y_test_labels, y_predict)
    print(cm)

    print("-------importance--------")
    importance = pd.DataFrame({'feature': feature_list, 'importance': np.round(forest.feature_importances_, 3)})
    importance.sort_values('importance', ascending=False, inplace=True)
    print(importance)
    importance.to_csv(fr'{dataframe_dir_results}\feature_importance\{filename}-randomForest_f_importance.csv')

    print("---------------SHAP PLOTS-------------")
    print(f'0: {forest.classes_[0]}, 1: {forest.classes_[1]}')
    # forest.classes_ = ['no_rabbithole' 'rabbit_hole']
    explainer = shap.TreeExplainer(forest)
    shap_values = explainer.shap_values(x_train_features, check_additivity=False)
    print(type(x_train_features))

    plt.figure()
    fig = plt.figure(dpi=200)
    shap.summary_plot(shap_values[0], x_train_features, plot_type="bar", max_display=30, show=False)
    plt.title("Random Forest - Shap values 0")
    fig.tight_layout()
    matplotlib.rcParams["figure.dpi"] = 200
    plt.show()

    fig = plt.figure(dpi=200)
    shap.summary_plot(shap_values[0], x_train_features, plot_type="dot", max_display=30, show=False)
    plt.title("Random Forest - Shap values 0")
    fig.tight_layout()
    plt.show()

    fig = plt.figure(dpi=200)
    shap.summary_plot(shap_values[1], x_train_features, plot_type="bar", max_display=30, show=False)
    plt.title("Random Forest - Shap values 1")
    fig.tight_layout()
    plt.show()

    fig = plt.figure(dpi=200)
    shap.summary_plot(shap_values[1], x_train_features, plot_type="dot", max_display=30, show=False)
    plt.title("Random Forest - Shap values 1")
    fig.tight_layout()
    plt.show()

    # shap.summary_plot(shap_values[1], features=x_train_features, plot_type='dot', feature_names=feature_list) #, max_display=features_list_g.shape[0])
    # shap.summary_plot(shap_values[0], x_train_features, plot_type='layered_violin', max_display=30)
    # plt.show()

    return pd.concat([report_df, report])


def decision_tree_classifier(x, y, filename, report_df):
    print('***Decision tree***')
    feature_list = x.columns
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    clf_model = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=42, min_samples_leaf=5)
    clf_model.fit(x_train, y_train)

    y_predict = clf_model.predict(x_test)

    print("-----report----------")
    print(metrics.classification_report(y_test, y_predict))  # output_dict=True), file=f)
    report = pd.DataFrame.from_dict(metrics.classification_report(y_test, y_predict, output_dict=True))
    report['target'] = filename
    report['algorithm'] = "decision_tree"  # 'str' + df['col'].astype(str)

    print("-----score----------")
    score = metrics.accuracy_score(y_test, y_predict)
    print(score)
    report['score'] = score

    print("---------confusion matrix--------")
    cm = confusion_matrix(y_test, y_predict)
    print(cm)

    print("-------importance--------")
    importance = pd.DataFrame({'feature': x_train.columns, 'importance': np.round(clf_model.feature_importances_, 3)})
    importance.sort_values('importance', ascending=False, inplace=True)
    importance.reset_index(drop=True, inplace=True)
    print(importance)
    importance.to_csv(fr'{dataframe_dir_results}\feature_importance\{filename}-decision_tree_f_importance.csv')
    print(type(report_df))
    print(type(report))

    print("---------------SHAP PLOTS-------------")
    print(f'0: {clf_model.classes_[0]}, 1: {clf_model.classes_[1]}')
    # forest.classes_ = ['no_rabbithole' 'rabbit_hole']
    explainer = shap.TreeExplainer(clf_model)
    shap_values = explainer.shap_values(x_train)

    print(type(x_train))
    plt.show()

    plt.figure()

    # plt.figure()
    shap.summary_plot(shap_values[0], x_train, plot_type="bar", max_display=15, show=False)
    plt.title("Decision Tree - Shap values 0")
    plt.show()

    shap.summary_plot(shap_values[0], x_train, plot_type="dot", max_display=15, show=False)
    plt.title("Decision Tree - Shap values 0")
    plt.show()

    shap.summary_plot(shap_values[1], x_train, plot_type="bar", max_display=15, show=False)
    plt.title("Decision Tree - Shap values 1")
    plt.show()

    shap.summary_plot(shap_values[1], x_train, plot_type="dot", max_display=15, show=False)
    plt.title("Decision Tree - Shap values 1")
    plt.show()

    print(type(feature_list))
    return pd.concat([report_df, report])


def dt_grid_search(X, y):
    print("grid_search")
    std_slc = StandardScaler()
    pca = decomposition.PCA()
    dec_tree = DecisionTreeClassifier()

    pipe = Pipeline(steps=[('std_slc', std_slc),
                           ('pca', pca),
                           ('dec_tree', dec_tree)])
    n_components = list(range(1, X.shape[1] + 1, 1))
    criterion = ['gini', 'entropy']
    max_depth = [2, 4, 6, 8, 10, 12]

    parameters = dict(pca__n_components=n_components,
                      dec_tree__criterion=criterion,
                      dec_tree__max_depth=max_depth)
    pram = {"criterion": criterion,
            "max_depth": max_depth,
            "min_samples_split": range(1, 10),
            "min_samples_lead": range(1, 5)}

    clf_GS = GridSearchCV(dec_tree, param_grid=pram, cv=10)
    clf_GS.fit(X, y)

    print('Best Criterion:', clf_GS.best_estimator_.get_params()['criterion'])
    print('Best max_depth:', clf_GS.best_estimator_.get_params()['max_depth'])
    print('min_samplesplit:', clf_GS.best_estimator_.get_params()['min_samples_split'])
    print('min samples_lead:', clf_GS.best_estimator_.get_params()['min_samples_lead'])
    print()
    print(clf_GS.best_estimator_.get_params()['dec_tree'])


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    report_all = pd.DataFrame()

    path = fr'{dataframe_dir_ml_labeled}\user-sessions_features_all_labled_more_than_intention_normal_age_no_esm_no_personal.pickle'
    # path = fr'{dataframe_dir_ml_labeled}\user-sessions_features_all_labled_more_than_intention_normal_age_no_esm.pickle'

    print(f'###################  target: {path}   #############################')  # , file=f)
    df_sessions = pd.read_pickle(path)
    x, y = ML_helpers.prepare_df_undersampling(df_sessions)

    filename = "more_than_intention"

    report_all = decision_tree_classifier(x, y, filename, report_all)

    report_all = random_forest_classifier(x, y, filename, report_all)

    report_all = naive_bayes_classifier(x, y, filename, report_all)

    report_all = kNeighbors_classifier(x, y, filename, report_all)

    report_all = svm_classifier(x, y, filename, report_all)

    eport_all.to_csv(fr'{dataframe_dir_ml}\report_ml_undersampling_combined_test_no_personal_more1.csv')
