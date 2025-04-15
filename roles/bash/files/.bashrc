#
# ~/.bashrc
#
# ansible_managed

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

alias e="emacsclient -t -a ''"  # ansible_managed

# ANSIBLE MANAGED BLOCK - emacs keychain"
# keychain keeps track of ssh-agents
[ -f $HOME/.keychain/$HOSTNAME-sh ] \
    && . $HOME/.keychain/$HOSTNAME-sh

# ANSIBLE MANAGED BLOCK - emacs EDITOR"
export EDITOR="e"  # ansible_managed
export VISUAL="$EDITOR"  # ansible_managed

eval "$(starship init bash)"
