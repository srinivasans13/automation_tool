import OutDocument.front_page as front_page
import OutDocument.glossary as glossary
import OutDocument.confidentiality_agreement as confidentiality
import OutDocument.assessment_generation as assessment
import OutDocument.reportSummary as report
import sys
import Dependencies.PyPDF2 as PyPDF2
import Constants
import os

def generate_report(config,platform):


    front_page.return_pdf(Constants.APP_NAME, platform)

    assessment.create_pages(config)

    report.returnpdfcode(config,platform)

    glossary.return_pdf()

    confidentiality.returnpdf()

    pdf_write_object = PyPDF2.PdfFileWriter()

    pdf_list = Constants.PDF_LIST

    for i in pdf_list:
        pdf_read_object = PyPDF2.PdfFileReader(i)
        for page in range(pdf_read_object.numPages):
            pdf_write_object.addPage(pdf_read_object.getPage(page))

    final_file_object = open(f"{Constants.REPORT_FOLDER}/assessment_report.pdf", 'wb')
    pdf_write_object.write(final_file_object)
    final_file_object.close()

    for name in Constants.PDF_LIST:
        os.remove(name)
