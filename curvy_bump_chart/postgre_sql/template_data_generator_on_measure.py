import pandas as pd
from time import process_time
from config import config
import sqlalchemy as db

# Set the path to the location of file.
xlsx = "../data/regional_refund_data_measures_py.xlsx"

# Load the Entry Sheet from the xlsx file, skip the Measure column.
data = pd.read_excel(xlsx, sheet_name='Entry Sheet', header=0, usecols='A,B,D,E')


def build_template(data):

    # Star building the Data Template based on rank column itself. #

    # Record the start time for the process.
    start_time = process_time()

    # 1. Build the 'Dimension & Time' column - concatenate 'Dimension' and 'Time' columns, map values to string.
    data['Dimension & Time'] = data['Dimension'].map(str) + data['Time'].map(str)

    # 2. Build the 'Dimension & Next Time' column - concatenate 'Dimension' and 'Time' columns, increment time by 1, map values to string.
    data['Dimension & Next Time'] = data['Dimension'].map(str) + (data['Time'] + 1).map(str)

    # 3. Build the 'Rank' column, calculated based on measure values, grouped by (partitioned over) 'Time'.
    data['Rank'] = data.groupby("Time")["Measure"].rank("dense", ascending=False)

    # 4. Build 'Next Rank' column from Rank column.
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

    # 5. Build the Join column. Simply set this to 1, indication a join.
    data["Join"] = 1

    # 6. Reorder columns as per template.
    data[['Dimension', 'Time', 'Dimension & Time', 'Dimension & Next Time', 'Rank', 'Next Rank', 'Join', 'Measure', 'Actual Time']]

    # 7. Rename Columns.
    data.rename(columns={'Dimension': 'dimension', 'Time': 'time',
                         'Dimension & Time': 'dimension_time', 'Dimension & Next Time': 'dimension_next_time',
                         'Next Rank': 'next_rank', 'Join': 'path_join',
                         'Measure': 'measure', 'Actual Time': 'actual_time'}, inplace=True)

    # Record the end time for the process.
    end_time = process_time()

    # Calculate the time for the entire process.
    elapsed_time = end_time - start_time

    # Return the process time to the user.
    return f"Data Template is ready for processing. \nElapsed time: {elapsed_time:0.4f} seconds.\n"


def to_sql(data_frame):

    # 8. Finally save the data to the PostgreSQL Database.

    # Record the start time for the process.
    start_time = process_time()

    # Get the PostgreSQL configuration parameters.
    db_host = config()['host']
    db_user = config()['user']
    db_pass = config()['password']
    db_name = config()['dbname']

    # Set the connection string.
    con_string = str(f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}")

    # Create the database engine object.
    engine = db.create_engine(con_string)

    # Create the connection to the database and connect.
    con = engine.connect()

    # Write the DataFrame to the table.
    data_frame.to_sql("bump_chart", con, if_exists="replace", index=False)

    # Record the end time for the process.
    end_time = process_time()

    # Close the connection to the database.
    con.close()

    # Calculate the time for the entire process.
    elapsed_time = end_time - start_time

    # Return the process time to the user.
    return f"Frame written to table. \nElapsed time: {elapsed_time:0.4f} seconds.\n"


# Generate data template.
if __name__ == '__main__':
    print(build_template(data))
    print(to_sql(data))
