# Otimização de Consultas com a API do Google Maps
Este projeto foi desenvolvido para automatizar consultas de distâncias e tempos de viagem entre municípios do estado de São Paulo utilizando a API do Google Maps. 
Além disso, também foi criado um processo para identificação de municípios com base em rodovias e quilometragens (não mostrado nesse repositório).
O foco principal do projeto foi otimizar o processamento de grandes volumes de dados e superar as limitações da API, como quotas de requisição e falhas em chamadas.

## Funcionalidades
- **Consulta de Distâncias:** Consulta de distâncias e tempos de viagem entre municípios, com tratamento de exceções e multithreading para otimizar o tempo de resposta
- **Tratamento de Exceções:** Implementação de tentativas automáticas em caso de falhas, com limites curtos para evitar bloqueios ou erros contínuos
- **Controle de Quotas:** Gerenciamento inteligente das requisições para evitar exceder a quota da API do Google Maps
- **Caching de Resultados:** Armazenamento temporário de resultados de consultas para reduzir o número de chamadas repetidas à API
- **Exportação de Dados:** Salvamento dos resultados das consultas em arquivos CSV ou Excel, facilitando a visualização e manipulação dos dados

## Ferramentas utilizadas
- **Linguagem:** Python
- **APIs do Google:** API de Direções e API de Geocoding ativadas
- **Bibliotecas:**
  - `Pandas`: Manipulação e análise de dados
  - `GoogleMaps`: Interface para as APIs de mapas
  - `Time`: Controle de tempo e tentativas
  - `Functools`: Funções de apoio, incluindo caching
  - `ThreadPoolExecutor`: Para multithreading

## Conectando-se à API do Google
1. Crie um projeto no Google Cloud Console
2. Ative as APIs necessárias: Directions API e Geocoding API
3. Gere uma chave de API e a adicione ao projeto
4. No código, configure a variável API_KEY com sua chave:
   
   ```ruby
   API_KEY = 'SUA_API_KEY'
   gmaps = googlemaps.Client(key=API_KEY)
   ```

## Código
1. **Carregar os municípios:** A partir de um arquivo Excel, os municípios são carregados com base na região intermediária escolhida
2. **Calcular distâncias:** Utilizando multithreading, as distâncias e tempos de viagem entre os municípios e a cidade central são calculados
3. **Exportar resultados:** Os resultados são salvos em um arquivo CSV ou Excel para fácil manipulação

## Considerações sobre Otimização
- **Multithreading:** Permite o processamento de múltiplas consultas em paralelo, acelerando a execução
- **Cache de Resultados:** Reduz a repetição de chamadas para a API, economizando quota e melhorando a eficiência
- **Tentativas Automáticas:** Em caso de falhas, o código faz novas tentativas até um limite configurado, mantendo a continuidade do processo

## Limitações
- A precisão das APIs pode ser menor em áreas rurais ou remotas, especialmente ao tentar localizar rodovias e pontos exatos com base em quilometragem
- Ainda não foi implementada a integração com outras fontes de dados geográficos para melhorar a precisão das consultas
- Há limites de requisições por dia e por minuto

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar issues.
