# Pitch (3 minutos)

## Roteiro Sugerido

### 1. O Problema (30 seg)

> Qual dor do cliente você resolve?

"No cenário financeiro atual, os clientes buscam respostas rápidas e personalizadas. No entanto, os canais de atendimento tradicionais falham de duas formas: ou sobrecarregam o suporte humano com filas de espera para dúvidas simples, ou utilizam chatbots rígidos baseados em árvores de decisão que frustram o usuário por não entenderem a linguagem natural. Além disso, as poucas soluções de IA que existem no mercado sofrem com alucinações, inventando saldos, transações e induzindo o cliente a erros de cálculo perigosos."

### 2. A Solução (1 min)

> Como seu agente resolve esse problema?

"Para resolver isso, desenvolvemos o **FinAI**, uma experiência digital de relacionamento financeiro guiada por IA Generativa local e fundamentada em ótimas práticas de UX. O grande diferencial do FinAI é sua arquitetura híbrida de segurança: nós isolamos a inteligência da LLM (`llama3.1` via Ollama) dos cálculos matemáticos.

Toda a leitura de saldo, histórico de atendimento e agrupamento de gastos do cliente é processada de forma exata em código Python usando a biblioteca Pandas. Esses dados reais são injetados dinamicamente em um bloco de contexto seguro, permitindo que a IA converse com o cliente de forma extremamente empática, fluida, educativa e, acima de tudo, **100% precisa e livre de alucinações**."

### 3. Demonstração (1 min)

> Mostre o agente funcionando (pode ser gravação de tela)

No vídeo, a tela do protótipo desenvolvido em **Streamlit** é exibida demonstrando os seguintes passos em tempo real:

1. **Consulta Dinâmica de Gastos:** O usuário pergunta quanto gastou com assinaturas. A aplicação roda o Pandas por trás, soma os valores do arquivo `transacoes.csv` e a IA responde amigavelmente o valor de R$ 340,00, sugerindo uma meta de economia.
2. **Filtro de Suitability (Segurança):** O usuário pede uma recomendação de investimento. A IA lê o `perfil_investidor.json` (Moderado) e o catálogo de produtos, oferecendo apenas opções compatíveis (CDB e Fundo Multimercado), demonstrando a trava de segurança em ação.
3. **Tratamento de Escopo (Edge Cases):** O usuário tenta tirar o agente do foco perguntando sobre o clima ou roteiros para Barcelona. O FinAI nega a resposta de forma polida e traz o usuário de volta para o planejamento financeiro da viagem, provando a resiliência do prompt.

### 4. Diferencial e Impacto (30 seg)

> Por que essa solução é inovadora e qual é o impacto dela na sociedade?

"O FinAI inova ao provar que é possível ter a empatia e a flexibilidade da IA Generativa sem abrir mão da governança de dados rígida do setor bancário. O impacto disso na sociedade é a democratização da educação financeira de qualidade: entregamos um mentor acessível na mão de cada cliente, reduzindo custos operacionais das instituições e aumentando a segurança e a consciência financeira do usuário final."

---

## Checklist do Pitch

* [X] Duração máxima de 3 minutos
* [X] Problema claramente definido
* [X] Solução demonstrada na prática
* [X] Diferencial explicado
* [X] Áudio e vídeo com boa qualidade

---

## Link do Vídeo

> Cole aqui o link do seu pitch (YouTube, Loom, Google Drive, etc.)

[[https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://youtu.be/ghK1t2fYlbE)]([https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://youtu.be/ghK1t2fYlbE))
