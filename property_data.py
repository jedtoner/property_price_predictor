import pandas as pd
import requests
import json
import os
import google.generativeai as genai
import numpy as np
from statsmodels.tsa.api import VAR
import sys

PROPERTY_CSV = 'domain_properties.csv' #obtained from https://www.kaggle.com/datasets/alexlau203/sydney-house-prices
CRIME_XLSX = 'LgaRankings_27_Offences.xlsx' #obtained from https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets/local-area-rankings.html
LGA_MAPPING_TSV = 'lga.tsv' #obtained from https://www.slhd.nsw.gov.au/postcodes/holder.cfm
API_KEY = os.getenv('API_KEY')


class PropertyMetaDataLoader:

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.load_data(data_path)

    def load_data(self, data_path):
        raw_df =  pd.read_csv(data_path)
        cols_to_keep = ['date_sold', 'price', 'suburb', 'num_bath', 'num_bed', 'num_parking',
                        'property_size', 'type']
        subset_df = raw_df[cols_to_keep]

        subset_df.loc[:, 'date_sold'] = pd.to_datetime(subset_df['date_sold'], format="mixed", dayfirst=True)

        subset_df = subset_df[subset_df['type'] != 'Vacant land'] # remove any land vacanicies will not be used in model
        
        return subset_df
    
class MacroEconomicDataLoader:
    def __init__(self, api_url):
        self.api_url = api_url
        self.json_file = self.fetch_data()

    def fetch_data(self):
        response = requests.get(self.api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    
class SuburbCrimeDataLoader:
    def __init__(self, data_path, lga_mapping):
        self.data_path = data_path
        self.data = self.load_data(data_path)
        self.lga_mapping = lga_mapping
        self.lga_list = self.extract_lga_list()
        print(self.lga_list)
        self.clean_data = self.clean_data()

    def load_data(self, data_path):
        header_row = 5
        last_row = 135
        sheets_dict = pd.read_excel(data_path, header = header_row, nrows = last_row - header_row, sheet_name=None)
        return sheets_dict
    
    def extract_lga_list(self):
        return list(set(element for sublist in self.lga_mapping.values() for element in sublist))
    
    def clean_data(self):
        data = self.data
        clean_data = {}
        for key in data.keys():
            df = data[key]
            df = df.drop(columns=df.filter(regex='(?i)total|rank', axis=1).columns) # we only want to observe rate per 100,000 population
            df.columns = ['LGA', '2019', '2020', '2021', '2022', '2023']
            df = df.T 
            df.columns = df.iloc[0]
            df = df[1:] # Ensure LGA names are column names
            df.columns.name = None
            df_with_na = self.remove_na(df) #NA values are stored as 'nc' strings in original excel
            clean_data[key] = df_with_na
        return clean_data
    
    def back_forecast(self, df):
        # Ensure the index is datetime for time series forecasting
        df.index = pd.to_datetime(df.index, format='%Y')
        # Fit VAR model on the available data (2019-2023)
        model = VAR(df, freq = 'YS-JAN')
        model_fit = model.fit(maxlags=1)
        # Forecast the missing years (2016-2018)
        lag_order = model_fit.k_ar
        forecast_input = df.values[-lag_order:]
        forecast = model_fit.forecast(y=forecast_input, steps=3)
        # Create a DataFrame for the forecasted values
        forecasted_index = pd.date_range(start='2016', periods = 3, freq='YS-JAN')
        forecasted_df = pd.DataFrame(forecast, index=forecasted_index, columns=df.columns)
        
        # Combine the forecasted values with the original data
        combined_df = pd.concat([forecasted_df, df])
        combined_df = combined_df.sort_index()
        return combined_df


    def remove_na(self, df):
        
        def to_na_if_string(value):
            if isinstance(value, str):
                return np.nan
            return value
        
        df_with_na =  df.map(to_na_if_string)
        return df_with_na.dropna(axis = 1, how = 'all') # columns with NA are because not enough population to calculate crime rates - not an issue in Sydney
    
class LGAMapping:
    def __init__(self, suburbs, lgas, mapping_file_path):
        self.suburbs = suburbs
        self.lgas = lgas
        self.mapping_file_path = mapping_file_path
        self.provided_mapping = self.load_data(mapping_file_path)
    
    def load_data(self, data_path):
        df = pd.read_csv(data_path, sep='\t')
        return df
    
    def map_suburb_to_lga(self, save = False):
        mapping_json = json.dumps(self.provided_mapping.to_dict())
        suburb_list = str(self.suburbs)
        lga_list = str(self.lgas)
        prompt = f"""
        I have a list of suburbs: {suburb_list}
        I have a list of LGAs: {lga_list}
        Here is a table in JSON format with columns 'postcode', 'suburb', and 'lga':
        {mapping_json}
        
        Please return a mapping between the provided list of suburbs and the provided list of LGAs. 
        Note that the LGA and suburb names may not directly match up between the provided list and json table (e.g., 'shire of sydney' vs 'sydney'). 
        In the case where there are two LGAs for a given suburb, return both LGAs in the mapping.
        The response should be in json format, which can be directly parsed into a python dictionary.
        Ensure that the response starts and ends with curly braces, and there is no additional formatting.
        """
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        output = model.generate_content(prompt).text

        if save:
            with open('suburb_to_lga_mapping.json', 'w') as f:
                f.write(output)
        return output
    
            


if __name__ == '__main__':
    property_loader = PropertyMetaDataLoader(PROPERTY_CSV)
    # print(property_loader.data.head())

    lga_mapping = json.loads(open('suburb_to_lga_mapping.json').read())
    #print(lga_mapping)
    suburb_crime_loader = SuburbCrimeDataLoader(CRIME_XLSX, lga_mapping)
    x = suburb_crime_loader.clean_data['Assault - domestic violence']
    print(list(x.columns))
    #y = suburb_crime_loader.back_forecast(x)

    # suburbs = property_loader.data['suburb'].unique()
    # lga_mapping = LGAMapping(suburbs, lgas, LGA_MAPPING_TSV)
    # lga_mapping.map_suburb_to_lga(save = True)

    # import tabula
    # import pandas as pd

    # # Path to the PDF file
    # pdf_path = 'path_to_your_pdf_file.pdf'

    # # Extract tables from the PDF
    # tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)


    