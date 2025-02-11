(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(safe-local-variable-values
   '((eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq python-shell-virtualenv-path
       (concat
        (if
            (stringp local-path)
            (file-name-directory local-path)
          (car local-path))
        "../../../Python-2.7")))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setenv "PYTHONPATH"
              (shell-command-to-string
               (concat
                (concat
                 (if
                     (stringp local-path)
                     (file-name-directory local-path)
                   (car local-path))
                 "../../bin/zopepy")
                " -c \"import sys; print ':'.join(sys.path)\""))))
     (eval setq python-shell-interpreter "python2")
     (eval let
      ((local-path
        (dir-locals-find-file "."))
       (path
        (if
            (stringp local-path)
            (file-name-directory local-path)
          (car local-path))))
      (setq python-shell-virtualenv-path
            (concat path "../../..")))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setenv "PYTHONPATH"
              (shell-command-to-string
               (concat
                (concat
                 (if
                     (stringp local-path)
                     (file-name-directory local-path)
                   (car local-path))
                 "../../../bin/zopepy")
                " -c \"import sys; print ':'.join(sys.path)\""))))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq flycheck-python-flake8-executable
            (concat
             (if
                 (stringp local-path)
                 (file-name-directory local-path)
               (car local-path))
             "../../bin/flake8")))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq python-shell-interpreter
            (concat
             (if
                 (stringp local-path)
                 (file-name-directory local-path)
               (car local-path))
             "../../bin/zopepy")))
     (eval setq ansible-vault-password-file
      (expand-file-name "~/.vault_pass_bizak.txt"))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq-local flycheck-python-flake8-executable
                  (concat
                   (if
                       (stringp local-path)
                       (file-name-directory local-path)
                     (car local-path))
                   "../../bin/flake8")))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq-local python-shell-interpreter
                  (concat
                   (if
                       (stringp local-path)
                       (file-name-directory local-path)
                     (car local-path))
                   "../../bin/zopepy")))
     (eval let
      ((local-path
        (dir-locals-find-file ".")))
      (setq-local lsp-python-ms-extra-paths
                  (vconcat
                   []
                   (split-string
                    (shell-command-to-string
                     (concat
                      (if
                          (stringp local-path)
                          (file-name-directory local-path)
                        (car local-path))
                      "../../bin/zopepy -c \"import sys; sys.stdout.write(';'.join(sys.path))\""))
                    ";"))))
     (eval setq ansible::vault-password-file
      (expand-file-name "~/.vault_pass_ansible.txt"))
     (eval let
      ((home-path
        (getenv "HOME")))
      (setq lsp-dart-sdk-dir
            (concat home-path "/.flutter_development/flutter/bin/cache/dart-sdk"))
      (setq lsp-dart-flutter-sdk-dir
            (concat home-path "/.flutter_development/flutter"))
      (setq flutter-sdk-path
            (concat home-path "/.flutter_development/flutter"))))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
