if has("nvim") && exists("g:neovide")
    let g:neovide_remember_window_size = v:true
    let g:neovide_cursor_antialiasing = v:true 
	let g:transparency = 0.8
	let g:neovide_background_color = '#0f1117'.printf('%x', float2nr(255 * g:transparency))
	let g:neovide_cursor_animation_length = 0.1
	let g:neovide_cursor_trail_size = 0.7
	let g:neovide_cursor_vfx_mode = "torpedo"
	let g:neovide_cursor_animate_in_insert_mode = v:true
	let g:neovide_cursor_animate_command_line = v:true
	let g:neovide_cursor_antialiasing = v:true
	let g:neovide_cursor_vfx_opacity = 10.0
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
set scrolloff=4
" set mouse=a

call plug#begin()
Plug 'morhetz/gruvbox'
Plug 'scrooloose/nerdtree'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'airblade/vim-gitgutter'
Plug 'jiangmiao/auto-pairs'
call plug#end()

let g:NERDTreeShowHidden=1
let g:gitgutter_enabled = 1
let g:gitgutter_terminal_reports_focus = 0
let g:AutoPairs = {'(':')', '[':']', '{':'}',"'":"'",'"':'"'}

autocmd FocusGained,BufEnter * checktime
autocmd vimenter * nested colorscheme gruvbox
