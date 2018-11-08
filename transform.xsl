<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" version="1.0"
encoding="UTF-8"/>

<xsl:template match="article">

--- <xsl:value-of select="title"/> ---

Ingredients:
------------
<xsl:value-of select="ingredients"/>

Procedure:
----------
<xsl:apply-templates select="body"/>

**********************************************
</xsl:template>
</xsl:transform>
