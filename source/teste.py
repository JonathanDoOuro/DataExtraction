import PyPDF2

# Open the input PDF file
input_pdf = PyPDF2.PdfFileReader(open('input.pdf', 'rb'))

# Loop through each page of the input PDF file
for page_num in range(input_pdf.numPages):
    # Get the current page
    page = input_pdf.getPage(page_num)

    # Get the page's text content
    text = page.extractText()

    # Split the text content into separate questions
    questions = text.split('Question')

    # Loop through each question
    for i, question in enumerate(questions[1:]):
        # Create a new PDF file for this question
        output_pdf = PyPDF2.PdfFileWriter()

        # Add the current question to the new PDF file
        question_page = PyPDF2.pdf.PageObject.createBlankPage(None, page.mediaBox.getWidth(), page.mediaBox.getHeight())
        question_page.mergePage(page)
        question_page.artBox.lowerLeft = (0, 0)
        question_page.artBox.upperRight = (page.mediaBox.getWidth(), page.mediaBox.getHeight())
        question_page.cropBox.lowerLeft = (0, 0)
        question_page.cropBox.upperRight = (page.mediaBox.getWidth(), page.mediaBox.getHeight())
        question_page.trimBox.lowerLeft = (0, 0)
        question_page.trimBox.upperRight = (page.mediaBox.getWidth(), page.mediaBox.getHeight())
        question_page.rotateClockwise(90)
        question_content = f"Question {i+1}\n\n{question}"
        question_page.addContent(PyPDF2.pdf.ContentStream(question_content.encode()))
        output_pdf.addPage(question_page)

        # Save the new PDF file
        with open(f'output_{page_num}_question_{i+1}.pdf', 'wb') as output_file:
            output_pdf.write(output_file)
