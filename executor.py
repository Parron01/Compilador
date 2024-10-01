# executor.py

import sys

class MaqHipoExecutor:
    def __init__(self, codigo_objeto_file):
        self.codigo_objeto = []
        self.labels = {}
        self.memory = {}  # Mapeamento de endereços para valores
        self.stack = []
        self.call_stack = []
        self.program_counter = 0
        self.debug = False  # Variável de controle do modo debug
        self.load_code(codigo_objeto_file)
        self.build_label_table()

    def load_code(self, filename):
        """Carrega o código objeto do arquivo."""
        try:
            with open(filename, 'r') as file:
                self.codigo_objeto = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado.")
            sys.exit(1)

    def build_label_table(self):
        """Construir uma tabela de rótulos mapeando-os para seus índices no código objeto."""
        new_codigo_objeto = []
        for line in self.codigo_objeto:
            if line.endswith(':'):
                label = line[:-1]
                self.labels[label] = len(new_codigo_objeto)
            else:
                new_codigo_objeto.append(line)
        self.codigo_objeto = new_codigo_objeto
        if self.debug:
            print(f"Rótulos mapeados: {self.labels}")  # Debug: Verificar mapeamento de rótulos

    def execute(self):
        """Executa o código objeto."""
        self.program_counter = 0
        while self.program_counter < len(self.codigo_objeto):
            instruction = self.codigo_objeto[self.program_counter]
            if self.debug:
                print(f"Executando instrução [{self.program_counter}]: {instruction}")  # Debug
            self.execute_instruction(instruction)
            self.program_counter += 1

    def execute_instruction(self, instruction):
        """Interpreta e executa uma única instrução."""
        parts = instruction.split()
        opcode = parts[0]

        if opcode == 'INPP':
            if self.debug:
                print("Programa iniciado.")

        elif opcode == 'CHPR':
            func_label = parts[1]
            if func_label not in self.labels:
                print(f"Erro: Função '{func_label}' não encontrada.")
                sys.exit(1)
            self.call_stack.append(self.program_counter)
            self.program_counter = self.labels[func_label] - 1  # -1 para compensar o incremento no loop
            if self.debug:
                print(f"Chamando função '{func_label}'.")

        elif opcode == 'PARA':
            if self.debug:
                print("Programa finalizado.")
            sys.exit(0)

        elif opcode == 'CRCT':
            value = float(parts[1])
            self.stack.append(value)
            if self.debug:
                print(f"Empilhando constante numérica: {value}")

        elif opcode == 'ARMZ':
            address = int(parts[1])
            if not self.stack:
                print("Erro: Pilha vazia durante ARMZ.")
                sys.exit(1)
            value = self.stack.pop()
            self.memory[address] = value
            if self.debug:
                print(f"Armazenando valor {value} na variável (endereço {address})")

        elif opcode == 'CRVL':
            address = int(parts[1])
            value = self.memory.get(address, 0.0)
            self.stack.append(value)
            if self.debug:
                print(f"Carregando valor da variável (endereço {address}): {value}")

        elif opcode == 'SUBT':
            if len(self.stack) < 2:
                print("Erro: Pilha com menos de dois valores durante SUBT.")
                sys.exit(1)
            a = self.stack.pop()
            b = self.stack.pop()
            result = b - a
            self.stack.append(result)
            if self.debug:
                print(f"Subtraindo: {b} - {a} = {result}")

        elif opcode == 'CPMA':
            if len(self.stack) < 2:
                print("Erro: Pilha com menos de dois valores durante CPMA.")
                sys.exit(1)
            a = self.stack.pop()
            b = self.stack.pop()
            condition = b > a
            self.stack.append(1 if condition else 0)
            if self.debug:
                print(f"Comparação CPMA: {b} > {a} = {condition}")

        elif opcode == 'DSVF':
            label = parts[1]
            if not self.stack:
                print("Erro: Pilha vazia durante DSVF.")
                sys.exit(1)
            condition = self.stack.pop()
            if self.debug:
                print(f"Desviando para '{label}' se condição for falsa ({condition} == 0)")
            if condition == 0:
                if label not in self.labels:
                    print(f"Erro: Rótulo '{label}' não encontrado durante DSVF.")
                    sys.exit(1)
                self.program_counter = self.labels[label] - 1  # -1 para compensar o incremento no loop

        elif opcode == 'DSVI':
            label = parts[1]
            if self.debug:
                print(f"Desviando incondicionalmente para '{label}'")
            if label not in self.labels:
                print(f"Erro: Rótulo '{label}' não encontrado durante DSVI.")
                sys.exit(1)
            self.program_counter = self.labels[label] - 1  # -1 para compensar o incremento no loop

        elif opcode == 'IMPR':
            if not self.stack:
                print("Erro: Pilha vazia durante IMPR.")
                sys.exit(1)
            value = self.stack.pop()
            print(value)  # Imprime o valor para o usuário

        elif opcode == 'LEIT':
            try:
                value = float(input("Digite um número: "))  # Prompt descritivo
                self.stack.append(value)
                if self.debug:
                    print(f"Leitura: {value} empilhado")
            except ValueError:
                print("Erro: Entrada inválida. Esperado um número.")
                sys.exit(1)

        elif opcode == 'RTPR':
            if not self.call_stack:
                print("Erro: Call stack vazio durante RTPR.")
                sys.exit(1)
            return_address = self.call_stack.pop()
            self.program_counter = return_address
            if self.debug:
                print(f"Retornando para instrução [{return_address}]")

        else:
            print(f"Erro: Instrução desconhecida '{opcode}'.")
            sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Uso: python executor.py <codigo_objeto.txt>")
        sys.exit(1)

    codigo_objeto_file = sys.argv[1]
    executor = MaqHipoExecutor(codigo_objeto_file)
    # Ative o modo debug definindo 'self.debug' como True
    # executor.debug = True  # Descomente esta linha para ativar o modo debug
    executor.execute()

if __name__ == "__main__":
    main()
