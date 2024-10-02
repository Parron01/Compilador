# main_semantico.py

import os
import sys

if __name__ == "__main__":
    # Ajusta o sys.path para incluir o diretório raiz quando executado diretamente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, root_dir)

from AnalisadorSemantico.Analisador_semantico import AnalisadorSemantico
from AnalisadorSintatico.ArvoreSintaticaAbstrata import carregar_ast

def main():
    # Carrega a AST gerada anteriormente
    ast_path = os.path.join(os.path.dirname(__file__), '..', 'Dados', 'ast_output.pickle')
    ast = carregar_ast(ast_path)
    if not ast:
        raise Exception("Erro: Falha ao carregar a AST.")
    
    # Instancia o analisador semântico
    analisador = AnalisadorSemantico()
    
    # Realiza a análise semântica
    print("=== Executando Análise Semântica ===")
    analisador.visitar(ast)
    
    # Verifica se houve erros semânticos
    if hasattr(analisador, 'erros_semanticos') and analisador.erros_semanticos:
        print("\n=== Erros Semânticos Encontrados ===")
        for erro in analisador.erros_semanticos:
            print(f"- {erro}")
        raise Exception("Análise semântica falhou devido a erros.")
    else:
        print("\nNenhum erro semântico encontrado.")

if __name__ == "__main__":
    main()
