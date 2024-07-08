import tensorflow as tf
import tensorflow_decision_forests as tfdf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

train_fp = "train.csv"
train_df = pd.read_csv(train_fp)
train_df = train_df.drop('Id', axis=1)
print(train_df.head(3))
train_df.info()

print(train_df['SalePrice'].describe())

# split the dataset
def split_dataset(dataset, test_ratio=0.30, random_state=None):
  if random_state is not None:
        np.random.seed(random_state) # if random state is set, then make reproducible
  test_indices = np.random.rand(len(dataset)) < test_ratio
  return dataset[~test_indices], dataset[test_indices]

train_ds_pd, test_ds_pd = split_dataset(train_df, random_state=10)
print("{} examples in training, {} examples in testing.".format(
    len(train_ds_pd), len(test_ds_pd)))

# convert pandas dataframe to tensorflow dataset
label = 'SalePrice'
training_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_ds_pd, label=label, task = tfdf.keras.Task.REGRESSION)
validation_ds = tfdf.keras.pd_dataframe_to_tf_dataset(test_ds_pd, label=label, task = tfdf.keras.Task.REGRESSION)

# define the model
rfm = tfdf.keras.RandomForestModel(task = tfdf.keras.Task.REGRESSION, num_trees=1000)
rfm.compile(metrics=["mae"])

# train the model
rfm.fit(x=training_ds)

# evaluate the model
inspector = rfm.make_inspector()
print(inspector.evaluation())

evaluation = rfm.evaluate(x=validation_ds,return_dict=True)
for name, value in evaluation.items():
  print(f"{name}: {value:.4f}")

# # feature importances
# importance = inspector.variable_importances()["NUM_AS_ROOT"]

# # Create a dictionary of feature importances
# feature_importance_dict = {}
# for item in importance:
#     feature_name = item[0].name  # Extract the feature name
#     feature_importance_dict[feature_name] = item[1]  # Assign the importance value
        
# # Add any missing features with zero importance
# all_features = set(train_df.columns) - {label}
# for feature in all_features:
#     if feature not in feature_importance_dict:
#         feature_importance_dict[feature] = 0

# # Sort features by importance
# sorted_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

# # Print feature importances
# print("Feature Importances:")
# for feature, score in sorted_importances:
#     print(f"{feature}: {score:.4f}")

# LOAD TEST DATA #
test_file_path = "test.csv"
test_data = pd.read_csv(test_file_path)

ids = test_data.pop('Id')

# Convert test pandas dataframe to tf dataset
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    test_data,
    task = tfdf.keras.Task.REGRESSION)

# Make predictions
preds = rfm.predict(test_ds)

# Create a submission dataframe
output = pd.DataFrame({'Id': ids,
                       'SalePrice': preds.squeeze()})

print(output.head())

# Save submission to CSV
output.to_csv('submissionTf.csv', index=False)