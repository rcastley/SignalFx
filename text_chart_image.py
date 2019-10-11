import sys
import base64
 
company = sys.argv[2]
 
with open(sys.argv[1], 'rb') as image_file:
  image_64_encode = base64.b64encode(image_file.read())
print "<table width=\"100%\" height=\"100%\" rules=\"none\"><tr><td valign=\"middle\" align=\"center\"><img src=\"data:image/png;base64,",image_64_encode,"\" width=\"200\"><br><br><b>",company,"</b></td></tr></table>"
