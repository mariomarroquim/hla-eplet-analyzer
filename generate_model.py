# Import libraries

import warnings; warnings.simplefilter('ignore')
import pandas                  as pd
import numpy                   as np
import sklearn.model_selection as ms
import sklearn.metrics         as mt
from imblearn.under_sampling   import RandomUnderSampler
from sklearn.ensemble          import RandomForestClassifier
from sklearn.model_selection   import RandomizedSearchCV
from joblib                    import dump, load

# Prepare datasets

rus = RandomUnderSampler()

instances_pe = pd.read_csv('./validation/datasets/pe-dataset.csv')
print('PE raw dataset:', instances_pe.shape)

cln_instances_pe = instances_pe.drop(columns=['panel_info', 'panel_eplet'])
print('PE cleaned dataset:', cln_instances_pe.shape)

imb_train_labels_pe = np.array(cln_instances_pe['reactive'])
imb_instances_pe = cln_instances_pe.drop(columns=['reactive'])
train_instances_pe, train_labels_pe = rus.fit_resample(imb_instances_pe, imb_train_labels_pe)

print('PE train instances:', train_instances_pe.shape)
print('PE train labels:', train_labels_pe.shape)

# Build production model

clf = RandomForestClassifier()

param_grid = {
  'n_estimators': [100, 200, 400],
  'criterion': ['gini', 'entropy'],
  'min_samples_split': [2, 4, 8],
  'min_samples_leaf': [1, 2, 4],
  'max_features': [None, 'auto', 'sqrt', 'log2']
}

params_search = RandomizedSearchCV(estimator=clf, param_distributions=param_grid, scoring='roc_auc', n_jobs=7)
params_search.fit(train_instances_pe, train_labels_pe)

production_model = params_search.best_estimator_

# Persist production model

dump(production_model, 'model.joblib')

# Test production model

test_model = load('model.joblib')

test_data = [[0, 1, 0, 0, 0, 0, 10, 1000, 1500]]

result = test_model.predict(test_data)
print('Test classification (should be 1): ' + str(result[0]))

probabilities = test_model.predict_proba(test_data)
print('Probability of being 0: ' + str(probabilities[0][0]))
print('Probability of being 1: ' + str(probabilities[0][1]))