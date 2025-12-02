# Projeto TEC

Este repositório contém o trabalho prático da disciplina de Teoria da Computação (TEC).

## Como Utilizar

### Entrada de Dados

O código da Máquina de Turing a ser convertida deve ser colado no arquivo `mt.in` como um bloco de texto.

**Regras para o arquivo `mt.in`:**
* Não utilize linhas em branco.
* Não inclua comentários, exceto na primeira linha.
* A primeira linha deve conter **apenas** a indicação do tipo de máquina de entrada:
    * `;S` para Máquina de Turing Semi-Infinita.
    * `;I` para Máquina de Turing Duplamente Infinita (Veja a seção **Aviso**).

### Execução

1.  Abra um terminal no diretório raiz do repositório.
2.  Execute o seguinte comando:
    ```bash
    python3 main.py
    ```
3.  A máquina convertida será gerada no arquivo `mt.out`.
