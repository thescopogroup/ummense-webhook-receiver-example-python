# Ummense Webhook Receiver

Este é um aplicativo Flask simples para receber webhooks da Ummense. Ele valida a assinatura HMAC-SHA256 do payload recebido.

## Requisitos

- Python 3.x
- Flask
- Python `dotenv` para carregar variáveis de ambiente a partir de um arquivo `.env`

## Instalação

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/thescopogroup/ummense-webhook-receiver-example-python.git
   cd ummense-webhook-receiver-example-python
2. **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
3. **Ative o ambiente virtual:**
- Windows:
    ```bash
    venv\Scripts\activate
- Linux/MacOs:
    ```bash
    source venv/bin/activate
4. **Instale as dependências:**

    ````bash
    pip install -r requirements.txt
5. **Crie um arquivo .env no diretório do seu aplicativo com as configurações necessárias. Exemplo:**

    ```makefile
    DEBUG=False
    UMMENSE_WEBHOOK_KEY=SuaChaveSecretaDaUmmense
6. **Execute:**

    ````bash
    python webhook_app.py
## Configuração

Certifique-se de configurar corretamente as variáveis de ambiente no arquivo **.env**. Aqui está um exemplo de configuração:

- **DEBUG**: Define o modo de depuração do Flask. Configure como True para ativar o modo de depuração.
- **UMMENSE_WEBHOOK_KEY**: Chave secreta fornecida pela Ummense para autenticação de webhook.

## Uso

1. Inicie o aplicativo.
2. O aplicativo estará disponível em http://localhost:5001/webhook.
3. Certifique-se de que o webhook na Ummense esteja configurado para apontar para a URL do seu aplicativo.
4. Envie webhooks da Ummense para testar o aplicativo.

## Estrutura do Código

- webhook_app.py: O ponto de entrada do aplicativo Flask.
- InvalidPayload: Classe de exceção personalizada para erros relacionados ao webhook da Ummense.
- webhook(): Rota principal para receber webhooks.
- listColumns(): Função auxiliar para iterar e listar colunas do payload.
- payloadIsValid(): Função para validar a assinatura HMAC-SHA256 do payload.