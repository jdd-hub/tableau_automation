import pandas as pd

# Set the path to the location of file.
xlsx = "../data/template_data_py.xlsx"

# Load the Entry Sheet from the xlsx file, skip the Measure column.
data = pd.read_excel(xlsx, sheet_name='Entry Sheet', header=0, usecols='A:C, E')

# Star building the Data Template based on rank column itself. #

# 1. Build the 'Dimension & Time' column - concatenate 'Dimension' and 'Time' columns, map values to string.
data['Dimension & Time'] = data['Dimension'].map(str) + data['Time'].map(str)

# 2. Build the 'Dimension & Next Time' column - concatenate 'Dimension' and 'Time' columns, increment time by 1, map values to string.
data['Dimension & Next Time'] = data['Dimension'].map(str) + (data['Time']+1).map(str)

# 3. Build 'Next Rank' column from Rank column.
next_rank = []
for index, row in data.iterrows():
    try:
        """
        Find the corresponding 'Dimension & Next Time' value in the 'Dimension & Time', 
        store the rank value item to the temporary next_rank list.  
        """
        next_rank.append(data.loc[data['Dimension & Time'] == row['Dimension & Next Time'], 'Rank'].item())
    except ValueError:
        # Set value to 0 where no matches are found.
        next_rank.append(0)

# Add the next_rank list to the DataFrame column 'Next Rank'.
data["Next Rank"] = pd.Series(next_rank)

# 4. Build the Join column. Simply set this to 1, indication a join.
data["Join"] = 1

# 5. Build the Measure column. Simply set this to 0 since the template is for rank.
data["Measure"] = 0

# 6. Reorder columns as per template.
data = data[['Dimension', 'Time', 'Dimension & Time', 'Dimension & Next Time', 'Rank', 'Next Rank', 'Join', 'Measure', 'Actual Time']]

# 7. Finally save the data to a new sheet.
with pd.ExcelWriter(xlsx, mode='a') as writer:
    """
    Note: this will not overwrite the current Data Template sheet. 
    It creates a new sheet: Data Template x.  
    This is so that as you should, always open the sheet, verify the data, 
    remove the old sheet and rename the new.
    """
    data.to_excel(writer, sheet_name='Data Template', index=False)