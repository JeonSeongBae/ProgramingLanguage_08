# -*- coding: utf-8 -*-
from string import letters, digits, whitespace


class CuteType:
    INT = 1
    ID = 4

    MINUS = 2
    PLUS = 3

    L_PAREN = 5
    R_PAREN = 6

    TRUE = 8
    FALSE = 9

    TIMES = 10
    DIV = 11

    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15

    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30

    KEYWORD_LIST = ('define', 'lambda', 'cond', 'quote', 'not', 'car', 'cdr', 'cons',
                    'atom?', 'null?', 'eq?')

    BINARYOP_LIST = (DIV, TIMES, MINUS, PLUS, LT, GT, EQ)
    BOOLEAN_LIST = (TRUE, FALSE)


def check_keyword(token):
    """
    :type token:str
    :param token:
    :return:
    """
    if token.lower() in CuteType.KEYWORD_LIST:
        return True
    return False


def _get_keyword_type(token):
    return {
        'define': CuteType.DEFINE,
        'lambda': CuteType.LAMBDA,
        'cond': CuteType.COND,
        'quote': CuteType.QUOTE,
        'not': CuteType.NOT,
        'car': CuteType.CAR,
        'cdr': CuteType.CDR,
        'cons': CuteType.CONS,
        'atom?': CuteType.ATOM_Q,
        'null?': CuteType.NULL_Q,
        'eq?': CuteType.EQ_Q
    }[token]


CUTETYPE_NAMES = dict((eval(attr, globals(), CuteType.__dict__), attr) for attr in dir(
    CuteType()) if not callable(attr) and not attr.startswith('__'))


class Token(object):
    def __init__(self, type, lexeme):
        """
        :type type:CuteType
        :type lexeme: str
        :param type:
        :param lexeme:
        :return:
        """
        if check_keyword(lexeme):
            self.type = _get_keyword_type(lexeme)
            self.lexeme = lexeme
        else:
            self.type = type
            self.lexeme = lexeme
        # print type

    def __str__(self):
        # return self.lexeme
        return '[' + CUTETYPE_NAMES[self.type] + ': ' + self.lexeme + ']'

    def __repr__(self):
        return str(self)


class Scanner:

    def __init__(self, source_string=None):
        """
        :type self.__source_string: str
        :param source_string:
        """
        self.__source_string = source_string
        self.__pos = 0
        self.__length = len(source_string)
        self.__token_list = []

    def __make_token(self, transition_matrix, build_token_func=None):
        old_state = 0
        self.__skip_whitespace()
        temp_char = ''
        return_token = ''
        while not self.eos():
            temp_char = self.get()
            if old_state == 0 and temp_char in (')', '('):
                return_token = temp_char
                old_state = transition_matrix[(old_state, temp_char)]
                break

            return_token += temp_char
            old_state = transition_matrix[(old_state, temp_char)]
            next_char = self.peek()
            if next_char in whitespace or next_char in ('(', ')'):
                break

        return build_token_func(old_state, return_token)

    def scan(self, transition_matrix, build_token_func):
        while not self.eos():
            self.__token_list.append(self.__make_token(
                transition_matrix, build_token_func))
        return self.__token_list

    def pos(self):
        return self.__pos

    def eos(self):
        return self.__pos >= self.__length

    def skip(self, pattern):
        while not self.eos():
            temp_char = self.peek()
            if temp_char in pattern:
                temp_char = self.get()
            else:
                break

    def __skip_whitespace(self):
        self.skip(whitespace)

    def peek(self, length=1):
        return self.__source_string[self.__pos: self.__pos + length]

    def get(self, length=1):
        return_get_string = self.peek(length)
        self.__pos += len(return_get_string)
        return return_get_string


