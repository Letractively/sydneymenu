<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs ="http://www.w3.org/2001/XMLSchema">

<xsl:param name="name"/>

<xsl:template name="main" match = "/xs:schema">
 <xsl:for-each select="./xs:complexType[@name=$name]"> 
   <xsl:element name="{$name}">
    <xsl:for-each select="./xs:attribute">
     <xsl:attribute name="{./@name}">{{REQUEST.<xsl:value-of select="./@name"/>}}</xsl:attribute>
    </xsl:for-each>
    <xsl:for-each select = "./xs:sequence/xs:element|./xs:element">
     <xsl:element name="{./@name}">
     {{REQUEST.<xsl:value-of select="./@name"/>}}
     </xsl:element>
    </xsl:for-each>
   </xsl:element>
 </xsl:for-each>
</xsl:template>
</xsl:stylesheet>
