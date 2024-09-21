Property Price Prediction Analysis

Overview

This project focuses on analyzing and predicting property prices in Sydney using a comprehensive dataset. By integrating data collection, processing, and advanced machine learning techniques, the codebase provides valuable insights for stakeholders in the real estate market, including investors, developers, and buyers.

Features
Data Loading: Imports property data from a CSV file sourced from Kaggle.
Postcode Enrichment: Utilizes the Gemini API to append postcode information to suburb names, enhancing data accuracy.
Suburb Ranking: Scrapes suburb rankings from domain.com.au based on various quality indicators such as traffic, access to schools, cafes, and proximity to the CBD.
Data Integration: Merges property data with suburb rankings to create a unified dataset for analysis.
Machine Learning Models: Implements multiple models including Linear Regression, Decision Trees, Random Forest, XGBoost, and SVM to predict property prices.
Hyperparameter Tuning: Conducts hyperparameter optimization for the XGBoost model to improve prediction accuracy.
Model Evaluation: Evaluates model performance using metrics like RMSE (Root Mean Square Error) and MAPE (Mean Absolute Percentage Error) on k-fold cross-validation. *****

Installation

git clone https://github.com/your-username/property-price-prediction.git
cd property-price-prediction
python3 -m venv property_venv
source property_venv/bin/activate
pip install -r requirements.txt
export API_KEY='your_gemini_api_key'

N.B. If recreating the postcode enrichment, you will need to sign up for a Gemini API key and set the API_KEY environment variable.

Data Sources

Property Data: Obtained from Kaggle.
Suburb Rankings: Scraped from domain.com.au.
Postcode Mappings: Obtained from the Gemini API (or stored locally in the repository).

Usage

Run through the property_data.ipynb notebook to load, clean, and enrich the data.
Run through property_model.Rmd to build and evaluate the models.

