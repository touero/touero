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
set updatetime=500
set cursorline
set relativenumber
set incsearch
set showmode
set showcmd
set tabstop=4
set softtabstop=4
set shiftwidth=4
set noexpandtab
set autoindent
set scrolloff=4
set clipboard=unnamedplus

map Q gq
map tt :NERDTreeToggle<CR>


Plug 'machakann/vim-highlightedyank'
Plug 'tpope/vim-commentary'
Plug 'preservim/nerdtree'
