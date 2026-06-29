# Base de Conhecimento

## Dados Utilizados

O agente FinAI consome integralmente os dados contidos na pasta `data` do repositório para contextualizar cada interação e garantir respostas hiper-personalizadas de acordo com a realidade financeira do cliente.

| Arquivo | Formato | Utilização no Agente |
| --- | --- | --- |
| `transacoes.csv` | CSV | Utilizado para analisar o padrão de consumo recente do cliente, calcular o saldo atual operacional e identificar possíveis desvios ou oportunidades de economia. |
| `historico_atendimento.csv` | CSV | Consultador no início da sessão para identificar solicitações anteriores abertas, dúvidas recorrentes ou problemas técnicos relatados, garantindo a persistência histórica do relacionamento. |
| `perfil_investidor.json` | JSON | Mapeia o perfil de risco do cliente (Ex: Conservador, Moderado, Arrojado) e seus objetivos financeiros. É a principal trava de segurança e diretriz para a explicação de produtos. |
| `produtos_financeiros.json` | JSON | Funciona como o catálogo oficial do banco. O agente consulta esse arquivo para detalhar taxas, regras de resgate, carências e descrição dos produtos financeiros válidos para o cliente. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados originais fornecidos no laboratório foram mantidos em sua estrutura estrutural para fins de reprodutibilidade, porém foram aplicados **tratamentos dinâmicos em tempo de execução via Pandas** no ecossistema Python:

1. **Computação de Variáveis:** O arquivo de transações é agrupado por categoria e somado dinamicamente para gerar um resumo de "Gastos por Categoria" antes do envio ao modelo.
2. **Filtragem por Perfil de Risco:** O catálogo de `produtos_financeiros.json` passa por uma máscara lógica em Python que oculta produtos de risco incompatíveis com o perfil capturado em `perfil_investidor.json`.

---

## Estratégia de Integração

### Como os dados são carregados?

> Descreva como seu agente acessa a base de conhecimento.

No momento em que a interface em **Streamlit** é iniciada, um script em Python lê os arquivos CSV e JSON armazenados localmente na pasta `data/`. Esses arquivos são convertidos em estruturas nativas do Python (Dicionários e DataFrames do Pandas). Para otimizar a performance da aplicação e evitar leituras de disco a cada mensagem enviada, os dados processados do cliente logado são armazenados em cache na memória de sessão do Streamlit (`st.session_state`).

### Como os dados são usados no prompt?

> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são injetados de forma **dinâmica e contextualizada**. O `System Prompt` define estritamente as regras de comportamento do FinAI (a persona, tom de voz e diretrizes de segurança). Quando o cliente faz uma pergunta na interface, uma camada intermediária em Python extrai o estado atual consolidado do usuário (saldo, perfil e os produtos elegíveis) e formata esses dados como uma string estruturada. Essa string é injetada logo acima da mensagem do usuário como uma mensagem de contexto (`Context Block`), permitindo que a LLM processe a resposta com dados em tempo real sem sobrecarregar o prompt do sistema.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```text
[CONTEXTO DO CLIENTE LOGADO]
Dados Cadastrais e Perfil:
- Nome do Cliente: Renan Evangelista
- Perfil de Investidor: Moderado
- Objetivos Declarados: Reserva de emergência e transição de carreira internacional

Resumo Financeiro Atualizado (Via Pandas):
- Saldo Consolidado em Conta: R$ 7.420,00
- Maior Categoria de Gastos Recentes: Serviços & Assinaturas (R$ 340,00)
- Status do Último Atendimento (05/06/2026): Concluído (Dúvida sobre taxas de câmbio)

Produtos Financeiros Elegíveis Filtrados (Injetados para Consulta da IA):
[
  {"nome": "CDB Pós-Fixado Liquidez Diária", "rendimento": "100% do CDI", "risco": "Baixo"},
  {"nome": "Fundo Multimercado Estabilidade", "rendimento": "112% do CDI", "risco": "Moderado"}
]
--------------------------------------------------------------------------------
[MENSAGEM DO USUÁRIO]: "Quais são as melhores opções de rendimento seguras para mim hoje e quanto meu saldo renderia nelas?"

```
