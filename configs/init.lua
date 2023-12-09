vim.api.nvim_set_keymap('i', 'jk', '<Esc>', { noremap = true, silent = true })

vim.api.nvim_set_keymap('i', '<TAB>', "pumvisible() ? coc.pum.next(1) : CheckBackspace() ? '<Tab>' : coc.refresh()", { expr = true, silent = true })
vim.api.nvim_set_keymap('i', '<S-TAB>', "pumvisible() ? coc.pum.prev(1) : '<C-h>'", { expr = true, silent = true })

vim.api.nvim_set_keymap('n', ';', '<expr> v:count ? ";" : ":"', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<Tab>', '>>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<S-Tab>', '<<', { noremap = true, silent = true })

vim.api.nvim_set_keymap('x', '<Tab>', '>gc', { noremap = true, silent = true })
vim.api.nvim_set_keymap('x', '<S-Tab>', '<gv', { noremap = true, silent = true })

vim.api.nvim_set_keymap('', '<C-e>', ':NERDTreeToggle<CR>', { noremap = true, silent = true })

vim.o.updatetime = 100
vim.wo.signcolumn = 'yes'
vim.wo.relativenumber = true
vim.o.autoindent = true
vim.wo.cursorline = true
vim.o.clipboard = 'unnamed'

local packer_exists = pcall(vim.cmd, [[packadd packer.nvim]])

if not packer_exists then
    local install_path = vim.fn.stdpath('data')..'/site/pack/packer/opt/packer.nvim'
    vim.fn.system({'git', 'clone', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd('packadd packer.nvim')
end

require('packer').startup(function()
    use 'morhetz/gruvbox'
    use 'scrooloose/nerdtree'
    use {'neoclide/coc.nvim', branch = 'release'}
    use 'airblade/vim-gitgutter'
    use 'jiangmiao/auto-pairs'
end)

vim.g.gitgutter_enabled = 1
vim.g.gitgutter_terminal_reports_focus = 0

vim.g.AutoPairs = {['('] = ')', ['['] = ']', ['{'] = '}', ["'"] = "'", ['"'] = '"'}

vim.cmd('autocmd vimenter * nested colorscheme gruvbox')
