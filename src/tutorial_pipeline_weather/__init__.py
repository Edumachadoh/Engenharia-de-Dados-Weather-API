import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url:str) -> list:
    response = requests.get(url)
    # transformar resposta da url em dicionário python
    data = response.json()
    
    if response.status_code != 200:
        logging.error("Erro na requisição)")
        return []
    
    if not data:
        logging.info("Nenhum dado retornado")    
        return []
    
    
    output_path = 'data/weather_data.json'
    # sair da pasta source e ir para pasta data
    output_dir = Path(output_path).parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # f é o arquivo onde serão escritos os dados 
    # with open já fecha automaticamente o arquivo após a escrita
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    return data

# parei 17:19 min video