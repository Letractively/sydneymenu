<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match = "/item">
 <ul>
  <div class='icon'>
    <img>
      <xsl:attribute name="src">
        <xsl:value-of select="./@icon"/>
      </xsl:attribute>
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
 </ul>
</xsl:template>
<xsl:template match = "/timetable">
  <li>
   <span class='label'><xsl:value-of select="./@day"/>:</span>
   <a><xsl:value-of select="./@from"/></a>
   <a><xsl:value-of select="./@to"/></a>
  </li>
</xsl:template>

</xsl:stylesheet>
