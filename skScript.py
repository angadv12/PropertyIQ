from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

# load data
data_fp = "train.csv"
data = pd.read_csv(data_fp)

# separate features and target vars
X = data.drop(['SalePrice', 'Id'], axis=1) # features
y = data['SalePrice'] # target

# separate columns by categorical and numerical data
data.info()
categorical_cols = [cname for cname in X.columns if X[cname].dtype == "object"]
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]

# numerical preprocessing
numerical_transformer = SimpleImputer(strategy='mean') # fill missing values

# categorical preprocessing
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # fill missing values
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # convert categorical to numerical
])

# bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
])

# define model
model = RandomForestRegressor(n_estimators=100, random_state=0) # 100 trees

# create and evaluate the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

# split data - training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# preprocess trainig data and fit model
pipeline.fit(X_train, y_train)

# preprocess validation data and predict
preds = pipeline.predict(X_valid)

# evaluate model
rmse = np.sqrt(mean_squared_error(y_valid, preds))
print('RMSE:', rmse)