class CuteScanner(object):

    transM = {}

    def __init__(self, source):
        """
        :type source:str
        :param source:
        :return:
        """
        self.source = source
        self._init_TM()

    def _init_TM(self):
        for alpha in letters:
            self.transM[(0, alpha)] = 4
            self.transM[(4, alpha)] = 4

        for digit in digits:
            self.transM[(0, digit)] = 1
            self.transM[(1, digit)] = 1
            self.transM[(2, digit)] = 1
            self.transM[(4, digit)] = 4

        self.transM[(4, '?')] = 16
        self.transM[(0, '-')] = 2
        self.transM[(0, '+')] = 3
        self.transM[(0, '(')] = 5
        self.transM[(0, ')')] = 6

        self.transM[(0, '#')] = 7
        self.transM[(7, 'T')] = 8
        self.transM[(7, 'F')] = 9

        self.transM[(0, '/')] = 11
        self.transM[(0, '*')] = 10

        self.transM[(0, '<')] = 12
        self.transM[(0, '>')] = 13
        self.transM[(0, '=')] = 14
        self.transM[(0, "'")] = 15

    def tokenize(self):

        def build_token(type, lexeme): return Token(type, lexeme)
        cute_scanner = Scanner(self.source)
        return cute_scanner.scan(self.transM, build_token)


class TokenType():
    INT = 1
    ID = 4
    MINUS = 2
    PLUS = 3
    LIST = 5
    TRUE = 8
    FALSE = 9
    TIMES = 10
    DIV = 11
    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15
    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30


NODETYPE_NAMES = dict((eval(attr, globals(), TokenType.__dict__), attr) for attr in dir(
    TokenType()) if not callable(attr) and not attr.startswith('__'))

class Node (object):

    def __init__(self, type, value=None):
        self.next = None
        self.value = value
        self.type = type

    def set_last_next(self, next_node):
        if self.next is not None:
            self.next.set_last_next(next_node)

        else:
            self.next = next_node

    def __str__(self):
        result = ''

        if self.type is TokenType.ID:
            result = '[' + NODETYPE_NAMES[self.type] + ':' + self.value + ']'
        elif self.type is TokenType.INT:
            result = '['+NODETYPE_NAMES[self.type]+':' + self.value + ']'
        elif self.type is TokenType.LIST:
            if self.value is not None:
                if self.value.type is TokenType.QUOTE:
                    result = str(self.value)
                else:
                    result = '(' + str(self.value) + ')'
            else:
                result = '(' + str(self.value) + ')'
        elif self.type is TokenType.QUOTE:
            result = "\'"
        else:
            result = '['+NODETYPE_NAMES[self.type]+']'

        # fill out
        if self.next is not None:
            return result + ' ' + str(self.next)
        else:
            return result


class BasicPaser(object):

    def __init__(self, token_list):
        """
        :type token_list:list
        :param token_list:
        :return:
        """
        self.token_iter = iter(token_list)

    def _get_next_token(self):
        """
        :rtype: Token
        :return:
        """
        next_token = next(self.token_iter, None)
        if next_token is None:
            return None
        return next_token

    def parse_expr(self):
        """
        :rtype : Node
        :return:
        """
        token = self._get_next_token()

        '"":type :Token""'
        if token is None:
            return None
        result = self._create_node(token)
        return result

    def _create_node(self, token):
        if token is None:
            return None
        elif token.type is CuteType.INT:
            return Node(TokenType.INT,  token.lexeme)
        elif token.type is CuteType.ID:
            return Node(TokenType.ID,   token.lexeme)
        elif token.type is CuteType.L_PAREN:
            return Node(TokenType.LIST, self._parse_expr_list())
        elif token.type is CuteType.R_PAREN:
            return None
        elif token.type in CuteType.BOOLEAN_LIST:
            return Node(token.type)
        elif token.type in CuteType.BINARYOP_LIST:
            return Node(token.type, token.lexeme)
        elif token.type is CuteType.QUOTE:
            return Node(TokenType.QUOTE, token.lexeme)
        elif token.type is CuteType.APOSTROPHE:
            node = Node(TokenType.LIST, Node(TokenType.QUOTE, token.lexeme))
            node.value.next = self.parse_expr()
            return node
        elif check_keyword(token.lexeme):
            return Node(token.type, token.lexeme)

    def _parse_expr_list(self):
        head = self.parse_expr()
        '"":type :Node""'
        if head is not None:
            head.next = self._parse_expr_list()
        return head


