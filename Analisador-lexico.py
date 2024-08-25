import re

with open('codigo.txt', 'r') as arquivo:
    codigo_fonte = arquivo.read()

patterns = [
    (r'[ \n\t\r\f]+', None),  # Espaços em branco e quebras de linha
    (r'\b\d+[a-zA-Z_]+\b', 'ERRO LEXICO'),  # Erros léxicos
    (r'(public|class|static|void|main|String|double|if|else|while|return|System\.out\.println|lerDouble\(\))', 'Palavras Reservadas'),  # Palavras reservadas
    (r'\b\d+(\.\d+)?\b', 'Numeral'),  # Números inteiros e reais
    (r'\b[a-zA-Z_][0-9a-zA-Z_]*\b', 'Identificador'),  # Identificadores
    (r'(==|!=|>=|<=|=|>|<|\+|\-|\*|\/|\!|\.)', 'Operador'),  # Operadores
    (r'[()\[\]{};.,]', 'Pontuacao')  # Pontuação
]

def GerarTokens(codigo):
    tokens = []
    posicao = 0
    max_iteracoes = 1000 

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

    return tokens

tokens = GerarTokens(codigo_fonte)

print("\n    TOKENS")
for tipo, valor in tokens:
    print(f"[{tipo}, {valor}]")

with open('tokens.txt', 'w') as arquivo:
    for tipo, valor in tokens:
        arquivo.write(f"[{tipo}, {valor}]\n")
