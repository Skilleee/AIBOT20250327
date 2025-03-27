import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

def train_classification_models(X: np.ndarray, y: np.ndarray) -> dict:
    models = {}
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X, y)
    models['random_forest'] = rf
    
    gb = GradientBoostingClassifier(n_estimators=100)
    gb.fit(X, y)
    models['gradient_boosting'] = gb
    
    svm = SVC(probability=True)
    svm.fit(X, y)
    models['svm'] = svm
    
    return models

def classify_signals(models: dict, X_test: np.ndarray) -> dict:
    predictions = {}
    for name, model in models.items():
        predictions[name] = model.predict(X_test)
    return predictions
