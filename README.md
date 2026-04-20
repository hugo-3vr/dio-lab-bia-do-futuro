# 🛡️ Aura Performance | CFO Digital Estrategista

> **Desafio BIA do Futuro (DIO & Bradesco)**
> Agente de Inteligência Artificial Generativa Local para Gestão Proativa de Capital de Giro em PMEs.

---

## 🎯 O Problema de Negócio
A maior causa de mortalidade de PMEs no Brasil não é a falta de lucro, mas a **quebra do fluxo de caixa**. O fenômeno do "descasamento de prazos" (pagar fornecedores antes de receber de clientes) cria furos de liquidez que forçam o gestor a recorrer a créditos caros por falta de planejamento.

**A Aura Performance resolve isso atuando como um "Escudo de Margem":**
1. **Identificação Preditiva:** Detecta déficits futuros antes mesmo do gestor abrir o extrato.
2. **Análise de Custo de Capital:** Compara taxas de Antecipação vs. Empréstimos de forma determinística.
3. **Execução Consultiva:** Sugere a estratégia de menor Custo Efetivo Total (CET) para proteger o lucro da operação.

---

## 🚀 Diferenciais de Engenharia

### 1. Privacy by Design (IA Local)
Utilização do **Ollama** com o modelo `gpt-oss` rodando localmente. Isso garante que dados sensíveis de faturamento e movimentação bancária da empresa nunca saiam do perímetro de segurança local.

### 2. Motor de Dados Evergreen
Implementação de lógica em **Pandas** que realiza o *Time-Shifting* dinâmico dos dados. O sistema recalcula as datas de vencimento em relação ao tempo real, garantindo que o cenário de teste esteja sempre atualizado.

### 3. Blindagem contra Alucinação (Guardrails)
* **Cálculo Determinístico:** A IA é proibida de realizar contas. O backend em Python processa os números e injeta os resultados exatos no contexto.
* **Restrição de Domínio:** Filtros de escopo impedem a IA de discorrer sobre temas irrelevantes (política, lazer), mantendo o foco 100% corporativo.

---

## 🏗️ Arquitetura do Sistema

```mermaid
flowchart TD
    A[Gestor Financeiro] -->|Interação Natural| B[Interface Streamlit]
    B -->|Processamento ETL| C[Pandas Engine]
    C -->|Recálculo Evergreen| D[(Arquivos Corporativos CSV/JSON)]
    C -->|Contexto Sanitizado| E[Injeção de Prompt]
    E -->|IA Local / Ollama| F[LLM - gpt-oss]
    F -->|Recomendação Estratégica| B
    B -->|Visualização de Dados| A
