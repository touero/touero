if has("nvim") && exists("g:neovide")
    let g:neovide_remember_window_size = 1
    let g:neovide_cursor_antialiasing = 1
    let g:neovide_transparency = 0.0
    let g:transparency = 0.8
    set guifont=Monaco:h18
    let g:neovide_background_color = '#0f1117'.printf('%x', float2nr(255 * g:transparency))
endif

inoremap jk <Esc>
inoremap jkf <Esc>:wq<CR>
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"
inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<CR>"

nnoremap ; :
nnoremap <expr> ; v:count ? ';' : ':'
nnoremap <Tab> >>
nnoremap <S-Tab> <<
nnoremap <CR> :normal o<CR>
nnoremap <S-Enter> :normal O<CR>

vnoremap <Tab> >gc
vnoremap <S-Tab> <gv

map tt :NERDTreeToggle<CR>

set updatetime=100
set signcolumn=yes
set relativenumber
set tabstop=4
set softtabstop=4
set shiftwidth=4
set noexpandtab
set autoindent
set cursorline
set clipboard=unnamed

call plug#begin()
Plug 'morhetz/gruvbox'
Plug 'scrooloose/nerdtree'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'airblade/vim-gitgutter'
Plug 'jiangmiao/auto-pairs'
call plug#end()

let g:gitgutter_enabled = 1
let g:gitgutter_terminal_reports_focus = 0
let g:AutoPairs = {'(':')', '[':']', '{':'}',"'":"'",'"':'"'}

autocmd vimenter * nested colorscheme gruvbox
