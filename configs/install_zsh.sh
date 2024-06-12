# !/bin/bash
# author: weiensong
# email: touer0018@gmail.com
# date: 2023.10.27

sudo apt update && sudo apt upgrade

sudo apt install zsh -y

wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/plugins/zsh-syntax-highlighting &&
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/plugins/zsh-autosuggestions &&
git clone https://github.com/hlissner/zsh-autopair ~/.oh-my-zsh/plugins/zsh-autopair &&
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting fzf zsh-autopair tmux ag fd zsh-interactive-cd)/g' ~/.zshrc

chsh -s /bin/zsh

git config --global user.name "touero"
git config --global user.email "touer0018@gmail.com"
