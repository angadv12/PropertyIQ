import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from keras import models
from keras import layers
from sklearn.metrics import mean_squared_error
import numpy as np

# LOAD DATA #
data = pd.read_csv('train.csv')

# HANDLE MISSING VALUES #
data['Electrical'] = data['Electrical'].ffill() # forward fill for 'Electrical' feature

# mode imputation for categorical features
for col in ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageType', 
            'GarageFinish', 'GarageQual', 'GarageCond', 'BsmtExposure', 'BsmtFinType2', 
            'BsmtFinType1', 'BsmtCond', 'BsmtQual', 'MasVnrType']:
    data[col] = data[col].fillna('None')

# mean/median imputation for numerical features
data['LotFrontage'] = data['LotFrontage'].fillna(data['LotFrontage'].mean())
data['MasVnrArea'] = data['MasVnrArea'].fillna(data['MasVnrArea'].median())
data['GarageYrBlt'] = data['GarageYrBlt'].fillna(data['GarageYrBlt'].median())

# Feature engineering
data['Age'] = data['YrSold'] - data['YearBuilt']
data['RemodAge'] = data['YrSold'] - data['YearRemodAdd']

# Drop the target variable and ID from features
X = data.drop(['SalePrice', 'Id'], axis=1) # features
y = data['SalePrice'] # target

# convert categorical variables to numerical
X = pd.get_dummies(X)

# normalize numerical features
scaler = StandardScaler()
numerical_features = X.select_dtypes(include=['float64', 'int64']).columns
X[numerical_features] = scaler.fit_transform(X[numerical_features])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# Define a simple neural network model
model = models.Sequential()
model.add(layers.Input(shape=(X_train.shape[1],)))  # Using Input layer
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))  # Single output for regression

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model with a specified number of epochs
epochs = 50
history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_split=0.2, verbose=1)

# Make predictions
y_pred = model.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)

# LOAD TEST DATA #
test_data = pd.read_csv('test.csv')

# HANDLE MISSING VALUES IN TEST DATA #
test_data['Electrical'] = test_data['Electrical'].ffill() # forward fill for 'Electrical' feature

# mode imputation for categorical features
for col in ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageType', 
            'GarageFinish', 'GarageQual', 'GarageCond', 'BsmtExposure', 'BsmtFinType2', 
            'BsmtFinType1', 'BsmtCond', 'BsmtQual', 'MasVnrType']:
    test_data[col] = test_data[col].fillna('None')

# mean/median imputation for numerical features
test_data['LotFrontage'] = test_data['LotFrontage'].fillna(test_data['LotFrontage'].mean())
test_data['MasVnrArea'] = test_data['MasVnrArea'].fillna(test_data['MasVnrArea'].median())
test_data['GarageYrBlt'] = test_data['GarageYrBlt'].fillna(test_data['GarageYrBlt'].median())

# Feature engineering
test_data['Age'] = test_data['YrSold'] - test_data['YearBuilt']
test_data['RemodAge'] = test_data['YrSold'] - test_data['YearRemodAdd']

# Drop the ID from features
test_ids = test_data['Id']
X_test_final = test_data.drop('Id', axis=1)

# convert categorical variables to numerical
X_test_final = pd.get_dummies(X_test_final)

# Align the train and test data
X_test_final = X_test_final.reindex(columns = X.columns, fill_value=0)

# normalize numerical features
X_test_final[numerical_features] = scaler.transform(X_test_final[numerical_features])

# Fill NaN values with 0 for basement and garage related features
basement_garage_features = ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'GarageCars', 'GarageArea']
X_test_final[basement_garage_features] = X_test_final[basement_garage_features].fillna(0)

# Make predictions
test_predictions = model.predict(X_test_final)

# Create submission dataframe
submission = pd.DataFrame({
    "Id": test_ids,
    "SalePrice": test_predictions.flatten()  # Ensure the predictions are in the correct shape
})

print('missing preds: ', np.isnan(submission['SalePrice']).sum()) # ensure no missing predictions

# Save submission to CSV
submission.to_csv('submissionNNtf.csv', index=False)