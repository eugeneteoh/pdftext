import io
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path


def pdftext(text: str, pos: tuple):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet)
    pdfmetrics.registerFont(TTFont('Montserrat-Medium', 'Montserrat-Medium.ttf'))
    can.setFont('Montserrat-Medium', 17)
    can.drawCentredString(595, 220, text)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("certificate.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    name = text.replace('/', '')
    outputStream = open(Path('output', f"Certificate of Participation - Startup Weekend - {name}.pdf"), "wb")
    output.write(outputStream)
    outputStream.close()