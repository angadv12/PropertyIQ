![Alt text](/frontend/src/assets/PropertyIQHomePage.png "Home Page")

# GameFeed

Platform for listing & viewing properties and predicting their prices.

## Description

PropertyIQ is a platform where users can list their properties as well as view other properties. The platform is built on a Django backend with rest_framework, and a ReactJS frontend. Additioanlly, Tailwind CSS was employed for styling and jsonwebtoken (JWT) for user authorization. Most importantly, the platform incorporates an XGBoost (Extreme Gradient Boosting) predictor model to implement the price predicting feature. This XGBoost model was finetuned through hundreds of trials to select the best hyperparameters through Optuna, a library for hyperparameter optimization. Several versions of feature engineering had to be created, various methods of dataset manipulation, as well as several unique models being developed prior to settling on the most-accurate XGBoost model.

## Features

- Create listings of your own properties
![Alt text](/frontend/src/assets/CreateListing.gif "Your Listings View")
- Predict the price of your listing, powered by ML
![Alt text](/frontend/src/assets/PredictPrice.gif "Predict Price View")
- User authentication and profile management
![Alt text](/frontend/src/assets/PageProfile.png "Profile View")
- Interaction with other users' listings
![Alt text](/frontend/src/assets/OtherListings.gif "Other Listings View")

## Contributing
Contributions are welcome! To contribute to PropertyIQ, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.

## License
This project is licensed under the MIT License

## Acknowledgments
- Sci-kit Learn
- Optuna
- XGBoost 
- Django
- React
- Vite
- Tailwind CSS