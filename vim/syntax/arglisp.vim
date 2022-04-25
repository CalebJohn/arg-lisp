" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if v:version < 600
  syntax clear
elseif exists('b:current_syntax')
  finish
endif


syn keyword arglispKeyword       let be on skipwhite
syn keyword arglispKeyword       fn nextgroup=arglispFunction skipwhite
syn keyword arglispConditional   is lessthan if then else skipwhite
syn keyword arglispMath          multiply by add and subtract from divide skipwhite
syn match   arglispFunction      ":{.*}" contained
syn match   arglispComment       "//.*$"

if v:version >= 508 || !exists('did_nim_syn_inits')
  if v:version <= 508
    let did_nim_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink arglispKeyword Keyword
  HiLink arglispConditional Conditional
  HiLink arglispFunction Function
  HiLink arglispMath Operator
  HiLink arglispComment Comment

endif

let b:current_syntax = 'arglisp'
