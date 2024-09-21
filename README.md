# Property Price Prediction Analysis

## Overview
This project aims to analyze and predict property prices in Sydney using a comprehensive dataset. By combining data collection, processing, and advanced machine learning techniques, it offers valuable insights to key stakeholders in the real estate market, such as investors, developers, and buyers.

## Features
- **Data Loading**: Loads property data from a CSV file sourced from Kaggle.
- **Postcode Enrichment**: Enhances data accuracy by using the Gemini API to append postcode information to suburb names.
- **Suburb Ranking**: Scrapes suburb rankings from domain.com.au, based on indicators like traffic, school accessibility, proximity to cafes, and distance to the CBD.
- **Data Integration**: Merges property data with suburb rankings to create a unified dataset for analysis.
- **Machine Learning Models**: Implements various models including Linear Regression, Decision Trees, Random Forest, XGBoost, and SVM to predict property prices.
- **Hyperparameter Tuning**: Optimizes the XGBoost model's hyperparameters to improve prediction accuracy.
- **Model Evaluation**: Evaluates model performance using metrics such as RMSE (Root Mean Square Error) and MAPE (Mean Absolute Percentage Error) through k-fold cross-validation.

## Installation
To set up the project locally, follow these steps:

```bash
git clone https://github.com/jedtoner/property_price_predictor.git
cd property-price-prediction
python3 -m venv property_venv
source property_venv/bin/activate
pip install -r requirements.txt
export API_KEY='your_gemini_api_key'
```

> **Note**: If recreating the postcode enrichment, you will need to sign up for a Gemini API key and set the `API_KEY` environment variable.

## Data Sources
- **Property Data**: Obtained from [Kaggle](https://www.kaggle.com).
- **Suburb Rankings**: Scraped from [domain.com.au](https://www.domain.com.au).
- **Postcode Mappings**: Obtained from the Gemini API (or stored locally in the repository).

## Usage
- Run the `property_data.ipynb` notebook to load, clean, and enrich the data.
- Run the `property_model.Rmd` file to build and evaluate the models.


