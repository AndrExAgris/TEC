# Lógica do Tradutor de Máquinas de Turing

## Funcionamento Geral

O programa lê a primeira linha do arquivo `mt.in` para determinar o tipo de conversão:

---

## Se ler `;S` no começo (Fita Semi-infinita → Fita Duplamente Infinita):

### 1. Renomear Estados Iniciais
- Renomeia todos os estados `0` para `q_ini`
- Isso preserva o estado inicial original da máquina

### 2. Adicionar Rotina Inicial - Parte 1: Marcar Início e Fazer Shift
**Estado 0 - Leitura inicial:**
- Se ler `0`: escreve `#` (marca de parede), vai para direita, vai para estado `move0`
- Se ler `1`: escreve `#` (marca de parede), vai para direita, vai para estado `move1`

**Estados move0 e move1 - Shift da palavra:**
- `move0` ao ler `0`: mantém `0`, vai para direita, continua em `move0`
- `move0` ao ler `1`: escreve `0`, vai para direita, vai para `move1`
- `move0` ao ler `_` (branco): escreve `0`, vai para direita, vai para `voltaComeco`

- `move1` ao ler `0`: escreve `1`, vai para direita, vai para `move0`
- `move1` ao ler `1`: mantém `1`, vai para direita, continua em `move1`
- `move1` ao ler `_` (branco): escreve `1`, vai para direita, vai para `voltaComeco`

**A ideia aqui é:** empurrar cada símbolo da palavra uma casa para a direita, liberando espaço para a marca `#` no início.

### 3. Adicionar Rotina Inicial - Parte 2: Voltar ao Início
**Estado voltaComeco:**
- Ao ler qualquer símbolo (`*`): não escreve nada, vai para esquerda, continua em `voltaComeco`
- Ao ler `#`: não escreve nada, vai para direita, vai para estado `q_ini`

**A ideia aqui é:** depois de fazer o shift, voltar ao começo da palavra original (logo após o `#`) e começar a execução da máquina original no estado `q_ini`.

### 4. Adicionar Proteção de Parede
**Regra universal:**
- Para qualquer estado (`*`): ao ler `#`, mantém `#`, vai para direita, volta para o mesmo estado (`*`)

**A ideia aqui é:** sempre que a máquina tentar ir além da parede esquerda (bater no `#`), ela é automaticamente redirecionada uma casa para a direita, simulando o comportamento de uma fita semi-infinita que não permite movimento além do início.

### 5. Salvar Saída
- Gera o arquivo `mt.out` com todas as transições

---

## Se ler `;I` no começo (Fita Duplamente Infinita → Fita Semi-infinita):

### 1. Renomear Estados Iniciais
- Renomeia todos os estados `0` para `q_ini`
- Coleta todos os símbolos do alfabeto da fita (exceto `_`)

### 2. Adicionar Rotina Inicial - Adicionar Marcadores e Fazer Shift

**Estado 0 - Leitura inicial:**
- Se ler `0`: escreve `#`, vai para direita, vai para estado `move0`
- Se ler `1`: escreve `#`, vai para direita, vai para estado `move1`

**Estados move0 e move1 - Shift da palavra:**
- `move0` ao ler `0`: mantém `0`, vai para direita, continua em `move0`
- `move0` ao ler `1`: escreve `0`, vai para direita, vai para `move1`
- `move0` ao ler `_`: escreve `0`, vai para direita, vai para `colocaMarca`

- `move1` ao ler `0`: escreve `1`, vai para direita, vai para `move0`
- `move1` ao ler `1`: mantém `1`, vai para direita, continua em `move1`
- `move1` ao ler `_`: escreve `1`, vai para direita, vai para `colocaMarca`

**Estado colocaMarca:**
- Ao ler `_`: escreve `&` (marca de fim), vai para esquerda, vai para `voltaComeco`

**Estado voltaComeco:**
- Ao ler qualquer símbolo (`*`): não escreve nada, vai para esquerda, continua em `voltaComeco`
- Ao ler `#`: não escreve nada, vai para direita, vai para estado `q_ini`

