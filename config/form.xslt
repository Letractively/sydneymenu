<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs ="http://www.w3.org/2001/XMLSchema">
<xsl:param name="name"/>
<xsl:template name="main" match = "/xs:schema">
 <form id="xsd-{$name}-form" class="xsd-form">
 <xsl:for-each select="./xs:complexType[@name=$name]"> 
   <xsl:for-each select = "./xs:attribute">
    <div class="attribute-cell">
      <label><xsl:value-of select="./@name"/></label>
      <input type="textfield">
        <xsl:attribute name = "name">
          <xsl:value-of select="./@name"/>
        </xsl:attribute>
        <xsl:attribute name = "value">{%with '/'|add:PATH|add:'/@<xsl:value-of select="./@name"/>' as XPATH%}{%xattr ITEM XPATH %}{%endwith%}</xsl:attribute>
      </input>
    </div>
   </xsl:for-each>
   <xsl:for-each select = "./xs:sequence/xs:element|./xs:element">
    <div class="element-cell">
      <label><xsl:value-of select="./@name"/></label>
      <textarea>
      <xsl:attribute name = "name">
        <xsl:value-of select="./@name"/>
      </xsl:attribute>
      <xsl:value-of select="./@name"/>
      </textarea>
    </div>
   </xsl:for-each>
 </xsl:for-each>
 </form>
</xsl:template>
</xsl:stylesheet>
