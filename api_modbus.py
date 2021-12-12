'''
    API simples para comunicação com servidor Modbus

    Foi utilizado um simulador Modbus (ELipse Modbus Simulator).
    A API usa o Modbus que estiver ouvindo na porta configurada (padrão 5020).
    Caso necessário, mudar a variável porta_modbus para outra porta.
    A cada escrita/leitura, é gerado uma informação no log.txt.

    Dependências necessárias para funcionamento da API:

    - pip install flask
    - pip install pymodbus
    - pip install flask_cors

    Abrir o arquivo vw_modbus.html para testar a API.
    O arquivo html foi criado com base nas duas tarefas da avaliação.

    Para iniciar esta API, executar no cmd:

    - python sw_modbus.py
'''

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from datetime import datetime
from flask import Flask
from flask import request
from flask_cors import CORS

#Configurações da API Modbus
porta_modbus = 5020
servidor_api = '0.0.0.0'
servidor_modbus = '127.0.0.1'
registrador_inicial = 0
registrador_final = 120
#---------------------------

#Gera log para cada tipo de opração (E = Escreveu, L = Leu)
def gerar_log(tipo_operacao, registrador, valor):
    arq = open("log.txt", "a")
    dat_atu = datetime.now()
    dat_str = dat_atu.strftime('%d/%m/%Y %H:%M')

    if tipo_operacao == 'E':
        log = '\n[' + dat_str +']' + ' Escreveu ' + str(valor) + ' no registrador ' + str(registrador)
    
    if tipo_operacao == 'L':
        log = '\n[' + dat_str +']' + ' Leu ' + str(valor) + ' no registrador ' + str(registrador)

    arq.write(log)
    arq.close()

#Escreve no registrador o valor passado como parâmetro
def escreve_registrador(registrador, valor):
    client = ModbusClient(servidor_modbus, port=porta_modbus)

    client.connect()

    client.write_register(registrador - 1, valor, unit=1)
    gerar_log('E', registrador, valor)

    client.close()

#Lê o valor do registrador passado como parâmetro
def le_registrador(registrador):
    client = ModbusClient(servidor_modbus, port=porta_modbus)

    client.connect()

    rr = client.read_holding_registers(registrador_inicial, registrador_final - 1, unit=1)
    
    client.close()
    
    valor = rr.registers[registrador - 1]
    gerar_log('L', registrador, valor)
    
    return rr.registers[registrador - 1]


#INICIA CONSTRUÇÃO DA API
app = Flask(__name__)
CORS(app)

#RETORNA O VALOR CONTIDO NO REGISTRADOR PASSADO COMO PARAMETRO
@app.route('/ler', methods=['GET'])
def getRegister():
    register = request.args.get('register')
    
    return str(le_registrador(int(register)))

#GRAVA O VALOR NO REGISTRADOR PASSADO COMO PARAMETRO E RETORNA O VALOR INSERIDO
@app.route('/escrever', methods=['GET'])
def postRegister():
    register = request.args.get('register')
    value = request.args.get('value')

    escreve_registrador(int(register), int(value))

    return 'Valor ' + value + ' escrito no registrador ' + register

if __name__ == '__main__':
    # Executa a aplicação
    app.run(host=servidor_api, debug=True)