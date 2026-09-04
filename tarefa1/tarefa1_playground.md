# Tarefa 1 — Estudo Dirigido: TensorFlow Playground

**Aluno:** Lucas Medeiros
**Disciplina:** Aprendizado Profundo — PPgTI/IMD/UFRN
**Docente:** Prof. Josenalde Oliveira

Todos os experimentos abaixo foram executados de fato no [TensorFlow Playground](https://playground.tensorflow.org), interagindo com a interface (troca de hiperparâmetros, treino, reset) e registrando os valores reais de época, perda de treino/teste e o formato da fronteira de decisão observada.

## a) Padrões aprendidos por uma NN (configuração padrão)

Configuração: dataset *Circle*, 2 features (X1, X2), 2 camadas ocultas (4 e 2 neurônios), ativação **tanh**, taxa de aprendizagem 0.03, sem regularização, ruído 0, batch size 10.

Ao treinar, a rede converge rapidamente: em **699 épocas** obtive perda de teste = **0.002** e perda de treino = **0.001**, com uma fronteira de decisão circular suave, coerente com a distribuição dos dados. Isso confirma o comportamento descrito: os neurônios da primeira camada oculta aprendem padrões simples (retas/curvas separando parcialmente o espaço) e a segunda camada combina essas saídas para formar a fronteira circular final — quanto mais camadas/neurônios, mais complexos os padrões que a rede pode compor.

## b) Função de ativação

Mantendo a arquitetura de (a), troquei apenas a ativação:

| Ativação | Épocas | Perda teste | Perda treino | Fronteira de decisão |
|---|---|---|---|---|
| Tanh (baseline) | 699 | 0.002 | 0.001 | curva suave (circular) |
| ReLU | 621 | 0.001 | 0.000 | **poligonal/angular**, com "quinas" nas bordas |
| Linear | 1918 (sem melhora) | 0.514 | 0.492 | **nenhuma fronteira útil** — praticamente uma reta/gradiente difuso |

Com **ReLU** a rede convergiu um pouco mais rápido que com tanh e chegou a uma perda ligeiramente menor, mas a fronteira deixou de ser suave: como o ReLU é linear por partes, a região de decisão vira um polígono (faces retas), enquanto o tanh gera fronteiras curvas por ser uma função suave/saturante.

Com **Linear**, mesmo depois de quase 2000 épocas o erro não sai de ~0.5 (equivalente a chute aleatório). Isso é esperado: uma composição de camadas totalmente lineares equivale, algebricamente, a uma única camada linear (não importa a profundidade), e um classificador linear não consegue separar um padrão circular, que não é linearmente separável. Não consegue classificar de forma alguma.

## c) Taxa de aprendizagem (learning rate)

Mantendo tanh e demais parâmetros fixos:

| Learning rate | Épocas | Perda teste | Perda treino | Observação |
|---|---|---|---|---|
| 0.03 (baseline) | 699 | 0.002 | 0.001 | convergência estável |
| **0.00001** (muito baixa) | 841 | 0.512 | 0.493 | **quase não aprende** — pesos mudam tão devagar que a perda praticamente não sai do valor inicial (~0.5) |
| **10** (muito alta) | 790 | 0.768 | 0.816 | **diverge/instável** — a perda piora (fica pior que o chute aleatório inicial), os pesos saturam em valores extremos e a fronteira de decisão colapsa numa reta diagonal sem relação com os dados |

Ou seja: taxa de aprendizado baixa demais faz o treinamento ser extremamente lento (paralisia de aprendizado); alta demais faz o gradiente descendente "pular" o mínimo e divergir, tornando o treino instável e a perda pode até aumentar em vez de diminuir.

## d) Risco de mínimos locais (1 camada oculta, 3 neurônios)

Arquitetura reduzida para 1 camada oculta com 3 neurônios (tanh, lr 0.03). Treinei a rede 4 vezes, resetando os pesos (reinicialização aleatória) entre cada tentativa:

| Tentativa | Épocas até parar | Perda teste final | Resultado |
|---|---|---|---|
| 1 | 1019 | 0.011 | convergiu bem |
| 2 | 1121 | 0.009 | convergiu bem |
| 3 | 1209 | 0.009 | convergiu bem |
| 4 | 1152 | **0.268** | **preso em mínimo local** — fronteira virou uma faixa diagonal, não o círculo |

Na tentativa 4, a curva de perda estabiliza num platô alto e a rede nunca escapa dele. Isso ilustra exatamente o risco de mínimos locais: com poucos neurônios/pesos, a superfície de erro tem menos "rotas" de escape, e dependendo da inicialização aleatória dos pesos o gradiente descendente pode ficar preso numa solução ruim. O tempo de treinamento (nº de épocas) também variou bastante entre as tentativas (1019 a 1209 antes de estabilizar).

## e) Poucos neurônios (2 neurônios, 1 camada)

Reduzindo ainda mais, para 2 neurônios em 1 camada oculta: em **duas tentativas independentes** (reset + novo treino), a rede ficou presa exatamente na mesma perda de teste = **0.231**, com a mesma fronteira (uma faixa diagonal), mesmo após mais de 1200 épocas em ambas. Ou seja, aqui não é "azar" de inicialização (como em d) — **a arquitetura simplesmente não tem parâmetros/capacidade suficiente** para representar a fronteira circular; ela satura sempre na melhor aproximação linear possível dos dados. Isso confirma a observação do estudo dirigido: com poucos parâmetros, o modelo se adapta apenas grosseiramente ao conjunto de treinamento e não consegue mais reduzir o erro.

## f) Rede maior (8 neurônios, 1 camada)

Com 8 neurônios numa única camada oculta, repeti o treino duas vezes: convergência em **651 e 659 épocas**, ambas com perda de teste ≈ **0.008–0.009**, mesma velocidade e sem nenhum sinal de estagnação. Isso confirma que redes com mais parâmetros (maior capacidade) tendem a não ficar presas em mínimos locais ruins — há muito mais "caminhos" na superfície de erro que levam a soluções boas, e o excesso de parâmetros facilita o treinamento (mesmo que aumente o risco de overfitting em problemas mais complexos, o que não é o caso aqui pela simplicidade do dataset *circle*).

## g) Dataset espiral, 4 camadas ocultas × 8 neurônios

Configurei o dataset **Spiral**, com 4 camadas ocultas de 8 neurônios cada (tanh):

- **Baseline** (lr = 0.03, sem regularização): a perda caiu devagar no início (0.323 aos 330 épocas) e, na tentativa registrada, terminou resolvendo bem a espiral: perda de teste = **0.003** aos **812 épocas** — mas o próprio traçado da curva de perda mostrou um trecho de estagnação (platô) antes de despencar, ilustrando como redes profundas em datasets difíceis podem demorar bastante e passar por platôs antes de convergir (em outras rodadas, é comum que fique preso no platô por muito mais tempo, dependendo da inicialização).
- **Learning rate alta (0.1) + regularização L2 (0.01):** a perda ficou **travada em 0.480** entre as épocas 319 e 858 (nenhuma melhora), com boa parte dos pesos "apagados" (linhas quase invisíveis no diagrama, i.e., pesos empurrados para perto de zero pela L2) — a combinação de LR alta com regularização forte tirou a capacidade da rede de ajustar a espiral, ficando presa num platô ruim.
- **Learning rate alta (0.1) + regularização L1 (0.01):** resultado ainda mais drástico — em **371 épocas** a perda estagnou em **0.501** (equivalente a chute aleatório) e **praticamente todos os pesos da rede foram zerados** (efeito de esparsificação característico da L1, que "mata" conexões inteiras). A rede parou de aprender completamente.

Conclusão do item g: no dataset espiral (não linearmente separável e bem mais complexo que o círculo), uma rede profunda consegue, em princípio, aprender a fronteira, mas o treinamento é sensível a plateaus. Adicionar uma taxa de aprendizagem alta **junto com** regularização L1/L2 forte é contraproducente aqui: a regularização penaliza pesos grandes/todos os pesos exatamente quando a rede mais precisa de parâmetros expressivos para modelar a espiral, então o resultado observado foi sempre pior que o baseline sem regularização.

---

## Exercícios de fixação

**1) Três funções de ativação populares:**

