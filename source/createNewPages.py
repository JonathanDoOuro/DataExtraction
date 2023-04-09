import PyPDF2

# Open the PDF file
pdf_file = open('data/input/f12022Q_X.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Loop through each page
for page_num in range(len(pdf_reader.pages)):
    # Extract the text content and images from the page
    page = pdf_reader.pages[page_num]
    text_content = page.extract_text()
    images = page.images

    # Search for "QUESTÃO {i}" in the text content
    for i in range(1, 6):  # Assuming there are less than 1000 questions
        question_start = f'QUESTÃO {i}'
        question_end = f'QUESTÃO {i+1}'
        
        # If we find a question, start a new PDF file for it
        if question_start in text_content:
            new_pdf = PyPDF2.PdfFileWriter()
            question_content = []
            in_question = True
            
        # If we're in a question, add the content to it
        if in_question:
            question_content.append(page)
            
        # If we reach the end of the question, save the new PDF file
        if question_end in text_content:
            in_question = False
            question_file = open(f'question_{i}.pdf', 'wb')
            for page in question_content:
                new_pdf.addPage(page)
            new_pdf.write(question_file)
            question_file.close()
            
            # Remove the processed question content from the page content
            text_content = text_content[text_content.find(question_end) + len(question_end):]
            page = PyPDF2.PdfFileReader(page).getPage(0)
