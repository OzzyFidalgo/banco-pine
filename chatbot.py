key = "AIzaSyAJh10Qt4ON5lwQfrNx4nrWs7-kzXcKTfA"
fkey = "ac63ac57690271fb660fe215"
import google.generativeai as genai
import requests
import json
from datetime import datetime
import yfinance as yf

genai.configure(api_key=key)  # Substitua pela sua API key

model = genai.GenerativeModel("gemini-1.5-flash")

contexto_banco_pine = {
    "BancoPine": {
        "HistoriaEValores": {
            "descricao": "O Banco Pine foi fundado em 1997 por Noberto N. Pinheiro, com uma história familiar de atuação no mercado financeiro que remonta a 1939. Com mais de 25 anos de experiência, a instituição se posiciona como um banco de negócios, buscando oferecer soluções financeiras personalizadas.",
            "missao": "Crescimento saudável dos negócios dos clientes.",
            "valores": ["Ética", "Empreendedorismo", "Inovação", "Relacionamento de longo prazo"]
        },
        "ProdutosEServicos": {
            "Credito": {
                "descricao": "Disponível para empresas com foco em diferentes necessidades financeiras.",
                "opcoes": [
                    {"nome": "Capital de Giro", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "NCE/CCE", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Nota Comercial", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Cheque Empresa", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Conta Garantida", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "FGI", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Fiança", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Confirming", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "Multi Sacado", "link": "https://www.pine.com/para-sua-empresa/credito/"},
                    {"nome": "CPR Financeira", "link": "https://www.pine.com/para-sua-empresa/credito/"}
                ]
            },
            "Investimentos": {
                "descricao": "Opções para empresas e indivíduos.",
                "empresas": [
                    {"nome": "CDB", "link": "https://www.pine.com/para-sua-empresa/investimentos/"},
                    {"nome": "Compromissadas", "link": "https://www.pine.com/para-sua-empresa/investimentos/"},
                    {"nome": "Letra Financeira", "link": "https://www.pine.com/para-sua-empresa/investimentos/"}
                ],
                "individuos": [
                    {"nome": "LCI", "link": "https://www.pine.com/para-sua-empresa/investimentos/"},
                    {"nome": "LCA", "link": "https://www.pine.com/para-sua-empresa/investimentos/"},
                    {"nome": "CDB", "link": "https://www.pine.com/para-sua-empresa/investimentos/"}
                ]
            },
            "Commodities": {
                "Energia": [
                    "Petróleo bruto",
                    "Gás natural",
                    "Carvão",
                    "Óleo combustível",
                    "Energia elétrica"
                ],
                "Metais Preciosos": [
                    "Ouro",
                    "Prata",
                    "Platina",
                    "Paládio"
                ],
                "Metais Industriais": [
                    "Alumínio",
                    "Cobre",
                    "Níquel",
                    "Zinco",
                    "Chumbo",
                    "Estanho",
                    "Lítio"
                ],
                "Agrícolas": [
                    "Milho",
                    "Soja",
                    "Trigo",
                    "Algodão",
                    "Café",
                    "Açúcar",
                    "Cacau",
                    "Arroz",
                    "Suco de laranja"
                ],
                "Pecuária": [
                    "Gado de corte",
                    "Gado leiteiro",
                    "Suínos magros"
                ],
                "Outros": [
                    "Madeira",
                    "Borracha",
                    "Fibras naturais"
                ]
            },
            "CambioETradeFinance": {
                "descricao": "Soluções para operações internacionais.",
                "opcoes": [
                    {"nome": "ACC", "link": "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/"},
                    {"nome": "Carta de Crédito", "link": "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/"},
                    {"nome": "Câmbio Pronto", "link": "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/"},
                    {"nome": "Câmbio Futuro", "link": "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/"},
                    {"nome": "Finimp", "link": "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/"}
                ]
            }
        },
        "SegurancaEPrivacidade": {
            "descricao": "O Banco Pine adota medidas rigorosas para proteger informações sensíveis e orientar clientes contra fraudes.",
            "dicas": [
                "Verificar canais de comunicação.",
                "Não compartilhar informações confidenciais.",
                "Denúncias por meio de um canal específico."
            ]
        }
    }
}
commodities_symbols = {
    "milho": "ZC=F",
    "soja": "ZS=F",
    "petroleo": "CL=F",
    "ouro": "GC=F",
    "cafe": "KC=F",}
def buscar_abertura_commodity_por_nome(nome_commodity):
    """
    Busca o valor de abertura de uma commodity usando seu nome, mapeando para o símbolo do Yahoo Finance.
    """
    nome_commodity = nome_commodity.lower()  # Para lidar com letras maiúsculas e minúsculas

    if nome_commodity not in commodities_symbols:
        print(f"Comodidade {nome_commodity} não encontrada.")
        return None

    # Obtém o símbolo correspondente à commodity
    commodity_symbol = commodities_symbols[nome_commodity]

    try:
        # Obtém os dados históricos para o símbolo da commodity
        commodity = yf.Ticker(commodity_symbol)
        dados = commodity.history(period="1d")  # Obtém dados diários
        if dados.empty:
            print(f"Nenhum dado encontrado para a commodity {nome_commodity}.")
            return None

        # Retorna o valor de abertura (open)
        return dados['Open'].iloc[0]  # Retorna o valor de abertura do primeiro dia disponível
    except Exception as e:
        print(f"Erro ao acessar os dados da commodity {nome_commodity}: {e}")
        return None
def extrair_contexto_relevante(contexto_json, pergunta):
    """ Extrai o contexto relevante com base na pergunta do usuário. """
    pergunta = pergunta.lower()
    contexto_relevante = ""
    if "crédito" in pergunta:
        contexto_relevante += f"**Crédito:** {contexto_json['BancoPine']['ProdutosEServicos']['Credito']['descricao']}\n"
        contexto_relevante += "Opções de crédito: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Credito"]["opcoes"]:
            contexto_relevante += f"- {opcao['nome']}\n"
    elif "investimento" in pergunta:
        contexto_relevante += f"**Investimentos:** {contexto_json['BancoPine']['ProdutosEServicos']['Investimentos']['descricao']}\n"
        contexto_relevante += "Investimentos para empresas: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Investimentos"]["empresas"]:
            contexto_relevante += f"- {opcao['nome']}\n"
            contexto_relevante += "Investimentos para pessoas físicas: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Investimentos"]["individuos"]:
            contexto_relevante += f"- {opcao['nome']}\n"
    elif  "nome" in pergunta or "valor" in pergunta or "preço" in pergunta or "saca" in pergunta:
        # Identificar commodities no prompt e buscar seu valor de abertura
        for commodity in commodities_symbols.keys():
            if commodity in pergunta:
                abertura = buscar_abertura_commodity_por_nome(commodity)
                if abertura is not None:
                    contexto_relevante += f"O valor de abertura da commodity atual {commodity} é: {abertura}\n"
                else:
                    contexto_relevante += f"Não foi possível obter o valor de abertura da commodity {commodity}.\n"
                return contexto_relevante
    elif "câmbio" in pergunta or "trade finance" in pergunta or "cotação" in pergunta or "moeda" in pergunta or "dinheiro" in pergunta:
        contexto_relevante += f"**Câmbio e Trade Finance:** {contexto_json['BancoPine']['ProdutosEServicos']['CambioETradeFinance']['descricao']}\n"
        contexto_relevante += "Opções de Câmbio e Trade Finance: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["CambioETradeFinance"]["opcoes"]:
            contexto_relevante += f"- {opcao['nome']}\n"
            try:
                cotacao = buscar_cotacao_moeda()
                contexto_relevante += f"A cotação atual do USD para BRL é: {cotacao}\n"
            except Exception as e:
                contexto_relevante += f"Erro ao buscar cotação: {str(e)}\n"
    elif "derivativo" in pergunta:
        contexto_relevante += f"**Derivativos:** {contexto_json['BancoPine']['ProdutosEServicos']['Derivativos']['descricao']}\n"
        contexto_relevante += "Opções de derivativos: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Derivativos"]["opcoes"]:
            contexto_relevante += f"- {opcao['nome']}\n"
    elif "cotação" or "moeda" or "dolar" or "euro" or "valor" in pergunta:
        try:
            cotacao = buscar_cotacao_moeda()
            contexto_relevante += f"A cotação atual do USD para BRL é: {cotacao}\n"
        except Exception as e:
            contexto_relevante += f"Erro ao buscar cotação: {str(e)}\n"
    elif "mercado de capitais" in pergunta:
        contexto_relevante += f"**Mercado de Capitais:** {contexto_json['BancoPine']['ProdutosEServicos']['MercadoDeCapitais']['descricao']}\n"
    elif "seguros" in pergunta:
        contexto_relevante += f"**Seguros:** {contexto_json['BancoPine']['ProdutosEServicos']['Seguros']['descricao']}\n"
        contexto_relevante += "Opções de Seguros: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Seguros"]["opcoes"]:
            contexto_relevante += f"- {opcao['nome']}\n"
    elif "serviços" in pergunta:
        contexto_relevante += f"**Serviços:** {contexto_json['BancoPine']['ProdutosEServicos']['Servicos']['descricao']}\n"
        contexto_relevante += "Opções de Serviços: \n"
        for opcao in contexto_json["BancoPine"]["ProdutosEServicos"]["Servicos"]["opcoes"]:
            contexto_relevante += f"- {opcao['nome']}\n"
    elif "setor" in pergunta or "agronegocio" in pergunta or "imobiliário" in pergunta:
        contexto_relevante += "**Soluções por Setor:**\n"
        if "agronegocio" in pergunta:
            contexto_relevante += f"Agronegócio: {contexto_json['BancoPine']['ProdutosEServicos']['SolucoesPorSetor']['Agronegocio']}\n"
        if "imobiliário" in pergunta:
            contexto_relevante += f"Imobiliário: {contexto_json['BancoPine']['ProdutosEServicos']['SolucoesPorSetor']['Imobiliario']}\n"
    elif "empréstimo consignado" in pergunta:
        contexto_relevante += f"**Empréstimos Consignados:** {contexto_json['BancoPine']['ProdutosEServicos']['EmprestimosConsignados']['descricao']}\n"
    elif "cartão consignado" in pergunta:
        contexto_relevante += f"**Cartões Consignados:** {contexto_json['BancoPine']['ProdutosEServicos']['CartoesConsignados']['descricao']}\n"
    elif "segurança" in pergunta or "fraude" in pergunta:
        contexto_relevante += f"**Segurança e Privacidade:** {contexto_json['BancoPine']['SegurancaEPrivacidade']['descricao']}\n"
        contexto_relevante += "Dicas de segurança: \n"
        for dica in contexto_json["BancoPine"]["SegurancaEPrivacidade"]["dicas"]:
            contexto_relevante += f"- {dica}\n"
    elif "atendimento" in pergunta or "contato" in pergunta:
        contexto_relevante += f"**Canais de Atendimento:** {contexto_json['BancoPine']['CanaisDeAtendimento']['descricao']}\n"
        contexto_relevante += "Canais de Atendimento: \n"
        for opcao in contexto_json["BancoPine"]["CanaisDeAtendimento"]["opcoes"]:
            contexto_relevante += f"- **{opcao['nome']}**: {opcao['descricao']}\n"
    else:
        contexto_relevante += f"**História e Valores:** {contexto_json['BancoPine']['HistoriaEValores']['descricao']}\n"
    return contexto_relevante

