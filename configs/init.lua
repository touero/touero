if vim.fn.has("nvim") and vim.fn.exists("g:neovide") then
    vim.g.neovide_remember_window_size = true
    vim.g.neovide_cursor_antialiasing = true
    vim.g.transparency = 0.8
    vim.g.neovide_background_color = string.format('#0f1117%x', vim.fn.float2nr(255 * vim.g.transparency))
    vim.g.neovide_cursor_animation_length = 0.1
    vim.g.neovide_cursor_trail_size = 0.7
    vim.g.neovide_cursor_vfx_mode = "torpedo"
    vim.g.neovide_cursor_animate_in_insert_mode = true
    vim.g.neovide_cursor_animate_command_line = true
    vim.g.neovide_cursor_antialiasing = true
    vim.g.neovide_cursor_vfx_opacity = 10.0
end

vim.api.nvim_set_keymap('i', 'jk', '<Esc>', {})
vim.api.nvim_set_keymap('i', 'jkf', '<Esc>:wq<CR>', { silent = true })

vim.api.nvim_set_keymap('i', '<TAB>', 'coc#pum#visible() ? coc#pum#next(1) : CheckBackspace() ? "\<Tab>" : coc#refresh()', { expr = true, silent = true })
vim.api.nvim_set_keymap('i', '<S-TAB>', 'coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"', { expr = true })

vim.api.nvim_set_keymap('i', '<CR>', 'pumvisible() ? "\<C-y>" : "\<CR>"', { expr = true })

vim.api.nvim_set_keymap('n', ';', ':', {})
vim.api.nvim_set_keymap('x', ';', ':', { expr = true })
vim.api.nvim_set_keymap('n', '<Tab>', '>>', {})
vim.api.nvim_set_keymap('n', '<S-Tab>', '<<', {})
vim.api.nvim_set_keymap('n', '<CR>', ':normal o<CR>', {})
vim.api.nvim_set_keymap('n', '<S-Enter>', ':normal O<CR>', {})

vim.api.nvim_set_keymap('v', '<Tab>', '>gc', {})
vim.api.nvim_set_keymap('v', '<S-Tab>', '<gv', {})

vim.api.nvim_set_keymap('n', 'tt', ':NERDTreeToggle<CR>', {})

vim.o.updatetime = 100
vim.o.signcolumn = 'yes'
vim.o.relativenumber = true
vim.o.tabstop = 4
vim.o.softtabstop = 4
vim.o.shiftwidth = 4
vim.o.expandtab = false
vim.o.autoindent = true
vim.o.cursorline = true
vim.o.clipboard = 'unnamed'
vim.o.scrolloff = 4

vim.cmd([[call plug#begin()]])
vim.cmd([[Plug 'morhetz/gruvbox']])
vim.cmd([[Plug 'scrooloose/nerdtree']])
vim.cmd([[Plug 'neoclide/coc.nvim', {'branch': 'release'}]])
vim.cmd([[Plug 'airblade/vim-gitgutter']])
vim.cmd([[Plug 'jiangmiao/auto-pairs']])
vim.cmd([[call plug#end()]])

vim.g.NERDTreeShowHidden = 1
vim.g.gitgutter_enabled = 1
vim.g.gitgutter_terminal_reports_focus = 0
vim.g.AutoPairs = {['('] = ')', ['['] = ']', ['{'] = '}', ["'"] = "'", ['"'] = '"'}

vim.cmd([[autocmd FocusGained,BufEnter * checktime]])
vim.cmd([[autocmd vimenter * nested colorscheme gruvbox]])
