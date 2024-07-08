import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

# LOAD DATA #
train_data = pd.read_csv('train.csv')

# HANDLE MISSING VALUES #
train_data['Electrical'] = train_data['Electrical'].ffill() # forward fill for 'Electrical' feature

# mode imputation for categorical features
for col in ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageType', 
            'GarageFinish', 'GarageQual', 'GarageCond', 'BsmtExposure', 'BsmtFinType2', 
            'BsmtFinType1', 'BsmtCond', 'BsmtQual', 'MasVnrType']:
    train_data[col] = train_data[col].fillna('None')

# mean/median imputation for numerical features
train_data['LotFrontage'] = train_data['LotFrontage'].fillna(train_data['LotFrontage'].mean())
train_data['MasVnrArea'] = train_data['MasVnrArea'].fillna(train_data['MasVnrArea'].median())
train_data['GarageYrBlt'] = train_data['GarageYrBlt'].fillna(train_data['GarageYrBlt'].median())

# Verify that there are no more missing values
missing_values_after = train_data.isnull().sum()
missing_values_after = missing_values_after[missing_values_after > 0].sort_values(ascending=False)
print('missing values left: ', len(missing_values_after))

# feature engineering
train_data['Age'] = train_data['YrSold'] - train_data['YearBuilt']
train_data['RemodAge'] = train_data['YrSold'] - train_data['YearRemodAdd']

# drop id and separate features and target vars
X = train_data.drop(['SalePrice', 'Id'], axis=1) # features
y = train_data['SalePrice'] # target

# convert categorical variables to numerical
X = pd.get_dummies(X)

# normalize numerical features
scaler = StandardScaler()
numerical_features = X.select_dtypes(include=['float64', 'int64']).columns
X[numerical_features] = scaler.fit_transform(X[numerical_features])

bool_cols = X.select_dtypes(include=['bool']).columns
print('BOOL COLUMNS: ', bool_cols)

# model training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

model = RandomForestRegressor(n_estimators=100, random_state=10)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("RMSE:", root_mean_squared_error(y_test, y_pred))

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

# feature engineering
test_data['Age'] = test_data['YrSold'] - test_data['YearBuilt']
test_data['RemodAge'] = test_data['YrSold'] - test_data['YearRemodAdd']

# drop id
test_ids = test_data['Id']
X_test_final = test_data.drop('Id', axis=1)

# convert categorical variables to numerical
X_test_final = pd.get_dummies(X_test_final)

# align the train and test data
X_test_final = X_test_final.reindex(columns = X.columns, fill_value=0)

# normalize numerical features
X_test_final[numerical_features] = scaler.transform(X_test_final[numerical_features])

# make predictions
test_predictions = model.predict(X_test_final)

# create submission dataframe
submission = pd.DataFrame({
    "Id": test_ids,
    "SalePrice": test_predictions
})

print(submission.head())

# Save to csv
submission.to_csv('submissionSk.csv', index=False)