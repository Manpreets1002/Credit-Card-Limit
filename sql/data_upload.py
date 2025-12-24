import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

data_path = os.getenv("DATA_PATH")

df = pd.read_csv(data_path)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")

engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_password}@127.0.0.1:{db_port}/{db_database}?ssl_disabled=true"
)

conn = engine.connect()

try:
    df.to_sql(
        "credit",
        con=conn,
        if_exists="append",
        index=False
    )
    print("✅ Data inserted successfully")
finally:
    engine.dispose()