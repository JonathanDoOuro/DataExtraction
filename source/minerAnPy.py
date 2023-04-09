import PyPDF2
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTFigure, LTTextBoxHorizontal

# Open the input PDF file
input_pdf = PyPDF2.PdfFileReader(open('input.pdf', 'rb'))

# Set the start and end strings
start_string = "Start String"
end_string = "End String"

# Loop through each page of the input PDF file
for page_num in range(input_pdf.numPages):
    # Get the current page
    page = input_pdf.getPage(page_num)

    # Create a PDF writer for the output
    output_pdf = PyPDF2.PdfFileWriter()

    # Create a buffer for the extracted content
    content_buffer = BytesIO()

    # Extract the content of the current page
    extract_pages(open('input.pdf', 'rb'), page_numbers=[page_num+1], output_file=content_buffer)

    # Reset the buffer position to the beginning
    content_buffer.seek(0)

    # Parse the content of the current page
    for page_layout in extract_pages(open('input.pdf', 'rb'), page_numbers=[page_num+1]):
        for element in page_layout:
            # Check if the element is a text box and contains the start string
            if isinstance(element, LTTextBoxHorizontal) and start_string in element.get_text():
                # Add the element to the output PDF
                output_pdf.addPage(page)

                # Loop through the remaining elements on the page
                for remaining_element in page_layout[page_layout.index(element)+1:]:
                    # Check if the remaining element is a text box and contains the end string
                    if isinstance(remaining_element, LTTextBoxHorizontal) and end_string in remaining_element.get_text():
                        # Save the output PDF to a file
                        with open(f"output_{page_num}.pdf", "wb") as output_file:
                            output_pdf.write(output_file)

                        # Exit the loop
                        break

                    # Check if the remaining element is an image or a figure
                    elif isinstance(remaining_element, (LTImage, LTFigure)):
                        # Add the image or figure to the output PDF
                        output_pdf.addPage(page)

                        # Save the output PDF to a file
                        with open(f"output_{page_num}.pdf", "wb") as output_file:
                            output_pdf.write(output_file)

                        # Exit the loop
                        break
