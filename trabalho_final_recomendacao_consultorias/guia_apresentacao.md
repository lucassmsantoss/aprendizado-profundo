# Guia de apresentação
### Propensão de Contratação de Consultoria — Sebrae/RN

14 slides, cerca de 15 minutos. Os tempos são sugestão, não camisa de força: se atrasar, os slides
5, 6 e 13 são os que aceitam corte sem quebrar a história.

Uma orientação que vale para todos: **cada slide tem uma faixa de conclusão no rodapé**. Ela é o
resumo do slide. Se você não souber como terminar de falar sobre um slide, leia a faixa em voz alta
e passe para o próximo — ela foi escrita para isso.

---

## Slide 1 — Capa (0:00–0:30)

Nome, disciplina, professor. Uma frase para situar:

> "O trabalho responde uma pergunta: dá para saber, antes de falar qualquer coisa com o cliente,
> quem tem propensão a contratar uma consultoria?"

Não adiante resultado aqui. Deixe a curiosidade.

---

## Slide 2 — Hoje ninguém oferece nada (0:30–2:00)

**Este é o slide mais importante da apresentação.** É ele que faz a sala se importar. Fale devagar.

Percorra os três passos: o cliente chega com uma demanda, a gente resolve, ele vai embora. E então
o ponto que muda tudo:

> "Repare que não existe prospecção. Não é descuido nem preguiça — é que oferecer no escuro tem
> risco. Uma oferta fora de hora pode afastar o cliente. Então o Sebrae espera a demanda chegar, e
> a oportunidade de aprofundar o relacionamento se perde em silêncio."

Termine com a faixa: dá para saber, antes de falar qualquer coisa, com quem vale aprofundar?

**Se perguntarem "isso é uma crítica ao Sebrae?"** — não. É a descrição de um processo que funciona
bem para atender demanda e que não foi desenhado para prospectar. O trabalho propõe uma capacidade
que hoje não existe, não conserta uma que está quebrada.

---

## Slide 3 — E se começássemos a oferecer no chute? (2:00–3:00)

Agora o número. 207.611 empresas depois da limpeza, 2,5% contratam, 1 acerto a cada 40 tentativas.

> "Fiz uma simulação: sortear quem abordar, 200 vezes. A taxa de acerto ficou em 2,49%, variando de
> 1,33% a 4,39%. É a taxa-base, e nada além dela."

Mencione que o MCC do chute é zero por definição — chutar não tem correlação nenhuma com a
resposta. Isso planta a semente do MCC, que volta no slide 11.

---

## Slide 4 — Os dois erros não custam o mesmo (3:00–4:15)

**Slide da justificativa metodológica.** É aqui que você defende a escolha da métrica, então não
corra.

> "Um falso positivo é uma ligação que não converte: custa alguns minutos. Um falso negativo é uma
> empresa que contrataria e nunca foi abordada: custa a oportunidade inteira. E o pior é que ela
> nem aparece em relatório, porque ninguém registra a venda que não aconteceu."

Daí sai a métrica prioritária: recall. E o argumento contra acurácia:

> "Acurácia não serve aqui. Responder 'não contrata' para todo mundo já acerta 97,5% e não encontra
> absolutamente ninguém."

A faixa fecha com o vocabulário do protocolo: métrica prioritária recall, contrapesos MCC e Brier.

---

## Slide 5 — Sete variáveis, e o que ficou de fora (4:15–5:15)

Passe rápido pelas sete variáveis: três numéricas de histórico de atendimento e quatro categóricas
de perfil cadastral.

Pare na linha destacada em âmbar:

> "Essa coluna aqui, quantidade de consultorias contratadas, eu tirei. Testei com uma tabela
> cruzada: ela é zero exatamente quando a empresa não contratou, e maior que zero exatamente quando
> contratou. É vazamento perfeito. Faz sentido, porque ela só é preenchida depois da contratação —
> no momento em que preciso decidir, esse número ainda não existe. Um modelo com ela teria acerto
> quase perfeito no papel e serventia nenhuma na prática."

**Se perguntarem por que não usou a coluna de qual consultoria foi contratada** — mesmo problema, e
além disso o tema da consultoria está fora do escopo deste trabalho.

---

## Slide 6 — Existe sinal para aprender (5:15–6:15)

Slide de sanidade: prova que o problema é aprendível.

> "Uma EPP contrata a 12%, um MEI a 0,3% — 37 vezes de diferença. Energia contrata a 11%, TIC a
> 2,6%. E quem contrata tem histórico maior: mediana de 17 atendimentos contra 4."

O fechamento é o argumento:

> "Se todas as fatias tivessem 2,5%, não haveria padrão nenhum para a rede achar. Tem."

---

## Slide 7 — Protocolo experimental (6:15–7:30)

Percorra os cinco passos sem se demorar. Depois pare na tabela:

> "A divisão é estratificada, e isso importa muito numa base com 2,5% de positivos: a proporção de
> contratantes ficou praticamente idêntica nos três conjuntos — 2,500%, 2,501% e 2,501%. Se eu
> tivesse sorteado sem estratificar, os conjuntos poderiam ficar desbalanceados entre si e a
> comparação seria injusta."

