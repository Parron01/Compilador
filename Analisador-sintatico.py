from funcoes_analisador_sintatico import Parser
import pickle

def ler_tokens(filename):
    """Lê os tokens que vieram do arquivo e retorna eles em uma lista de tuplas (tipo, valor)."""
    tokens = []
    with open(filename, 'r') as file:
        for line in file:
            token_type, token_value = line.strip()[1:-1].split(', ')
            token_type = token_type.strip()
            token_value = token_value.strip()

            if token_type == 'Identificador':
                # Para identificadores, mantemos 'id' como tipo, mas usamos o valor real
                tokens.append(('id', token_value))
            elif token_type == 'Numeral':
                # Para numerais, mantemos 'num' como tipo, mas usamos o valor real
                tokens.append(('num', token_value))
            else:
                # Para outros casos (Pontuacao, Operador, Palavras Reservadas), usamos o valor diretamente
                tokens.append((token_value, token_value))
    
    return tokens

def main():
    tokens = ler_tokens('tokens.txt')
    parser = Parser(tokens)
    try:
        parser.parse_PROG()  # Realiza a análise sintática e cria a AST
        print("Análise sintática concluída com sucesso!")
        
        # Salvando a AST em formato binário usando pickle
        parser.save_ast_to_pickle('ast_output.pickle')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()