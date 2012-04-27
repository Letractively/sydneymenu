<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match = "/item">
 <ul>
  <div class='icon'>
    <img>
      <xsl:attribute name="src"><xsl:value-of select="./@icon"/>/?sc=true</xsl:attribute>
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
<xsl:template match = "/plant">
 <ul>
  <div class='icon'>
    <img>
      <xsl:attribute name="src"><xsl:value-of select="./@icon"/>/?sc=true</xsl:attribute>
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
  <li class='hint'>
    <a>
      <xsl:attribute name="href">/garden/hint/soil/<xsl:value-of select="./@name"/>/</xsl:attribute>
      soil hint:
    </a>
    Best grown in deep sandy, loamy soil
  </li>
  <li class='hint'>
    <a>fertilize reminder:</a> no fertilizing needed if the soil is well prepared before
  </li>
  <div style="clear:both"/>
 </ul>
</xsl:template>
<xsl:template match = "/timetable">
  <li>
   <span class='label'><xsl:value-of select="./@day"/>:</span>
   <a><xsl:value-of select="./@from"/> - <xsl:value-of select="./@to"/></a>
  </li>
</xsl:template>

</xsl:stylesheet>
