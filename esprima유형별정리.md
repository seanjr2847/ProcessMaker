# Program

##설명
A program can be either a script or a module.
스크립트나 모듈인지 알려줌.
xfdl은 스크립트니까 제외.

## 예시
{
    "id": "dc533f13-6afb-4bdb-96a7-cc4ba811338e",
    "parent_id": [],
    "child_ids": ["d2bbfa7f-cc47-4c34-99a4-eb217bf701ea"],
    "type": "Program",
    "body": [{"child_node_id": "d2bbfa7f-cc47-4c34-99a4-eb217bf701ea"}],
    "sourceType": "script",
    "errors": [],
}

# FunctionDeclaration

##설명
함수 선언


##예시
interface FunctionDeclaration {
    type: 'FunctionDeclaration';
    id: Identifier | null;
    params: FunctionParameter[];
    body: BlockStatement;
    generator: boolean;
    async: boolean;
    expression: false;
}
with

type FunctionParameter = AssignmentPattern | Identifier | BindingPattern;


# BlockStatement
##기본 포맷
여러가지 블럭들이 올 수 있음 ㅇㅇ
아래 블럭들 올 수 있음

type Statement = BlockStatement | BreakStatement | ContinueStatement |
    DebuggerStatement | DoWhileStatement | EmptyStatement |
    ExpressionStatement | ForStatement | ForInStatement |
    ForOfStatement | FunctionDeclaration | IfStatement |
    LabeledStatement | ReturnStatement | SwitchStatement |
    ThrowStatement | TryStatement | VariableDeclaration |
    WhileStatement | WithStatement;
A declaration can be one of the following:

type Declaration = ClassDeclaration | FunctionDeclaration |  VariableDeclaration;
A statement list item is either a statement or a declaration:

##설명
interface BlockStatement: BlockStatement라는 이름의 인터페이스를 정의합니다.
type: 'BlockStatement': 이 인터페이스의 타입이 'BlockStatement'로 설정되어 있습니다.
body: StatementListItem[]: BlockStatement의 body 속성은 StatementListItem 타입의 배열로, 여러 개의 문장 요소를 포함할 수 있습니다.

#VariableDeclaration
변수 선언함
Variable Declaration
interface VariableDeclaration {
    type: 'VariableDeclaration';
    declarations: VariableDeclarator[];
    kind: 'var' | 'const' | 'let';
}
with

interface VariableDeclarator {
    type: 'VariableDeclarator';
    id: Identifier | BindingPattern;
    init: Expression | null;
}

- ExpressionStatement
실행문임
Expression Statement
interface ExpressionStatement {
    type: 'ExpressionStatement';
    expression: Expression;
    directive?: string;
}
When the expression statement represents a directive (such as "use strict"), then the directive property will contain the directive string.

- IfStatement

