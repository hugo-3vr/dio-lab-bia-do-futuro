import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURAÇÃO E ESTILIZAÇÃO (UI)
# ==========================================
st.set_page_config(page_title="Aura - Capital de Giro", page_icon="🛡️", layout="wide")

# Remove botões padrão do Streamlit (Deploy, Menu, etc) para visual de produção
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    </style>
    """, unsafe_allow_html=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

# ==========================================
# 2. MOTOR DE DADOS
# ==========================================
@st.cache_data
@st.cache_data
def carregar_dados():
    try:
        transacoes = pd.read_csv('data/transacoes.csv')
        historico = pd.read_csv('data/historico_atendimento.csv')
        with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
            perfil = json.load(f)
        with open('data/produtosfinanceiros.json', 'r', encoding='utf-8') as f:
            linhas_credito = json.load(f)

        # ==========================================
        # TRUQUE DE PORTFÓLIO: DADOS "EVERGREEN"
        # Garante que as datas sempre fiquem no futuro,
        #  independente de quando testar o app.
        # ==========================================
        transacoes['data'] = pd.to_datetime(transacoes['data']) # Converte a coluna para formato de data
        data_mais_antiga = transacoes['data'].min() # Acha a data mais antiga no CSV
        
        # Calcula a diferença entre "Hoje + 2 dias" e a data mais antiga do CSV
        diferenca = (datetime.now() + timedelta(days=2)) - data_mais_antiga
        
        # Empurra todas as datas para frente mantendo o mesmo espaçamento entre elas
        transacoes['data'] = transacoes['data'] + diferenca
        transacoes['data'] = transacoes['data'].dt.strftime('%Y-%m-%d') # Volta para formato texto bonitinho
        # ==========================================

        return transacoes, historico, perfil, linhas_credito
    except Exception as e:
        st.error(f"Erro ao carregar dados corporativos: {e}")
        return None, None, None, None

def calcular_analise_caixa(df, saldo_atual):
    df_futuro = df[df['status'].isin(['agendado', 'previsto'])].copy()
    total_saidas = df_futuro[df_futuro['tipo'] == 'saida']['valor'].sum()
    total_entradas = df_futuro[df_futuro['tipo'] == 'entrada']['valor'].sum()
    saldo_projetado = saldo_atual - total_saidas
    return total_saidas, total_entradas, saldo_projetado

# ==========================================
# 3. PROMPTS E API
# ==========================================
SYSTEM_PROMPT = """Você é Aura, uma IA especialista em Estratégia de Capital de Giro para PMEs.
Seu objetivo é analisar o fluxo de caixa do cliente de forma direta e objetiva.

