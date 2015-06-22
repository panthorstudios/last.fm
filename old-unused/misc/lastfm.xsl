<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" indent="yes"/> 
 
  <xsl:template match="/">
    <table>
    <xsl:variable name="numartists">5</xsl:variable>
    <xsl:variable name="maxwidth">200.0</xsl:variable>
    <xsl:variable name="max">
      <xsl:for-each select="/lfm/weeklyartistchart/artist/playcount">
        <xsl:sort data-type="number" order="descending"/>
        <xsl:if test="position()=1"><xsl:value-of select="."/></xsl:if>
      </xsl:for-each>
    </xsl:variable>
    <xsl:for-each select="/lfm/weeklyartistchart/artist[@rank &lt;= $numartists]">
      <tr>
         <td align="right" style="font-size:30px;font-family:Arial,Helvetica"><a target="_blank"><xsl:attribute name="href"><xsl:value-of select="url"/></xsl:attribute><xsl:value-of select="name"/></a></td>
         <td><img><xsl:attribute name="src">http://userserve-ak.last.fm/serve/64/2588646.jpg</xsl:attribute></img></td>
         <td>
            <table cellpadding="0" cellspacing="0">
               <tr>
                 <td align="center" height="45" style="font-size:30px;font-family:Arial,Helvetica; background-color: #a0a0a0"><xsl:attribute name="width"><xsl:value-of select="round((playcount * $maxwidth) div $max)"/></xsl:attribute><xsl:value-of select="playcount"/></td>
                 <xsl:if test="playcount &lt; $max">
                 <td align="center" style="background-color:#e0e0e0"><xsl:attribute name="width"><xsl:value-of select="$maxwidth - (playcount * $maxwidth div $max)"/></xsl:attribute>&#160;<xsl:value-of select="round($maxwidth - ((playcount * $maxwidth) div $max))"/></td>
                 </xsl:if>
               </tr>
            </table>
         </td>
      </tr>
    </xsl:for-each>
    </table>
  </xsl:template>
 
</xsl:stylesheet>