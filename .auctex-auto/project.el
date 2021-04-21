(TeX-add-style-hook
 "project"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "top=1in" "bottom=1.25in" "left=1.25in" "right=1.25in") ("embedall" "main" "include") ("tcolorbox" "many")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "geometry"
    "embedall"
    "fvextra"
    "tcolorbox")
   (TeX-add-symbols
    '("EFrdix" 1)
    '("EFrdiix" 1)
    '("EFrdvii" 1)
    '("EFrdvi" 1)
    '("EFrdv" 1)
    '("EFrdiv" 1)
    '("EFrdiii" 1)
    '("EFrdii" 1)
    '("EFrdi" 1)
    '("EFhs" 1)
    '("EFhq" 1)
    '("EFhn" 1)
    '("EFrb" 1)
    '("EFrc" 1)
    '("EFcd" 1)
    '("EFf" 1)
    '("EFv" 1)
    '("EFnc" 1)
    '("EFpp" 1)
    '("EFc" 1)
    '("EFct" 1)
    '("EFb" 1)
    '("EFw" 1)
    '("EFs" 1)
    '("EFt" 1)
    '("EFd" 1)
    '("EFk" 1)
    '("EFD" 1))
   (LaTeX-add-labels
    "sec:org124c731"
    "sec:org0cbc82a"
    "sec:org4e20b33"
    "sec:org57e0bc1"
    "sec:org756c669"
    "sec:orgf700212"
    "sec:orgfb6978a"
    "sec:orgdb78b19"
    "sec:orgea88f54"
    "sec:org8b58e87"
    "sec:orgc31b0eb"
    "sec:org2a4fc91"
    "sec:orgc010276"
    "sec:orgdf6e5f4"
    "sec:org8c1d1fd"
    "sec:org4ff4bab"
    "sec:org02f7487"
    "sec:orgdd8392d"
    "sec:orga97ea47"
    "sec:orgf84b4f2"
    "sec:org5fc0047"
    "sec:org9f5945b")
   (LaTeX-add-bibliographies))
 :latex)

