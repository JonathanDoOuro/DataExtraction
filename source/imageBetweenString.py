import PyPDF2
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox

# Open the input PDF file
input_pdf = PyPDF2.PdfReader(open('data/input/f12022Q_X.pdf', 'rb'))

# Set the start and end strings
start_string = "QUESTÃO 1"
end_string = "QUESTÃO 2"

# Loop through each page of the input PDF file
for page_num in range(len(input_pdf.pages)):
    # Create a buffer for the extracted content
    content_buffer = BytesIO()

    # Extract the content of the current page
    extract_pages(open('data/input/f12022Q_X.pdf', 'rb'), page_numbers=[page_num+1])

    # Reset the buffer position to the beginning
    content_buffer.seek(0)

    # Parse the content of the current page
    has_image_between_strings = False
    for page_layout in extract_pages(open('data/input/f12022Q_X.pdf', 'rb'), page_numbers=[page_num+1]):
        for element in page_layout:
            # Check if the element is a text box and contains the start string
            if isinstance(element, LTTextBoxHorizontal) and start_string in element.get_text():
                # Loop through the remaining elements on the page
                for remaining_element in page_layout[page_layout.index(element)+1:]:
                    # Check if the remaining element is a text box and contains the end string
                    if isinstance(remaining_element, LTTextBoxHorizontal) and end_string in remaining_element.get_text():
                        # Exit the loop
                        break

                    # Check if the remaining element is an image
                    elif isinstance(remaining_element, LTImage):
                        has_image_between_strings = True
                        # Exit the loop
                        break

                # Exit the loop
                break

    # Print whether there is an image between the strings on the current page
    print(f"Page {page_num+1}: {has_image_between_strings}")