def run_list(root_node):
    """
    :type root_node: Node
    """
    op_code_node = root_node.value

    return run_func(op_code_node)(root_node)


def run_func(op_code_node):
    """
    :type op_code_node:Node/
    """
    def quote(node):
        return node

    def strip_quote(node):
        """
        :type node: Node
        """
        if node.type is TokenType.LIST:
            if node.value is TokenType.QUOTE or TokenType.APOSTROPHE:
                return node.value.next
        if node.type is TokenType.QUOTE:
            return node.next
        return node

    def cons(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        r_node = l_node.next
        r_node = run_expr(r_node)
        l_node = run_expr(l_node)
        new_r_node = r_node
        new_l_node = l_node
        new_r_node = strip_quote(new_r_node)
        new_l_node = strip_quote(new_l_node)
        new_l_node.next = new_r_node.value

        return create_new_quote_list(new_l_node, True)

    def car(node):
        l_node = run_expr(node.value.next)
        result = strip_quote(l_node).value
        if result.type is not TokenType.LIST:
            return result
        return create_new_quote_list(result)

    def cdr(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        l_node = run_expr(lookupTable(l_node))
        new_r_node = strip_quote(l_node)
        return create_new_quote_list(new_r_node.value.next, True)

    def null_q(node):
        l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node).value
        if new_l_node is None:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def atom_q(node):
        l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node)

        if new_l_node.type is TokenType.LIST:
            if new_l_node.value is None:
                return Node(TokenType.TRUE)
            return Node(TokenType.FALSE)
        else:
            return Node(TokenType.TRUE)

    def eq_q(node):
        l_node = node.value.next
        r_node = l_node.next
        new_l_node = strip_quote(run_expr(l_node))
        new_r_node = strip_quote(run_expr(r_node))
        if (new_l_node.type or new_r_node.type) is not TokenType.INT:
            return Node(TokenType.FALSE)
        if new_l_node.value == new_r_node.value:
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    # Fill Out
    # table을 보고 함수를 작성하시오
    def not_op(node):
        l_node = node.value.next
        if l_node.type is TokenType.FALSE:
            return Node(TokenType.TRUE, l_node.value)
        return Node(TokenType.FALSE, l_node.value)

    def plus(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node.next)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        return Node(l_node.type, int(lookupTable(l_node).value)+int(lookupTable(l_node.next).value))

    def minus(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node.next)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        return Node(l_node.type, int(lookupTable(l_node).value) - int(lookupTable(l_node.next).value))

    def multiple(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        return Node(l_node.type, int(lookupTable(l_node).value) * int(lookupTable(l_node.next).value))

    def divide(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        return Node(l_node.type, int(lookupTable(l_node).value) / int(lookupTable(l_node.next).value))

    def lt(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        if int(l_node.value) < int(l_node.next.value):
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    def gt(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        if int(l_node.value) > int(l_node.next.value):
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    def eq(node):
        l_node = node.value.next
        if l_node.type is TokenType.LIST:
            m_node = run_expr(l_node)
            l_node.value = m_node.value
            l_node.type = m_node.type
        if l_node.next.type is TokenType.LIST:
            n_node = run_expr(l_node)
            l_node.next.value = n_node.value
            l_node.next.type = n_node.type
        if int(l_node.value) == int(l_node.next.value):
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    def cond(node):
        l_node = node.value.next
        if l_node is not None:
            return run_cond(l_node)
        else:
            print('cond null error!')

    def run_cond(node):
        """
        :type node: Node
        """
        #Fill Out
        l_node = run_expr(node.value)
        if l_node.type is TokenType.TRUE:
            return run_expr(node.value.next)
        return run_cond(node.next)

    def create_new_quote_list(value_node, list_flag=False):
        """
        :type value_node: Node
        """
        quote_list = Node(TokenType.QUOTE, 'quote')
        wrapper_new_list = Node(TokenType.LIST, quote_list)
        if value_node is None:
            pass
        elif value_node.type is TokenType.LIST:
            if list_flag:
                inner_l_node = Node(TokenType.LIST, value_node)
                quote_list.next = inner_l_node
            else:
                quote_list.next = value_node
            return wrapper_new_list
        new_value_list = Node(TokenType.LIST, value_node)
        quote_list.next = new_value_list
        return wrapper_new_list
    # 함수 define 정의
    def define(node):
        l_node = node.value.next # type define 이후의 순수한 노드의 값 불러오기
        result = strip_quote(l_node).value # id 추출하기
        insertTable(result, l_node.next.value) # insertTable 함수를 이용하여 idTable에 { id : value } 값 저장

    # 함수 lambda 정의
    def run_lambda(node):
        a = strip_quote(node)
        b = strip_quote(node.value)
        if b.type is TokenType.LAMBDA: # Type이 lambda 일때
            insertTable(b.next.value.value, node.next.value.next.value)
            return run_expr(node.next.value.value.next.next)
        if b.value.next is not None: # .next 값이 존재할때
            aa=strip_quote(a)
            secondVariable= b.value.next.value  # 두번째 변수 값
            if b.value.next.next is None: # .next 값이 존재하지 않을때
                secondValue = a.next.value  # 두번째 저장될 값
                insertTable(secondVariable, secondValue)
            else: # .next.next 값이 존재할때
                secondValue = aa.value.value # 두번재 저장될 값 (세번째 변수 있을 경우)
                insertTable(secondVariable, secondValue)
                insertTable(b.value.next.next.value, aa.value.next.value) # 세번째 변수와 값
                firstVariable=strip_quote(b.value).value  # 첫번째 입력될 변수
                firstValue=a.value.value  # 첫번째 저장될 값
                insertTable(firstVariable,firstValue)
                temp6 = run_expr(firstValue.next.next)
                insertTable(b.value.next.next.value, temp6)
                secondValue.next.next.next = temp6
                return run_expr(secondValue.next.next)
        a = run_expr(a)
        insertTable(b.value.value, a.value)
        if lookupTable(b.next.value).type is TokenType.LIST: # Type 이 LIST일때
            first = lookupTable(b.next.value)
            if lookupTable(b.next.value.next).type is TokenType.LIST: # Type 이 LIST일때
                second = lookupTable(b.next.value.next)
                first.set_last_next(second)
                makeList = Node(TokenType.LIST, first)
                makeList = run_expr(makeList)
                return makeList
            else: # Type 이 LIST 이외일때
                second = b.next.value.next
                second = lookupTable(second)
                first.set_last_next(second)
                makeList = Node(TokenType.LIST, first)
                makeList = run_expr(makeList)
                return makeList

        is_define = b.next #Nested 구현을 할 때, 실행부분에 define이 있는 경우 처리하기 위한 is_define변수
        nested_define_Table = [] #Nested로 define 된 것이 내부에서만 define 되도록 지역변수 배열 만들어줌
        save_define = {} #미리 전역변수로 선언된 경우. 저장해두기 위한 dictionary자료구조
        while is_define.value.type is TokenType.DEFINE: #TokenType.DEFINE이라면 처리해줌
            save_data = is_define.value.next.value #define의 key 값
            if save_data in idTable: #key값이 idTable에 이미 존재한다면
                save_define[save_data] = idTable[save_data] #save_define dictionary에 값을 저장
            nested_define_Table.append(save_data) #nested_define_Table에 해당하는 value 값을 똑같이 넣어둠
            run_expr(is_define) # define을 해줌
            is_define = is_define.next #next에 define Token이 또 있는지 확인하기 위해 전진

        return_val = run_expr(is_define)

        while nested_define_Table.__len__() is not 0: #nested_define_Table이 빌때까지
            del idTable[nested_define_Table.pop()]  #idTable에서 nested로 Define된 key, Value를 지워줌

        for save_define_data in save_define: # save_define에 data가 있다면
            idTable[save_define_data] = save_define[save_define_data] #그 data를 다시 idTable에 바인딩

        return return_val

    table = {}
    table['define'] = define
    table['cons'] = cons
    table["'"] = quote
    table['quote'] = quote
    table['cdr'] = cdr
    table['car'] = car
    table['eq?'] = eq_q
    table['null?'] = null_q
    table['atom?'] = atom_q
    table['not'] = not_op
    table['+'] = plus
    table['-'] = minus
    table['*'] = multiple
    table['/'] = divide
    table['<'] = lt
    table['>'] = gt
    table['='] = eq
    table['cond'] = cond
    table['lambda'] = run_lambda
    if op_code_node.type is TokenType.LIST:
        return table[op_code_node.value.value]
    if op_code_node.value in idTable:
        return run_expr(Node(TokenType.LIST,idTable[lookupTable(op_code_node)]))
    return table[op_code_node.value]

idTable = {}
#함수 insertTable 정의
def insertTable(id, value):
    idTable[id] = value
    return idTable[id]
#함수 lookupTable 정의
def lookupTable(id):
    firstTemp = id.value
    if firstTemp in idTable:
        temp = idTable[firstTemp]
        if type(temp) is int: #함수 id의 value 값의 type이 int일 경우
            return lookupTable(Node(TokenType.INT, temp))
        elif type(temp) is str: #함수 id의 value 값의 type이 str일 경우
            return lookupTable(Node(TokenType.ID, temp))
        elif  temp.type is TokenType.ID: #함수 id의 value 값의 type이 ID일 경우
            return temp
        elif temp.type is TokenType.LAMBDA: #함수 id의 value 값의 type이 LAMBDA일 경우
            temp = Node(TokenType.LIST, temp) #함수 temp에 Node를 생성
            if id.next is not None:
                if id.next.type is TokenType.ID:
                    temp.next = Node(lookupTable(id.next).type, lookupTable(id.next))
                else:
                    temp.next = id.next
            return temp
        return run_expr(lookupTable(Node(TokenType.LIST, temp)))
    return id

def run_expr(root_node):
    """
    :type root_node : Node
    """
    if root_node is None:
        return None
    if root_node.type is TokenType.ID:
        return lookupTable(root_node)
    elif root_node.type is TokenType.INT:
        return root_node
    elif root_node.type is TokenType.TRUE:
        return root_node
    elif root_node.type is TokenType.FALSE:
        return root_node
    elif root_node.type is TokenType.LIST:
        if root_node.value.value in idTable:
            root_node = Node(TokenType.LIST, lookupTable(root_node.value))
        return run_list(root_node)
    else:
        print 'Run Expr Error'
    return None


def print_node(node):
    """
    "Evaluation 후 결과를 출력하기 위한 함수"
    "입력은 List Node 또는 atom"
    :type node: Node
    """
    def print_list(node):
        """
        "List노드의 value에 대해서 출력"
        "( 2 3 )이 입력이면 2와 3에 대해서 모두 출력함"
        :type node: Node
        """
        def print_list_val(node):
            if node.next is not None:
                return print_node(node)+' '+print_list_val(node.next)
            return print_node(node)

        if node.type is TokenType.LIST:
            if node.value is None:
                return '( )'
            if node.value.type is TokenType.QUOTE:
                return print_node(node.value)
            return '('+print_list_val(node.value)+')'

    if node is None:
        return ''
    if node.type in [TokenType.ID, TokenType.INT]:
        return node.value
    if node.type is TokenType.TRUE:
        return '#T'
    if node.type is TokenType.FALSE:
        return '#F'
    if node.type is TokenType.PLUS:
        return '+'
    if node.type is TokenType.MINUS:
        return '-'
    if node.type is TokenType.TIMES:
        return '*'
    if node.type is TokenType.DIV:
        return '/'
    if node.type is TokenType.GT:
        return '>'
    if node.type is TokenType.LT:
        return '<'
    if node.type is TokenType.EQ:
        return '='
    if node.type is TokenType.LIST:
        return print_list(node)
    if node.type is TokenType.ATOM_Q:
        return 'atom?'
    if node.type is TokenType.CAR:
        return 'car'
    if node.type is TokenType.CDR:
        return 'cdr'
    if node.type is TokenType.COND:
        return 'cond'
    if node.type is TokenType.CONS:
        return 'cons'
    if node.type is TokenType.LAMBDA:
        return 'lambda'
    if node.type is TokenType.NULL_Q:
        return 'null?'
    if node.type is TokenType.EQ_Q:
        return 'eq?'
    if node.type is TokenType.NOT:
        return 'not'
    if node.type is TokenType.QUOTE:
        return "'" + print_node(node.next)
    if node.type is TokenType.DEFINE:
        return 'define'


def Test_method(input):
    test_cute = CuteScanner(input)
    test_tokens = test_cute.tokenize()
    test_basic_paser = BasicPaser(test_tokens)
    node = test_basic_paser.parse_expr()
    cute_inter = run_expr(node)
    if cute_inter is not None:
        print "...", print_node(cute_inter)
    if node.type is TokenType.LIST and node.value.type is TokenType.LIST and node.value.value.type is TokenType.LAMBDA:
        temp = node.value.value.next.value
        del idTable[temp.value]
        if temp.next is not None:
             del idTable[temp.next.value]


def Test_All():
    Test_method("(define a 1)")
    Test_method("a") #1
    Test_method("(define b '(1 2 3))")
    Test_method("b") #'(1 2 3)
    Test_method("(define c (- 5 2))")
    Test_method("c") # 3
    Test_method("(define d '(+ 2 3))")
    Test_method("d") # '(+2 3)
    Test_method("(define test b)")
    Test_method("test") # '(1 2 3)
    Test_method("(+ a 3)") # 4
    Test_method("(define a 2)")
    Test_method("(* a 4)") #  8
    Test_method("((lambda (x) (* x -2)) 3)") # -6
    Test_method("((lambda (x) (/ x 2)) a)") # 1
    Test_method("((lambda (x y) (* x y)) 3 5)") # 15
    Test_method("((lambda (x y) (* x y)) a 5)") # 10
    Test_method("(define plus1 (lambda (x) (+ x 1)))")
    Test_method("(plus1 3)") # 4
    Test_method("(define mul1 (lambda (x) (* x a)))")
    Test_method("(mul1 a)") # 4
    Test_method("(define plus2 (lambda (x) (+ (plus1 x) 1)))")
    Test_method("(plus2 4)") # 6
    Test_method("(define plus3 (lambda (x) (+ (plus1 x) a)))")
    Test_method("(plus3 a)") # 5
    Test_method("(define mul2 (lambda (x) (* (plus1 x) -2))) (mul2 7)")
    Test_method("(mul2 7)") # -16
    Test_method("(define lastitem (lambda (ls) (cond ((null? (cdr ls)) (car ls)) (#T (lastitem (cdr ls))))))")
    Test_method("(lastitem '(1 2 3 4))") # 4
    Test_method("(define square (lambda (x) (* x x)))")
    Test_method("(define yourfunc (lambda (x func) (func x)))")
    Test_method("(yourfunc 3 square)") # 9
    Test_method("(define multwo (lambda (x) (* 2 x)))")
    Test_method("(define newfun (lambda (fun1 fun2 x) (fun2 (fun1 x))))")
    Test_method("(newfun square multwo 10)") # 200
    # Test_method("(define sqrt (lambda (x) (* 3 x)))") sqrt가 먼저 전역 변수로 선언된 경우 실행이 제대로 되는지 확인하기 위한 Testcod
    Test_method("(define cube (lambda (n) (define sqrt (lambda (n) (* n n))) (* (sqrt n) n)))")
    # Test_method("(cube 3)") # 27 Nested define된 결과 또한 잘 실행되는지 확인하기 위한 TestCode
    Test_method("(sqrt 4)")
#함수 만약 입력을 원한다면 Input_All() 호출
def Input_All():
    test_input = 0
    while test_input != 'quit':
        test_input = raw_input('> ')
        Test_method(test_input)


# Test_All()
Input_All()