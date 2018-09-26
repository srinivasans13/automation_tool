import Dependencies.pdfkit as pdfkit
def return_pdf(app_name,platform):
    html_code = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
<img style="position:absolute;top:0.54in;left:1.33in;width:6.35in;height:9.67in" src="vi_1.png" />
<img style="position:absolute;top:0.58in;left:1.37in;width:1.14in;height:9.61in" src="ri_1.jpeg" />
<img style="position:absolute;top:0.58in;left:2.41in;width:5.19in;height:1.71in" src="ri_2.jpeg" />
<img style="position:absolute;top:2.29in;left:2.41in;width:5.18in;height:2.69in" src="ri_3.jpeg" />
<div style="position:absolute;top:5.32in;left:4.28in;width:5in;line-height:0.13in;"><span style="font-style:normal;font-weight:bold;font-size:9pt;font-family:Helvetica;color:#000000">App Name : {}</span><span style="font-style:normal;font-weight:bold;font-size:9pt;font-family:Helvetica;color:#000000"> </span><br/></SPAN></div>
<div style="position:absolute;top:5.87in;left:4.32in;width:1.46in;line-height:0.13in;"><span style="font-style:normal;font-weight:bold;font-size:9pt;font-family:Helvetica;color:#000000">App Platform : {}</span><span style="font-style:normal;font-weight:bold;font-size:9pt;font-family:Helvetica;color:#000000"> </span><br/></SPAN></div>
<span style="font-style:italic;font-weight:normal;font-size:7pt;font-family:Helvetica;color:#000000"> </span><br/></SPAN></div>
</body>
</html>

    """.format(app_name,platform)

    s = "OutDocument/temp.htm"
    file = open(s,'w')
    file.write(str(html_code))
    file.close()
    pdfkit.from_file(s,"pdf_related_files/firstpage.pdf")



