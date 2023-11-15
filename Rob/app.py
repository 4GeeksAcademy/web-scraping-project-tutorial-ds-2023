import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv


# load the .env file variables
load_dotenv()

# 1) Connect to the database here using the SQLAlchemy's create_engine function
page = "https://drive.google.com/drive/folders/1WcoN3SGNeOivgovQgFx0zS0ZjKWCEX5y"

engine = create_engine(page)

# 2) Execute the SQL sentences to create your tables using the SQLAlchemy's execute function

# 3) Execute the SQL sentences to insert your data using the SQLAlchemy's execute function

# 4) Use pandas to print one of the tables as dataframes using read_sql function