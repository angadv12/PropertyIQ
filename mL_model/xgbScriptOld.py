from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import optuna
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import joblib

# LOAD TRAINING DATA #
data=pd.read_csv('train.csv')
print(data.head())

# define feature classifications
quality_mapping = {
        'Ex': 5,
        'Gd': 4,
        'TA': 3,
        'Fa': 2,
        'Po': 1,
    }
quality_features = ['ExterQual', 'ExterCond', 'HeatingQC', 'KitchenQual']
col_keep_mode_impute = ['MSZoning', 'Utilities', 'Electrical', 'Exterior1st', 'Exterior2nd', 'KitchenQual', 'Functional', 'SaleType']
col_keep_zero_fill = ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
                          'BsmtFullBath', 'BsmtHalfBath', 'GarageCars', 'GarageArea']
# handle missing values
def handle_missing_values(df):
    missing_data = df.isnull().sum()
    cols_to_drop = missing_data[missing_data > 5].index
    print("cols to drop: ", cols_to_drop)
    cols_to_keep = missing_data[(missing_data > 0) & (missing_data <= 5)].index
    print("cols to keep: ", cols_to_keep)
    df = df.drop(columns=cols_to_drop)

    for col in cols_to_keep:
        if col in col_keep_mode_impute:
            df[col] = df[col].fillna(df[col].mode()[0])
        elif col in col_keep_zero_fill:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna(df[col].mean())

    print('Missing values left:', df.isnull().sum().max())
    return df

# feature engineering
def engineer_features(df):
    df['Age'] = df['YrSold'] - df['YearBuilt']
    df['RemodAge'] = df['YrSold'] - df['YearRemodAdd']
    
    return df

# convert categorical features to numerical
def convert_to_numerical(df):
    for feature in quality_features:
        df[feature] = df[feature].map(quality_mapping)

    # convert remaining categorical using Label Encoding
    label_encoders = {}
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col])
    return df

# call preprocessing functions
data = handle_missing_values(data)
data = engineer_features(data)
data = convert_to_numerical(data)

# examine correlation with target variable
print(data.corr()['SalePrice'].sort_values(ascending=False))

# separate features and target variables
X = data.drop(['SalePrice', 'Id'], axis=1)
y = data['SalePrice']

# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# define objective function for optuna tuning
def objective(trial):
    
    param = {
        'lambda': trial.suggest_float('lambda', 1e-3, 10.0, log=True),
        'alpha': trial.suggest_float('alpha', 1e-3, 10.0, log=True),
        'colsample_bytree': trial.suggest_categorical('colsample_bytree', [0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1.0]),
        'subsample': trial.suggest_categorical('subsample', [0.4,0.5,0.6,0.7,0.8,1.0]),
        'learning_rate': trial.suggest_categorical('learning_rate', [0.008,0.01,0.012,0.014,0.016,0.018, 0.02]),
        'n_estimators': 10000,
        'max_depth': trial.suggest_categorical('max_depth', [5,7,9,11,13,15,17]),
        'random_state': trial.suggest_categorical('random_state', [2020]),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 300),
        'early_stopping_rounds': 100
    }
    model = XGBRegressor(**param)  
    
    model.fit(X_train,y_train,eval_set=[(X_test,y_test)],verbose=False)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    return rmse

# run optuna study to tune hyperparameters
study = optuna.create_study(direction='minimize', sampler=optuna.samplers.RandomSampler(seed=42))
study.optimize(objective, n_trials=1000)

# print best hyperparameters and score
best_params = study.best_params
best_score = study.best_value
print(f"Best Hyperparameters: {best_params}")
print(f"Best Accuracy: {best_score:.3f}")

# PLOTTING DONE IN JUPYTER NOTEBOOK,NOT HERE #

#fetching the best values
best_lambda = best_params['lambda']
best_alpha = best_params['alpha']
colsample_bytree = best_params['colsample_bytree']
subsample = best_params['subsample']
learning_rate = best_params['learning_rate']
max_depth = best_params['max_depth']
random_state = best_params['random_state']
min_child_weight = best_params['min_child_weight']

# defining model with best hyperparameters
best_model = XGBRegressor(
    reg_lambda=best_lambda,
    alpha=best_alpha,
    colsample_bytree=colsample_bytree,
    subsample=subsample,
    learning_rate=learning_rate,
    max_depth=max_depth,
    random_state=random_state,
    min_child_weight=min_child_weight,
    n_estimators=1000
)

# fitting model on training data
best_model.fit(X_train, y_train)

# Save the model
joblib.dump(best_model, 'best_xgb_modelOld.joblib')
print("Model saved as 'best_xgb_modelOld.joblib'")

# Load the model (for demonstration)
loaded_model = joblib.load('best_xgb_modelOld.joblib')
print("Model loaded successfully")

# evaluate model and show metrics
y_pred = loaded_model.predict(X_test)

print('mae: ', mean_absolute_error(y_test, y_pred))
print('mse: ', mean_squared_error(y_test, y_pred))
print('rmse: ', np.sqrt(mean_squared_error(y_test, y_pred)))
print('R²: ', r2_score(y_test, y_pred))
r2_scores = cross_val_score(loaded_model, X_test, y_test, n_jobs=-1, cv=5, scoring='r2')
mean_r2_score = r2_scores.mean()
print("Mean R² score:", mean_r2_score)

# Load test data
test_file_path = "./test.csv"
test_data = pd.read_csv(test_file_path)

# Handle missing values in test data
test_data = handle_missing_values(test_data)

# Feature engineering
test_data = engineer_features(test_data)

# Convert categorical features to numerical
test_data = convert_to_numerical(test_data)

# Separate features and IDs
X_test_final = test_data.drop('Id', axis=1)
test_ids = test_data['Id']

# Make predictions using the loaded model
preds = loaded_model.predict(X_test_final)

# Create submission dataframe
output = pd.DataFrame({'Id': test_ids, 'SalePrice': preds})

print(output.head())

# Save to csv
output.to_csv('submissionXGB_Old.csv', index=False)
print('Saved to "submissionXGB_Old.csv"')
