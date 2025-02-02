import scipy.io as sio
import pandas as pd
import numpy as np

def flatten_cell_array(cell_array):
    return [item[0] if item.size > 0 else '' for item in cell_array.flatten()]

# Load the MATLAB file
data = sio.loadmat('./mydata.mat')
data_subs = data['data_subs'][0, 0]

# Create a dictionary to store all the data
data_dict = {}

# Process each field in data_subs
for field in data_subs.dtype.names:
    if field.startswith('Scen'):
        # For scenario data, we'll create separate columns for each condition
        scenario_data = data_subs[field]
        for i, condition in enumerate(['Dry Sound', 'Opera Hall', 'Reverb Hall', 'Small Office']):
            column_name = f"{field}_{condition}"
            data_dict[column_name] = scenario_data[:, i].flatten()
    else:
        # For other fields, flatten if necessary
        field_data = data_subs[field]
        if field_data.dtype.kind == 'O':  # Object type, likely a cell array
            data_dict[field] = flatten_cell_array(field_data)
        else:
            data_dict[field] = field_data.flatten()

# Create a DataFrame
df = pd.DataFrame(data_dict)

# Save to CSV
csv_filename = 'data_subs_export.csv'
df.to_csv(csv_filename, index=False)

print(f"Data has been exported to {csv_filename}")

# Display the first few rows of the DataFrame
print("\nFirst few rows of the exported data:")
print(df.head())

# Display information about the DataFrame
print("\nDataFrame Info:")
df.info()