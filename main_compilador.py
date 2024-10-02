# main_compilador.py
import sys
import os

# Adiciona o diretório raiz ao sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from AnalisadorLexico.Analisador_lexico import main as lexico_main
from AnalisadorSintatico.Analisador_sintatico import main as sintatico_main
from AnalisadorSemantico.main_semantico import main as semantico_main
from CodigoObjeto.main_gerador import main as gerador_main
from CodigoObjeto.executor import main as executor_main

def main():
    try:
        print("=== Etapa 1: Análise Léxica ===")
        lexico_main()
        print("Análise Léxica concluída com sucesso.\n")
    except Exception as e:
        print(f"Erro na Análise Léxica: {e}")
        sys.exit(1)

    try:
        print("=== Etapa 2: Análise Sintática ===")
        sintatico_main()
        print("Análise Sintática concluída com sucesso.\n")
    except Exception as e:
        print(f"Erro na Análise Sintática: {e}")
        sys.exit(1)

    try:
        print("=== Etapa 3: Análise Semântica ===")
        semantico_main()
        print("Análise Semântica concluída com sucesso.\n")
    except Exception as e:
        print(f"Erro na Análise Semântica: {e}")
        sys.exit(1)

    try:
        print("=== Etapa 4: Geração de Código Objeto ===")
        gerador_main()
        print("Geração de Código Objeto concluída com sucesso.\n")
    except Exception as e:
        print(f"Erro na Geração de Código Objeto: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
