# Curvy Bump Chart

The curvy_bump_chart project is a proccess I created the automate the data template behined Kevin Flerlage's Curvy Bump Chart and Slope Chart Template. https://www.flerlagetwins.com/2019/03/curvy-bump-chart-slope-chart-template_27.html Includes aone prccess xlsx which updates the excel version amd postgre_sql which updates a table within a PostgreSQL database.

xlsx - folder. 

The two files within this folder perform the same oprtion with one sliht diffeence. As each file implies it either generates the template using the rank (template_data_generator_on_rank.py) column itself or mesaure (template_data_generator_on_measure) column.

Both save the data to the source excel file.

postgre_sql - folder

Based on the same principles of the xlsx version the only differace here is the code is split into two functions, 1. build_template(data). As the name implies the function contains all the code that builds the data template, 2. to_sql(data) - simply processes the DataFrame and saves to a table within the Postgre SQL database.

Addiontally you need to update the database.ini file with you details and the table name within the to_sql function. The create_table.py process, helps with the cration of the table initally. 
