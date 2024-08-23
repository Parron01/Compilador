# Projeto de Compilador - Analisador Léxico e Sintático

Este projeto faz parte de uma disciplina de Compiladores 2 e envolve a construção de um compilador.

## Estrutura do Projeto

O projeto está organizado em vários arquivos:

- `codigo.txt`: Contém o código-fonte que será analisado.
- `Analisador-lexico.py`: Script que realiza a análise léxica do código-fonte, gerando um arquivo `tokens.txt`.
- `tokens.txt`: Arquivo gerado pelo analisador léxico contendo a lista de tokens.
- `Analisador-sintatico.py`: Script principal que realiza a análise sintática com base nos tokens gerados.
- `funcoes_analisador_sintatico.py`: Contém as funções de parsing que implementam a análise sintática recursiva preditiva.

## Pré-requisitos

Para rodar este projeto, você precisa ter o Python instalado na sua máquina. A versão mínima recomendada é Python 3.6 ou superior.

### Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```

2. **Verifique a versão do Python:**

   Certifique-se de que você está usando Python 3.6 ou superior:

   ```bash
   python --version
   ```

## Executando o Projeto

### 1. Realizar a Análise Léxica

Primeiro, você precisa executar o analisador léxico. Este analisador vai ler o código-fonte contido no arquivo `codigo.txt` e gerar um arquivo `tokens.txt` com os tokens encontrados.

```bash
python Analisador-lexico.py
```

### 2. Realizar a Análise Sintática

Após gerar o arquivo `tokens.txt`, você pode executar o analisador sintático para verificar a estrutura sintática do código com base nos tokens gerados.

```bash
python Analisador-sintatico.py
```