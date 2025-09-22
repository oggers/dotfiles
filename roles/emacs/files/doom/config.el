;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "Juan Carlos Coruña"
      user-mail-address "oggers@gmail.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom. Here
;; are the three important ones:
;;
;; + `doom-font'
;; + `doom-variable-pitch-font'
;; + `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;;
;; They all accept either a font-spec, font string ("Input Mono-12"), or xlfd
;; font string. You generally only need these two:
;; (setq doom-font (font-spec :family "monospace" :size 12 :weight 'semi-light)
;;       doom-variable-pitch-font (font-spec :family "sans" :size 13))

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-one)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type t)


;; Here are some additional functions/macros that could help you configure Doom:
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.

;; temporal fix https://www.reddit.com/r/DoomEmacs/comments/kts81q/spacemacslike_menu_when_pressing_leader_key/
;;(remove-hook 'doom-first-input-hook #'better-jumper-mode)

;; Using separate file for customization changes
(setq-default custom-file (expand-file-name ".custom.el" doom-private-dir))
(when (file-exists-p custom-file)
  (load custom-file))

;; Modify evil-escape
(setq-default evil-escape-key-sequence "df")
(setq-default evil-escape-unordered-key-sequence 't)

;; Language
(setq current-language-environment "Spanish")
(setq org-export-default-language "es")

(after! org
    (setq org-hide-leading-stars t)
    (setq org-ellipsis " \u2026")
    ;; (setq org-ellipsis " \u25bc")

    (when (file-exists-p "~/org")
      (load-file "~/org/setup/my-org-mode.el"))
)

(use-package! org-modern
  :hook (org-mode . global-org-modern-mode)
  :config
  (setq org-modern-label-border 0.3))

(after! org-modern
  (setq org-modern-todo-faces
        (quote (("PENDIENTE" :background "red" :foreground "white")
                ("SIGUIENTE" :background "green" :foreground "black")
                ("ESPERANDO" :background "yellow" :foreground "black"))))
  )

(after! org-roam
  (require 'org-roam-protocol)
  (setq org-roam-directory "~/org-roam")
  (setq org-roam-db-location "~/org-roam/org-roam.db")
)

(use-package! org-auto-tangle
  :defer t
  :hook (org-mode . org-auto-tangle-mode)
  :config
  (setq org-auto-tangle-default t))

(setq-default js-indent-level 2)
(setq-default typescript-indent-level 2)

;; keychain ssh-agent for emacs server
(keychain-refresh-environment)

;; enable beacon
(beacon-mode 1)

;; dired
(setq delete-by-moving-to-trash t
      trash-directory "~/.local/share/Trash/files/")

;; plantuml
(after! plantuml
        (setq plantuml-default-exec-mode 'jar)
        ;; (if
        ;;     (and (display-graphic-p)
        ;;          (not (file-exists-p plantuml-jar-path)))
        ;;     (plantuml-download-jar))
        )

;; lsp-angular
(after! lsp-angular
  (setq lsp-clients-angular-node-get-prefix-command "npm config get --location=global prefix"))

;; add Zope PageTemplates to mhtml mode
(add-to-list 'auto-mode-alist '("\\.pt\\'" . mhtml-mode))

(unless (member "Symbols Nerd Font Mono" (font-family-list))
  (nerd-icons-install-fonts t))

;; Use flycheck with ruff
(use-package! flycheck
  :config
  (setq flycheck-python-ruff-executable "ruff"))
;; Set ruff as the primary linter
(setq-hook! 'python-mode-hook
  flycheck-checker 'python-ruff)
;; disable mypy in flycheck
;; (after! flycheck
;;   (setq flycheck-python-mypy-executable nil))
(after! flycheck
  (setq flycheck-disabled-checkers '(python-mypy)))

;; Set SSH_AUTH_SOCK from keychain
(let ((ssh-auth-sock (string-trim
                      (shell-command-to-string
                       "keychain --eval --quiet --agents ssh 2>/dev/null | grep SSH_AUTH_SOCK | sed 's/.*SSH_AUTH_SOCK=\\([^;]*\\).*/\\1/'"))))
  (when (and ssh-auth-sock (file-exists-p ssh-auth-sock))
    (setenv "SSH_AUTH_SOCK" ssh-auth-sock)))
