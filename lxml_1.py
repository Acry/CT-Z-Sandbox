#!/usr/bin/env python
# expands to python 3, so this is an Python 3 example
# see:
# http://fhoerni.free.fr/comp/xslt.html
# https://www.w3schools.com/xml/ref_xsl_el_output.asp
from lxml import etree
dom = etree.parse("data.xml")
xslt = etree.parse("transform.xsl")
transform = etree.XSLT(xslt)
result = transform(dom)
print(result)