- **Sigmoide (logística):** σ(z) = 1/(1+e⁻ᶻ), saída entre 0 e 1, formato de "S".
- **Tangente hiperbólica (tanh):** tanh(z) = (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ), saída entre −1 e 1, também em "S", mas centrada em zero.
- **ReLU (Rectified Linear Unit):** ReLU(z) = max(0, z), zero para z<0 e igual a z para z≥0 (formato de "cotovelo"/dobra na origem).

(Todas têm um formato característico simples de esboçar: sigmoide e tanh são curvas em "S" — a tanh é a sigmoide reescalada para o intervalo [-1,1] —, e a ReLU é uma reta a 0 que "quebra" e passa a subir com inclinação 1 a partir da origem.)

**2) MLP com 10 neurônios de entrada, 1 camada oculta com 50 neurônios, saída com 3 neurônios, tudo ReLU.** (Notação de Géron, *Mãos à Obra*, 2ª ed., p. 219–220: m = nº de instâncias no lote.)

a) **X** (matriz de entradas): formato **(m, 10)** — uma linha por instância, uma coluna por feature de entrada.

b) Camada oculta: **Wh** tem formato **(10, 50)** (uma linha por neurônio de entrada, uma coluna por neurônio oculto) e **bh** (vetor de viés) tem formato **(50,)** — um bias por neurônio oculto.

