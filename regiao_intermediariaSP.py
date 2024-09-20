import googlemaps
import pandas as pd
import time
import functools
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed


# Inserir chave de API do Google Maps
API_KEY = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

# Carregar municípios por região intermediária a partir de um arquivo Excel que contém as regiões
def load_municipios_por_regiao_intermediaria(filename, regiao_intermediaria):
    df = pd.read_excel(filename)
    regiao_col = 'Região Geográfica Intermediária'
    municipio_col = 'MUNICIPIO COM ACENTO'
    municipios = df[df[regiao_col] == regiao_intermediaria][municipio_col].tolist()
    return municipios

# Função com cache para fazer a consulta à API e calcular distância e tempo
@functools.lru_cache(maxsize=1000)  # Cache de até 1000 resultados
def get_distance_with_cache(origem, central_city):
    return get_distance_retry(origem, central_city)

# Função para fazer a consulta à API com tentativas de retry
def get_distance_retry(origem, central_city, max_retries=2, delay=2):
    retries = 0
    while retries < max_retries:
        try:
            # Realiza a chamada para a API
            directions = gmaps.directions(origem, central_city, mode="driving")
            if directions:
                distance = directions[0]['legs'][0]['distance']['value'] / 1000  # Transformação para Km
                duration = directions[0]['legs'][0]['duration']['value'] / 3600  # Transformação em Horas
                return [origem, central_city, round(distance, 2), round(duration, 2), round(duration * 60, 2)] # Retorno das colunas necessárias
            else:
                return [origem, central_city, None, None, None]
        except Exception as e:
            retries += 1 # Em caso de erro na consulta
            print(f"Tentativa {retries} falhou para {origem}. Erro: {e}. Tentando novamente...")
            time.sleep(delay)  # Espera um tempo antes de tentar novamente

    # Se todas as tentativas falharem, retorna valores nulos
    return [origem, central_city, None, None, None]

# Função para limitar a taxa de requisições (rate limiter)
def rate_limited_get_distance(origem, central_city):
    time.sleep(0.1)  # Limitar para 10 requisições por segundo (ajuste conforme necessário)
    return get_distance_with_cache(origem, central_city)

# Função para calcular distâncias usando várias threads
def calculate_distances_multithreaded(municipios, central_city):
    results = []
    skipped_municipios = [central_city]  # Ignora a cidade central (que será igual ao nome da Região)

    # Ajustar o número de threads com base no número de CPUs disponíveis
    max_workers = min(len(municipios), multiprocessing.cpu_count() * 2)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(rate_limited_get_distance, origem, central_city) for origem in municipios if origem not in skipped_municipios]
        
        for future in as_completed(futures):
            results.append(future.result())

    return pd.DataFrame(results, columns=['Origem', 'Destino', 'Distância (km)', 'Tempo de Viagem (h)', 'Tempo de Viagem (min)'])

# Base excel
input_file = 'coloque_o_caminho_do_arquivo.xlsx'
regiao_intermediaria = 'ARARAQUARA' # Inserir a região escolhida

# Carregar municípios
municipios = load_municipios_por_regiao_intermediaria(input_file, regiao_intermediaria)
if municipios:
    central_city = regiao_intermediaria
    
    # Usar multithreading para calcular distâncias e tempos de viagem com cache e controle de taxa
    df_resultado = calculate_distances_multithreaded(municipios, central_city)
    
    # Salvar o DataFrame corrigido em um arquivo Excel já tratado
    output_excel_path = f'coloque_o_caminho_para_o_novo_arquivo\\distancias_e_tempos_{regiao_intermediaria}.xlsx'
    df_resultado.to_excel(output_excel_path, index=False)
    
    print(f"Resultados salvos em {output_excel_path}")
else:
    print("Nenhum município encontrado para a região intermediária especificada.")
