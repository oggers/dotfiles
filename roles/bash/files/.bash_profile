#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

# ANSIBLE MANAGED BLOCK - emacs keychain"
# https://stackoverflow.com/questions/42136745/using-an-ssh-agent-from-emacs-in-server-mode
# keychain manages ssh-agents
type keychain >&/dev/null \
    && keychain --agents ssh