c) Camada de saída: **Wo** tem formato **(50, 3)** (uma linha por neurônio oculto, uma coluna por neurônio de saída) e **bo** tem formato **(3,)**.

d) **Y** (saída da rede): formato **(m, 3)**.

e) Equação (com Z = X, seguindo a notação do livro):

Fh = ReLU(Z·Wh + bh)  →  Y = ReLU(Fh·Wo + bo)

ou, de forma explícita em uma única expressão:

**Y = ReLU( ReLU(Z·Wh + bh) · Wo + bo )**

**3) Neurônios/ativação na camada de saída:**

- **Spam ou não spam** (classificação binária): **1 neurônio** de saída, com ativação **sigmoide** (probabilidade da classe positiva; pode-se usar 2 neurônios com softmax também, mas 1+sigmoide é o padrão).
- **MNIST** (10 classes, dígitos 0–9, multiclasse exclusiva): **10 neurônios** de saída, com ativação **softmax**.
- **Predizer a cotação do dólar amanhã** (regressão de um valor contínuo): **1 neurônio** de saída, sem função de ativação (ativação **linear**/identidade), já que o valor não é limitado a um intervalo fixo como [0,1].

**4) Hiperparâmetros ajustáveis numa MLP básica e como tratar overfitting:**

Hiperparâmetros: número de camadas ocultas; número de neurônios por camada; função(ões) de ativação; taxa de aprendizagem; otimizador (SGD, Adam, RMSProp, etc.); número de épocas; tamanho do lote (batch size); tipo e taxa de regularização (L1/L2, dropout); inicialização dos pesos; e, quando aplicável, a arquitetura de conexões (ex.: skip connections).

Se a MLP **sobreajustar** (erro de treino baixo, mas erro de teste/validação alto), estratégias comuns para tentar resolver:

- Reduzir a complexidade do modelo (menos camadas/neurônios);
- Adicionar **regularização L1 ou L2** nos pesos;
- Adicionar **dropout** entre as camadas;
- Usar **early stopping** (parar o treino quando a perda de validação parar de melhorar);
- Aumentar a quantidade de dados de treinamento, ou usar **data augmentation**;
- Reduzir o número de épocas de treinamento;
- Normalizar/padronizar melhor os dados de entrada;
- Usar validação cruzada para escolher hiperparâmetros de forma mais robusta.
