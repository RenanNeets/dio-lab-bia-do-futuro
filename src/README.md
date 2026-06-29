# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura Sugerida

```
meu-projeto/
├── run.py
├── data/
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   └── produtos_financeiros.json
└── src/
    └── app.py
```


## Lembrete

O código foi projetado para funcionar com o Ollama utilizando o modelo llama3.1, ele deve estar instalado no seu dispositivo e com o modelo indicado no projeto

# Rodar a aplicação
streamlit run app.py
```