execute pathogen#infect()
call pathogen#infect('bundle/{}')

syntax on
filetype plugin indent on

set rtp+=$HOME/config_files/.vim/bundle/powerline/powerline/bindings/vim/

"let g:Powerline_symbols = "fancy"
set showtabline=2

nnoremap <silent> <C-S> :if expand("%") == ""<CR>browse confirm w<CR>else<CR>confirm w<CR>endif<CR>
set number
set t_Co=256
highlight LineNr ctermfg=grey
set laststatus=2
set noshowmode 

set tabstop=4
set expandtab

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
imap <C-w> <esc>/
map <C-w> <esc>/

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

imap Oa <C-Up>
imap Ob <C-Down>
imap Oc <C-Right>
imap Od <C-Left>

"imap ^[1;Oa <C-S-Up>
"imap ^[1;Ob <C-S-Down>
"imap ^[1;Oc <C-S-Right>
"imap ^[1;Od <C-S-Left>

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

start
