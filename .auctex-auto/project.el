(TeX-add-style-hook
 "project"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "top=1in" "bottom=1.25in" "left=1.25in" "right=1.25in") ("embedall" "main" "include") ("tcolorbox" "many")))
   (add-to-list 'LaTeX-verbatim-environments-local "VerbatimOut")
   (add-to-list 'LaTeX-verbatim-environments-local "SaveVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "EscVerb")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "EscVerb*")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "Verb*")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "Verb")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
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
    "parskip"
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
    "sec:org5ae5faa"
    "sec:orga506a2e"
    "sec:orge5ab2bf"
    "sec:org0c71eb1"
    "sec:org63aa24e"
    "sec:org09de8f2"
    "sec:orgf57b4a6"
    "sec:org9f3c667"
    "sec:orgbf80c9c"
    "sec:org8db77bd"
    "sec:org66280c0"
    "sec:orga4be1a2"
    "sec:org8abaedb"
    "sec:orgba64c7d"
    "sec:orga6c680a"
    "sec:org235ccac"
    "sec:orgd9d82d5"
    "sec:org6ba02a5"
    "sec:org9debea8"
    "sec:orge86b719"
    "sec:org455a30f"
    "sec:orgc14c26e"
    "sec:orgaa8eb12"
    "sec:orgac6d72f"
    "sec:orge7d6145"
    "sec:org23de98f"
    "sec:org4c1573b"
    "sec:org0718b0e")
   (LaTeX-add-bibliographies
    "ref")
   (LaTeX-add-xcolor-definecolors
    "EFD"
    "EFk"
    "EFd"
    "EFt"
    "EFs"
    "EFw"
    "EFb"
    "EFct"
    "EFc"
    "EFpp"
    "EFnc"
    "EFv"
    "EFf"
    "EFcd"
    "EFrc"
    "EFrb"
    "EFhn"
    "EFhq"
    "EFhs"
    "EFrdi"
    "EFrdii"
    "EFrdiii"
    "EFrdiv"
    "EFrdv"
    "EFrdvi"
    "EFrdvii"
    "EFrdiix"
    "EFrdix"))
 :latex)

