execute pathogen#infect()
call pathogen#infect('bundle/{}')

" Install plugins
call plug#begin('~/.vim/plugged')
Plug 'Shougo/deoplete.nvim'
Plug 'zchee/deoplete-clang'
Plug 'airblade/vim-gitgutter'
call plug#end()
" call :PlugInstall to install

" Need to be done first, before "syntax on"
set t_Co=256
"set termguicolors

" Indentation
set shiftwidth=4

syntax on
filetype plugin indent on

set rtp+=$HOME/config_files/.vim/bundle/powerline/powerline/bindings/vim/

"let g:airline_section_z = airline#section#create(['windowswap', '⮀%3p%% ', 'linenr', ':%3v'])
set guifont=Ubuntu\ Mono\ derivative\ Powerline\ 13

let g:airline_theme='kolor'
let g:airline_powerline_fonts = 1

"let g:Powerline_symbols = "fancy"
"set showtabline=2
let airline#extensions#tabline#enabled = 1
let airline#extensions#tabline#formatter = 'unique_tail'

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

" Git support

let g:gitgutter_sign_added = '┃'
let g:gitgutter_sign_modified = '┃'
let g:gitgutter_sign_removed = '┃'

" Make search case insensitive
set ignorecase

hi TabLine      ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineFill  ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineSel   ctermfg=White  ctermbg=DarkBlue  cterm=NONE

" Search and replace options
let EasyGrepSearchCurrentBufferOnly = 1
let EasyGrepMode = 1
let EasyGrepIgnoreCase = 0
let EasyGrepPatternType = "fixed"

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
"  autocmd InsertEnter * highlight LineNr ctermfg=67 ctermbg=44
"  autocmd InsertLeave * highlight LineNr ctermfg=67 ctermbg=55  
"augroup END
"
" Make Vim insert mode act like Nano to avoid mode switch
"

" map CTRL-E to end-of-line (insert mode)
imap <C-e> <esc>$i<right>
map <C-e> <esc>$i<right>

" map CTRL-A to beginning-of-line (insert mode)
imap <C-a> <esc>0i
map <C-a> <esc>0i

" CTRL-U to paste (insert mode)
imap <C-u> <esc>P
map <C-u> <esc>P

" CTRL+O to save (insert mode)
imap <C-o> <esc>:w<CR>li
map <C-o> <esc>:w<CR>li

" CTRL+W to search (insert mode)
imap <C-w> <esc>?
map <C-w> <esc>?

" CTRL+G goto line (insert mode)
imap <C-g> <esc>:
map <C-g> <esc>:

" CTRL+X to save and quit (insert mode)
imap <C-x> <esc>:confirm quit<CR>
map <C-x> <esc>:confirm quit<CR>

" map CTRL+K and CTRL+U to act like nano (insert mode)
imap <C-k> <esc><S-v>di
map <C-k> <esc><S-v>di

imap <C-u> <esc>Pi
map <C-u> <esc>Pi

" map CTRL+R to search and replace
imap <C-r> <esc>:ReplacePrompt<cr>
map <C-r> <esc>:ReplacePrompt<cr>

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


map ^[1;0a <C-S-Up>
map ^[1;0b <C-S-Down>
map ^[1;0c <C-S-Right>
map ^[1;0d <C-S-Left>
imap ^[1;0a <C-S-Up>
imap ^[1;0b <C-S-Down>
imap ^[1;0c <C-S-Right>
imap ^[1;0d <C-S-Left>

" Move line up and down
"noremap <ESC>[[a <C-S-Left>
"noremap! <ESC>[[a <C-S-Left>
"noremap <ESC>[[b <C-S-Right>
"noremap! <ESC>[[b <C-S-Right>

"imap <C-S-M> <esc>:m -2<ENTER>i
"imap <C-S-B> <esc>:m +1<ENTER>i

"noremap <C-S-Up> <esc>:m -2<ENTER>i
"noremap <C-S-Down> <esc>:m +1<ENTER>i

imap <C-S-Up> <esc>:m -2<ENTER>i
imap <C-S-Down> <esc>:m +1<ENTER>i
map <C-S-Up> <esc>:m -2<ENTER>i
map <C-S-Down> <esc>:m +1<ENTER>i

imap <C-S-Up> <esc>:m -2<ENTER>i
imap ^[1;Ob <esc>:m +1<ENTER>i

" Select chars when Shift is pressed
map <S-Right> vl
imap <S-Right> <esc>vl
map <S-Up> vk
imap <S-Up> <esc>vk
map <S-Down> vj
imap <S-Down> <esc>vj
map <S-Left> vj
imap <S-Left> <esc>vj

vmap <S-Up> <Up>
vmap <S-Down> <Down>

" Select next word
map <C-S-Right> vw
imap <C-S-Right> <esc>vw
map <C-S-Left> v<C-Left>
imap <C-S-Left> <esc>v<C-Left>

vmap <C-S-Left> <C-Left>
vmap <C-S-Right> <C-Right>

" Easy buffer switch
map <C-T> :bnext<CR>
map <C-S-T> :bprev<CR>
imap <C-T> :bnext<CR>i
imap <C-S-T> :bprev<CR>i

" Move line up and down
imap [a <esc>dd2kpi
imap [b <esc>ddpi
map [a <esc>dd2kpi
map [b <esc>ddpi

"imap <C-S-L> <esc>:q

"imap <C-S-Up> <esc><S-v>dk<esc>Pi
imap <C-S-Left> <esc>:q
imap <C-S-L> <esc>:q

" Remap F22
"let mapleader = "[36~"
"imap [36~ <esc><C+c><esc><esc><esc>CommandTBuffer<cr>

imap <F22> <esc><esc>CommandTBuffer<cr>

" Auto completion
set omnifunc=syntaxcomplete#Complete
"let g:deoplete#sources#clang#libclang_path = "/usr/lib64/llvm/4/lib64/libclang.so"
"let g:deoplete#sources#clang#clang_header = "/usr/lib64/llvm/4/include/clang/"
"let g:deoplete#enable_at_startup = 1


" Color
highlight LineNr ctermfg=67 ctermbg=232
highlight Visual cterm=NONE ctermbg=17 ctermfg=None
highlight CursorLineNR cterm=bold ctermbg=234 ctermfg=75

highlight clear CursorLine
highlight CursorLine cterm=bold ctermbg=232 ctermfg=None

start
