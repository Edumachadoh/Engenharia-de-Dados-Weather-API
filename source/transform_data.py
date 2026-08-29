# criar funções para rodar códigos do pandas
# também é possível rodar dentro do notebook, porem fica difícil para orquestração

import json
import pandas as pd
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# definir o caminho do arquivo json de maneira mais profissional
path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
# ou ../data/weather_data.json

# colunas para remover
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']

# colunas para renomear
columns_names_to_rename = {
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "clouds.all": "clouds_all",
    "dt": "timestamp",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
    "name": "city_name" 
}

# colunas para transformar em datetime
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:
    # receber o caminho do arquivo json e retornar um dataframe pandas
    logging.info(f"Carregando Dataframe do arquivo json")
    path = path_name
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    with open(path) as f:
        data = json.load(f)
        
    df = pd.json_normalize(data)
    logging.info(f"\n Dataframe criado com {len(df)} linhas e {len(df.columns)} colunas")
    return df
 
def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
     
    df_weather = pd.json_normalize(df['weather'][0].apply(lambda x: x[0]))
     
     # renomear colunas 
    df_weather = df_weather.rename(columns={
         'id': 'weather_id',
         'main': 'weather_main',
         'description': 'weather_description',
         'icon': 'weather_icon'
    })
     
    # juntar df com df_weather 
    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"\n Coluna 'weather' normalizada - {len(df_weather.columns)}")
     
    return df
 
def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    # remover colunas desnecessarias
    # passar como parametro lista de colunas a serem removidas
    logging.info(f"\n Removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    logging.info(f"\nColunas removidas: {len(df.columns)} colunas restantes")
    return df

def rename_columns(df:pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    logging.info(f"\nRenomeando {len(df.columns)} colunas")
    df = df.rename(columns=columns_names)
    logging.info(f"\nColunas renomeadas: {len(df.columns)} colunas restantes")
    return df
    
def normalize_datetime_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    # convertendo colunas para datetime
    logging.info(f"\n Convertendo colunas para datetime: {columns_names}")
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
    logging.info(f"\n Colunas convertidas para datetime")
    return df
 
def data_transformation():
    print("\nIniciando transformacoes")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(f"\nTransformacoes concluídas com sucesso")
    return df
    