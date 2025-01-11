// grammar.js
module.exports = grammar({
  name: 'jftt',

  extras: $ => [
      /\s/,         // whitespace
      $.comment     // comments are 'extra' tokens that can appear anywhere
  ],
  
  rules: {
      program_all: $ => seq(
          optional($.procedures),
          $.main
      ),

      comment: $ => /\#[^\n]*/,

      procedures: $ => repeat1($.procedure_def),

      procedure_def: $ => choice(
          seq(
              'PROCEDURE',
              $.proc_head,
              'IS',
              $.declarations,
              'BEGIN',
              $.commands,
              'END'
          ),
          seq(
              'PROCEDURE',
              $.proc_head,
              'IS',
              'BEGIN',
              $.commands,
              'END'
          )
      ),

      main: $ => choice(
          seq(
              'PROGRAM',
              'IS',
              $.declarations,
              'BEGIN',
              $.commands,
              'END'
          ),
          seq(
              'PROGRAM',
              'IS',
              'BEGIN',
              $.commands,
              'END'
          )
      ),

      commands: $ => choice(
          seq($.commands, $.command),
          $.command
      ),

      command: $ => choice(
          seq($.identifier, ':=', $.expression, ';'),
          seq('IF', $.condition, 'THEN', $.commands, 'ELSE', $.commands, 'ENDIF'),
          seq('IF', $.condition, 'THEN', $.commands, 'ENDIF'),
          seq('WHILE', $.condition, 'DO', $.commands, 'ENDWHILE'),
          seq('REPEAT', $.commands, 'UNTIL', $.condition, ';'),
          seq('FOR', $.pidentifier, 'FROM', $.value, 'TO', $.value, 'DO', $.commands, 'ENDFOR'),
          seq('FOR', $.pidentifier, 'FROM', $.value, 'DOWNTO', $.value, 'DO', $.commands, 'ENDFOR'),
          seq($.proc_call, ';'),
          seq('READ', $.identifier, ';'),
          seq('WRITE', $.value, ';')
      ),

      proc_head: $ => seq(
          $.pidentifier,
          '(',
          $.args_decl,
          ')'
      ),

      proc_call: $ => seq(
          $.pidentifier,
          '(',
          $.args,
          ')'
      ),

      declarations: $ => choice(
          seq($.declarations, ',', $.pidentifier),
          seq($.declarations, ',', $.pidentifier, '[', $.num, ':', $.num, ']'),
          $.pidentifier,
          seq($.pidentifier, '[', $.num, ':', $.num, ']')
      ),

      args_decl: $ => choice(
          seq($.args_decl, ',', $.pidentifier),
          seq($.args_decl, ',', 'T', $.pidentifier),
          $.pidentifier,
          seq('T', $.pidentifier)
      ),

      args: $ => choice(
          seq($.args, ',', $.pidentifier),
          $.pidentifier
      ),

      expression: $ => choice(
        $.value,
        seq($.value, '+', $.value),
        seq($.value, '-', $.value),
        seq($.value, '*', $.value),
        seq($.value, '/', $.value),
        seq($.value, '%', $.value)
    ),
    
    value: $ => choice(
        $.num,
        $.identifier
    ),
    
    identifier: $ => choice(
        $.pidentifier,
        seq($.pidentifier, '[', $.pidentifier, ']'),
        seq($.pidentifier, '[', $.num, ']')
    ),

      condition: $ => choice(
          seq($.expression, '=', $.expression),
          seq($.expression, '!=', $.expression),
          seq($.expression, '>', $.expression),
          seq($.expression, '<', $.expression),
          seq($.expression, '>=', $.expression),
          seq($.expression, '<=', $.expression)
      ),

      value: $ => choice(
          $.num,
          $.identifier
      ),

      identifier: $ => choice(
          $.pidentifier,
          seq($.pidentifier, '[', $.pidentifier, ']'),
          seq($.pidentifier, '[', $.num, ']')
      ),

      // Terminal tokens
      pidentifier: $ => /[_a-z][_a-z0-9]*/,
      num: $ => /-?[0-9]+/  // Added support for negative numbers
  }
});