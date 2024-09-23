# main.py

from Analisador_semantico import AnalisadorSemantico
from ArvoreSintaticaAbstrata import carregar_ast  # Supondo que tenha o código de carregamento da AST em outro arquivo

def main():
    # Carrega a AST gerada anteriormente
    ast = carregar_ast('ast_output.pickle')
    
    # Instancia o analisador semântico
    analisador = AnalisadorSemantico()
    
    # Realiza a análise semântica
    print("=== Executando Análise Semântica ===")
    analisador.visitar(ast)
    
    # Verifica se houve erros semânticos
    if analisador.erros_semanticos:
        print("\n=== Erros Semânticos Encontrados ===")
        for erro in analisador.erros_semanticos:
            print(erro)
    else:
        print("\nNenhum erro encontrado.")

if __name__ == "__main__":
    main()
