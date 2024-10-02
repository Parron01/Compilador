import pickle
import os

class Node:
    """Classe base para todos os nós da AST."""
    def __init__(self):
        pass

    def accept(self, visitor):
        """Método para aceitar um visitante, que será utilizado na análise semântica e geração de código."""
        return visitor.visit(self)

    def to_dict(self):
        """Converte o nó para um formato dicionário, útil para serialização em JSON."""
        return {'type': self.__class__.__name__}


class ProgramNode(Node):
    """Representa o nó da raiz do programa (PROG)."""
    def __init__(self, main_class, methods):
        self.main_class = main_class  # Estrutura da main
        self.methods = methods  # Lista de métodos adicionais

    def to_dict(self):
        return {
            'type': 'ProgramNode',
            'main_class': self.main_class.to_dict(),
            'methods': [method.to_dict() for method in (self.methods or [])]  # Verificando se há métodos
        }


class MethodNode(Node):
    """Representa um método dentro da classe."""
    def __init__(self, return_type, method_name, params, var_declarations, commands, return_expression):
        self.return_type = return_type  # Tipo de retorno
        self.method_name = method_name  # Nome do método
        self.params = params if params else []  # Lista de parâmetros
        self.var_declarations = var_declarations if var_declarations else []  # Declarações de variáveis
        self.commands = commands if commands else []  # Comandos (corpo do método)
        self.return_expression = return_expression  # Expressão de retorno

    def to_dict(self):
        return {
            'type': 'MethodNode',
            'return_type': self.return_type.to_dict(),
            'method_name': self.method_name,
            'params': [param.to_dict() for param in self.params],  # Certificando que seja uma lista de nós
            'var_declarations': [var_decl.to_dict() for var_decl in self.var_declarations],
            'commands': [cmd.to_dict() for cmd in self.commands],
            'return_expression': self.return_expression.to_dict() if self.return_expression else None
        }


class VarDeclarationNode(Node):
    """Representa a declaração de uma variável."""
    def __init__(self, var_type, var_names):
        self.var_type = var_type  # Tipo da variável
        self.var_names = var_names  # Lista de nomes de variáveis

    def to_dict(self):
        return {
            'type': 'VarDeclarationNode',
            'var_type': self.var_type.to_dict() if isinstance(self.var_type, Node) else self.var_type,
            'var_names': self.var_names  # Lista de nomes (não são nós da AST, logo, não precisam de to_dict)
        }


class CommandNode(Node):
    """Representa um comando genérico (CMD)."""
    def to_dict(self):
        return super().to_dict()


class IfNode(CommandNode):
    """Representa uma estrutura condicional 'if'."""
    def __init__(self, condition, if_commands, else_commands):
        self.condition = condition  # Condição do 'if'
        self.if_commands = if_commands  # Comandos executados se a condição for verdadeira
        self.else_commands = else_commands  # Comandos executados no 'else'

    def to_dict(self):
        return {
            'type': 'IfNode',
            'condition': self.condition.to_dict(),
            'if_commands': [cmd.to_dict() for cmd in self.if_commands],
            'else_commands': [cmd.to_dict() for cmd in self.else_commands] if self.else_commands else None
        }


class WhileNode(CommandNode):
    """Representa uma estrutura de repetição 'while'."""
    def __init__(self, condition, commands):
        self.condition = condition  # Condição do 'while'
        self.commands = commands  # Comandos executados enquanto a condição for verdadeira

    def to_dict(self):
        return {
            'type': 'WhileNode',
            'condition': self.condition.to_dict(),
            'commands': [cmd.to_dict() for cmd in self.commands]
        }


class PrintNode(CommandNode):
    """Representa um comando de impressão 'System.out.println'."""
    def __init__(self, expression):
        self.expression = expression  # Expressão a ser impressa

    def to_dict(self):
        return {
            'type': 'PrintNode',
            'expression': self.expression.to_dict()
        }


class AssignmentNode(CommandNode):
    """Representa uma atribuição de valor a uma variável."""
    def __init__(self, var_name, expression):
        self.var_name = var_name  # Nome da variável
        self.expression = expression  # Expressão atribuída à variável

    def to_dict(self):
        return {
            'type': 'AssignmentNode',
            'var_name': self.var_name,
            'expression': self.expression.to_dict()
        }


