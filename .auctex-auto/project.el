(TeX-add-style-hook
 "project"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "top=1in" "bottom=1.25in" "left=1.25in" "right=1.25in") ("embedall" "main" "include") ("tcolorbox" "many")))
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "SaveVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "VerbatimOut")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "EscVerb*")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "EscVerb")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "Verb")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "Verb*")
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
    "sec:org64b45eb"
    "sec:org02faee4"
    "sec:org018ff36"
    "sec:orgde62c75"
    "sec:org062f263"
    "sec:orge50f40c"
    "sec:org43fec0b"
    "sec:org731bb34"
    "sec:org1444c4e"
    "sec:org4fd4c21"
    "sec:orgbfc8a85"
    "sec:org73ad80c"
    "sec:org1ba9e1c"
    "sec:org6771566"
    "sec:org492ff92"
    "sec:org49d5bca"
    "sec:orge48eb5b"
    "sec:orge39fbde"
    "sec:orgb03cf5b"
    "sec:org5a406ec"
    "sec:org4712c24"
    "sec:org1c26a2a"
    "sec:org9c8443e"
    "sec:orgf959eb4"
    "sec:orgcad697e")
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

