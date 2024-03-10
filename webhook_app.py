from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union
import os
import hmac
import hashlib
import json
import logging

load_dotenv()
debugIsActive: bool = os.getenv('DEBUG', 'False').lower() == 'true'
logging.basicConfig(level=logging.DEBUG if debugIsActive else logging.INFO)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json()

        if not payloadIsValid(payload):
            raise InvalidPayload('Payload Inválido')

        event = request.headers.get('X-Ummense-Event')
        logging.debug(f'Evento Ummense: {event}')

        if not payload:
            return 'Empty payload received', 400

        print(f'Card: {payload['name']} - {payload['uuid']}')

        # Itera pelas colunas
        listColumns(payload['columns'], payload['flows'])

        return 'Webhook received successfully', 200

    except InvalidPayload as ipe:
        logging.error(str(ipe))

        return 'Invalid Payload', 400

    except Exception as e:
        logging.debug(f'Error processing webhook: {str(e)}')

        return 'Error processing webhook', 500

def listColumns(columns: list, flows: list) -> None:
    now: datetime = datetime.now()

    for column in columns:
        flow: Union[dict,str] = next((flow for flow in flows if flow['uuid'] == column['flow_id']), 'Fluxo não encontrado')

        start: datetime = datetime.strptime(column['started_at'], "%Y-%m-%d %H:%M:%S")

        columnName: str = column['name'] or 'Sem nome'

        flowName: str

        if isinstance(flow, dict):
            flowName = flow.get('name', 'Sem Nome')
        else:
            flowName = 'Fluxo não encontrado'

        status: str
        timeDiff: timedelta

        if column['ended_at'] is None:
            status= 'está ativo'
            timeDiff = now - start
        else:
            end: datetime = datetime.strptime(column['ended_at'], "%Y-%m-%d %H:%M:%S")
            status = 'foi finalizado'
            timeDiff = end - start

        print('Card {} há {} na coluna {} do fluxo {}'.format(status, timeDiff, columnName, flowName))

def payloadIsValid(payload: dict) -> bool:
    #Chave gerada pela Ummense
    secret: str | None = os.getenv('UMMENSE_WEBHOOK_KEY')

    if not secret:
        logging.debug('Ummense Secret não configurado no .env')

        return True

    signature: str | None = request.headers.get('Signature')

    if not signature:
        logging.debug('Signature não configurado no cabeçalho da requisição')

        return False

    payload_json: bytes = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

    # Calcula a assinatura HMAC-SHA256 usando a chave secreta
    hash = hmac.new(secret.encode('utf-8'), payload_json.encode('utf-8'), hashlib.sha256).hexdigest()

    logging.debug(f'Assinatura no header {signature} - Assinatura gerada: {hash}')

    return hash == signature

class InvalidPayload(Exception):
    """Exceção personalizada para erros relacionados ao webhook da Ummense."""
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