def buscar_cotacao_moeda(base_currency="USD", target_currency="BRL"):
    """
    Busca a cotação de uma moeda específica usando a API de Exchange Rates.
    """
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    response = requests.get(url, params={"apikey": fkey})
    if response.status_code == 200:
        data = response.json()
        if "rates" in data and target_currency in data["rates"]:
            return data["rates"][target_currency]
        else:
            raise ValueError("A moeda alvo não foi encontrada na resposta da API.")
    else:
        raise ConnectionError("Erro ao acessar a API de cotações. Verifique sua conexão ou a chave de API.")


def formatar_resposta(resposta):
    """Formata a resposta do modelo."""
    # Adiciona uma quebra de linha antes de listas:
    if "- " in resposta:
        resposta = resposta.replace("- ", "\n- ")
    return resposta


exemplos_few_shot = """
Pergunta: Quais as opções de crédito que o banco oferece ?
Resposta: O banco oferece Capital de Giro, NCE/CCE, Nota Comercial, Cheque Empresa, Conta Garantida, FGI, Fiança, Confirming, Multi Sacado e CPR Financeira.

Pergunta: Quais os tipos de investimentos para empresas ?
Resposta: Os investimentos para empresas são: CDB, Compromissadas e Letra Financeira.

Pergunta: Como entro em contato com o banco ?
Resposta: Você pode entrar em contato por Atendimento Presencial, Central de Atendimento, Internet Banking, Aplicativo Mobile e WhatsApp
"""

instrucoes = "Você é um assistente virtual do Banco Pine, que irá ajudar os clientes respondendo a dúvidas sobre os produtos e serviços oferecidos. Utilize a linguagem mais clara e objetiva possível, e responda as perguntas como se estivesse em um chat. "

historico_conversas = []

while True:
    pergunta = input("Digite sua pergunta sobre o Banco Pine (ou 'quit' para sair): ")
    if pergunta.lower() == "quit":
        break

    contexto_relevante = extrair_contexto_relevante(contexto_banco_pine, pergunta)
    prompt_com_historico = f"{instrucoes}\n"
    for pergunta_historico, resposta_historico in historico_conversas:
        prompt_com_historico += f"Pergunta: {pergunta_historico}\nResposta: {resposta_historico}\n"
    prompt_com_historico += f"{contexto_relevante}\n{exemplos_few_shot}\nPergunta: {pergunta}\nResposta:"

    try:
        response = model.generate_content(prompt_com_historico)
        resposta_formatada = formatar_resposta(response.text)
        print(resposta_formatada)
        historico_conversas.append((pergunta, resposta_formatada))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

print("Chat encerrado.")