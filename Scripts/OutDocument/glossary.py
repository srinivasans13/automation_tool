import Dependencies.pdfkit as pdfkit
def return_pdf():
    s = ['OutDocument/pg_0011.htm','OutDocument/pg_0012.htm']
    pdfkit.from_file(s,"pdf_related_files/glossary.pdf")