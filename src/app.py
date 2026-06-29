# src/app.py

# =====================================================================
# 1. IMPORTS
# =====================================================================
import os
import json
import pandas as pd
import requests
import streamlit as st

# =====================================================================
# 2. CONFIGURAÇÃO (Ollama & Modelo)
# =====================================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

# Configuração da página do Streamlit (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="FinAI - Assistente Financeiro", page_icon="💰", layout="centered")

# =====================================================================
# 3. CARREGAR DADOS (Pasta data/)
# =====================================================================
@st.cache_data
def carregar_base_de_conhecimento():
    """Busca os dados na pasta data/, lidando com caminhos relativos de execução"""
    # Encontra o caminho correto para a pasta data independente de onde o script é chamado
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    
    try:
        transacoes = pd.read_csv(os.path.join(data_dir, "transacoes.csv"))
        historico = pd.read_csv(os.path.join(data_dir, "historico_atendimento.csv"))
        
        with open(os.path.join(data_dir, "perfil_investidor.json"), "r", encoding="utf-8") as f:
            perfil = json.load(f)
            
        with open(os.path.join(data_dir, "produtos_financeiros.json"), "r", encoding="utf-8") as f:
            produtos = json.load(f)
            
        return transacoes, historico, perfil, produtos
    except FileNotFoundError as e:
        st.error(f"Erro: Arquivo base não encontrado na pasta data/. Detalhes: {e}")
        return None, None, None, None

df_transacoes, df_historico, json_perfil, json_produtos = carregar_base_de_conhecimento()

# =====================================================================
# 4. MONTAR CONTEXTO
# =====================================================================
def construir_bloco_contexto():
    """Processa as bases de dados e consolida em uma string estruturada para a LLM"""
    if df_transacoes is None:
        return "Dados indisponíveis."
    
    # Tratamento via Pandas: Agrupando maiores gastos por categoria
    gastos_categoria = df_transacoes.groupby('categoria')['valor'].sum().to_dict()
    gastos_formatados = ", ".join([f"{cat}: R$ {val:,.2f}" for cat, val in gastos_categoria.items()])
    
    # Simulação de saldo dinâmico (com base em um valor fictício inicial menos os gastos)
    saldo_calculado = 10000.00 - df_transacoes['valor'].sum()
    
    # Filtragem de produtos por adequação (exemplo simples usando o perfil do cliente)
    perfil_cliente = json_perfil.get("perfil", "Conservador")
    produtos_filtrados = [p for p in json_produtos.get("produtos", []) if p.get("risco") == perfil_cliente or p.get("risco") == "Baixo"]

    contexto = f"""
[CONTEXTO DO CLIENTE LOGADO]
Dados Cadastrais e Perfil:
- Nome do Cliente: {json_perfil.get("nome", "Jorge Batista")}
- Perfil de Investidor: {perfil_cliente}
- Objetivos: {", ".join(json_perfil.get("objetivos", []))}

Resumo Financeiro Atualizado (Computado via Pandas):
- Saldo Consolidado Calculado em Conta: R$ {saldo_calculado:,.2f}
- Histórico de Gastos por Categoria: {gastos_formatados}
- Última Interação no Histórico: {df_historico['assunto'].iloc[-1] if not df_historico.empty else "Nenhum histórico recente"}

Produtos Financeiros Elegíveis Filtrados (Injetados para Consulta):
{json.dumps(produtos_filtrados, ensure_ascii=False, indent=2)}
--------------------------------------------------------------------------------
"""
    return contexto

# =====================================================================
# 5. SYSTEM PROMPT
# =====================================================================
SYSTEM_PROMPT = """Você é o FinAI, um agente digital de relacionamento financeiro, consultivo e altamente educativo. Seu objetivo principal é guiar os usuários em suas dúvidas diárias sobre produtos financeiros, fornecer explicações didáticas e realizar simulações demonstrativas claras e seguras, sempre pautadas em boas práticas de UX.

REGRAS DE COMPORTAMENTO E OPERAÇÃO:
1. BASE DE DADOS E CONTEXTO: Suas respostas devem se fundamentar estritamente nos dados do cliente fornecidos no bloco de contexto estruturado. Nunca invente valores, transações ou produtos fora dessa base.
2. DIRETRIZ DE ANTI-ALUCINAÇÃO: Se a informação solicitada pelo usuário não estiver presente no contexto fornecido ou se envolver dados históricos ausentes, diga polidamente que não possui o dado no momento e redirecione-o para o suporte humano ou para o escopo disponível.
3. ESTILO DE COMUNICAÇÃO: Use tom acessível, empático e focado em educação financeira. Evite termos excessivamente técnicos sem explicá-los de forma simples logo em seguida.
4. TRAVA DE SEGURANÇA (SUITABILITY): Ao falar sobre investimentos ou produtos, verifique o "Perfil de Investidor" contido no contexto. Nunca recomende produtos de risco incompatíveis com o perfil do usuário.
5. SIMULAÇÕES DEMONSTRATIVAS: Ao efetuar cálculos financeiros demonstrativos, utilize uma linguagem clara indicando que os valores são projeções hipotéticas baseadas nas taxas vigentes contidas no catálogo."""

# =====================================================================
# 6. CHAMAR O OLLAMA
# =====================================================================
def consultar_ollama(prompt_usuario, contexto_cliente):
    """Realiza a chamada de inferência para o Ollama utilizando o modelo llama3.1"""
    # Concatenação seguindo a estratégia de engenharia de prompt desenhada
    prompt_completo = f"{SYSTEM_PROMPT}\n\n{contexto_cliente}\n\n[MENSAGEM DO USUÁRIO]: {prompt_usuario}"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt_completo,
        "stream": False
    }
    
    try:
        resposta = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if resposta.status_code == 200:
            return resposta.json().get("response", "Erro ao processar campo response.")
        else:
            return f"❌ Erro na API do Ollama: Status {resposta.status_code}. Certifique-se de que o modelo '{MODEL_NAME}' está carregado."
    except requests.exceptions.ConnectionError:
        return "❌ Erro de Conexão: O Ollama não parece estar rodando no localhost:11434. Inicie o serviço do Ollama e tente novamente."

# =====================================================================
# 7. INTERFACE (Streamlit)
# =====================================================================
st.title("💰 FinAI — Relacionamento Inteligente")
st.caption("Protótipo de IA Generativa voltado à experiência do cliente bancário")

# Inicializa o histórico de conversas na sessão do Streamlit (Persistência de Contexto)
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Exibe as mensagens anteriores do chat
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Entrada de nova mensagem do usuário
if entrada_usuario := st.chat_input("Como posso ajudar com suas finanças hoje?"):
    # Mostra e salva a mensagem do usuário
    st.session_state.historico_chat.append({"role": "user", "content": entrada_usuario})
    with st.chat_message("user"):
        st.markdown(entrada_usuario)
        
    # Processamento do agente
    with st.chat_message("assistant"):
        with st.spinner("Analisando dados do perfil e gerando resposta segura..."):
            contexto_atual = construir_bloco_contexto()
            resposta_agente = consultar_ollama(entrada_usuario, contexto_atual)
            st.markdown(resposta_agente)
            
    # Salva a resposta do assistente no histórico
    st.session_state.historico_chat.append({"role": "assistant", "content": resposta_agente})
