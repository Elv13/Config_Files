execute pathogen#infect()
call pathogen#infect('bundle/{}')

" Install plugins
call plug#begin('~/.vim/plugged')
Plug 'airblade/vim-gitgutter'
Plug 'terryma/vim-multiple-cursors/'
call plug#end()
" call :PlugInstall to install

" Need to be done first, before "syntax on"
"set t_Co=256
"set t_AB=^[[48;5;%dm
"set t_AF=^[[38;5;%dm
set notermguicolors

" Indentation
set shiftwidth=4

" Remove trailing spaces on save
autocmd BufWritePre * %s/\s\+$//e

" All the keymap and whatever is available using Lua
lua dofile(os.getenv("HOME").."/.config/nvim/lua/rc.lua")

" Add a Lua callback when the statusline gets updated
function! StatusUpdateCallback(m)
    let func = join(["lua status_update_callback(\"", a:m, "\")"])
    return execute(func, "silent")
endfunction


syntax on
filetype plugin indent on

set rtp+=$HOME/config_files/.vim/bundle/powerline/powerline/bindings/vim/

"let g:airline_section_z = airline#section#create(['windowswap', '⮀%3p%% ', 'linenr', ':%3v'])
set guifont=Ubuntu\ Mono\ derivative\ Powerline\ 13

"let g:airline_theme='kolor'
"let g:airline_powerline_fonts = 1

"let g:Powerline_symbols = "fancy"
"set showtabline=2
"let airline#extensions#tabline#enabled = 1
"let airline#extensions#tabline#formatter = 'unique_tail'

set mouse=a
set cursorline

" Remove the delay when presing escape
" https://www.johnhawthorn.com/2012/09/vi-escape-delays/
set timeoutlen=33 ttimeoutlen=33

nnoremap <silent> <C-S> :if expand("%") == ""<CR>browse confirm w<CR>else<CR>confirm w<CR>endif<CR>
set number

set laststatus=2
set noshowmode

colorscheme elflord

set tabstop=4
set expandtab

" Make search case insensitive
set ignorecase

hi TabLine      ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineFill  ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineSel   ctermfg=White  ctermbg=DarkBlue  cterm=NONE

" Search and replace options
"let EasyGrepSearchCurrentBufferOnly = 1
"let EasyGrepMode = 1
"let EasyGrepIgnoreCase = 0
"let EasyGrepPatternType = "fixed"

" Use relative line number in NORMAL mode
set number relativenumber

augroup numbertoggle
  " Change the line mode
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
  autocmd BufLeave,FocusLost,InsertEnter   * set norelativenumber
augroup END

" https://stackoverflow.com/questions/15561132/run-command-when-vim-enters-visual-mode
"augroup normalmodecolor
  "autocmd InsertEnter * highlight LineNr ctermfg=67 ctermbg=232
  "autocmd InsertLeave * highlight LineNr ctermfg=67 ctermbg=234
  "autocmd CmdlineEnter * highlight LineNr ctermfg=67 ctermbg=52
  "autocmd CmdlineLeave * highlight LineNr ctermfg=67 ctermbg=54
  "autocmd NormalEnter highlight LineNr ctermfg=67 ctermbg=234
"augroup END


" Wrap the cursor at the end of the line
set whichwrap+=<,>,h,l,[,]

set backspace=indent,eol,start

" Map alt+arrow to navigate panes
nnoremap <silent> <M-Right> <c-w>l
nnoremap <silent> <M-Left> <c-w>h
nnoremap <silent> <M-Up> <c-w>k
nnoremap <silent> <M-Down> <c-w>j

" Fix invalid arrow key mapping
"imap Oa <C-Up>
"imap Ob <C-Down>
"imap Oc <C-Right>
"imap Od <C-Left>
"imap "\e[1;5D" <C-Right>
"imap "\e[1;5C" <C-Left>

"imap ^[1;Oa <C-S-Up>
"imap ^[1;Ob <C-S-Down>
"imap ^[1;Oc <C-S-Right>
"imap ^[1;Od <C-S-Left>


imap \e[a <S-Up>
imap \e[b <S-Down>
imap \e[c <S-Right>
imap \e[d <S-Left>

"imap ^H <C-BS>

"map ^[1;0a <C-S-Up>
"map ^[1;0b <C-S-Down>
"map ^[1;0c <C-S-Right>
"map ^[1;0d <C-S-Left>
"imap ^[1;0a <C-S-Up>
"imap ^[1;0b <C-S-Down>
"imap ^[1;0c <C-S-Right>
"imap ^[1;0d <C-S-Left>
"imap ^[36~ <esc>ff


" Visual mode
"vmap <BS>

" Move line up and down
"imap [a <esc>dd2kpi
"imap [b <esc>ddpi
"map [a <esc>dd2kpi
"map [b <esc>ddpi

"imap <C-S-L> <esc>:q

"imap <C-S-Up> <esc><S-v>dk<esc>Pi
"imap <C-S-Left> <esc>:q
"imap <C-S-L> <esc>:q

" Remap F22
"let mapleader = "[36~"
"imap [36~ <esc><C+c><esc><esc><esc>CommandTBuffer<cr>

"imap <F14> <esc>
"imap <F22> <esc><esc>CommandTBuffer<cr>

" Auto completion
"set omnifunc=syntaxcomplete#Complete
"let g:deoplete#sources#clang#libclang_path = "/usr/lib64/llvm/4/lib64/libclang.so"
"let g:deoplete#sources#clang#clang_header = "/usr/lib64/llvm/4/include/clang/"
"let g:deoplete#enable_at_startup = 1


" Color
"highlight LineNr ctermfg=67 ctermbg=233
"highlight Visual cterm=NONE ctermbg=17 ctermfg=None
highlight CursorLineNR cterm=bold ctermbg=234 ctermfg=75

highlight clear CursorLine
highlight CursorLine cterm=bold ctermbg=232 ctermfg=None

":hi Normal ctermbg=Black ctermfg=Black cterm=NONE

function! SearchCount()
  let keyString=@/
  let pos=getpos('.')
  try
    redir => nth
      silent exe '0,.s/' . keyString . '//ne'
    redir => cnt
      silent exe '%s/' . keyString . '//ne'
    redir END
    return matchstr( nth, '\d\+' ) . '/' . matchstr( cnt, '\d\+' )
  finally
    call setpos('.', pos)
  endtry
endfunction

start
