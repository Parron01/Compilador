# main.py

from Analisador_semantico import AnalisadorSemantico
from ArvoreSintaticaAbstrata import carregar_ast 
from Gerador_codigoObj import generate_code
import sys  # Para sair do programa em caso de erros

def main():
    # Carrega a AST gerada anteriormente
    ast = carregar_ast('ast_output.pickle')
    if not ast:
        print("Erro: Falha ao carregar a AST.")
        sys.exit(1)
    
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
        print("\nGeração de código objeto abortada devido a erros semânticos.")
        sys.exit(1)  # Encerra o programa com código de erro
    else:
        print("\nNenhum erro semântico encontrado. Prosseguindo com a geração de código objeto.\n")
    
    # Gera o código objeto
    generate_code('ast_output.pickle', 'codigo_objeto.txt')
    print("=== Geração de Código Objeto Concluída ===")

if __name__ == "__main__":
    main()