class ExpressionNode(Node):
    """Representa uma expressão genérica (EXPRESSAO)."""
    def to_dict(self):
        return super().to_dict()


class BinaryOperationNode(ExpressionNode):
    """Representa uma operação binária, como soma, subtração, multiplicação ou divisão."""
    def __init__(self, left, operator, right):
        self.left = left  # Operando à esquerda
        self.operator = operator  # Operador (ex: +, -, *, /)
        self.right = right  # Operando à direita

    def to_dict(self):
        return {
            'type': 'BinaryOperationNode',
            'left': self.left.to_dict(),
            'operator': self.operator,
            'right': self.right.to_dict()
        }
    def __str__(self):
        return f'({self.left} {self.operator} {self.right})'


class UnaryOperationNode(ExpressionNode):
    """Representa uma operação unária (ex: -x)."""
    def __init__(self, operator, operand):
        self.operator = operator  # Operador (ex: -)
        self.operand = operand  # Operando (ex: x)

    def to_dict(self):
        return {
            'type': 'UnaryOperationNode',
            'operator': self.operator,
            'operand': self.operand.to_dict()
        }


class VariableNode(ExpressionNode):
    """Representa o uso de uma variável em uma expressão."""
    def __init__(self, var_name):
        self.var_name = var_name  # Agora armazena o nome real da variável

    def to_dict(self):
        return {
            'type': 'VariableNode',
            'var_name': self.var_name  # Nome real do identificador
        }
    def __str__(self):
        return self.var_name


class NumberNode(ExpressionNode):
    """Representa um número (constante numérica)."""
    def __init__(self, value):
        self.value = value  # Valor numérico

    def to_dict(self):
        return {
            'type': 'NumberNode',
            'value': self.value
        }
    def __str__(self):
        return str(self.value)

class ReturnNode(CommandNode):
    """Representa o comando de retorno de uma expressão."""
    def __init__(self, expression):
        self.expression = expression  # Expressão de retorno

    def to_dict(self):
        return {
            'type': 'ReturnNode',
            'expression': self.expression.to_dict()
        }

class ConditionNode(ExpressionNode):
    """Representa uma condição (CONDICAO), usada no 'if' e 'while'."""
    def __init__(self, left, operator, right):
        self.left = left  # Expressão à esquerda
        self.operator = operator  # Operador condicional (ex: >, <, ==)
        self.right = right  # Expressão à direita

    def to_dict(self):
        return {
            'type': 'ConditionNode',
            'left': self.left.to_dict(),
            'operator': self.operator,
            'right': self.right.to_dict()
        }
    def __str__(self):
        return f'({self.left} {self.operator} {self.right})'

# Novas classes

class TypeNode(Node):
    """Representa um tipo de dado (ex: 'double')."""
    def __init__(self, type_name):
        self.type_name = type_name

    def to_dict(self):
        return {
            'type': 'TypeNode',
            'type_name': self.type_name
        }

class ParamNode(Node):
    """Representa um parâmetro de método (TIPO id)."""
    def __init__(self, param_type, param_name):
        self.param_type = param_type  # Tipo do parâmetro
        self.param_name = param_name  # Nome do parâmetro

    def to_dict(self):
        return {
            'type': 'ParamNode',
            'param_type': self.param_type.to_dict(),
            'param_name': self.param_name
        }
    
class FunctionCallNode(ExpressionNode):
    """Representa uma chamada de função."""
    def __init__(self, function_name, arguments):
        self.function_name = function_name  # Nome da função
        self.arguments = arguments  # Lista de argumentos

    def to_dict(self):
        return {
            'type': 'FunctionCallNode',
            'function_name': self.function_name,
            'arguments': [arg.to_dict() for arg in self.arguments if arg is not None]
        }
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"{self.function_name}({args_str})"

def carregar_ast(filename='ast_output.pickle'):
    """Carrega a AST de um arquivo binário utilizando pickle."""
    filepath = os.path.join(os.path.dirname(__file__), '..', 'Dados', filename)

    class CustomUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'ArvoreSintaticaAbstrata':
                module = 'AnalisadorSintatico.ArvoreSintaticaAbstrata'
            return super().find_class(module, name)

    with open(filepath, 'rb') as file:
        ast = CustomUnpickler(file).load()
        return ast
