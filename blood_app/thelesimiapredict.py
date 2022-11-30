# Importing libraries
import numpy as np
import pandas as pd
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from django.conf import settings
from django.http import HttpResponse

def setdatapath():
    # Reading the train.csv by removing the
    # last column since it's an empty column
    DATA_PATH = str(settings.MEDIA_ROOT) + "/dataset/Training.csv"
    data = pd.read_csv(DATA_PATH)
    print(data)

    # Checking whether the dataset is balanced or not
    disease_counts = data["phenotype"].value_counts()
    temp_df = pd.DataFrame({
        "Disease": disease_counts.index,
        "Counts": disease_counts.values
    })

    # plt.figure(figsize=(18, 8))
    # sns.barplot(x="Disease", y="Counts", data=temp_df)
    # plt.xticks(rotation=90)
    # plt.show()


    encoder = LabelEncoder()
    data["phenotype"] = encoder.fit_transform(data["phenotype"])

    X = data.iloc[:, :-1]
    print("Bhuwan x is this  = ", X)
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=24)

    print(f"Train: {X_train.shape}, {y_train.shape}")
    print(f"Test: {X_test.shape}, {y_test.shape}")


    # Defining scoring metric for k-fold cross validation
    def cv_scoring(estimator, X, y):
        return accuracy_score(y, estimator.predict(X))


    # Initializing Models
    models = {
        "SVC": SVC(),
        "Gaussian NB": GaussianNB(),
        "Random Forest": RandomForestClassifier(random_state=18)
    }

    # Producing cross validation score for the models
    for model_name in models:
        model = models[model_name]
        scores = cross_val_score(model, X, y, cv=10,
                                 n_jobs=-1,
                                 scoring=cv_scoring)
        print("==" * 30)
        print(model_name)
        print(f"Scores: {scores}")
        print(f"Mean Score: {np.mean(scores)}")

    # Training and testing SVM Classifier
    svm_model = SVC()
    svm_model.fit(X_train, y_train)
    preds = svm_model.predict(X_test)

    print(f"Accuracy on train data by SVM Classifier\
    : {accuracy_score(y_train, svm_model.predict(X_train)) * 100}")

    print(f"Accuracy on test data by SVM Classifier\
    : {accuracy_score(y_test, preds) * 100}")
    cf_matrix = confusion_matrix(y_test, preds)
    # plt.figure(figsize=(12, 8))
    # sns.heatmap(cf_matrix, annot=True)
    # plt.title("Confusion Matrix for SVM Classifier on Test Data")
    # plt.show()

    # Training and testing Naive Bayes Classifier
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    preds = nb_model.predict(X_test)
    print(f"Accuracy on train data by Naive Bayes Classifier\
    : {accuracy_score(y_train, nb_model.predict(X_train)) * 100}")

    print(f"Accuracy on test data by Naive Bayes Classifier\
    : {accuracy_score(y_test, preds) * 100}")
    cf_matrix = confusion_matrix(y_test, preds)
    # plt.figure(figsize=(12, 8))
    # sns.heatmap(cf_matrix, annot=True)
    # plt.title("Confusion Matrix for Naive Bayes Classifier on Test Data")
    # plt.show()

    # Training and testing Random Forest Classifier
    rf_model = RandomForestClassifier(random_state=18)
    rf_model.fit(X_train, y_train)
    preds = rf_model.predict(X_test)
    print(f"Accuracy on train data by Random Forest Classifier\
    : {accuracy_score(y_train, rf_model.predict(X_train)) * 100}")

    print(f"Accuracy on test data by Random Forest Classifier\
    : {accuracy_score(y_test, preds) * 100}")

    cf_matrix = confusion_matrix(y_test, preds)



    final_svm_model = SVC()
    final_nb_model = GaussianNB()
    final_rf_model = RandomForestClassifier(random_state=18)
    final_svm_model.fit(X, y)
    final_nb_model.fit(X, y)
    final_rf_model.fit(X, y)


    test_data = pd.read_csv(DATA_PATH)

    test_X = test_data.iloc[:, :-1]
    test_Y = encoder.transform(test_data.iloc[:, -1])


    svm_preds = final_svm_model.predict(test_X)
    nb_preds = final_nb_model.predict(test_X)
    rf_preds = final_rf_model.predict(test_X)
    final_preds = [mode([i, j, k])[0][0] for i, j,
                                             k in zip(svm_preds, nb_preds, rf_preds)]

    print(f"Accuracy on Test dataset by the combined model\
    : {accuracy_score(test_Y, final_preds) * 100}")

    cf_matrix = confusion_matrix(test_Y, final_preds)


    symptoms = X.columns.values
    symptom_index = {}
    for index, value in enumerate(symptoms):
        symptom = " ".join([i.capitalize() for i in value.split("_")])
        symptom_index[symptom] = index

    data_dict = {
        "symptom_index": symptom_index,
        "predictions_classes": encoder.classes_
    }

    return data_dict, final_rf_model, final_nb_model, final_svm_model, accuracy_score(test_Y, final_preds) * 100

def changeint(myli):
    datali = []
    for i in myli:
        datali.append(float(i))
    return datali

def predictDisease(symptoms):
    data_dict, final_rf_model, final_nb_model, final_svm_model, accuracy_score = setdatapath()
    # symptoms = symptoms.split(",")
    print(symptoms)
    symptoms = changeint(symptoms)
    symptoms = [symptoms]

    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(symptoms)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(symptoms)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(symptoms)[0]]

    # making final prediction by taking mode of all predictions
    DESEASE = ((0, 'Alpha thalasemia'), (1, 'beta thalasemia'), (2, 'normal'))

    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
    rf_prediction = DESEASE[rf_prediction][1]
    nb_prediction = DESEASE[nb_prediction][1]
    svm_prediction = DESEASE[svm_prediction][1]
    final_prediction = DESEASE[final_prediction][1]
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }
    return predictions, accuracy_score