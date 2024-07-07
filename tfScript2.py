import tensorflow as tf
import tensorflow_decision_forests as tfdf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

# Load data
train_fp = "train.csv"
train_df = pd.read_csv(train_fp)

# Handle missing values
train_df['Electrical'] = train_df['Electrical'].ffill()

# Mode imputation for categorical features
cat_features = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageType', 
                'GarageFinish', 'GarageQual', 'GarageCond', 'BsmtExposure', 'BsmtFinType2', 
                'BsmtFinType1', 'BsmtCond', 'BsmtQual', 'MasVnrType']
for col in cat_features:
    train_df[col] = train_df[col].fillna('None')

# Mean/median imputation for numerical features
train_df['LotFrontage'] = train_df['LotFrontage'].fillna(train_df['LotFrontage'].mean())
train_df['MasVnrArea'] = train_df['MasVnrArea'].fillna(train_df['MasVnrArea'].median())
train_df['GarageYrBlt'] = train_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].median())

# Verify that there are no more missing values
missing_values_after = train_df.isnull().sum()
missing_values_after = missing_values_after[missing_values_after > 0].sort_values(ascending=False)
print('Missing values left:', len(missing_values_after))

# Feature engineering
train_df['Age'] = train_df['YrSold'] - train_df['YearBuilt']
train_df['RemodAge'] = train_df['YrSold'] - train_df['YearRemodAdd']

# Drop Id and separate features and target vars
X = train_df.drop(['SalePrice', 'Id'], axis=1)
y = train_df['SalePrice']

# Identify numerical and categorical columns
# numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
# categorical_features = X.select_dtypes(include=['object']).columns

# Convert categorical variables to numerical
X = pd.get_dummies(X)

# Normalize numerical features
scaler = StandardScaler()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
X[numerical_features] = scaler.fit_transform(X[numerical_features])

# # Convert categorical variables to string type
# for col in categorical_features:
#     X[col] = X[col].astype(str)


# # Split the dataset
# def split_dataset(X, y, test_ratio=0.20, random_state=None):
#     if random_state is not None:
#         np.random.seed(random_state)
#     test_indices = np.random.rand(len(X)) < test_ratio
#     X_train, X_test = X[~test_indices], X[test_indices]
#     y_train, y_test = y[~test_indices], y[test_indices]
#     return X_train, X_test, y_train, y_test

X.info()
bool_cols = X.select_dtypes(include=['bool']).columns
print('BOOL COLUMNS: ', bool_cols)
X[bool_cols] = X[bool_cols].astype(int)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

print(f"{len(X_train)} examples in training, {len(X_test)} examples in testing.")

# # Combine features and label for training and testing sets
# train_ds_pd = X_train.copy()
# train_ds_pd['SalePrice'] = y_train
# test_ds_pd = X_test.copy()
# test_ds_pd['SalePrice'] = y_test
train_ds_pd = pd.concat([X_train, y_train], axis=1)
valid_ds_pd = pd.concat([X_test, y_test], axis=1)

# Convert pandas dataframe to tensorflow dataset
training_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_ds_pd, label='SalePrice', task=tfdf.keras.Task.REGRESSION)
validation_ds = tfdf.keras.pd_dataframe_to_tf_dataset(valid_ds_pd, label='SalePrice', task=tfdf.keras.Task.REGRESSION)

# Define the model
model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.REGRESSION, num_trees=1000)
model.compile(metrics=["mse"])

# Train the model
model.fit(x=training_ds)
y_pred = model.predict(validation_ds)
print("RMSE:", root_mean_squared_error(y_test, y_pred))

# Evaluate the model
inspector = model.make_inspector()
print(inspector.evaluation())

# evaluation = model.evaluate(validation_ds, return_dict=True)
# for name, value in evaluation.items():
#     print(f"{name}: {value:.4f}")
#     if name == "mse":
#         print(f"rmse: {np.sqrt(value):.4f}")

# Feature importances
importance = inspector.variable_importances()["NUM_AS_ROOT"]

# Create a dictionary of feature importances
feature_importance_dict = {}
for item in importance:
    feature_name = item[0].name  # Extract the feature name
    feature_importance_dict[feature_name] = item[1]  # Assign the importance value

# Add any missing features with zero importance
all_features = set(X.columns)
for feature in all_features:
    if feature not in feature_importance_dict:
        feature_importance_dict[feature] = 0

# Sort features by importance
sorted_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

# Print feature importances
print("Top 10 Feature Importances:")
for feature, score in sorted_importances[0:10]:
    print(f"{feature}: {score:.4f}")

# Load test data
test_file_path = "test.csv"
test_data = pd.read_csv(test_file_path)
test_ids = test_data['Id']

# Handle missing values in test data
test_data['Electrical'] = test_data['Electrical'].ffill()

for col in cat_features:
    test_data[col] = test_data[col].fillna('None')

test_data['LotFrontage'] = test_data['LotFrontage'].fillna(test_data['LotFrontage'].mean())
test_data['MasVnrArea'] = test_data['MasVnrArea'].fillna(test_data['MasVnrArea'].median())
test_data['GarageYrBlt'] = test_data['GarageYrBlt'].fillna(test_data['GarageYrBlt'].median())

# Feature engineering
test_data['Age'] = test_data['YrSold'] - test_data['YearBuilt']
test_data['RemodAge'] = test_data['YrSold'] - test_data['YearRemodAdd']

# Drop Id
X_test_final = test_data.drop('Id', axis=1)

# Convert categorical variables to numerical
X_test_final = pd.get_dummies(X_test_final)

# Align the train and test data
X_test_final = X_test_final.reindex(columns=X.columns, fill_value=0)

# Normalize numerical features
X_test_final[numerical_features] = scaler.transform(X_test_final[numerical_features])

bool_cols_test = X_test_final.select_dtypes(include=['bool']).columns
X_test_final[bool_cols_test] = X_test_final[bool_cols_test].astype(int)

# Convert to TensorFlow dataset
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(X_test_final, task=tfdf.keras.Task.REGRESSION)

# Make predictions
preds = model.predict(test_ds)

# Create submission dataframe
output = pd.DataFrame({'Id': test_ids, 'SalePrice': preds.squeeze()})

print(output.head())

# Save to csv
output.to_csv('submissionTf2.csv', index=False)
print('saved to "submissionTf2.csv"')