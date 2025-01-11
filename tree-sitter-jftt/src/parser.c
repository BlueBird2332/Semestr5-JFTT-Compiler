#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 111
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 61
#define ALIAS_COUNT 0
#define TOKEN_COUNT 45
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 9
#define PRODUCTION_ID_COUNT 1

enum ts_symbol_identifiers {
  sym_comment = 1,
  anon_sym_PROCEDURE = 2,
  anon_sym_IS = 3,
  anon_sym_BEGIN = 4,
  anon_sym_END = 5,
  anon_sym_PROGRAM = 6,
  anon_sym_COLON_EQ = 7,
  anon_sym_SEMI = 8,
  anon_sym_IF = 9,
  anon_sym_THEN = 10,
  anon_sym_ELSE = 11,
  anon_sym_ENDIF = 12,
  anon_sym_WHILE = 13,
  anon_sym_DO = 14,
  anon_sym_ENDWHILE = 15,
  anon_sym_REPEAT = 16,
  anon_sym_UNTIL = 17,
  anon_sym_FOR = 18,
  anon_sym_FROM = 19,
  anon_sym_TO = 20,
  anon_sym_ENDFOR = 21,
  anon_sym_DOWNTO = 22,
  anon_sym_READ = 23,
  anon_sym_WRITE = 24,
  anon_sym_LPAREN = 25,
  anon_sym_RPAREN = 26,
  anon_sym_COMMA = 27,
  anon_sym_LBRACK = 28,
  anon_sym_COLON = 29,
  anon_sym_RBRACK = 30,
  anon_sym_T = 31,
  anon_sym_PLUS = 32,
  anon_sym_DASH = 33,
  anon_sym_STAR = 34,
  anon_sym_SLASH = 35,
  anon_sym_PERCENT = 36,
  anon_sym_EQ = 37,
  anon_sym_BANG_EQ = 38,
  anon_sym_GT = 39,
  anon_sym_LT = 40,
  anon_sym_GT_EQ = 41,
  anon_sym_LT_EQ = 42,
  sym_pidentifier = 43,
  sym_num = 44,
  sym_program_all = 45,
  sym_procedures = 46,
  sym_procedure_def = 47,
  sym_main = 48,
  sym_commands = 49,
  sym_command = 50,
  sym_proc_head = 51,
  sym_proc_call = 52,
  sym_declarations = 53,
  sym_args_decl = 54,
  sym_args = 55,
  sym_expression = 56,
  sym_value = 57,
  sym_identifier = 58,
  sym_condition = 59,
  aux_sym_procedures_repeat1 = 60,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_comment] = "comment",
  [anon_sym_PROCEDURE] = "PROCEDURE",
  [anon_sym_IS] = "IS",
  [anon_sym_BEGIN] = "BEGIN",
  [anon_sym_END] = "END",
  [anon_sym_PROGRAM] = "PROGRAM",
  [anon_sym_COLON_EQ] = ":=",
  [anon_sym_SEMI] = ";",
  [anon_sym_IF] = "IF",
  [anon_sym_THEN] = "THEN",
  [anon_sym_ELSE] = "ELSE",
  [anon_sym_ENDIF] = "ENDIF",
  [anon_sym_WHILE] = "WHILE",
  [anon_sym_DO] = "DO",
  [anon_sym_ENDWHILE] = "ENDWHILE",
  [anon_sym_REPEAT] = "REPEAT",
  [anon_sym_UNTIL] = "UNTIL",
  [anon_sym_FOR] = "FOR",
  [anon_sym_FROM] = "FROM",
  [anon_sym_TO] = "TO",
  [anon_sym_ENDFOR] = "ENDFOR",
  [anon_sym_DOWNTO] = "DOWNTO",
  [anon_sym_READ] = "READ",
  [anon_sym_WRITE] = "WRITE",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_COMMA] = ",",
  [anon_sym_LBRACK] = "[",
  [anon_sym_COLON] = ":",
  [anon_sym_RBRACK] = "]",
  [anon_sym_T] = "T",
  [anon_sym_PLUS] = "+",
  [anon_sym_DASH] = "-",
  [anon_sym_STAR] = "*",
  [anon_sym_SLASH] = "/",
  [anon_sym_PERCENT] = "%",
  [anon_sym_EQ] = "=",
  [anon_sym_BANG_EQ] = "!=",
  [anon_sym_GT] = ">",
  [anon_sym_LT] = "<",
  [anon_sym_GT_EQ] = ">=",
  [anon_sym_LT_EQ] = "<=",
  [sym_pidentifier] = "pidentifier",
  [sym_num] = "num",
  [sym_program_all] = "program_all",
  [sym_procedures] = "procedures",
  [sym_procedure_def] = "procedure_def",
  [sym_main] = "main",
  [sym_commands] = "commands",
  [sym_command] = "command",
  [sym_proc_head] = "proc_head",
  [sym_proc_call] = "proc_call",
  [sym_declarations] = "declarations",
  [sym_args_decl] = "args_decl",
  [sym_args] = "args",
  [sym_expression] = "expression",
  [sym_value] = "value",
  [sym_identifier] = "identifier",
  [sym_condition] = "condition",
  [aux_sym_procedures_repeat1] = "procedures_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_comment] = sym_comment,
  [anon_sym_PROCEDURE] = anon_sym_PROCEDURE,
  [anon_sym_IS] = anon_sym_IS,
  [anon_sym_BEGIN] = anon_sym_BEGIN,
  [anon_sym_END] = anon_sym_END,
  [anon_sym_PROGRAM] = anon_sym_PROGRAM,
  [anon_sym_COLON_EQ] = anon_sym_COLON_EQ,
  [anon_sym_SEMI] = anon_sym_SEMI,
  [anon_sym_IF] = anon_sym_IF,
  [anon_sym_THEN] = anon_sym_THEN,
  [anon_sym_ELSE] = anon_sym_ELSE,
  [anon_sym_ENDIF] = anon_sym_ENDIF,
  [anon_sym_WHILE] = anon_sym_WHILE,
  [anon_sym_DO] = anon_sym_DO,
  [anon_sym_ENDWHILE] = anon_sym_ENDWHILE,
  [anon_sym_REPEAT] = anon_sym_REPEAT,
  [anon_sym_UNTIL] = anon_sym_UNTIL,
  [anon_sym_FOR] = anon_sym_FOR,
  [anon_sym_FROM] = anon_sym_FROM,
  [anon_sym_TO] = anon_sym_TO,
  [anon_sym_ENDFOR] = anon_sym_ENDFOR,
  [anon_sym_DOWNTO] = anon_sym_DOWNTO,
  [anon_sym_READ] = anon_sym_READ,
  [anon_sym_WRITE] = anon_sym_WRITE,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [anon_sym_LBRACK] = anon_sym_LBRACK,
  [anon_sym_COLON] = anon_sym_COLON,
  [anon_sym_RBRACK] = anon_sym_RBRACK,
  [anon_sym_T] = anon_sym_T,
  [anon_sym_PLUS] = anon_sym_PLUS,
  [anon_sym_DASH] = anon_sym_DASH,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_SLASH] = anon_sym_SLASH,
  [anon_sym_PERCENT] = anon_sym_PERCENT,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_BANG_EQ] = anon_sym_BANG_EQ,
  [anon_sym_GT] = anon_sym_GT,
  [anon_sym_LT] = anon_sym_LT,
  [anon_sym_GT_EQ] = anon_sym_GT_EQ,
  [anon_sym_LT_EQ] = anon_sym_LT_EQ,
  [sym_pidentifier] = sym_pidentifier,
  [sym_num] = sym_num,
  [sym_program_all] = sym_program_all,
  [sym_procedures] = sym_procedures,
  [sym_procedure_def] = sym_procedure_def,
  [sym_main] = sym_main,
  [sym_commands] = sym_commands,
  [sym_command] = sym_command,
  [sym_proc_head] = sym_proc_head,
  [sym_proc_call] = sym_proc_call,
  [sym_declarations] = sym_declarations,
  [sym_args_decl] = sym_args_decl,
  [sym_args] = sym_args,
  [sym_expression] = sym_expression,
  [sym_value] = sym_value,
  [sym_identifier] = sym_identifier,
  [sym_condition] = sym_condition,
  [aux_sym_procedures_repeat1] = aux_sym_procedures_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_PROCEDURE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BEGIN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PROGRAM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SEMI] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_THEN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ELSE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ENDIF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WHILE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ENDWHILE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REPEAT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_UNTIL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FOR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FROM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ENDFOR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DOWNTO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_READ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WRITE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RBRACK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_T] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PLUS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SLASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PERCENT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BANG_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT_EQ] = {
    .visible = true,
    .named = false,
  },
  [sym_pidentifier] = {
    .visible = true,
    .named = true,
  },
  [sym_num] = {
    .visible = true,
    .named = true,
  },
  [sym_program_all] = {
    .visible = true,
    .named = true,
  },
  [sym_procedures] = {
    .visible = true,
    .named = true,
  },
  [sym_procedure_def] = {
    .visible = true,
    .named = true,
  },
  [sym_main] = {
    .visible = true,
    .named = true,
  },
  [sym_commands] = {
    .visible = true,
    .named = true,
  },
  [sym_command] = {
    .visible = true,
    .named = true,
  },
  [sym_proc_head] = {
    .visible = true,
    .named = true,
  },
  [sym_proc_call] = {
    .visible = true,
    .named = true,
  },
  [sym_declarations] = {
    .visible = true,
    .named = true,
  },
  [sym_args_decl] = {
    .visible = true,
    .named = true,
  },
  [sym_args] = {
    .visible = true,
    .named = true,
  },
  [sym_expression] = {
    .visible = true,
    .named = true,
  },
  [sym_value] = {
    .visible = true,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [sym_condition] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_procedures_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 3,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
  [52] = 52,
  [53] = 53,
  [54] = 54,
  [55] = 55,
  [56] = 56,
  [57] = 57,
  [58] = 58,
  [59] = 59,
  [60] = 60,
  [61] = 61,
  [62] = 62,
  [63] = 63,
  [64] = 64,
  [65] = 65,
  [66] = 66,
  [67] = 67,
  [68] = 68,
  [69] = 69,
  [70] = 70,
  [71] = 71,
  [72] = 72,
  [73] = 73,
  [74] = 5,
  [75] = 2,
  [76] = 70,
  [77] = 77,
  [78] = 78,
  [79] = 79,
  [80] = 80,
  [81] = 81,
  [82] = 82,
  [83] = 83,
  [84] = 84,
  [85] = 85,
  [86] = 86,
  [87] = 87,
  [88] = 88,
  [89] = 89,
  [90] = 90,
  [91] = 91,
  [92] = 92,
  [93] = 93,
  [94] = 94,
  [95] = 95,
  [96] = 96,
  [97] = 97,
  [98] = 98,
  [99] = 99,
  [100] = 100,
  [101] = 101,
  [102] = 102,
  [103] = 103,
  [104] = 104,
  [105] = 105,
  [106] = 106,
  [107] = 107,
  [108] = 103,
  [109] = 109,
  [110] = 110,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(72);
      ADVANCE_MAP(
        '!', 4,
        '#', 73,
        '%', 111,
        '(', 98,
        ')', 99,
        '*', 109,
        '+', 107,
        ',', 100,
        '-', 108,
        '/', 110,
        ':', 103,
        ';', 81,
        '<', 115,
        '=', 112,
        '>', 114,
        'B', 15,
        'D', 50,
        'E', 38,
        'F', 57,
        'I', 26,
        'P', 62,
        'R', 16,
        'T', 106,
        'U', 45,
        'W', 30,
        '[', 101,
        ']', 104,
      );
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(0);
      if (lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(118);
      END_STATE();
    case 1:
      ADVANCE_MAP(
        '!', 4,
        '#', 73,
        '%', 111,
        '(', 98,
        '*', 109,
        '+', 107,
        '-', 108,
        '/', 110,
        ':', 5,
        ';', 81,
        '<', 115,
        '=', 112,
        '>', 114,
        'D', 50,
        'E', 39,
        'F', 56,
        'I', 25,
        'R', 16,
        'T', 31,
        'W', 30,
        '[', 101,
      );
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(1);
      if (lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(118);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '#', 73,
        '-', 71,
        ':', 102,
        'D', 54,
        'E', 49,
        'F', 56,
        'I', 25,
        'R', 16,
        'T', 51,
        'W', 30,
        '[', 101,
      );
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(119);
      if (lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(118);
      END_STATE();
    case 3:
      if (lookahead == '#') ADVANCE(73);
      if (lookahead == 'T') ADVANCE(105);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(3);
      if (lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(118);
      END_STATE();
    case 4:
      if (lookahead == '=') ADVANCE(113);
      END_STATE();
    case 5:
      if (lookahead == '=') ADVANCE(80);
      END_STATE();
    case 6:
      if (lookahead == 'A') ADVANCE(11);
      if (lookahead == 'P') ADVANCE(18);
      END_STATE();
    case 7:
      if (lookahead == 'A') ADVANCE(44);
      END_STATE();
    case 8:
      if (lookahead == 'A') ADVANCE(65);
      END_STATE();
    case 9:
      if (lookahead == 'C') ADVANCE(24);
      if (lookahead == 'G') ADVANCE(61);
      END_STATE();
    case 10:
      if (lookahead == 'D') ADVANCE(78);
      END_STATE();
    case 11:
      if (lookahead == 'D') ADVANCE(96);
      END_STATE();
    case 12:
      if (lookahead == 'D') ADVANCE(69);
      END_STATE();
    case 13:
      if (lookahead == 'D') ADVANCE(28);
      END_STATE();
    case 14:
      if (lookahead == 'D') ADVANCE(77);
      END_STATE();
    case 15:
      if (lookahead == 'E') ADVANCE(29);
      END_STATE();
    case 16:
      if (lookahead == 'E') ADVANCE(6);
      END_STATE();
    case 17:
      if (lookahead == 'E') ADVANCE(84);
      END_STATE();
    case 18:
      if (lookahead == 'E') ADVANCE(8);
      END_STATE();
    case 19:
      if (lookahead == 'E') ADVANCE(86);
      END_STATE();
    case 20:
      if (lookahead == 'E') ADVANCE(97);
      END_STATE();
    case 21:
      if (lookahead == 'E') ADVANCE(88);
      END_STATE();
    case 22:
      if (lookahead == 'E') ADVANCE(74);
      END_STATE();
    case 23:
      if (lookahead == 'E') ADVANCE(46);
      END_STATE();
    case 24:
      if (lookahead == 'E') ADVANCE(12);
      END_STATE();
    case 25:
      if (lookahead == 'F') ADVANCE(82);
      END_STATE();
    case 26:
      if (lookahead == 'F') ADVANCE(82);
      if (lookahead == 'S') ADVANCE(75);
      END_STATE();
    case 27:
      if (lookahead == 'F') ADVANCE(85);
      END_STATE();
    case 28:
      if (lookahead == 'F') ADVANCE(58);
      if (lookahead == 'I') ADVANCE(27);
      if (lookahead == 'W') ADVANCE(32);
      END_STATE();
    case 29:
      if (lookahead == 'G') ADVANCE(36);
      END_STATE();
    case 30:
      if (lookahead == 'H') ADVANCE(33);
      if (lookahead == 'R') ADVANCE(34);
      END_STATE();
    case 31:
      if (lookahead == 'H') ADVANCE(23);
      END_STATE();
    case 32:
      if (lookahead == 'H') ADVANCE(37);
      END_STATE();
    case 33:
      if (lookahead == 'I') ADVANCE(41);
      END_STATE();
    case 34:
      if (lookahead == 'I') ADVANCE(66);
      END_STATE();
    case 35:
      if (lookahead == 'I') ADVANCE(40);
      END_STATE();
    case 36:
      if (lookahead == 'I') ADVANCE(47);
      END_STATE();
    case 37:
      if (lookahead == 'I') ADVANCE(42);
      END_STATE();
    case 38:
      if (lookahead == 'L') ADVANCE(64);
      if (lookahead == 'N') ADVANCE(10);
      END_STATE();
    case 39:
      if (lookahead == 'L') ADVANCE(64);
      if (lookahead == 'N') ADVANCE(13);
      END_STATE();
    case 40:
      if (lookahead == 'L') ADVANCE(90);
      END_STATE();
    case 41:
      if (lookahead == 'L') ADVANCE(19);
      END_STATE();
    case 42:
      if (lookahead == 'L') ADVANCE(21);
      END_STATE();
    case 43:
      if (lookahead == 'M') ADVANCE(92);
      END_STATE();
    case 44:
      if (lookahead == 'M') ADVANCE(79);
      END_STATE();
    case 45:
      if (lookahead == 'N') ADVANCE(68);
      END_STATE();
    case 46:
      if (lookahead == 'N') ADVANCE(83);
      END_STATE();
    case 47:
      if (lookahead == 'N') ADVANCE(76);
      END_STATE();
    case 48:
      if (lookahead == 'N') ADVANCE(67);
      END_STATE();
    case 49:
      if (lookahead == 'N') ADVANCE(14);
      END_STATE();
    case 50:
      if (lookahead == 'O') ADVANCE(87);
      END_STATE();
    case 51:
      if (lookahead == 'O') ADVANCE(93);
      END_STATE();
    case 52:
      if (lookahead == 'O') ADVANCE(43);
      END_STATE();
    case 53:
      if (lookahead == 'O') ADVANCE(9);
      END_STATE();
    case 54:
      if (lookahead == 'O') ADVANCE(70);
      END_STATE();
    case 55:
      if (lookahead == 'O') ADVANCE(95);
      END_STATE();
    case 56:
      if (lookahead == 'O') ADVANCE(59);
      END_STATE();
    case 57:
      if (lookahead == 'O') ADVANCE(59);
      if (lookahead == 'R') ADVANCE(52);
      END_STATE();
    case 58:
      if (lookahead == 'O') ADVANCE(60);
      END_STATE();
    case 59:
      if (lookahead == 'R') ADVANCE(91);
      END_STATE();
    case 60:
      if (lookahead == 'R') ADVANCE(94);
      END_STATE();
    case 61:
      if (lookahead == 'R') ADVANCE(7);
      END_STATE();
    case 62:
      if (lookahead == 'R') ADVANCE(53);
      END_STATE();
    case 63:
      if (lookahead == 'R') ADVANCE(22);
      END_STATE();
    case 64:
      if (lookahead == 'S') ADVANCE(17);
      END_STATE();
    case 65:
      if (lookahead == 'T') ADVANCE(89);
      END_STATE();
    case 66:
      if (lookahead == 'T') ADVANCE(20);
      END_STATE();
    case 67:
      if (lookahead == 'T') ADVANCE(55);
      END_STATE();
    case 68:
      if (lookahead == 'T') ADVANCE(35);
      END_STATE();
    case 69:
      if (lookahead == 'U') ADVANCE(63);
      END_STATE();
    case 70:
      if (lookahead == 'W') ADVANCE(48);
      END_STATE();
    case 71:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(119);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(73);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(anon_sym_PROCEDURE);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(anon_sym_IS);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(anon_sym_BEGIN);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(anon_sym_END);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(anon_sym_END);
      if (lookahead == 'F') ADVANCE(58);
      if (lookahead == 'I') ADVANCE(27);
      if (lookahead == 'W') ADVANCE(32);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(anon_sym_PROGRAM);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(anon_sym_COLON_EQ);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(anon_sym_SEMI);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(anon_sym_IF);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(anon_sym_THEN);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(anon_sym_ELSE);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(anon_sym_ENDIF);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(anon_sym_WHILE);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(anon_sym_DO);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(anon_sym_ENDWHILE);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(anon_sym_REPEAT);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(anon_sym_UNTIL);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(anon_sym_FOR);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(anon_sym_FROM);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(anon_sym_TO);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(anon_sym_ENDFOR);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(anon_sym_DOWNTO);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(anon_sym_READ);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(anon_sym_WRITE);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(anon_sym_COLON);
      if (lookahead == '=') ADVANCE(80);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(anon_sym_RBRACK);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(anon_sym_T);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(anon_sym_T);
      if (lookahead == 'H') ADVANCE(23);
      if (lookahead == 'O') ADVANCE(93);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(anon_sym_PLUS);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 111:
      ACCEPT_TOKEN(anon_sym_PERCENT);
      END_STATE();
    case 112:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 113:
      ACCEPT_TOKEN(anon_sym_BANG_EQ);
      END_STATE();
    case 114:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(116);
      END_STATE();
    case 115:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(117);
      END_STATE();
    case 116:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 117:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 118:
      ACCEPT_TOKEN(sym_pidentifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(118);
      END_STATE();
    case 119:
      ACCEPT_TOKEN(sym_num);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(119);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 1},
  [3] = {.lex_state = 1},
  [4] = {.lex_state = 1},
  [5] = {.lex_state = 1},
  [6] = {.lex_state = 0},
  [7] = {.lex_state = 0},
  [8] = {.lex_state = 0},
  [9] = {.lex_state = 0},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 1},
  [15] = {.lex_state = 0},
  [16] = {.lex_state = 0},
  [17] = {.lex_state = 0},
  [18] = {.lex_state = 2},
  [19] = {.lex_state = 0},
  [20] = {.lex_state = 2},
  [21] = {.lex_state = 2},
  [22] = {.lex_state = 0},
  [23] = {.lex_state = 0},
  [24] = {.lex_state = 0},
  [25] = {.lex_state = 1},
  [26] = {.lex_state = 0},
  [27] = {.lex_state = 2},
  [28] = {.lex_state = 1},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 1},
  [31] = {.lex_state = 0},
  [32] = {.lex_state = 1},
  [33] = {.lex_state = 2},
  [34] = {.lex_state = 2},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 2},
  [37] = {.lex_state = 2},
  [38] = {.lex_state = 2},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 2},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 2},
  [43] = {.lex_state = 2},
  [44] = {.lex_state = 2},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 2},
  [47] = {.lex_state = 1},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 1},
  [50] = {.lex_state = 3},
  [51] = {.lex_state = 0},
  [52] = {.lex_state = 0},
  [53] = {.lex_state = 0},
  [54] = {.lex_state = 0},
  [55] = {.lex_state = 0},
  [56] = {.lex_state = 0},
  [57] = {.lex_state = 0},
  [58] = {.lex_state = 0},
  [59] = {.lex_state = 0},
  [60] = {.lex_state = 0},
  [61] = {.lex_state = 0},
  [62] = {.lex_state = 0},
  [63] = {.lex_state = 0},
  [64] = {.lex_state = 2},
  [65] = {.lex_state = 0},
  [66] = {.lex_state = 3},
  [67] = {.lex_state = 0},
  [68] = {.lex_state = 0},
  [69] = {.lex_state = 0},
  [70] = {.lex_state = 2},
  [71] = {.lex_state = 0},
  [72] = {.lex_state = 0},
  [73] = {.lex_state = 0},
  [74] = {.lex_state = 2},
  [75] = {.lex_state = 2},
  [76] = {.lex_state = 2},
  [77] = {.lex_state = 2},
  [78] = {.lex_state = 0},
  [79] = {.lex_state = 0},
  [80] = {.lex_state = 1},
  [81] = {.lex_state = 0},
  [82] = {.lex_state = 0},
  [83] = {.lex_state = 0},
  [84] = {.lex_state = 0},
  [85] = {.lex_state = 0},
  [86] = {.lex_state = 0},
  [87] = {.lex_state = 0},
  [88] = {.lex_state = 0},
  [89] = {.lex_state = 0},
  [90] = {.lex_state = 2},
  [91] = {.lex_state = 0},
  [92] = {.lex_state = 0},
  [93] = {.lex_state = 1},
  [94] = {.lex_state = 0},
  [95] = {.lex_state = 0},
  [96] = {.lex_state = 2},
  [97] = {.lex_state = 2},
  [98] = {.lex_state = 0},
  [99] = {.lex_state = 0},
  [100] = {.lex_state = 0},
  [101] = {.lex_state = 0},
  [102] = {.lex_state = 0},
  [103] = {.lex_state = 0},
  [104] = {.lex_state = 0},
  [105] = {.lex_state = 0},
  [106] = {.lex_state = 2},
  [107] = {.lex_state = 0},
  [108] = {.lex_state = 0},
  [109] = {.lex_state = 2},
  [110] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_comment] = ACTIONS(3),
    [anon_sym_PROCEDURE] = ACTIONS(1),
    [anon_sym_IS] = ACTIONS(1),
    [anon_sym_BEGIN] = ACTIONS(1),
    [anon_sym_END] = ACTIONS(1),
    [anon_sym_PROGRAM] = ACTIONS(1),
    [anon_sym_COLON_EQ] = ACTIONS(1),
    [anon_sym_SEMI] = ACTIONS(1),
    [anon_sym_IF] = ACTIONS(1),
    [anon_sym_THEN] = ACTIONS(1),
    [anon_sym_ELSE] = ACTIONS(1),
    [anon_sym_ENDIF] = ACTIONS(1),
    [anon_sym_WHILE] = ACTIONS(1),
    [anon_sym_DO] = ACTIONS(1),
    [anon_sym_ENDWHILE] = ACTIONS(1),
    [anon_sym_REPEAT] = ACTIONS(1),
    [anon_sym_UNTIL] = ACTIONS(1),
    [anon_sym_FOR] = ACTIONS(1),
    [anon_sym_FROM] = ACTIONS(1),
    [anon_sym_TO] = ACTIONS(1),
    [anon_sym_ENDFOR] = ACTIONS(1),
    [anon_sym_READ] = ACTIONS(1),
    [anon_sym_WRITE] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [anon_sym_LBRACK] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [anon_sym_RBRACK] = ACTIONS(1),
    [anon_sym_T] = ACTIONS(1),
    [anon_sym_PLUS] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_SLASH] = ACTIONS(1),
    [anon_sym_PERCENT] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_BANG_EQ] = ACTIONS(1),
    [anon_sym_GT] = ACTIONS(1),
    [anon_sym_LT] = ACTIONS(1),
    [anon_sym_GT_EQ] = ACTIONS(1),
    [anon_sym_LT_EQ] = ACTIONS(1),
    [sym_pidentifier] = ACTIONS(1),
  },
  [1] = {
    [sym_program_all] = STATE(100),
    [sym_procedures] = STATE(54),
    [sym_procedure_def] = STATE(41),
    [sym_main] = STATE(92),
    [aux_sym_procedures_repeat1] = STATE(41),
    [sym_comment] = ACTIONS(3),
    [anon_sym_PROCEDURE] = ACTIONS(5),
    [anon_sym_PROGRAM] = ACTIONS(7),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(11), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(9), 13,
      anon_sym_COLON_EQ,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [23] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(15), 1,
      anon_sym_LBRACK,
    ACTIONS(17), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(13), 12,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [48] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(23), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(21), 5,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
    ACTIONS(19), 7,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [72] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(27), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(25), 12,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [94] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(29), 1,
      anon_sym_END,
    ACTIONS(31), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [115] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(33), 1,
      anon_sym_END,
    ACTIONS(35), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [136] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(37), 1,
      anon_sym_END,
    ACTIONS(39), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [157] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(41), 1,
      anon_sym_END,
    ACTIONS(43), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [178] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(45), 1,
      anon_sym_END,
    ACTIONS(47), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [199] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(49), 1,
      anon_sym_END,
    ACTIONS(51), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [220] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(53), 1,
      anon_sym_END,
    ACTIONS(55), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [241] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(57), 1,
      anon_sym_END,
    ACTIONS(59), 12,
      anon_sym_IF,
      anon_sym_ELSE,
      anon_sym_ENDIF,
      anon_sym_WHILE,
      anon_sym_ENDWHILE,
      anon_sym_REPEAT,
      anon_sym_UNTIL,
      anon_sym_FOR,
      anon_sym_ENDFOR,
      anon_sym_READ,
      anon_sym_WRITE,
      sym_pidentifier,
  [262] = 13,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(63), 1,
      anon_sym_ELSE,
    ACTIONS(65), 1,
      anon_sym_ENDIF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [302] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(18), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [339] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(14), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [376] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(20), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [413] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(79), 1,
      anon_sym_END,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [450] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(25), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [487] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(81), 1,
      anon_sym_END,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [524] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(83), 1,
      anon_sym_END,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [561] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(21), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [598] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(27), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [635] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(31), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [672] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(65), 1,
      anon_sym_ENDWHILE,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [709] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(28), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [746] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(85), 1,
      anon_sym_END,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [783] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(87), 1,
      anon_sym_ENDIF,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [820] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    STATE(7), 1,
      sym_command,
    STATE(30), 1,
      sym_commands,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [857] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(89), 1,
      anon_sym_ENDFOR,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [894] = 12,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(61), 1,
      anon_sym_IF,
    ACTIONS(67), 1,
      anon_sym_WHILE,
    ACTIONS(69), 1,
      anon_sym_REPEAT,
    ACTIONS(71), 1,
      anon_sym_FOR,
    ACTIONS(73), 1,
      anon_sym_READ,
    ACTIONS(75), 1,
      anon_sym_WRITE,
    ACTIONS(77), 1,
      sym_pidentifier,
    ACTIONS(91), 1,
      anon_sym_UNTIL,
    STATE(8), 1,
      sym_command,
    STATE(80), 1,
      sym_identifier,
    STATE(95), 1,
      sym_proc_call,
  [931] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(95), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(93), 7,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [948] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(4), 1,
      sym_value,
    STATE(5), 1,
      sym_identifier,
    STATE(35), 1,
      sym_expression,
    STATE(93), 1,
      sym_condition,
  [970] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(4), 1,
      sym_value,
    STATE(5), 1,
      sym_identifier,
    STATE(35), 1,
      sym_expression,
    STATE(83), 1,
      sym_condition,
  [992] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(103), 2,
      anon_sym_GT,
      anon_sym_LT,
    ACTIONS(101), 4,
      anon_sym_EQ,
      anon_sym_BANG_EQ,
      anon_sym_GT_EQ,
      anon_sym_LT_EQ,
  [1006] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(4), 1,
      sym_value,
    STATE(5), 1,
      sym_identifier,
    STATE(35), 1,
      sym_expression,
    STATE(81), 1,
      sym_condition,
  [1028] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(4), 1,
      sym_value,
    STATE(5), 1,
      sym_identifier,
    STATE(49), 1,
      sym_expression,
  [1047] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(4), 1,
      sym_value,
    STATE(5), 1,
      sym_identifier,
    STATE(105), 1,
      sym_expression,
  [1066] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(105), 1,
      anon_sym_PROCEDURE,
    ACTIONS(108), 1,
      anon_sym_PROGRAM,
    STATE(39), 2,
      sym_procedure_def,
      aux_sym_procedures_repeat1,
  [1080] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(5), 1,
      sym_identifier,
    STATE(79), 1,
      sym_value,
  [1096] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(5), 1,
      anon_sym_PROCEDURE,
    ACTIONS(110), 1,
      anon_sym_PROGRAM,
    STATE(39), 2,
      sym_procedure_def,
      aux_sym_procedures_repeat1,
  [1110] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(5), 1,
      sym_identifier,
    STATE(32), 1,
      sym_value,
  [1126] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(112), 1,
      sym_pidentifier,
    ACTIONS(114), 1,
      sym_num,
    STATE(64), 1,
      sym_value,
    STATE(74), 1,
      sym_identifier,
  [1142] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    ACTIONS(99), 1,
      sym_num,
    STATE(5), 1,
      sym_identifier,
    STATE(98), 1,
      sym_value,
  [1158] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(118), 1,
      anon_sym_LBRACK,
    ACTIONS(116), 2,
      anon_sym_BEGIN,
      anon_sym_COMMA,
  [1169] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(120), 1,
      anon_sym_LBRACK,
    ACTIONS(13), 2,
      anon_sym_TO,
      anon_sym_DOWNTO,
  [1180] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(13), 1,
      anon_sym_COLON_EQ,
    ACTIONS(15), 1,
      anon_sym_LBRACK,
    ACTIONS(122), 1,
      anon_sym_LPAREN,
  [1193] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(124), 1,
      anon_sym_BEGIN,
    ACTIONS(126), 1,
      sym_pidentifier,
    STATE(72), 1,
      sym_declarations,
  [1206] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(128), 3,
      anon_sym_SEMI,
      anon_sym_THEN,
      anon_sym_DO,
  [1215] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(130), 1,
      anon_sym_T,
    ACTIONS(132), 1,
      sym_pidentifier,
    STATE(73), 1,
      sym_args_decl,
  [1228] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(126), 1,
      sym_pidentifier,
    ACTIONS(134), 1,
      anon_sym_BEGIN,
    STATE(55), 1,
      sym_declarations,
  [1241] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(138), 1,
      anon_sym_LBRACK,
    ACTIONS(136), 2,
      anon_sym_BEGIN,
      anon_sym_COMMA,
  [1252] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(140), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1260] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(7), 1,
      anon_sym_PROGRAM,
    STATE(94), 1,
      sym_main,
  [1270] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(142), 1,
      anon_sym_BEGIN,
    ACTIONS(144), 1,
      anon_sym_COMMA,
  [1280] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(146), 1,
      sym_pidentifier,
    STATE(88), 1,
      sym_proc_head,
  [1290] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(148), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1298] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(150), 2,
      anon_sym_PROCEDURE,
      anon_sym_PROGRAM,
  [1306] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(97), 1,
      sym_pidentifier,
    STATE(79), 1,
      sym_identifier,
  [1316] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(152), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1324] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(154), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1332] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(156), 1,
      anon_sym_RPAREN,
    ACTIONS(158), 1,
      anon_sym_COMMA,
  [1342] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(160), 2,
      anon_sym_PROCEDURE,
      anon_sym_PROGRAM,
  [1350] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(162), 2,
      anon_sym_TO,
      anon_sym_DOWNTO,
  [1358] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(164), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1366] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(166), 1,
      anon_sym_T,
    ACTIONS(168), 1,
      sym_pidentifier,
  [1376] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(170), 1,
      sym_pidentifier,
    STATE(62), 1,
      sym_args,
  [1386] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(172), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [1394] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(174), 2,
      anon_sym_BEGIN,
      anon_sym_COMMA,
  [1402] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(176), 2,
      sym_pidentifier,
      sym_num,
  [1410] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(178), 2,
      anon_sym_BEGIN,
      anon_sym_COMMA,
  [1418] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(144), 1,
      anon_sym_COMMA,
    ACTIONS(180), 1,
      anon_sym_BEGIN,
  [1428] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(182), 1,
      anon_sym_RPAREN,
    ACTIONS(184), 1,
      anon_sym_COMMA,
  [1438] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(25), 2,
      anon_sym_TO,
      anon_sym_DOWNTO,
  [1446] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(9), 2,
      anon_sym_TO,
      anon_sym_DOWNTO,
  [1454] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(186), 2,
      sym_pidentifier,
      sym_num,
  [1462] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(188), 1,
      sym_num,
  [1469] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(190), 1,
      sym_pidentifier,
  [1476] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(192), 1,
      anon_sym_SEMI,
  [1483] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(194), 1,
      anon_sym_COLON_EQ,
  [1490] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(196), 1,
      anon_sym_DO,
  [1497] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(198), 1,
      anon_sym_IS,
  [1504] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(65), 1,
      anon_sym_SEMI,
  [1511] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(200), 1,
      sym_pidentifier,
  [1518] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(202), 1,
      anon_sym_SEMI,
  [1525] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(204), 1,
      sym_pidentifier,
  [1532] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(206), 1,
      sym_pidentifier,
  [1539] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(208), 1,
      anon_sym_IS,
  [1546] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(210), 1,
      anon_sym_RBRACK,
  [1553] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(212), 1,
      anon_sym_COLON,
  [1560] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(214), 1,
      anon_sym_IS,
  [1567] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(216), 1,
      ts_builtin_sym_end,
  [1574] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(218), 1,
      anon_sym_THEN,
  [1581] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(220), 1,
      ts_builtin_sym_end,
  [1588] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(222), 1,
      anon_sym_SEMI,
  [1595] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(224), 1,
      sym_num,
  [1602] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(226), 1,
      anon_sym_COLON,
  [1609] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(228), 1,
      anon_sym_DO,
  [1616] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(230), 1,
      anon_sym_RBRACK,
  [1623] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(232), 1,
      ts_builtin_sym_end,
  [1630] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(234), 1,
      ts_builtin_sym_end,
  [1637] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(236), 1,
      anon_sym_LPAREN,
  [1644] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(238), 1,
      anon_sym_RBRACK,
  [1651] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(240), 1,
      sym_pidentifier,
  [1658] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(242), 1,
      anon_sym_SEMI,
  [1665] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(244), 1,
      sym_num,
  [1672] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(246), 1,
      ts_builtin_sym_end,
  [1679] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(248), 1,
      anon_sym_RBRACK,
  [1686] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(250), 1,
      sym_num,
  [1693] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(252), 1,
      anon_sym_FROM,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 23,
  [SMALL_STATE(4)] = 48,
  [SMALL_STATE(5)] = 72,
  [SMALL_STATE(6)] = 94,
  [SMALL_STATE(7)] = 115,
  [SMALL_STATE(8)] = 136,
  [SMALL_STATE(9)] = 157,
  [SMALL_STATE(10)] = 178,
  [SMALL_STATE(11)] = 199,
  [SMALL_STATE(12)] = 220,
  [SMALL_STATE(13)] = 241,
  [SMALL_STATE(14)] = 262,
  [SMALL_STATE(15)] = 302,
  [SMALL_STATE(16)] = 339,
  [SMALL_STATE(17)] = 376,
  [SMALL_STATE(18)] = 413,
  [SMALL_STATE(19)] = 450,
  [SMALL_STATE(20)] = 487,
  [SMALL_STATE(21)] = 524,
  [SMALL_STATE(22)] = 561,
  [SMALL_STATE(23)] = 598,
  [SMALL_STATE(24)] = 635,
  [SMALL_STATE(25)] = 672,
  [SMALL_STATE(26)] = 709,
  [SMALL_STATE(27)] = 746,
  [SMALL_STATE(28)] = 783,
  [SMALL_STATE(29)] = 820,
  [SMALL_STATE(30)] = 857,
  [SMALL_STATE(31)] = 894,
  [SMALL_STATE(32)] = 931,
  [SMALL_STATE(33)] = 948,
  [SMALL_STATE(34)] = 970,
  [SMALL_STATE(35)] = 992,
  [SMALL_STATE(36)] = 1006,
  [SMALL_STATE(37)] = 1028,
  [SMALL_STATE(38)] = 1047,
  [SMALL_STATE(39)] = 1066,
  [SMALL_STATE(40)] = 1080,
  [SMALL_STATE(41)] = 1096,
  [SMALL_STATE(42)] = 1110,
  [SMALL_STATE(43)] = 1126,
  [SMALL_STATE(44)] = 1142,
  [SMALL_STATE(45)] = 1158,
  [SMALL_STATE(46)] = 1169,
  [SMALL_STATE(47)] = 1180,
  [SMALL_STATE(48)] = 1193,
  [SMALL_STATE(49)] = 1206,
  [SMALL_STATE(50)] = 1215,
  [SMALL_STATE(51)] = 1228,
  [SMALL_STATE(52)] = 1241,
  [SMALL_STATE(53)] = 1252,
  [SMALL_STATE(54)] = 1260,
  [SMALL_STATE(55)] = 1270,
  [SMALL_STATE(56)] = 1280,
  [SMALL_STATE(57)] = 1290,
  [SMALL_STATE(58)] = 1298,
  [SMALL_STATE(59)] = 1306,
  [SMALL_STATE(60)] = 1316,
  [SMALL_STATE(61)] = 1324,
  [SMALL_STATE(62)] = 1332,
  [SMALL_STATE(63)] = 1342,
  [SMALL_STATE(64)] = 1350,
  [SMALL_STATE(65)] = 1358,
  [SMALL_STATE(66)] = 1366,
  [SMALL_STATE(67)] = 1376,
  [SMALL_STATE(68)] = 1386,
  [SMALL_STATE(69)] = 1394,
  [SMALL_STATE(70)] = 1402,
  [SMALL_STATE(71)] = 1410,
  [SMALL_STATE(72)] = 1418,
  [SMALL_STATE(73)] = 1428,
  [SMALL_STATE(74)] = 1438,
  [SMALL_STATE(75)] = 1446,
  [SMALL_STATE(76)] = 1454,
  [SMALL_STATE(77)] = 1462,
  [SMALL_STATE(78)] = 1469,
  [SMALL_STATE(79)] = 1476,
  [SMALL_STATE(80)] = 1483,
  [SMALL_STATE(81)] = 1490,
  [SMALL_STATE(82)] = 1497,
  [SMALL_STATE(83)] = 1504,
  [SMALL_STATE(84)] = 1511,
  [SMALL_STATE(85)] = 1518,
  [SMALL_STATE(86)] = 1525,
  [SMALL_STATE(87)] = 1532,
  [SMALL_STATE(88)] = 1539,
  [SMALL_STATE(89)] = 1546,
  [SMALL_STATE(90)] = 1553,
  [SMALL_STATE(91)] = 1560,
  [SMALL_STATE(92)] = 1567,
  [SMALL_STATE(93)] = 1574,
  [SMALL_STATE(94)] = 1581,
  [SMALL_STATE(95)] = 1588,
  [SMALL_STATE(96)] = 1595,
  [SMALL_STATE(97)] = 1602,
  [SMALL_STATE(98)] = 1609,
  [SMALL_STATE(99)] = 1616,
  [SMALL_STATE(100)] = 1623,
  [SMALL_STATE(101)] = 1630,
  [SMALL_STATE(102)] = 1637,
  [SMALL_STATE(103)] = 1644,
  [SMALL_STATE(104)] = 1651,
  [SMALL_STATE(105)] = 1658,
  [SMALL_STATE(106)] = 1665,
  [SMALL_STATE(107)] = 1672,
  [SMALL_STATE(108)] = 1679,
  [SMALL_STATE(109)] = 1686,
  [SMALL_STATE(110)] = 1693,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(56),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(82),
  [9] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 4, 0, 0),
  [11] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_identifier, 4, 0, 0),
  [13] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(70),
  [17] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_identifier, 1, 0, 0),
  [19] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expression, 1, 0, 0),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [23] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_expression, 1, 0, 0),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_value, 1, 0, 0),
  [27] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_value, 1, 0, 0),
  [29] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 9, 0, 0),
  [31] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 9, 0, 0),
  [33] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_commands, 1, 0, 0),
  [35] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_commands, 1, 0, 0),
  [37] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_commands, 2, 0, 0),
  [39] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_commands, 2, 0, 0),
  [41] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 2, 0, 0),
  [43] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 2, 0, 0),
  [45] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 3, 0, 0),
  [47] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 3, 0, 0),
  [49] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 4, 0, 0),
  [51] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 4, 0, 0),
  [53] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 5, 0, 0),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 5, 0, 0),
  [57] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 7, 0, 0),
  [59] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 7, 0, 0),
  [61] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [63] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [67] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [69] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [71] = {.entry = {.count = 1, .reusable = true}}, SHIFT(78),
  [73] = {.entry = {.count = 1, .reusable = true}}, SHIFT(59),
  [75] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [77] = {.entry = {.count = 1, .reusable = true}}, SHIFT(47),
  [79] = {.entry = {.count = 1, .reusable = true}}, SHIFT(58),
  [81] = {.entry = {.count = 1, .reusable = true}}, SHIFT(107),
  [83] = {.entry = {.count = 1, .reusable = true}}, SHIFT(63),
  [85] = {.entry = {.count = 1, .reusable = true}}, SHIFT(101),
  [87] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [89] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [91] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [93] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expression, 3, 0, 0),
  [95] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_expression, 3, 0, 0),
  [97] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [99] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [101] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [103] = {.entry = {.count = 1, .reusable = false}}, SHIFT(37),
  [105] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_procedures_repeat1, 2, 0, 0), SHIFT_REPEAT(56),
  [108] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_procedures_repeat1, 2, 0, 0),
  [110] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_procedures, 1, 0, 0),
  [112] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [114] = {.entry = {.count = 1, .reusable = true}}, SHIFT(74),
  [116] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_declarations, 3, 0, 0),
  [118] = {.entry = {.count = 1, .reusable = true}}, SHIFT(109),
  [120] = {.entry = {.count = 1, .reusable = true}}, SHIFT(76),
  [122] = {.entry = {.count = 1, .reusable = true}}, SHIFT(67),
  [124] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [126] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [128] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition, 3, 0, 0),
  [130] = {.entry = {.count = 1, .reusable = true}}, SHIFT(104),
  [132] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [134] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [136] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_declarations, 1, 0, 0),
  [138] = {.entry = {.count = 1, .reusable = true}}, SHIFT(77),
  [140] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args_decl, 4, 0, 0),
  [142] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [144] = {.entry = {.count = 1, .reusable = true}}, SHIFT(87),
  [146] = {.entry = {.count = 1, .reusable = true}}, SHIFT(102),
  [148] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args_decl, 3, 0, 0),
  [150] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_procedure_def, 6, 0, 0),
  [152] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args_decl, 1, 0, 0),
  [154] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args, 1, 0, 0),
  [156] = {.entry = {.count = 1, .reusable = true}}, SHIFT(85),
  [158] = {.entry = {.count = 1, .reusable = true}}, SHIFT(86),
  [160] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_procedure_def, 7, 0, 0),
  [162] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [164] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args_decl, 2, 0, 0),
  [166] = {.entry = {.count = 1, .reusable = true}}, SHIFT(84),
  [168] = {.entry = {.count = 1, .reusable = true}}, SHIFT(57),
  [170] = {.entry = {.count = 1, .reusable = true}}, SHIFT(61),
  [172] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_args, 3, 0, 0),
  [174] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_declarations, 6, 0, 0),
  [176] = {.entry = {.count = 1, .reusable = true}}, SHIFT(103),
  [178] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_declarations, 8, 0, 0),
  [180] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [182] = {.entry = {.count = 1, .reusable = true}}, SHIFT(91),
  [184] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [186] = {.entry = {.count = 1, .reusable = true}}, SHIFT(108),
  [188] = {.entry = {.count = 1, .reusable = true}}, SHIFT(97),
  [190] = {.entry = {.count = 1, .reusable = true}}, SHIFT(110),
  [192] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [194] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [196] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [198] = {.entry = {.count = 1, .reusable = true}}, SHIFT(48),
  [200] = {.entry = {.count = 1, .reusable = true}}, SHIFT(53),
  [202] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_proc_call, 4, 0, 0),
  [204] = {.entry = {.count = 1, .reusable = true}}, SHIFT(68),
  [206] = {.entry = {.count = 1, .reusable = true}}, SHIFT(45),
  [208] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [210] = {.entry = {.count = 1, .reusable = true}}, SHIFT(69),
  [212] = {.entry = {.count = 1, .reusable = true}}, SHIFT(96),
  [214] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_proc_head, 4, 0, 0),
  [216] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_program_all, 1, 0, 0),
  [218] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [220] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_program_all, 2, 0, 0),
  [222] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [224] = {.entry = {.count = 1, .reusable = true}}, SHIFT(99),
  [226] = {.entry = {.count = 1, .reusable = true}}, SHIFT(106),
  [228] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [230] = {.entry = {.count = 1, .reusable = true}}, SHIFT(71),
  [232] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [234] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_main, 5, 0, 0),
  [236] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [238] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [240] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [242] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [244] = {.entry = {.count = 1, .reusable = true}}, SHIFT(89),
  [246] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_main, 6, 0, 0),
  [248] = {.entry = {.count = 1, .reusable = true}}, SHIFT(75),
  [250] = {.entry = {.count = 1, .reusable = true}}, SHIFT(90),
  [252] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_jftt(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
