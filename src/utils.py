import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine


TIME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"

def connection_enable():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")

    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@127.0.0.1:{db_port}/{db_database}?ssl_disabled=true"
    )

    return engine

def connection_disable(engine):
    engine.dispose()


def upload_path(preprocessor_path,model_path):
    engine = connection_enable()
    conn = engine.connect()

    table_create = """
    CREATE TABLE IF NOT EXISTS paths (
        pipeline varchar(255),
        catboost_path varchar(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    conn.execute(table_create)

    inser_command = f"""
    INSERT INTO paths VALUES ({preprocessor_path},{model_path});
    """

    conn.execute(inser_command)

    connection_disable(engine)