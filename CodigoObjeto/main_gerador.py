# main_gerador.py

import sys
import os

if __name__ == "__main__":
    # Ajusta o sys.path para incluir o diretório raiz quando executado diretamente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, root_dir)

from CodigoObjeto.gerador_codigo import generate_code
from AnalisadorSintatico.ArvoreSintaticaAbstrata import carregar_ast

def main():
    # Defina o caminho para o arquivo pickle da AST
    ast_file = os.path.join(os.path.dirname(__file__), '..', 'Dados', 'ast_output.pickle')

    # Verifica se o arquivo da AST existe
    if not os.path.exists(ast_file):
        raise Exception(f"Erro: Arquivo AST não encontrado em {ast_file}")
    
    # Gera o código objeto
    print("=== Gerando Código Objeto ===")
    codigo_objeto_path = os.path.join(os.path.dirname(__file__), '..', 'Dados', 'codigo_objeto.txt')
    try:
        generate_code(ast_file, output_file=codigo_objeto_path)
        print(f"Código objeto gerado com sucesso em '{codigo_objeto_path}'.")
    except Exception as e:
        raise Exception(f"Erro durante a geração do código objeto: {e}")

if __name__ == "__main__":
    main()
