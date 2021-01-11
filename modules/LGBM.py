import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.model_selection import KFold

quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
lgb_params = {
    'n_estimators':5000,
    'learning_rate':0.02,
    'feature_fraction': 0.7
}

def LGBM(q, X_train, Y_train, X_valid, Y_valid):  
    model = LGBMRegressor(objective='quantile', alpha=q, **lgb_params)                        
    model.fit(X_train, Y_train, eval_metric = ['quantile'],
          eval_set=[(X_valid, Y_valid)], early_stopping_rounds=300, verbose=500)
    loss = model.best_score_['valid_0']['quantile']
    return model, loss

def train_model(X_train, Y_train, X_valid, Y_valid):
    print("Training LightGB Model .. ")
    models=[]
    totalLoss = 0
    for q in quantiles:
        print(f"quantile: {q}")
        model,loss = LGBM(q, X_train, Y_train, X_valid, Y_valid)
        models.append(model)
        totalLoss += loss
    return models, totalLoss

def predict_data(models, X_test):
    predictions = pd.DataFrame()
    for model in models:
        pred = pd.Series(model.predict(X_test).round(2))
        predictions = pd.concat([predictions,pred],axis=1)
    predictions.columns = quantiles
    return predictions

def kFold_train_and_predict(origin_X_train, origin_Y_train, X_test):
    kfold = KFold(n_splits=4,shuffle=True, random_state=0)
    result = pd.DataFrame()
    totalLoss = 0
    for idx, (train_idx, valid_idx) in enumerate(kfold.split(origin_X_train)):
        print(f"==={idx}st kFold..")
        X_train, X_valid = origin_X_train.iloc[train_idx], origin_X_train.iloc[valid_idx]
        Y_train, Y_valid = origin_Y_train.iloc[train_idx], origin_Y_train.iloc[valid_idx]
        models, loss = train_model(X_train, Y_train, X_valid, Y_valid)
        predictions = predict_data(models, X_test)
        totalLoss += loss
        if idx == 0:
            result = predictions
        else:
            result = result+predictions
    return (result / 4), totalLoss