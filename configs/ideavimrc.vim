inoremap jk <esc>

nnoremap ; :
nnoremap <expr> ; v:count ? ';' : ':'
nnoremap <Tab> >>
nnoremap <S-Tab> <<
nnoremap <CR> :normal o<CR>
nnoremap <S-Enter> :normal O<CR>
nnoremap <Leader>fi :action GotoFile<CR>
nnoremap <Leader>ff :action FileStructurePopup<CR>

vnoremap <Tab> >gv
vnoremap <S-Tab> <gv

set number
set updatetime=100
set cursorline
set relativenumber
set incsearch
set showmode
set showcmd
set tabstop=4
set noexpandtab
set autoindent
set scrolloff=2
set clipboard+=unnamed
set easymotion

map Q gq
map tt :NERDTreeToggle<CR>

nmap m; <Action>(ShowBookmarks)
nmap m' <Action>(Bookmarks)
nmap 'a <Action>(GotoBookmarkA)
nmap 'b <Action>(GotoBookmarkB)
nmap 'c <Action>(GotoBookmarkC)
nmap 'd <Action>(GotoBookmarkD)
nmap 'e <Action>(GotoBookmarkE)
nmap 'f <Action>(GotoBookmarkF)
nmap 'g <Action>(GotoBookmarkG)
nmap 'h <Action>(GotoBookmarkH)
nmap 'i <Action>(GotoBookmarkI)
nmap 'j <Action>(GotoBookmarkJ)
nmap 'k <Action>(GotoBookmarkK)
nmap 'l <Action>(GotoBookmarkL)
nmap 'm <Action>(GotoBookmarkM)
nmap 'n <Action>(GotoBookmarkN)
nmap 'o <Action>(GotoBookmarkO)
nmap 'p <Action>(GotoBookmarkP)
nmap 'q <Action>(GotoBookmarkQ)
nmap 'r <Action>(GotoBookmarkR)
nmap 's <Action>(GotoBookmarkS)
nmap 't <Action>(GotoBookmarkT)
nmap 'u <Action>(GotoBookmarkU)
nmap 'v <Action>(GotoBookmarkV)
nmap 'w <Action>(GotoBookmarkW)
nmap 'x <Action>(GotoBookmarkX)
nmap 'y <Action>(GotoBookmarkY)
nmap 'z <Action>(GotoBookmarkZ)

Plug 'machakann/vim-highlightedyank'
Plug 'tpope/vim-commentary'
Plug 'preservim/nerdtree'
Plug 'easymotion/vim-easymotion'