**A ideia aqui é:** criar uma "janela" delimitada entre `#` (esquerda) e `&` (direita) onde a palavra fica. Quando precisar expandir, a máquina saberá que precisa criar mais espaço.

### 3. Criar Estados de Expansão à Esquerda (3 Loops Principais)

Esta é a parte mais complexa. Para cada estado original da máquina, são criados conjuntos de estados auxiliares.

#### **Loop 1: Estados Base para Expansão**
Para cada combinação de (estado, símbolo do alfabeto):

**Quando um estado lê `#` (bateu na parede esquerda):**
- `estado` ao ler `#`: mantém `#`, fica parado (`r`), vai para `estadoauxHash`

**Estado auxiliar inicial:**
- `estadoauxHash` ao ler `_`: mantém `_`, vai para direita, vai para `estadoauxHashVazio`
- `estadoauxHashVazio` ao ler `_`: mantém `_`, vai para direita, continua em `estadoauxHashVazio`
- `estadoauxHashVazio` ao ler cada símbolo do alfabeto: apaga (escreve `_`), vai para direita, vai para `estadoauxHashsimbolo`
- `estadoauxHash` ao ler cada símbolo: apaga (escreve `_`), vai para direita, vai para `estadoauxHashsimbolo`

**A ideia aqui é:** quando bater em `#`, começar um processo de busca pelo final da palavra (o primeiro branco após os símbolos).

#### **Loop 2: Shift de Símbolos**
Para cada combinação de (estado, símbolo1, símbolo2):
- `estadoauxHashsimbolo1` ao ler `simbolo2`: escreve `simbolo1`, vai para direita, vai para `estadoauxHashsimbolo2`

**A ideia aqui é:** carregar cada símbolo da palavra e deslocá-lo uma casa para a direita, como em uma cascata. O símbolo que acabamos de ler é escrito na casa seguinte, e continuamos.

#### **Loop 3: Finalização e Retorno**
Para cada combinação de (estado, símbolo):

**Casos especiais de finalização:**
- `estadoauxHashVaziosimbolo` ao ler `_`: escreve `0`, vai para direita, volta para `estado` original
- `estadoauxHashsimbolo` ao ler `_`: escreve `simbolo`, vai para direita, vai para `simboloretestado`

**Estados de retorno ao início:**
- `simboloretestado` ao ler qualquer coisa (`*`): não escreve, vai para esquerda, continua em `simboloretestado`
- `simboloretestado` ao ler `#`: não escreve, vai para direita, volta para `estado` original

**A ideia geral dos 3 loops é:** quando a máquina tenta ir à esquerda do `#`, ela:
1. Encontra o final da palavra (primeiro branco)
2. Desloca toda a palavra uma casa para a direita
3. Volta ao início da palavra (logo após o `#`)
4. Retorna ao estado em que estava antes, como se tivesse "criado" uma nova casa à esquerda

### 4. Criar Estados de Expansão à Direita

Para cada estado da máquina (exceto estados auxiliares da rotina inicial):
- `estado` ao ler `&`: apaga `&` (escreve `_`), vai para direita, vai para `expandeDireitaestado`
- `expandeDireitaestado` ao ler `_`: escreve `&`, vai para esquerda, volta para `estado`

**A ideia aqui é:** quando a máquina bate em `&` (fim da palavra), ela cria um novo espaço à direita, move o `&` uma casa adiante, e volta ao estado original. Isso simula uma fita que cresce à direita conforme necessário.

### 5. Salvar Saída
- Gera o arquivo `mt.out` com todas as transições

---

## Resumo da Lógica

### Sipser → Infinita (;S → ;I):
- **Problema:** Fita com início fixo precisa virar fita infinita
- **Solução:** Adiciona marca `#` no início e bloqueia qualquer movimento além dessa marca, empurrando de volta para direita

### Infinita → Sipser (;I → ;S):
- **Problema:** Fita infinita precisa ser simulada em fita com início fixo
- **Solução:** 
  - Cria "janela" entre `#` e `&`
  - Quando tentar ir à esquerda do `#`: desloca toda palavra para direita, criando espaço
  - Quando tentar ir à direita do `&`: move `&` uma casa adiante
  - Retorna sempre ao estado correto após cada expansão