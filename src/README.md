# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

# O Desafio de Negócio
Muitas PMEs fecham o mês no "azul", mas quebram durante o mês por falta de Capital de Giro. O problema não é o lucro, mas o descasamento de prazos (pagar fornecedores antes de receber dos clientes).

Aura resolve isso atuando como uma CFO Digital que:
1. Identifica furos de caixa em tempo real (D-0).
2. Analisa o custo-benefício de linhas de crédito (Antecipação vs. Giro vs. Cheque Especial).
3. Sugere estratégias proativas para evitar juros abusivos.

## Estrutura Sugerida

```
├── data/
│   ├── transacoes.csv           # Base de lançamentos futuros
│   ├── historico_atendimento.csv  # Memória de interações passadas
│   ├── perfil_investidor.json    # Dados da empresa e metas
│   └── produtosfinanceiros.json  # Taxas e prazos de crédito
├── src/
│   ├── app.py                   # Interface Streamlit e Lógica de Negócio
│   └── ...                      # Módulos de suporte
├── requirements.txt             # Dependências do sistema
```

## Exemplo de requirements.txt

```
streamlit
pandas
requests
ollama API
```

## Como Rodar

```bash
# Pré-requisitos
Ter o Ollama instalado.
Baixar o modelo: gpt-oss

# Clone o repositório
git clone https://github.com/seu-usuario/aura-bradesco.git

# Entre na pasta
cd aura-bradesco

# Instale as dependências
pip install -r requirements.txt


# Rodar a aplicação
streamlit run src/app.py
```
