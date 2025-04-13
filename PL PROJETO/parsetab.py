
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftORleftANDleftEQNELTLEGTGEleftPLUSMINUSleftTIMESDIVIDEDIVMODrightNOTUMINUSAND ARRAY ASSIGN BEGIN BOOLEAN COLON COMMA DIV DIVIDE DO DOT DOTDOT DOWNTO ELSE END EQ FALSE FOR FUNCTION GE GT ID IF INTEGER LBRACKET LE LPAREN LT MINUS MOD NE NOT NUMBER OF OR PLUS PROGRAM RBRACKET READLN REAL RPAREN SEMICOLON STRING STRING_LITERAL THEN TIMES TO TRUE VAR WHILE WRITE WRITELNprogram : PROGRAM ID SEMICOLON declarations block DOTdeclarations : declaration_list\n| emptydeclaration_list : declaration\n| declaration_list declarationdeclaration : VAR var_decl_list\n| function_declfunction_decl_list : function_decl\n| function_decl_list function_declfunction_decl : FUNCTION ID LPAREN param_list RPAREN COLON base_type SEMICOLON declarations block SEMICOLONparam_list : param\n| param_list SEMICOLON paramparam : id_list COLON typevar_decl_list : var_decl_list var_decl \n| var_declvar_decl : id_list COLON type SEMICOLONid_list : ID\n| id_list COMMA IDtype : base_type\n| array_typearray_type : ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF base_typebase_type : INTEGER\n| BOOLEAN\n| STRING\n| REALblock : BEGIN statement_list ENDstatement_list : statement\n| statement_list SEMICOLON statementstatement : assignment\n| if_statement\n| while_statement\n| for_statement\n| write_statement\n| read_statement\n| block\n| emptyassignment : ID ASSIGN expressionif_statement : IF expression THEN statement \n| IF expression THEN statement ELSE statementwhile_statement : WHILE expression DO statementfor_statement : FOR ID ASSIGN expression TO expression DO statement\n| FOR ID ASSIGN expression DOWNTO expression DO statementwrite_statement : WRITE LPAREN write_args RPAREN\n| WRITELN LPAREN write_args RPARENwrite_args : expression\n| write_args COMMA expressionread_statement : READLN LPAREN expression RPARENexpression : expression PLUS expression\n| expression MINUS expression\n| expression TIMES expression\n| expression DIVIDE expression\n| expression DIV expression\n| expression MOD expression\n| expression EQ expression\n| expression NE expression\n| expression LT expression\n| expression LE expression\n| expression GT expression\n| expression GE expression\n| expression AND expression\n| expression OR expressionexpression : NOT expressionexpression : MINUS expression %prec UMINUSexpression : LPAREN expression RPARENexpression : NUMBERexpression : STRING_LITERALexpression : TRUE\n| FALSEexpression : IDexpression : ID LBRACKET expression RBRACKETexpression : ID LPAREN expression_list RPARENexpression_list : expression\n| expression_list COMMA expressionempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,20,],[0,-1,]),'ID':([2,9,11,13,15,16,32,33,34,38,40,41,43,44,46,47,48,56,57,58,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,93,94,99,102,126,133,136,137,138,148,149,],[3,18,19,31,18,-15,53,53,55,-14,67,18,31,53,53,53,53,53,53,53,31,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,31,53,-16,18,53,31,53,53,53,31,31,]),'SEMICOLON':([3,13,21,22,23,24,25,26,27,28,29,30,42,43,49,50,51,52,53,59,60,61,62,63,64,65,68,69,71,72,73,88,89,93,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,123,125,127,128,131,132,133,134,135,141,142,148,149,152,153,155,156,],[4,-74,43,-27,-29,-30,-31,-32,-33,-34,-35,-36,-26,-74,-65,-66,-67,-68,-69,99,-19,-20,-22,-23,-24,-25,102,-11,-28,-37,-74,-63,-62,-74,-38,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,-40,-43,-44,-47,-12,-13,-74,-70,-71,147,-39,-74,-74,-41,-42,157,-21,]),'BEGIN':([4,5,6,7,8,10,13,14,15,16,38,43,73,93,99,133,147,148,149,151,157,],[-74,13,-2,-3,-4,-7,13,-5,-6,-15,-14,13,13,13,-16,13,-74,13,13,13,-10,]),'VAR':([4,6,8,10,14,15,16,38,99,147,157,],[9,9,-4,-7,-5,-6,-15,-14,-16,9,-10,]),'FUNCTION':([4,6,8,10,14,15,16,38,99,147,157,],[11,11,-4,-7,-5,-6,-15,-14,-16,11,-10,]),'DOT':([12,42,],[20,-26,]),'IF':([13,43,73,93,133,148,149,],[32,32,32,32,32,32,32,]),'WHILE':([13,43,73,93,133,148,149,],[33,33,33,33,33,33,33,]),'FOR':([13,43,73,93,133,148,149,],[34,34,34,34,34,34,34,]),'WRITE':([13,43,73,93,133,148,149,],[35,35,35,35,35,35,35,]),'WRITELN':([13,43,73,93,133,148,149,],[36,36,36,36,36,36,36,]),'READLN':([13,43,73,93,133,148,149,],[37,37,37,37,37,37,37,]),'END':([13,21,22,23,24,25,26,27,28,29,30,42,43,49,50,51,52,53,71,72,73,88,89,93,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,123,125,127,128,133,134,135,142,148,149,152,153,],[-74,42,-27,-29,-30,-31,-32,-33,-34,-35,-36,-26,-74,-65,-66,-67,-68,-69,-28,-37,-74,-63,-62,-74,-38,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,-40,-43,-44,-47,-74,-70,-71,-39,-74,-74,-41,-42,]),'COLON':([17,18,67,70,101,],[39,-17,-18,103,130,]),'COMMA':([17,18,49,50,51,52,53,67,70,88,89,95,96,97,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,121,122,134,135,139,143,],[40,-17,-65,-66,-67,-68,-69,-18,40,-63,-62,126,-45,126,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,136,-72,-70,-71,-46,-73,]),'LPAREN':([19,32,33,35,36,37,44,46,47,48,53,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[41,48,48,56,57,58,48,48,48,48,92,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'ELSE':([23,24,25,26,27,28,29,30,42,49,50,51,52,53,72,73,88,89,93,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,123,125,127,128,133,134,135,142,148,149,152,153,],[-29,-30,-31,-32,-33,-34,-35,-36,-26,-65,-66,-67,-68,-69,-37,-74,-63,-62,-74,133,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,-40,-43,-44,-47,-74,-70,-71,-39,-74,-74,-41,-42,]),'ASSIGN':([31,55,],[44,94,]),'NOT':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'MINUS':([32,33,44,45,46,47,48,49,50,51,52,53,54,56,57,58,72,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,94,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,126,134,135,136,137,138,139,143,144,145,],[46,46,46,75,46,46,46,-65,-66,-67,-68,-69,75,46,46,46,75,46,46,46,46,46,46,46,46,46,46,46,46,46,46,-63,-62,75,46,46,46,75,75,-48,-49,-50,-51,-52,-53,75,75,75,75,75,75,75,75,-64,75,75,75,46,-70,-71,46,46,46,75,75,75,75,]),'NUMBER':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,100,126,136,137,138,140,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,129,49,49,49,49,146,]),'STRING_LITERAL':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'TRUE':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'FALSE':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'INTEGER':([39,103,130,154,],[62,62,62,62,]),'BOOLEAN':([39,103,130,154,],[63,63,63,63,]),'STRING':([39,103,130,154,],[64,64,64,64,]),'REAL':([39,103,130,154,],[65,65,65,65,]),'ARRAY':([39,103,],[66,66,]),'THEN':([45,49,50,51,52,53,88,89,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,134,135,],[73,-65,-66,-67,-68,-69,-63,-62,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,-70,-71,]),'PLUS':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[74,-65,-66,-67,-68,-69,74,74,-63,-62,74,74,74,-48,-49,-50,-51,-52,-53,74,74,74,74,74,74,74,74,-64,74,74,74,-70,-71,74,74,74,74,]),'TIMES':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[76,-65,-66,-67,-68,-69,76,76,-63,-62,76,76,76,76,76,-50,-51,-52,-53,76,76,76,76,76,76,76,76,-64,76,76,76,-70,-71,76,76,76,76,]),'DIVIDE':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[77,-65,-66,-67,-68,-69,77,77,-63,-62,77,77,77,77,77,-50,-51,-52,-53,77,77,77,77,77,77,77,77,-64,77,77,77,-70,-71,77,77,77,77,]),'DIV':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[78,-65,-66,-67,-68,-69,78,78,-63,-62,78,78,78,78,78,-50,-51,-52,-53,78,78,78,78,78,78,78,78,-64,78,78,78,-70,-71,78,78,78,78,]),'MOD':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[79,-65,-66,-67,-68,-69,79,79,-63,-62,79,79,79,79,79,-50,-51,-52,-53,79,79,79,79,79,79,79,79,-64,79,79,79,-70,-71,79,79,79,79,]),'EQ':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[80,-65,-66,-67,-68,-69,80,80,-63,-62,80,80,80,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,80,80,-64,80,80,80,-70,-71,80,80,80,80,]),'NE':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[81,-65,-66,-67,-68,-69,81,81,-63,-62,81,81,81,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,81,81,-64,81,81,81,-70,-71,81,81,81,81,]),'LT':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[82,-65,-66,-67,-68,-69,82,82,-63,-62,82,82,82,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,82,82,-64,82,82,82,-70,-71,82,82,82,82,]),'LE':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[83,-65,-66,-67,-68,-69,83,83,-63,-62,83,83,83,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,83,83,-64,83,83,83,-70,-71,83,83,83,83,]),'GT':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[84,-65,-66,-67,-68,-69,84,84,-63,-62,84,84,84,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,84,84,-64,84,84,84,-70,-71,84,84,84,84,]),'GE':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[85,-65,-66,-67,-68,-69,85,85,-63,-62,85,85,85,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,85,85,-64,85,85,85,-70,-71,85,85,85,85,]),'AND':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[86,-65,-66,-67,-68,-69,86,86,-63,-62,86,86,86,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,86,-64,86,86,86,-70,-71,86,86,86,86,]),'OR':([45,49,50,51,52,53,54,72,88,89,90,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,124,134,135,139,143,144,145,],[87,-65,-66,-67,-68,-69,87,87,-63,-62,87,87,87,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,87,87,87,-70,-71,87,87,87,87,]),'DO':([49,50,51,52,53,54,88,89,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,134,135,144,145,],[-65,-66,-67,-68,-69,93,-63,-62,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,-70,-71,148,149,]),'RPAREN':([49,50,51,52,53,60,61,62,63,64,65,68,69,88,89,90,95,96,97,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,121,122,131,132,134,135,139,143,156,],[-65,-66,-67,-68,-69,-19,-20,-22,-23,-24,-25,101,-11,-63,-62,119,125,-45,127,128,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,135,-72,-12,-13,-70,-71,-46,-73,-21,]),'RBRACKET':([49,50,51,52,53,88,89,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,134,135,146,],[-65,-66,-67,-68,-69,-63,-62,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,134,-70,-71,150,]),'TO':([49,50,51,52,53,88,89,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,124,134,135,],[-65,-66,-67,-68,-69,-63,-62,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,137,-70,-71,]),'DOWNTO':([49,50,51,52,53,88,89,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,124,134,135,],[-65,-66,-67,-68,-69,-63,-62,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-64,138,-70,-71,]),'LBRACKET':([53,66,],[91,100,]),'DOTDOT':([129,],[140,]),'OF':([150,],[154,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declarations':([4,147,],[5,151,]),'declaration_list':([4,147,],[6,6,]),'empty':([4,13,43,73,93,133,147,148,149,],[7,30,30,30,30,30,7,30,30,]),'declaration':([4,6,147,],[8,14,8,]),'function_decl':([4,6,147,],[10,10,10,]),'block':([5,13,43,73,93,133,148,149,151,],[12,29,29,29,29,29,29,29,155,]),'var_decl_list':([9,],[15,]),'var_decl':([9,15,],[16,38,]),'id_list':([9,15,41,102,],[17,17,70,70,]),'statement_list':([13,],[21,]),'statement':([13,43,73,93,133,148,149,],[22,71,104,123,142,152,153,]),'assignment':([13,43,73,93,133,148,149,],[23,23,23,23,23,23,23,]),'if_statement':([13,43,73,93,133,148,149,],[24,24,24,24,24,24,24,]),'while_statement':([13,43,73,93,133,148,149,],[25,25,25,25,25,25,25,]),'for_statement':([13,43,73,93,133,148,149,],[26,26,26,26,26,26,26,]),'write_statement':([13,43,73,93,133,148,149,],[27,27,27,27,27,27,27,]),'read_statement':([13,43,73,93,133,148,149,],[28,28,28,28,28,28,28,]),'expression':([32,33,44,46,47,48,56,57,58,74,75,76,77,78,79,80,81,82,83,84,85,86,87,91,92,94,126,136,137,138,],[45,54,72,88,89,90,96,96,98,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,122,124,139,143,144,145,]),'type':([39,103,],[59,132,]),'base_type':([39,103,130,154,],[60,60,141,156,]),'array_type':([39,103,],[61,61,]),'param_list':([41,],[68,]),'param':([41,102,],[69,131,]),'write_args':([56,57,],[95,97,]),'expression_list':([92,],[121,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID SEMICOLON declarations block DOT','program',6,'p_program','pascal_yacc.py',16),
  ('declarations -> declaration_list','declarations',1,'p_declarations','pascal_yacc.py',22),
  ('declarations -> empty','declarations',1,'p_declarations','pascal_yacc.py',23),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','pascal_yacc.py',27),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list','pascal_yacc.py',28),
  ('declaration -> VAR var_decl_list','declaration',2,'p_declaration','pascal_yacc.py',32),
  ('declaration -> function_decl','declaration',1,'p_declaration','pascal_yacc.py',33),
  ('function_decl_list -> function_decl','function_decl_list',1,'p_function_decl_list','pascal_yacc.py',40),
  ('function_decl_list -> function_decl_list function_decl','function_decl_list',2,'p_function_decl_list','pascal_yacc.py',41),
  ('function_decl -> FUNCTION ID LPAREN param_list RPAREN COLON base_type SEMICOLON declarations block SEMICOLON','function_decl',11,'p_function_decl','pascal_yacc.py',45),
  ('param_list -> param','param_list',1,'p_param_list','pascal_yacc.py',49),
  ('param_list -> param_list SEMICOLON param','param_list',3,'p_param_list','pascal_yacc.py',50),
  ('param -> id_list COLON type','param',3,'p_param','pascal_yacc.py',54),
  ('var_decl_list -> var_decl_list var_decl','var_decl_list',2,'p_var_decl_list','pascal_yacc.py',58),
  ('var_decl_list -> var_decl','var_decl_list',1,'p_var_decl_list','pascal_yacc.py',59),
  ('var_decl -> id_list COLON type SEMICOLON','var_decl',4,'p_var_decl','pascal_yacc.py',63),
  ('id_list -> ID','id_list',1,'p_id_list','pascal_yacc.py',67),
  ('id_list -> id_list COMMA ID','id_list',3,'p_id_list','pascal_yacc.py',68),
  ('type -> base_type','type',1,'p_type','pascal_yacc.py',72),
  ('type -> array_type','type',1,'p_type','pascal_yacc.py',73),
  ('array_type -> ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF base_type','array_type',8,'p_array_type','pascal_yacc.py',77),
  ('base_type -> INTEGER','base_type',1,'p_base_type','pascal_yacc.py',81),
  ('base_type -> BOOLEAN','base_type',1,'p_base_type','pascal_yacc.py',82),
  ('base_type -> STRING','base_type',1,'p_base_type','pascal_yacc.py',83),
  ('base_type -> REAL','base_type',1,'p_base_type','pascal_yacc.py',84),
  ('block -> BEGIN statement_list END','block',3,'p_block','pascal_yacc.py',89),
  ('statement_list -> statement','statement_list',1,'p_statement_list','pascal_yacc.py',93),
  ('statement_list -> statement_list SEMICOLON statement','statement_list',3,'p_statement_list','pascal_yacc.py',94),
  ('statement -> assignment','statement',1,'p_statement','pascal_yacc.py',99),
  ('statement -> if_statement','statement',1,'p_statement','pascal_yacc.py',100),
  ('statement -> while_statement','statement',1,'p_statement','pascal_yacc.py',101),
  ('statement -> for_statement','statement',1,'p_statement','pascal_yacc.py',102),
  ('statement -> write_statement','statement',1,'p_statement','pascal_yacc.py',103),
  ('statement -> read_statement','statement',1,'p_statement','pascal_yacc.py',104),
  ('statement -> block','statement',1,'p_statement','pascal_yacc.py',105),
  ('statement -> empty','statement',1,'p_statement','pascal_yacc.py',106),
  ('assignment -> ID ASSIGN expression','assignment',3,'p_assignment','pascal_yacc.py',110),
  ('if_statement -> IF expression THEN statement','if_statement',4,'p_if_statement','pascal_yacc.py',114),
  ('if_statement -> IF expression THEN statement ELSE statement','if_statement',6,'p_if_statement','pascal_yacc.py',115),
  ('while_statement -> WHILE expression DO statement','while_statement',4,'p_while_statement','pascal_yacc.py',119),
  ('for_statement -> FOR ID ASSIGN expression TO expression DO statement','for_statement',8,'p_for_statement','pascal_yacc.py',123),
  ('for_statement -> FOR ID ASSIGN expression DOWNTO expression DO statement','for_statement',8,'p_for_statement','pascal_yacc.py',124),
  ('write_statement -> WRITE LPAREN write_args RPAREN','write_statement',4,'p_write_statement','pascal_yacc.py',131),
  ('write_statement -> WRITELN LPAREN write_args RPAREN','write_statement',4,'p_write_statement','pascal_yacc.py',132),
  ('write_args -> expression','write_args',1,'p_write_args','pascal_yacc.py',136),
  ('write_args -> write_args COMMA expression','write_args',3,'p_write_args','pascal_yacc.py',137),
  ('read_statement -> READLN LPAREN expression RPAREN','read_statement',4,'p_read_statement','pascal_yacc.py',141),
  ('expression -> expression PLUS expression','expression',3,'p_expression','pascal_yacc.py',146),
  ('expression -> expression MINUS expression','expression',3,'p_expression','pascal_yacc.py',147),
  ('expression -> expression TIMES expression','expression',3,'p_expression','pascal_yacc.py',148),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','pascal_yacc.py',149),
  ('expression -> expression DIV expression','expression',3,'p_expression','pascal_yacc.py',150),
  ('expression -> expression MOD expression','expression',3,'p_expression','pascal_yacc.py',151),
  ('expression -> expression EQ expression','expression',3,'p_expression','pascal_yacc.py',152),
  ('expression -> expression NE expression','expression',3,'p_expression','pascal_yacc.py',153),
  ('expression -> expression LT expression','expression',3,'p_expression','pascal_yacc.py',154),
  ('expression -> expression LE expression','expression',3,'p_expression','pascal_yacc.py',155),
  ('expression -> expression GT expression','expression',3,'p_expression','pascal_yacc.py',156),
  ('expression -> expression GE expression','expression',3,'p_expression','pascal_yacc.py',157),
  ('expression -> expression AND expression','expression',3,'p_expression','pascal_yacc.py',158),
  ('expression -> expression OR expression','expression',3,'p_expression','pascal_yacc.py',159),
  ('expression -> NOT expression','expression',2,'p_expression_not','pascal_yacc.py',163),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','pascal_yacc.py',167),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','pascal_yacc.py',171),
  ('expression -> NUMBER','expression',1,'p_expression_number','pascal_yacc.py',175),
  ('expression -> STRING_LITERAL','expression',1,'p_expression_string','pascal_yacc.py',179),
  ('expression -> TRUE','expression',1,'p_expression_boolean','pascal_yacc.py',183),
  ('expression -> FALSE','expression',1,'p_expression_boolean','pascal_yacc.py',184),
  ('expression -> ID','expression',1,'p_expression_id','pascal_yacc.py',188),
  ('expression -> ID LBRACKET expression RBRACKET','expression',4,'p_expression_array_access','pascal_yacc.py',192),
  ('expression -> ID LPAREN expression_list RPAREN','expression',4,'p_expression_function_call','pascal_yacc.py',196),
  ('expression_list -> expression','expression_list',1,'p_expression_list','pascal_yacc.py',200),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list','pascal_yacc.py',201),
  ('empty -> <empty>','empty',0,'p_empty','pascal_yacc.py',206),
]
