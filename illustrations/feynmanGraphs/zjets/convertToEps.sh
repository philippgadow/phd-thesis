#!/bin/sh
# $Id: pdf2eps,v 0.01 2005/10/28 00:55:46 Herbert Voss Exp $
# Convert PDF to encapsulated PostScript.
# usage:
# convertToEps.sh <page number>
# 
# 84.815997 85.985997 291.329991 255.689992
# 82.241997 147.959995 293.885991 258.173992
# 83.249997 118.583996 291.653991 257.111992
# 82.241997 147.959995 293.885991 258.173992
# --bbox "82 85 294 259"
pdfcrop "$1.pdf" "$1-temp.pdf"
pdftops -f 1 -l 1 -eps "$1-temp.pdf" "$1.eps"
rm  "$1-temp.pdf"
