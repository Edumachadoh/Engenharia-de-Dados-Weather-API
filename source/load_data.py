# conectar com banco de dados e criar conexao e fazer comandos sql
from sqlalchemy import create_engine, text
# nenhum erro de conversao de nomenclatura de dados
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# caminho do arquivo .env
env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)

user= os.getenv('user')
password= os.getenv('password')
database= os.getenv('database')
# host= 'host.docker.internal'
host= 'localhost'

#criar conexao
def get_engine():
    logging.info("Criando conexão com o banco de dados")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )
    
engine = get_engine()

def load_weather_data(table_name:str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )
    
    logging.info(f"Dados carregados na tabela {table_name} com sucesso!")
    
    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}.")