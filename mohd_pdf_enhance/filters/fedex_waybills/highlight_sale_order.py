##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##
#
# Highlight the sale order from the FedEx waybill
#
##

import io
import logging
import re
from typing import Any, Optional

import PyPDF2

import reportlab.pdfgen.canvas


def get_sale_order_from_pdf(filename: str,
                            options: dict[str, Any]) -> Optional[str]:
    """
    Get the sale order from the PDF file

    :param filename: PDF document to load
    :param options: dictionary with options
    :return: detected sale order (or None)
    """
    result = None
    with open(filename, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            # Search the carrier name text before attempting to search
            # the sale order
            if re.search(pattern=options['regex-fedex'],
                         string=page.extract_text()):
                # Get the sale order from the first page only
                content = pdf.pages[0].extract_text()
                if matches := re.search(pattern=options['regex-sale_order'],
                                        string=content):
                    result = matches.groups()[0]
                break
    return result


def highlight_sale_order(filename: str,
                         destination: str,
                         sale_order: str,
                         options: dict[str, Any]) -> None:
    """
    Highlight the sale order in the PDF file

    :param filename: PDF file to process
    :param destination: PDF file to write
    :param sale_order: Sale order to highlight
    :param options: dictionary with options
    """
    # Create in-memory canvas with the sale order number
    watermark = io.BytesIO()
    canvas = reportlab.pdfgen.canvas.Canvas(filename=watermark)
    canvas.setFont(psfontname=options.get('result-font-face', 'Helvetica'),
                   size=options.get('result-font-size', 20))
    canvas.rotate(theta=options.get('result-text-rotation', 0))
    canvas.drawString(x=options.get('result-text-x', 0),
                      y=options.get('result-text-y', 0),
                      text=sale_order)
    canvas.save()
    watermark.seek(0)
    watermark_pdf = PyPDF2.PdfReader(watermark)
    # Add the watermark to the original PDF and apply to the destination PDF
    original_pdf = PyPDF2.PdfReader(stream=filename)
    destination_pdf = PyPDF2.PdfWriter()
    for page in original_pdf.pages:
        page.merge_page(watermark_pdf.pages[0])
        destination_pdf.add_page(page)
    # Save destination PDF file
    with open(destination, 'wb') as file:
        destination_pdf.write(file)


def process(filename: str,
            destination: str,
            options: dict[str, Any]) -> bool:
    """
    Highlight the sale order

    :param filename: source PDF file to process
    :param destination: destination PDF file to write the output
    :param options: dictionary with options
    :return: process status
    """
    if sale_order := get_sale_order_from_pdf(filename=filename,
                                             options=options):
        # Highlight sale order in the PDF
        logging.info(f'Highlight sale order {sale_order}')
        highlight_sale_order(filename=filename,
                             destination=destination,
                             sale_order=sale_order,
                             options=options)
        result = True
    else:
        # No operation was needed/executed
        logging.debug('No sale order was found, no processing')
        result = False
    return result
