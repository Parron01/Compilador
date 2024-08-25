from funcoes_analisador_sintatico import Parser

def ler_tokens(filename):
    """Lê os tokens que vieram do arquivo e retorna eles em uma lista."""
    tokens = []
    with open(filename, 'r') as file:
        for line in file:
            token_type, token_value = line.strip()[1:-1].split(', ')
            if token_type.strip() == 'Identificador':
                tokens.append('id')
            if token_type.strip() == 'Numeral':
                tokens.append('num')
            elif token_type.strip() in ['Palavras Reservadas', 'Pontuacao', 'Operador', 'Numeral']:
                tokens.append(token_value.strip())
    return tokens

def main():
    tokens = ler_tokens('tokens.txt')
    parser = Parser(tokens)
    try:
        parser.parse_PROG()
        print("Analise sintatica concluida com sucesso!")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()