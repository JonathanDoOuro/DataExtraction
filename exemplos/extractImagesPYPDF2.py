import PyPDF2 as pd

# Open the PDF file in read-binary mode
with open('./data/input/f12022Q_X.pdf', 'rb') as pdf_file:

    # Create a PDF reader object
    pdf_reader = pd.PdfReader(pdf_file)

    # Loop through each page of the PDF
    for i in range(2, len(pdf_reader.pages)):

        # Get the page object
        selected_page = pdf_reader.pages[i]

        # Extract text from the page
        page_text = selected_page.extract_text()

        # Print the extracted text
        print(f'Page {i+1}')

        # Extract images from the page
        xObject = selected_page['/Resources']['/XObject'].get_object()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                # Save the image to a file
                print(xObject)
                image_data = xObject[obj].get_data()
                with open(f'page{i+1}_image{obj[1:]}.jpg', 'wb') as image_file:
                    image_file.write(image_data)
