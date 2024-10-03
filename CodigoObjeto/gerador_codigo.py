# gerador_codigo.py

import pickle

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.symbol_table = {}
        self.current_address = 0
        self.label_count = 0
        self.function_table = {}

    def generate_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
            return
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(f"Nenhum método visit_{node.__class__.__name__} definido")

    def visit_ProgramNode(self, node):
        print("Visitando ProgramNode")
        # Registrar o método 'main' com o rótulo 'MAIN'
        func_label = "MAIN"
        self.function_table[node.main_class.method_name] = func_label

        # Registrar as outras funções
        for method in node.methods:
            func_label = f"FUNC_{method.method_name}"
            self.function_table[method.method_name] = func_label

        # Processar o método principal
        if node.main_class:
            print("Processando o método principal (main)")
            self.code.append("INPP")
            self.visit(node.main_class)
            self.code.append("PARA")
        else:
            print("Aviso: Método principal não encontrado na AST.")

        # Visitar os métodos adicionais
        for method in node.methods:
            self.visit(method)

    def visit_MethodNode(self, node):
        print(f"Visitando MethodNode: {node.method_name}")
        func_label = self.function_table.get(node.method_name)

        # Verificar se é o método 'main'
        is_main = node.method_name == "main"

        if not is_main:
            self.code.append(f"{func_label}:")

        previous_symbol_table = self.symbol_table.copy()
        previous_address = self.current_address
        self.symbol_table = {}
        # Não redefinir 'current_address' para evitar conflito de endereços
        # self.current_address = 0

        # Mapear parâmetros para endereços
        for param in node.params:
            self.symbol_table[param.param_name] = self.current_address
            print(f"Parâmetro '{param.param_name}' mapeado para endereço {self.current_address}")
            self.current_address += 1

        # Desempilhar os argumentos e armazená-los nos parâmetros (apenas se não for 'main')
        if not is_main:
            for param in reversed(node.params):
                param_address = self.symbol_table[param.param_name]
                self.code.append(f"ARMZ {param_address}")

        # Declarar variáveis locais
        for var_decl in node.var_declarations:
            self.visit(var_decl)

        # Processar comandos no método
        for cmd in node.commands:
            self.visit(cmd)

        # Processar expressão de retorno, se houver
        if node.return_expression:
            print("Processando expressão de retorno")
            self.visit(node.return_expression)
            # Aqui, podemos assumir que o valor de retorno está no topo da pilha

        # Instrução de retorno para métodos que não são 'main'
        if not is_main:
            self.code.append("RTPR")

        # Restaurar a tabela de símbolos e o endereço atual
        self.symbol_table = previous_symbol_table
        self.current_address = previous_address


    def visit_VarDeclarationNode(self, node):
        print(f"Declarando variáveis: {node.var_names}")
        for var_name in node.var_names:
            self.symbol_table[var_name] = self.current_address
            print(f"Variável '{var_name}' mapeada para endereço {self.current_address}")
            self.current_address += 1

    def visit_AssignmentNode(self, node):
        print(f"Processando AssignmentNode: {node.var_name} = {node.expression}")
        self.visit(node.expression)
        var_address = self.symbol_table.get(node.var_name)
        if var_address is None:
            print(f"Erro: Variável '{node.var_name}' não declarada.")
        else:
            print(f"Armazenando valor na variável '{node.var_name}' (endereço {var_address})")
            self.code.append(f"ARMZ {var_address}")

    def visit_NumberNode(self, node):
        print(f"Empilhando constante numérica: {node.value}")
        self.code.append(f"CRCT {node.value}")

    def visit_VariableNode(self, node):
        var_address = self.symbol_table.get(node.var_name)
        if var_address is None:
            print(f"Erro: Variável '{node.var_name}' não declarada.")
        else:
            print(f"Carregando valor da variável '{node.var_name}' (endereço {var_address})")
            self.code.append(f"CRVL {var_address}")

    def visit_BinaryOperationNode(self, node):
        print(f"Processando operação binária: {node.operator}")
        self.visit(node.left)
        self.visit(node.right)
        operator_map = {
            '+': 'SOMA',
            '-': 'SUBT',
            '*': 'MULT',
            '/': 'DIVI'
        }
        instr = operator_map.get(node.operator)
        if instr:
            print(f"Gerando instrução: {instr}")
            self.code.append(instr)
        else:
            print(f"Operador desconhecido: {node.operator}")

    def visit_UnaryOperationNode(self, node):
        print(f"Processando operação unária: {node.operator}{node.operand}")
        self.visit(node.operand)
        if node.operator == '-':
            print("Gerando instrução: INVE")
            self.code.append("INVE")
        else:
            print(f"Operador unário desconhecido: {node.operator}")

    def visit_PrintNode(self, node):
        print("Processando PrintNode")
        self.visit(node.expression)
        self.code.append("IMPR")

    def visit_IfNode(self, node):
        print("Processando IfNode")
        self.visit(node.condition)
        label_else = self.generate_label()
        label_end = self.generate_label()
        print(f"Se condição falsa, desviar para {label_else}")
        self.code.append(f"DSVF {label_else}")
        print("Bloco IF:")
        self.visit(node.if_commands)
        print(f"Desviar para {label_end}")
        self.code.append(f"DSVI {label_end}")
        self.code.append(f"{label_else}:")
        if node.else_commands:
            print("Bloco ELSE:")
            self.visit(node.else_commands)
        self.code.append(f"{label_end}:")

    def visit_WhileNode(self, node):
        print("Processando WhileNode")
        label_start = self.generate_label()
        label_end = self.generate_label()
        self.code.append(f"{label_start}:")
        print(f"Avaliando condição do WHILE")
        self.visit(node.condition)
        print(f"Se condição falsa, desviar para {label_end}")
        self.code.append(f"DSVF {label_end}")
        print("Bloco WHILE:")
        self.visit(node.commands)
        print(f"Desviar para {label_start}")
        self.code.append(f"DSVI {label_start}")
        self.code.append(f"{label_end}:")

    def visit_ConditionNode(self, node):
        print(f"Processando ConditionNode: {node.operator}")
        self.visit(node.left)
        self.visit(node.right)
        operator_map = {
            '>': 'CPMA',
            '<': 'CPME',
            '>=': 'CPMAIG',
            '<=': 'CPMEIG',
            '==': 'CPIG',
            '!=': 'CDES'
        }
        instr = operator_map.get(node.operator)
        if instr:
            print(f"Gerando instrução: {instr}")
            self.code.append(instr)
        else:
            print(f"Operador de condição desconhecido: {node.operator}")

    def visit_FunctionCallNode(self, node):
        print(f"Processando chamada de função: {node.function_name}")
        if node.function_name == 'lerDouble':
            print("Chamando função embutida 'lerDouble'")
            self.code.append("LEIT")
        else:
            func_label = self.function_table.get(node.function_name)
            if func_label:
                print(f"Chamando função definida pelo usuário: {node.function_name}")
                # Avaliar argumentos e empilhá-los
                for arg in node.arguments:
                    self.visit(arg)
                # Chamar a função
                self.code.append(f"CHPR {func_label}")
            else:
                print(f"Erro: Função '{node.function_name}' não definida.")

    def visit_ReturnNode(self, node):
        print("Processando ReturnNode")
        self.visit(node.expression)
        # Decidir como tratar o valor de retorno

    def generate_code(self):
        return '\n'.join(self.code)

# Função para carregar a AST e gerar o código objeto
def generate_code(pickle_file, output_file='codigo_objeto.txt'):
    # Corrigir problemas de módulo durante a carga do pickle
    class CustomUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'ArvoreSintaticaAbstrata':
                module = 'AnalisadorSintatico.ArvoreSintaticaAbstrata'
            return super().find_class(module, name)

    with open(pickle_file, 'rb') as f:
        ast = CustomUnpickler(f).load()

    generator = CodeGenerator()
    generator.visit(ast)
    code = generator.generate_code()
    with open(output_file, 'w') as f:
        f.write(code)
    print(f"Código objeto gerado e salvo em {output_file}")