REGRAS:
1. ZERO MATEMÁTICA: Você é ESTRITAMENTE PROIBIDA de fazer cálculos de cabeça, médias diárias, rateios ou estimativas. 
2. USE O CONTEXTO: Você deve ler e informar APENAS o valor de "Saldo Projetado (Déficit)" e "Saídas" que já foram pré-calculados no bloco [CONTEXTO ATUALIZADO].
3. TEXTO LIMPO: É PROIBIDO usar formatação markdown (como asteriscos ** para negrito) nos valores financeiros. Escreva os valores de forma limpa e padronizada (ex: R$ 15.500,00).
4. SEM FÓRMULAS: Nunca mostre contas matemáticas na tela. Apenas informe a situação do caixa e sugira a solução.
5. PRIORIDADE: Sempre priorize sugerir a Antecipação de Recebíveis antes do Cheque Especial.
6. Seja direta, executiva e consultiva. Máximo de 3 parágrafos curtos.
7. FOCO EXCLUSIVO (CONSTRANGIMENTO DE DOMÍNIO): Você só tem autorização para falar sobre gestão financeira, fluxo de caixa e estratégias de capital de giro baseadas nos dados fornecidos. 
   - Se o usuário perguntar sobre QUALQUER outro assunto (política, esportes, culinária, previsões de mercado, piadas ou tarefas gerais), responda: "Como sua consultora estratégica de capital de giro, meu foco é restrito à saúde financeira da sua operação. Não possuo informações ou autorização para tratar de outros temas."
   - Você NÃO realiza transações financeiras (Pix, pagamentos)."""

def gerar_contexto(perfil, saídas, entradas, saldo_proj, linhas, df_transacoes):
    # Transforma as linhas do CSV em um formato de texto que a IA consiga ler
    df_futuro = df_transacoes[df_transacoes['status'].isin(['agendado', 'previsto'])]
    resumo_lancamentos = df_futuro[['descricao', 'valor', 'tipo']].to_dict(orient='records')
    
    return f"""
    [CONTEXTO ATUALIZADO]
    Empresa: {perfil['razao_social']} | Saldo: R$ {perfil['saldo_atual_conta']:.2f}
    Projeção: Saídas R$ {saídas:.2f} | Saldo Projetado (Déficit) R$ {saldo_proj:.2f}
    Lançamentos na Tabela: {resumo_lancamentos}
    Linhas: {json.dumps(linhas, ensure_ascii=False)}
    """

def perguntar_ollama(msg, contexto):
    prompt_completo = f"{SYSTEM_PROMPT}\n\n{contexto}\n\nUsuário: {msg}"
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt_completo, "stream": False})
        return r.json().get('response', 'Erro de resposta.')
    except Exception as e:
        return f"Falha de comunicação interna. Detalhes: {e}"

# ==========================================
# 4. INTERFACE PRINCIPAL
# ==========================================
st.title("🛡️ Aura | Portal de Tesouraria Corporativa")
st.markdown("---")

transacoes, historico, perfil, linhas = carregar_dados()

if transacoes is not None:
    # Sidebar Corporativa
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2933/2933116.png", width=60) # Ícone genérico de banco/empresa
        st.header("Resumo da Conta")
        st.write(f"**{perfil['razao_social']}**")
        st.metric("Saldo Disponível", f"R$ {perfil['saldo_atual_conta']:,.2f}")
        st.divider()
        st.caption(f"🎯 Meta Corporativa: {perfil['meta_financeira']}")

    # Layout de Painel
    col_dados, col_espaco, col_chat = st.columns([1.2, 0.1, 1])

    with col_dados:
        st.subheader("📅 Próximos Lançamentos (D+15)")
        
        # Formatação elegante da tabela
        df_futuro = transacoes[transacoes['status'].isin(['agendado', 'previsto'])]
        st.dataframe(
            df_futuro,
            column_config={
                "data": st.column_config.DateColumn("Data Venc."),
                "descricao": "Descrição",
                "categoria": "Centro de Custo",
                "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                "tipo": "Fluxo",
                "status": "Status"
            },
            hide_index=True,
            use_container_width=True
        )

    with col_chat:
        st.subheader("💬 Consultoria Estratégica")
        
        # MENSAGEM PROATIVA DA AURA (O truque para parecer profissional)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Olá! Sou a Aura, sua CFO Digital. Atualizei seu painel e identifiquei um **déficit projetado** para os próximos dias devido à Folha de Pagamento. Gostaria que eu simulasse uma estratégia de cobertura usando seus recebíveis?"}
            ]

        # Container do chat
        caixa_chat = st.container(height=400, border=False)
        with caixa_chat:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Input do usuário
        if prompt := st.chat_input("Digite sua mensagem ou autorize a simulação..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with caixa_chat.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Analisando cenários de crédito..."):
                s_tot, e_tot, s_proj = calcular_analise_caixa(transacoes, perfil['saldo_atual_conta'])
                
                # ATENÇÃO: A linha abaixo mudou a última palavra para 'transacoes'
                contexto = gerar_contexto(perfil, s_tot, e_tot, s_proj, linhas, transacoes)
                
                resposta_aura = perguntar_ollama(prompt, contexto)
                resposta_aura = resposta_aura.replace("$", "\\$")

            with caixa_chat.chat_message("assistant"):
                st.markdown(resposta_aura)
            st.session_state.messages.append({"role": "assistant", "content": resposta_aura})
