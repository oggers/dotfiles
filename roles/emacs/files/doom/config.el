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

;; org
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

;; javascript
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
(after! flycheck
  (setq flycheck-python-mypy-executable nil)
  (global-flycheck-mode) ;; Forzar modo global si no viene por defecto
  (map! :map flycheck-mode-map
        "M-n" #'flycheck-next-error
        "M-p" #'flycheck-previous-error))
;;(after! flycheck
;;  (setq flycheck-disabled-checkers '(python-mypy)))

;; require dirvish package first
(use-package! dirvish
  :config
  (dirvish-override-dired-mode))  ; This replaces dired with dirvish transparently

;; tree-sitter
;; (use-package! treesit
;;   :when
;;   (fboundp 'treesit-install-language-grammar) ;; install only if emacs supports treesit (v29+)
;;   :mode
;;   (("\\.tsx\\'" . tsx-ts-mode)
;;    ("\\.js\\'" . typescript-ts-mode)
;;    ("\\.mjs\\'" . typescript-ts-mode)
;;    ("\\.mts\\'" . typescript-ts-mode)
;;    ("\\.cjs\\'" . typescript-ts-mode)
;;    ("\\.ts\\'" . typescript-ts-mode)
;;    ("\\.jsx\\'" . typescript-ts-mode)
;;    ("\\.json\\'" . typescript-ts-mode)
;;    ("\\.Dockerfile\\'" . dockerfile-ts-mode))
;;   :init
;;   ;; The remap must be made in :init so that emacs knows
;;   ;; what to use before loading the actual mode
;;   (dolist (mapping
;;            '((python-mode . python-ts-mode)
;;              (css-mode . css-ts-mode)
;;              (typescript-mode . typescript-ts-mode)
;;              (js-mode . typescript-ts-mode)
;;              (c-mode . c-ts-mode)
;;              (c-or-c++-mode . c-or-c++-ts-mode)
;;              (bash-mode . bash-ts-mode)
;;              (sh-mode . bash-ts-mode)
;;              (sh-base-mode . bash-ts-mode)
;;              (json-mode . json-ts-mode)
;;              (js-json-mode . json-ts-mode)))
;;     (add-to-list 'major-mode-remap-alist mapping))
;;   :config
;;   (defun os/setup-install-grammars ()
;;     "Install Tree-sitter grammars if they are absent."
;;     (interactive)
;;     (dolist (grammar
;;              '((css . ("https://github.com/tree-sitter/tree-sitter-css" "v0.20.0"))
;;                (bash "https://github.com/tree-sitter/tree-sitter-bash")
;;                (html . ("https://github.com/tree-sitter/tree-sitter-html" "v0.20.1"))
;;                (javascript . ("https://github.com/tree-sitter/tree-sitter-javascript" "v0.21.2" "src"))
;;                (json . ("https://github.com/tree-sitter/tree-sitter-json" "v0.20.2"))
;;                (python . ("https://github.com/tree-sitter/tree-sitter-python" "v0.20.4"))
;;                (go . ("https://github.com/tree-sitter/tree-sitter-go" "v0.20.0"))
;;                (markdown "https://github.com/ikatyang/tree-sitter-markdown")
;;                (make "https://github.com/alemuller/tree-sitter-make")
;;                (elisp "https://github.com/Wilfred/tree-sitter-elisp")
;;                (cmake "https://github.com/uyha/tree-sitter-cmake")
;;                (c "https://github.com/tree-sitter/tree-sitter-c")
;;                (cpp "https://github.com/tree-sitter/tree-sitter-cpp")
;;                (toml "https://github.com/tree-sitter/tree-sitter-toml")
;;                (tsx . ("https://github.com/tree-sitter/tree-sitter-typescript" "v0.20.3" "tsx/src"))
;;                (typescript . ("https://github.com/tree-sitter/tree-sitter-typescript" "v0.20.3" "typescript/src"))
;;                (yaml . ("https://github.com/ikatyang/tree-sitter-yaml" "v0.5.0"))
;;                (prisma "https://github.com/victorhqc/tree-sitter-prisma")))
;;       (add-to-list 'treesit-language-source-alist grammar)
;;       ;; only install if it is not available
;;       (unless (treesit-language-available-p (car grammar))
;;         (treesit-install-language-grammar (car grammar)))))
;;   ;; execute grammar setup when loading setup
;;   (os/setup-install-grammars))

;; ;; We use 'after!' to configure lsp-mode when it is already loaded by Doom.
;; (after! lsp-mode
;;   :init
;;   ;; La optimización de plists debe establecerse antes de que lsp inicie completamente
;;   (setq lsp-use-plists t)

;;   :config
;;   ;; Hooks para activar LSP en los modos Tree-sitter
;;   (add-hook! '(tsx-ts-mode-hook
;;                typescript-ts-mode-hook
;;                js-ts-mode-hook)
;;              #'lsp-deferred)

;;   ;; activate completion
;;   (add-hook 'lsp-mode-hook #'lsp-completion-mode)

;;   ;; Integraciones básicas
;;   (add-hook 'lsp-mode-hook #'lsp-enable-which-key-integration)

;;   ;; Configuration variables (using setq! to override defaults)
;;   (setq! lsp-keymap-prefix "C-c l"           ; Prefijo (OJO: Doom usa SPC c / SPC l por defecto)
;;          lsp-completion-provider :none       ; Usamos Corfu
;;          lsp-diagnostics-provider :flycheck
;;          lsp-session-file (locate-user-emacs-file ".lsp-session")
;;          lsp-log-io nil                      ; Rendimiento: mantener nil
;;          lsp-keep-workspace-alive nil
;;          lsp-idle-delay 0.5

;;          ;; Core & Features
;;          lsp-enable-xref t
;;          lsp-auto-configure t
;;          lsp-eldoc-enable-hover t
;;          lsp-enable-dap-auto-configure t
;;          lsp-enable-file-watchers nil        ; Rendimiento
;;          lsp-enable-folding nil              ; Usas origami
;;          lsp-enable-imenu t
;;          lsp-enable-indentation nil          ; Usas prettier
;;          lsp-enable-links nil
;;          lsp-enable-on-type-formatting nil   ; Usas prettier
;;          lsp-enable-suggest-server-download t
;;          lsp-enable-symbol-highlighting t
;;          lsp-enable-text-document-color nil  ; Trabajo de Treesitter

;;          ;; Completion options
;;          lsp-completion-enable t
;;          lsp-completion-enable-additional-text-edit t
;;          lsp-enable-snippet t
;;          lsp-completion-show-kind t

;;          ;; Headerline (Breadcrumbs)
;;          lsp-headerline-breadcrumb-enable t
;;          lsp-headerline-breadcrumb-enable-diagnostics nil
;;          lsp-headerline-breadcrumb-enable-symbol-numbers nil
;;          lsp-headerline-breadcrumb-icons-enable nil

;;          ;; Modeline
;;          lsp-modeline-code-actions-enable nil
;;          lsp-modeline-diagnostics-enable nil
;;          lsp-modeline-workspace-status-enable nil
;;          lsp-signature-doc-lines 1
;;          lsp-eldoc-render-all nil

;;          ;; Lens & Semantic
;;          lsp-lens-enable nil
;;          lsp-semantic-tokens-enable nil))


;; (after! lsp-ui
;;   :config
;;   ;; Configuración de variables visuales
;;   (setq lsp-ui-doc-enable t
;;         lsp-ui-doc-show-with-cursor nil      ; No mostrar doc automáticamente al mover el cursor (distrae)
;;         lsp-ui-doc-include-signature t       ; Mostrar la firma de la función
;;         lsp-ui-doc-position 'at-point)       ; Mostrar en la posición del cursor

;;   ;; Integración con Evil
;;   ;; Esto hace que la tecla 'K' (en modo normal) use lsp-ui-doc-glance
;;   (setq evil-lookup-func #'lsp-ui-doc-glance)

;;   ;; Atajos de teclado
;;   ;; Usamos map! que es la macro de Doom para definir teclas
;;   (map! :map lsp-mode-map
;;         "C-c C-d" #'lsp-ui-doc-glance)

;;   (setq! lsp-ui-sideline-enable t
;;          lsp-ui-sideline-show-diagnostics t
;;          lsp-ui-sideline-show-hover nil
;;          lsp-ui-sideline-diagnostic-max-lines 20
;;          lsp-ui-doc-use-childframe t))


;; set SSH_AUTH_SOCK from keychain if SSH_AUTH_SOCK does not exist or is invalid
(when (or (not (getenv "SSH_AUTH_SOCK"))
          (not (file-exists-p (getenv "SSH_AUTH_SOCK"))))
  (let ((ssh-auth-sock (string-trim
                        (shell-command-to-string
                         "keychain --eval --quiet --agents ssh 2>/dev/null | grep SSH_AUTH_SOCK | sed 's/.*SSH_AUTH_SOCK=\\([^;]*\\).*/\\1/'"))))
    (when (and ssh-auth-sock (file-exists-p ssh-auth-sock))
      (setenv "SSH_AUTH_SOCK" ssh-auth-sock)))
)


;; Hook the LSP server to web-mode (which handles .jsx, .js, etc.)
(add-hook 'web-mode-hook #'lsp)

(after! python
  (setq-hook! 'python-mode-hook flycheck-checker 'lsp))
