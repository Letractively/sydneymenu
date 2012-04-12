<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match = "/info">
 <ul>
  <div class='icon'>
    <img>
      <xsl:attribute name="src"><xsl:value-of select="./@icon"/></xsl:attribute>
    </img>
  </div>
  <xsl:for-each select="./@*">
   <xsl:if test="name()!='icon'">
   <li>
    <label><xsl:value-of select="name()"/>:</label>
    <span><xsl:value-of select="."/></span>
   </li>
   </xsl:if>
  </xsl:for-each>
  <xsl:for-each select = "./*">
   <div>
      <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
     <xsl:value-of select="."/>
   </div>
  </xsl:for-each>
  <div style="clear:both"/>
 </ul>
</xsl:template>
<xsl:template match = "/hint">
 <ul>
  <div class='icon'>
    <img>
      <xsl:attribute name="src"><xsl:value-of select="./@icon"/></xsl:attribute>
    </img>
  </div>
  <xsl:for-each select="./@*">
   <xsl:if test="name()!='icon'">
   <li>
    <label><xsl:value-of select="name()"/>:</label>
    <span><xsl:value-of select="."/></span>
   </li>
   </xsl:if>
  </xsl:for-each>
  <xsl:for-each select = "./*">
   <div>
      <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
     <xsl:value-of select="."/>
   </div>
  </xsl:for-each>
  <div style="clear:both"/>
 </ul>
</xsl:template>
</xsl:stylesheet>