E o compromisso metodológico:

> "O conjunto de teste foi usado uma vez só, no final. Tudo que é escolha — hiperparâmetro, peso de
> classe, arquitetura — saiu da validação."

---

## Slide 8 — MLP e busca de hiperparâmetros (7:30–9:00)

Começe pelo tipo de rede:

> "É um MLP, rede densa, que é a arquitetura adequada para dado tabular. Não é CNN, que serve para
> imagem e explora estrutura espacial, nem RNN, que serve para sequência. Aqui cada empresa é uma
> linha independente."

Percorra as caixas e pare na saída:

> "A saída é uma sigmoide: devolve um número entre 0 e 1, uma nota para cada empresa. Quem passa de
> 0,5 é sinalizado — é o corte padrão de qualquer classificador binário, e eu não mexi nele."

Sobre o Optuna:

> "Vinte tentativas em oito minutos e meio. O MedianPruner interrompeu quatro delas no meio do
> treino, quando já estavam piores que a mediana das anteriores — isso libera tempo de máquina para
> testar mais configurações."

E o detalhe que vale ouro na faixa:

> "Um ponto de coerência: o EarlyStopping monitora o recall de validação, não a perda. Se
> monitorasse a perda, o modelo restaurado no fim do treino seria o de menor perda, que não é
> necessariamente o de maior recall. Treino e busca ficariam desalinhados."

**Os cinco chips na parte de baixo** são a configuração escolhida pelo Optuna. Não leia um por um
— aponte e diga "foi isso que a busca escolheu". A lista completa de hiperparâmetros está no
notebook, e a evolução do treino época a época (com o gif animado) está em `figuras/`, caso queira
mostrar.

---

## Slide 9 — Quanto peso dar a quem contrata? (9:00–10:30)

**Slide técnico mais denso.** Se você entender bem esta tabela, responde qualquer pergunta sobre
desbalanceamento.

Comece explicando o que é o contra-peso:

> "O contra-peso diz para a rede quanto custa cada tipo de erro. Sem ele, todos os exemplos pesam
> igual — e como só 2,5% contratam, ignorar a minoria é estatisticamente a jogada mais esperta que
> existe. A rede aprende a não apontar ninguém."

Percorra as três linhas:

> "Sem peso: 104 empresas apontadas em 31 mil, recall de 3%. Com peso suave, razão de 6 vezes:
> quase metade dos contratantes. Com peso balanceado, razão de 39 vezes — perder um contratante
> custa 39 vezes mais que um falso alarme —, 89% de recall."

O padrão é o que interessa:

> "Repare: o recall sobe de 3 para 89, e a precisão cai de 25 para 10. Isso não é defeito de
> configuração, é o mecanismo. Para capturar mais contratantes a rede precisa baixar a guarda, e ao
> baixar a guarda ela traz junto quem não contrata. São três pontos da mesma curva, e eu escolhi o
> da direita porque o critério do trabalho é recall."

E o preço, que não está no slide mas você fala:

> "Isso tem um custo escondido. A taxa real de contratação é 2,5%, mas o modelo balanceado prevê
> 26,6% em média — as probabilidades ficam infladas e o Brier vai de 0,033 para 0,137. Na prática:
> essa saída serve para ordenar empresas, não para dizer a alguém 'este cliente tem 26% de chance'."

As setas embaixo da tabela são o resumo visual: recall sobe, precisão cai.

---

## Slide 10 — 720 dos 779 contratantes (10:30–12:00)

O resultado principal. Vá pelos cartões e depois pela matriz de confusão:

> "No conjunto de teste, que nenhuma etapa do treino viu, o modelo capturou 720 dos 779
> contratantes e deixou passar 59. Recall de 92,4%. Para isso ele sinalizou 9.006 empresas, 28,9%
> da base."

Na matriz, aponte a linha de baixo — 720 acertos contra 59 escapes. A faixa fecha com o ROC-AUC
de 0,900.

**Se perguntarem sobre calibração** (a curva está no notebook, não no slide): ela fica bem longe da
diagonal, e é exatamente o efeito do contra-peso do slide anterior. O modelo ordena bem, mas o valor
absoluto da probabilidade está inflado — é consequência de uma escolha, não erro de ordenação.

---

## Slide 11 — Comparação no mesmo teste (12:00–13:15)

**O slide mais interessante do trabalho.** Apresente com calma, porque é o que mostra maturidade.

> "Treinei duas arquiteturas nos mesmos dados. A base codifica cada categoria pela frequência dela.
> A segunda usa embeddings: a rede aprende um vetor para cada município e cada segmento, em vez de
> reduzir tudo a um número."

Aponte as células em âmbar:

> "O modelo com embeddings ganha em precisão, MCC e ROC-AUC — e também no Brier, que não coube na
> tabela: 0,124 contra 0,163. Perde só no recall, por 1,6 ponto. Traduzindo: captura 13 contratantes
> a menos e poupa 2.710 abordagens."

