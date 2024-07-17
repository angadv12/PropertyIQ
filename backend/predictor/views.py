import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HouseListingSerializer
from .models import HouseListing
import joblib
from sklearn.preprocessing import LabelEncoder
from django.utils import timezone
import os
from django.conf import settings
from math import ceil

class PredictPrice(APIView):
    def post(self, request, pk, format=None):
        try:
            # Retrieve the house listing by primary key (pk)
            house_listing = HouseListing.objects.get(pk=pk)
            
            # Load your model
            base_dir = os.path.dirname(settings.BASE_DIR)  # This will give you the directory one level up from BASE_DIR
            model_path = os.path.join(base_dir, 'mL_model', 'best_xgb_model.joblib')
            feature_names_path = os.path.join(base_dir, 'mL_model', 'feature_names.joblib')

            model = joblib.load(model_path)
            feature_names = joblib.load(feature_names_path)
            
            # Get the feature names used by the model
            model_features = model.get_booster().feature_names
            
            # Prepare input data
            input_data = {k: v for k, v in house_listing.__dict__.items() if k in model_features}
            
            # Convert to DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Apply any necessary feature engineering
            input_df = self.engineer_features(input_df)

            input_df = self.convert_to_numerical(input_df)

            # Reorder columns to match model's expected order
            input_df = input_df[feature_names]
            
            # Make prediction
            prediction = model.predict(input_df)

            # Update the house listing with the predicted price
            house_listing.predicted_price = ceil(prediction[0] * 100) / 100.0
            house_listing.save()

            return Response({
                'predicted_price': prediction[0],
                'listing_id': house_listing.id
            })
        
        except HouseListing.DoesNotExist:
            return Response({'error': 'House listing not found'}, status=404)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def engineer_features(self, df):
        current_year = timezone.now().year
        df['Age'] = current_year - df['YearBuilt']
        if 'YearRemodAdd' in df.columns:
            df['RemodAge'] = current_year - df['YearRemodAdd']
        return df
    
    def convert_to_numerical(self, df):
        # convert remaining categorical using Label Encoding
        label_encoders = {}
        categorical_cols = df.select_dtypes(include=['object']).columns

        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            df[col] = label_encoders[col].fit_transform(df[col])
        return df