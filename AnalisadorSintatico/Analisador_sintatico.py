import sys
import os

if __name__ == "__main__":
    # Adjust sys.path to include the parent directory when running directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, parent_dir)

from AnalisadorSintatico.funcoes_analisador_sintatico import Parser

def ler_tokens(filename):
    """Lê os tokens que vieram do arquivo e retorna eles em uma lista de tuplas (tipo, valor)."""
    tokens = []
    with open(filename, 'r') as file:
        for line in file:
            token_type, token_value = line.strip()[1:-1].split(', ')
            token_type = token_type.strip()
            token_value = token_value.strip()

            if token_type == 'Identificador':
                tokens.append(('id', token_value))
            elif token_type == 'Numeral':
                tokens.append(('num', token_value))
            else:
                tokens.append((token_value, token_value))
    
    return tokens

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dados_dir = os.path.abspath(os.path.join(script_dir, "..", "Dados"))
    tokens_path = os.path.join(dados_dir, 'tokens.txt')

    tokens = ler_tokens(tokens_path)
    parser = Parser(tokens)

    parser.parse_PROG()  # Realiza a análise sintática e cria a AST
    print("Análise sintática concluída com sucesso!")
        
    # Construir o caminho completo para 'ast_output.pickle' na pasta "Dados"
    ast_path = os.path.join(dados_dir, 'ast_output.pickle')
        
    # Salvando a AST em formato binário usando pickle na pasta "Dados"
    parser.save_ast_to_pickle(ast_path)

if __name__ == "__main__":
    main()