E a conclusão honesta:

> "Como o critério declarado deste trabalho é recall, o modelo base é o escolhido. Mas isso expõe o
> limite de decidir por uma métrica só — se o critério fosse qualquer outra coluna dessa tabela, a
> decisão se inverteria. É por isso que MCC e Brier estão aqui como contrapesos: para que essa
> tensão fique visível em vez de escondida."

---

## Slide 12 — A ordenação é o que tem valor (13:15–14:15)

Traduza o modelo para linguagem de operação:

> "Dividi as empresas do teste em dez faixas, ordenadas pela probabilidade prevista. A primeira
> faixa converte a 15,35% — seis vezes o acaso — e já contém 61% de todos os contratantes. Nos 20%
> melhores estão 83%. Da metade da lista para baixo praticamente não há ninguém."

Na curva do meio:

> "Quanto mais distante a linha azul fica da pontilhada, melhor o modelo está ordenando."

Fecho:

> "Numa prospecção sem critério seriam 40 contatos para cada contratação. Seguindo a ordenação do
> modelo, 12,5."

---

## Slide 13 — Limitações (14:15–15:00)

Uma frase por item, sem se alongar. A primeira é a mais importante:

> "A mais séria é esta: como hoje o Sebrae não prospecta, a base registra quem procura o serviço
> espontaneamente — não quem aceitaria uma oferta. São coisas parecidas, mas não são a mesma. O
> modelo é uma boa aproximação inicial, e a única forma de medir a diferença é gerar dado de
> oferta."

As outras três você já demonstrou ao longo da apresentação: o ponto cego do recall (slide 11), a
calibração (slides 9 e 10) e o conjunto enxuto de variáveis.

---

## Slide 14 — O modelo é o começo, não o fim (15:00–15:30)

> "O passo que mais muda o jogo é o piloto: abordar um grupo sinalizado e registrar a resposta.
> É isso que gera o dado que hoje não existe."

Mencione rapidamente engenharia de atributos e a busca de hiperparâmetros para os embeddings. E o
destino:

> "Num cenário hipotético, isso viveria dentro do CRM. Não como uma ordem de venda — como um sinal
> para quem atende de que vale a pena aprofundar o relacionamento com aquele cliente."

Encerre com o link do repositório na tela.

---

# Perguntas prováveis

**"Por que 0,5 de limiar? Por que não ajustou?"**
É o corte padrão de qualquer classificador binário e não foi garimpado. O tratamento do
desbalanceamento acontece num lugar só, no treino, pelo contra-peso. O experimento do slide 9
mostra medido o que acontece nesse mesmo corte sob cada configuração de peso.

**"Por que não usou SMOTE ou oversampling?"**
O contra-peso resolve o mesmo problema sem duplicar nem sintetizar dado. Numa base de 145 mil
linhas com 3,6 mil positivos, gerar exemplos artificiais adicionaria risco de sobreajuste sem
ganho claro.

**"O modelo não está apenas sinalizando mais gente?"**
Em parte sim, e por isso a coluna de empresas sinalizadas aparece em todas as tabelas. O que mostra
que não é só volume é a ordenação: os 10% do topo concentram 61,4% dos contratantes, o que um
modelo que apenas aponta mais gente não conseguiria.

**"Por que escolheu o modelo com pior precisão e pior Brier?"**
Porque o critério declarado é recall, e ele vem do custo assimétrico dos erros. A tabela do slide
11 deixa o custo dessa escolha explícito em vez de escondê-lo.

**"Por que o Brier está tão alto?"**
Porque o contra-peso balanceado infla as probabilidades. A referência de quem responde sempre a
taxa-base é 0,024, e o modelo ficou em 0,163. A saída serve para ranquear, não como probabilidade
literal. Sem contra-peso o Brier cai para 0,033, mas o recall despenca para 3%.

**"Por que MLP e não uma CNN ou uma rede mais profunda?"**
Dado tabular, cada empresa é uma linha independente, sem estrutura espacial nem temporal. E a
própria busca do Optuna escolheu 3 camadas — arquiteturas maiores foram testadas e não venceram.

**"O que garante que não houve vazamento?"**
Três coisas: a coluna que vazava foi identificada por tabela cruzada e removida; o pré-processador
é ajustado só no treino, e validação e teste apenas transformam; e o teste foi usado uma única vez,
no fim.

**"Isso está em produção?"**
Não. É um trabalho de disciplina. O cenário do CRM é hipotético, e o próximo passo real seria um
piloto controlado.

---

# Checklist antes de apresentar

- Abrir o notebook executado numa aba, caso peçam para ver código ou uma saída específica.
- Se for mostrar o gif do treinamento, deixá-lo aberto separadamente (o slide traz o quadro final).
- Cronometrar uma passada completa: o alvo é 15 minutos, e os slides 5, 6 e 13 são os cortáveis.
- Ter na ponta da língua três números: **92,4% de recall**, **720 de 779**, **6,1x o acaso nos 10%
  do topo**.
