import re

def ler_codigo_fonte(nome_arquivo):
    """Lê o código-fonte de um arquivo e retorna como uma string."""
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.read()

# Definição dos padrões de tokens
patterns = [
    # Espaços em branco e quebras de linha (ignorados)
    (r'[ \n\t\r\f]+', None),
    # Erros léxicos (números seguidos de letras)
    (r'\b\d+[a-zA-Z_]+\b', 'ERRO LEXICO'),
    # Palavras reservadas e funções especiais
    (r'(public|class|static|void|main|String|double|if|else|while|return|System\.out\.println|lerDouble\(\))', 'Palavras Reservadas'),
    # Números inteiros e reais
    (r'\b\d+(\.\d+)?\b', 'Numeral'),
    # Identificadores
    (r'\b[a-zA-Z_][0-9a-zA-Z_]*\b', 'Identificador'),
    # Operadores
    (r'(==|!=|>=|<=|=|>|<|\+|\-|\*|\/|\!|\.)', 'Operador'),
    # Pontuação
    (r'[()\[\]{};.,]', 'Pontuacao')
]

def gerar_tokens(codigo):
    """Gera uma lista de tokens a partir do código-fonte fornecido."""
    tokens = []
    posicao = 0

    while posicao < len(codigo):
        match = None

        for pattern, token_type in patterns:
            regex = re.compile(pattern)
            match = regex.match(codigo, posicao)

            if match:
                valor = match.group(0)
                if token_type is not None:
                    tokens.append((token_type, valor))
                posicao = match.end()
                break

        if not match:
            # Se nenhum padrão corresponder, trata-se de um erro léxico
            erro_posicao = posicao
            while posicao < len(codigo) and not re.match(r'[ \n\t\r\f]+', codigo[posicao]):
                posicao += 1
            sequencia_errada = codigo[erro_posicao:posicao].strip()

            # Verifica se a sequência parece ser uma chamada de método inválida
            if re.match(r'[a-zA-Z_]+\s*\(\s*[^\)]\s', sequencia_errada):
                tokens.append(('ERRO LEXICO - Chamada de Método Inválida', sequencia_errada))
            else:
                tokens.append(('ERRO LEXICO', sequencia_errada))

            # Avança a posição para evitar loop infinito
            if posicao == erro_posicao:
                posicao += 1

    return tokens

def escrever_tokens(tokens, nome_arquivo='tokens.txt'):
    """Escreve a lista de tokens em um arquivo especificado."""
    with open(nome_arquivo, 'w') as arquivo:
        for tipo, valor in tokens:
            arquivo.write(f"[{tipo}, {valor}]\n")

def main():
    """Função principal que coordena a execução do analisador léxico."""
    # Lê o código-fonte do arquivo
    codigo_fonte = ler_codigo_fonte('codigo.txt')

    # Gera a lista de tokens
    tokens = gerar_tokens(codigo_fonte)

    # Imprime os tokens no console
    print("\nTOKENS")
    for tipo, valor in tokens:
        print(f"[{tipo}, {valor}]")

    # Escreve os tokens no arquivo 'tokens.txt'
    escrever_tokens(tokens)

if __name__ == "__main__":
    main()
