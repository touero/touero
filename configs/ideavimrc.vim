inoremap jk <esc>
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"

nnoremap ; :
nnoremap <expr> ; v:count ? ';' : ':'
nnoremap <Tab> >>
nnoremap <S-Tab> <<
nnoremap <CR> :normal o<CR>
nnoremap <S-Enter> :normal O<CR>

vnoremap <Tab> >gv
vnoremap <S-Tab> <gv

set number
set scrolloff=5
set updatetime=100
set cursorline
set relativenumber
set incsearch
set showmode
set showcmd

map Q gq

Plug 'machakann/vim-highlightedyank'
Plug 'tpope/vim-commentary'
