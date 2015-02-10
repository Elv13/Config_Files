execute pathogen#infect()
call pathogen#incubate()
syntax on
filetype plugin indent on

let g:Powerline_symbols = "fancy"
set showtabline=2

nnoremap <silent> <C-S> :if expand("%") == ""<CR>browse confirm w<CR>else<CR>confirm w<CR>endif<CR>
set number
set t_Co=256
highlight LineNr ctermfg=grey
set rtp+=~/.vim/bundle/powerline/powerline/bindings/vim
set laststatus=2

hi TabLine      ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineFill  ctermfg=Black  ctermbg=Gray     cterm=NONE
hi TabLineSel   ctermfg=White  ctermbg=DarkBlue  cterm=NONE

"
" Make Vim insert mode act like Nano to avoid mode switch
"

" map CTRL-E to end-of-line (insert mode)
imap <C-e> <esc>$i<right>

" map CTRL-A to beginning-of-line (insert mode)
imap <C-a> <esc>0i

" CTRL-U to paste (insert mode)
imap <C-u> <esc>P

" CTRL+O to save (insert mode)
imap <C-o> <esc>:w<CR>i

" CTRL+W to search (insert mode)
imap <C-w> <esc>/

" CTRL+G goto line (insert mode)
imap <C-g> <esc>:

" CTRL+X to save and quit (insert mode)
imap <C-x> <esc>:confirm quit<CR>
map <C-x> <esc>:confirm quit<CR>

start
