import Dependencies.pdfkit as pdfkit
import Dependencies.PyPDF2 as PyPDF2
import os
import Constants

def return_htmlcode(title,severity,status,owasp,compliance,abstract,description,test_findings,remediation):

    modified_html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" type="text/css" href="modified.css">
</head>
<body>

<div class="header">
  <h3>{}</h3>
</div>

<div class="menu">
	<h3 style = "margin:3px;">Severity - {}</h3>
</div>
</div><div class="menu">
	<h3 style = "margin:3px;">Status - {}</h3>
</div>

<div class="main">
  <h1 class="heading" style="margin-top:110px">OWASP Reference 2017 v1.0</h1>
  <p>{}</p>
</div>
<div class="main">
  <h1 class="heading">Compliance/Security Control Reference</h1>
  <p>{}</p>
</div>
<div class="main">
  <h1 class="heading">Abstract</h1>
  <p>{}</p>
</div>
<div class="main">
  <h1 class="heading">Vulnerability Description</h1>
  <p>{}</p>
  
</div>
<div class="main">
  <h1 class="heading">Instance(s)</h1>
  <p>{}</p>
 
</div>
<div class="main">
  <h1 class="heading">Recommendations</h1>
  <p>{}</p>
  
</div>
</body>
</html>
    """.format(title,severity,status,owasp,compliance,abstract,description,test_findings,remediation)
    return modified_html_code


def create_pages(config):
    count = 0
    pdf_list = []
    for keys, values in config.items():
        file_name = "OutDocument/temp.htm"

        with open(file_name, 'w') as file:
            string = return_htmlcode(config[keys]['title'].strip('_').title(), config[keys]['severity'],config[keys][Constants.STATUS],config[keys]['owasp'],config[keys]['Compliance'],config[keys]['abstract'],
                            config[keys]['description'],config[keys][Constants.EXECUTION_OUTPUT] ,config[keys]['remediation'])
            string = string.replace("•","-")
            file.write(string)
        pdffilename = "pdf_related_files/" + str(count) + ".pdf"
        pdf_list.append(pdffilename)
        pdfkit.from_file(file_name, pdffilename)

        count += 1
    pdf_write_object = PyPDF2.PdfFileWriter()

    for i in pdf_list:
        pdf_read_object = PyPDF2.PdfFileReader(i)
        for page in range(pdf_read_object.numPages):
            pdf_write_object.addPage(pdf_read_object.getPage(page))

    final_file_object = open('pdf_related_files/assessment_details.pdf', 'wb')
    pdf_write_object.write(final_file_object)
    final_file_object.close()

    for i in pdf_list:
        os.remove(i)




