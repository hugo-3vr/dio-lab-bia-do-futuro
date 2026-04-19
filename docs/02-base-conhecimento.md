# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar preocupações anteriores da diretoria (ex: aversão a altas taxas de juros) para calibrar a abordagem da IA. |
| `perfil_empresa.json` | JSON | Fornecer a situação atual da empresa (faturamento, saldo atual em conta, setor e metas financeiras corporativas).s |
| `linhas_credito.json` | JSON | Listar o catálogo de produtos de crédito disponíveis (antecipação, giro parcelado, cheque especial) com suas taxas exatas. |
| `transacoes.csv` | CSV | Projetar o fluxo de caixa, mapeando as datas de Contas a Pagar (folha, fornecedores) versus Contas a Receber (cartões, boletos). |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Para adequar o projeto ao caso de uso de Gestão de Capital de Giro para PMEs, os dados sugeridos originalmente (focados em pessoa física/investimentos) foram totalmente substituídos por dados corporativos (mockados):

- De Pessoa Física para PJ: O arquivo perfil_investidor.json virou perfil_empresa.json, focando em razão social, saldo em conta e faturamento, em vez de idade e renda pessoal.
- De Investimentos para Crédito: O arquivo produtos_financeiros.json virou linhas_credito.json, substituindo CDBs e Fundos por produtos de alavancagem e cobertura de caixa (Antecipação de Recebíveis e Cheque Especial).
- Descasamento Proposital: O arquivo transacoes.csv foi construído com um "furo de caixa" intencional (grandes despesas no dia 15 e grandes recebimentos apenas no dia 25) para engatilhar a proatividade do agente

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV e JSON são lidos localmente na inicialização da aplicação usando a biblioteca Pandas no Python (backend do Streamlit). Eles permanecem na memória da sessão para consultas rápidas.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados não são despejados crus no System Prompt. Para evitar alucinações matemáticas, o Pandas realiza o cálculo do saldo futuro primeiro. O resultado desse cálculo (junto com as taxas dos produtos) é formatado em um bloco de texto estruturado e injetado dinamicamente como "Contexto Atualizado" no prompt a cada nova interação do usuário, garantindo que a IA apenas interprete os números, sem precisar calculá-los.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados da Empresa:
- Razão Social: TechIndustrial Peças LTDA
- Perfil de Risco: Conservador
- Saldo atual em conta: R$ 14.500,00

Cenário de Caixa (Próximos 15 dias):
- 15/05: Saída - Folha de Pagamento (R$ 25.000,00)
- 15/05: Saída - Aluguel Galpão (R$ 5.000,00)
- ALERTA: Déficit projetado para 15/05 é de R$ -15.500,00.
- 25/05: Entrada - Recebimento Cartões (R$ 45.000,00)

Linhas de Crédito Disponíveis para Cobertura:
1. Antecipação de Recebíveis Cartão (Taxa: 1.85% a.m. | D+0)
2. Capital de Giro Parcelado (Taxa: 3.50% a.m. | D+2)
3. Cheque Especial PJ (Taxa: 8.90% a.m. | Imediato)

Histórico de Relacionamento:
- 10/03: Cliente demonstrou preocupação com taxas altas. Priorizar soluções de menor Custo Efetivo.
...
```
