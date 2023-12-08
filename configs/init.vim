inoremap jk <Esc>
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()

nnoremap ; :
nnoremap <expr> ; v:count ? ';' : ':'
nnoremap <Tab> >>
nnoremap <S-Tab> <<

vnoremap <Tab> >gv
vnoremap <S-Tab> <gv

map <C-e> :NERDTreeToggle<CR>


set updatetime=100
set signcolumn=yes
set relativenumber
set autoindent
set cursorline


call plug#begin()
Plug 'morhetz/gruvbox'
Plug 'scrooloose/nerdtree'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'airblade/vim-gitgutter'
call plug#end()


let g:gitgutter_enabled = 1
let g:gitgutter_terminal_reports_focus = 0


autocmd vimenter * nested colorscheme gruvbox
