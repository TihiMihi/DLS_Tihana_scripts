rsc - BibTeX styles for Royal Society of Chemistry and Wiley journals
=====================================================================

The `rsc` package provides BibTeX style files to produce
bibliographies in accordance with the guidelines of the Royal
Society of Chemistry and Wiley chemistry-related journals. The
styles require the use of `natbib`.  In addition, a short LaTeX 
package is included; this provides a convenient user interface to 
the customisation hooks made available by the BibTeX styles.

Installation
------------

The package is supplied in `.dtx` format and as a pre-extracted
zip file, `rsc.tds.zip`. The later is most convenient for
most users: simply unzip this in your local `texmf` directory.
If you want to unpack the `.dtx` yourself, running `tex
rsc.dtx` will extract the package whereas 'latex rsc.dtx
will extract it and also typeset the documentation.

Typesetting the documentation requires a number of packages in
addition to those needed to use the package. This is mainly 
because of the number of demonstration items included in the 
text. To compile the documentation without error, you will 
need the packages:
 - `helvet`
 - `hypdoc`
 - `listings`
 - `lmodern`
 - `mathpazo`
 - `microtype`