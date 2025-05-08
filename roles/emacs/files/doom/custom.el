(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(magit-todos-insert-after '(bottom) nil nil "Changed by setter of obsolete option `magit-todos-insert-at'")
 '(safe-local-variable-values
   '((eval setq ansible::vault-password-file
      (expand-file-name "~/.vault_pass_oggers.txt"))
     (eval let
      ((home-path
        (getenv "HOME")))
      (setq lsp-dart-sdk-dir
            (concat home-path "/.flutter_development/flutter/bin/cache/dart-sdk"))
      (setq lsp-dart-flutter-sdk-dir
            (concat home-path "/.flutter_development/flutter"))
      (setq flutter-sdk-path
            (concat home-path "/.flutter_development/flutter")))
     (eval let
      ((home-path
        (getenv "HOME")))
      (setq lsp-dart-sdk-dir
            (concat home-path "/snap/flutter/common/flutter/bin/cache/dart-sdk"))
      (setq lsp-dart-flutter-sdk-dir
            (concat home-path "/snap/flutter/common/flutter"))
      (setq flutter-sdk-path
            (concat home-path "/snap/flutter/common/flutter")))
     (eval let
      ((home-path
        (getenv "HOME")))
      (setq lsp-dart-sdk-dir
            (concat home-path "/snap/flutter/common/flutter/bin/cache/dart-sdk"))
      (setq lsp-dart-flutter-sdk-dir
            (concat home-path "/snap/flutter/common/flutter")))
     (eval setq ansible::vault-password-file
      (expand-file-name "~/.vault_pass_ansible.txt")))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
