import pandas as pd
from datetime import datetime, timedelta
import os

# Base directory = folder containing this script (Models/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1: Define the file path
file_path = os.path.join(BASE_DIR, 'Scats_Data_October_2006.xls')
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found")
    exit()
df = pd.read_excel(file_path, sheet_name='Data', skiprows=1) # Data.csv is inside the xls file

# 2: Define column groups
id_vars = ['SCATS Number', 'Location', 'NB_LATITUDE', 'NB_LONGITUDE', 'Date'] 
flow_cols = [f'V{i:02d}' for i in range(96)] # Each row is a 15-minute interval

# 3: Convert data from Wide format → Long format
# Wide format: each row has 96 columns (V00–V95)
# Long format: each row represents ONE time interval
df_long = pd.melt(
    df,
    id_vars=id_vars,    
    value_vars=flow_cols, 
    var_name='Interval',    
    value_name='Flow'      
)

# 4: Convert interval labels into minutes
# Extract the number from 'Vxx', convert to int, multiply by 15
df_long['Minutes_Offset'] = (
    df_long['Interval']
    .str.extract(r'(\d+)')   # extract digits from string
    .astype(int)             # convert to integer
    * 15                     # convert interval index to minutes
)

# 5: Create actual timestamps
df_long['Date_Clean'] = pd.to_datetime(df_long['Date'])
# Add the minute offset to the date to get full timestamp
df_long['Timestamp'] = (
    df_long['Date_Clean'] +
    pd.to_timedelta(df_long['Minutes_Offset'], unit='m')
)

# 6: Final cleanup and formatting
final_df = df_long[['SCATS Number', 'Timestamp', 'NB_LATITUDE', 'NB_LONGITUDE', 'Flow']]
final_df = final_df.sort_values(by=['SCATS Number', 'Timestamp']) # Sort data by SCATS Number and time
final_df = final_df.dropna(subset=['Flow'])

# 7: Export to CSV and Confirm
final_df.to_csv(os.path.join(BASE_DIR, 'processed_traffic_data.csv'), index=False)
print(final_df.head())