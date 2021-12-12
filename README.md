# api-modbus
API Simples para Comunicação com Servidor Modbus

Foi utilizado um simulador Modbus (ELipse Modbus Simulator).
A API usa o Modbus que estiver ouvindo na porta configurada (padrão 5020).
Caso necessário, mudar a variável porta_modbus para outra porta.
A cada escrita/leitura, é gerado uma informação no log.txt.

Dependências necessárias para funcionamento da API:

- pip install flask
- pip install pymodbus
- pip install flask_cors

Para iniciar esta API, executar no cmd:

- python api_modbus.py

Exemplo de URL's para uso da API:

Escrever 25 no registrador 100:
- http://localhost:5000/escrever?value=25&register=100
- Retorno (String): 'Valor 25 escrito no registrador 100'

Ler o registrador 100
- http://localhost:5000/ler?register=100
- Retorno (String): 25
