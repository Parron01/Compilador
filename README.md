# Projeto de Compilador - Analisador Léxico, Sintático e Semântico

Este projeto faz parte da disciplina de Compiladores 2 e envolve a construção de um compilador completo.

## Estrutura do Projeto

O projeto está organizado nos seguintes diretórios:

- `AnalisadorLexico/`: Contém o script `analisador_lexico.py` responsável pela análise léxica.
- `AnalisadorSintatico/`: Contém o script `Analisador_sintatico.py` e módulos relacionados à análise sintática.
- `AnalisadorSemantico/`: Contém o script `main_semantico.py` responsável pela análise semântica.
- `CodigoObjeto/`: Contém o script `main_gerador.py` para geração do código objeto e `executor.py` para executar o código gerado.
- `Dados/`: Pasta que armazena os arquivos intermediários e o código-fonte:
  - `codigo.txt`: Contém o código-fonte que será analisado.
  - `tokens.txt`: Arquivo gerado pelo analisador léxico contendo a lista de tokens.
  - `ast_output.pickle`: Arquivo gerado pelo analisador sintático contendo a Árvore Sintática Abstrata (AST).
  - `codigo_objeto.txt`: Arquivo gerado pelo gerador de código contendo o código objeto.

## Pré-requisitos

Para executar este projeto, você precisa ter o Python instalado em sua máquina. A versão mínima recomendada é Python 3.6 ou superior.

### Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Parron01/Compilador.git
   cd seu_repositorio
   ```

2. **Verifique a versão do Python:**

   Certifique-se de que você está usando Python 3.6 ou superior:

   ```bash
   python --version
   ```

## Executando o Projeto

### Opção 1: Executar todo o processo de compilação

Para executar todas as etapas do compilador de uma só vez, utilize o script `main_compilador.py` na raiz do projeto:

```bash
python main_compilador.py
```

Este script executa as etapas de análise léxica, sintática, semântica, geração de código objeto e execução do código gerado.

### Opção 2: Executar cada etapa individualmente

#### 1. Análise Léxica

Execute o analisador léxico para ler o código-fonte em `Dados/codigo.txt` e gerar o arquivo `tokens.txt` com os tokens encontrados:

```bash
python AnalisadorLexico/analisador_lexico.py
```

#### 2. Análise Sintática

Execute o analisador sintático para verificar a estrutura sintática do código com base nos tokens gerados e criar a AST:

```bash
python AnalisadorSintatico/Analisador_sintatico.py
```

#### 3. Análise Semântica

Execute o analisador semântico para verificar a coerência semântica do código:

```bash
python AnalisadorSemantico/main_semantico.py
```

#### 4. Geração de Código Objeto

Gere o código objeto a partir da AST gerada nas etapas anteriores:

```bash
python CodigoObjeto/main_gerador.py
```

#### 5. Execução do Código Objeto

**Nota:** Para executar o código objeto, é necessário estar no diretório raiz do projeto.

Execute o código objeto gerado utilizando o script `executor.py`:

```bash
python CodigoObjeto/executor.py
```

## Observações

- Certifique-se de que o arquivo `Dados/codigo.txt` contém o código-fonte que você deseja compilar.
- Os arquivos intermediários (`tokens.txt`, `ast_output.pickle`, `codigo_objeto.txt`) são armazenados na pasta `Dados/`.
- Em caso de erros durante alguma das etapas, o processo será interrompido e uma mensagem de erro será exibida.

---