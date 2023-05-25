import fitz
import tabula

path = f'exemplos/nem2022_GB_impresso_D1_CD1.pdf'

doc = fitz.open(path)  # open document
texto = ''
for page in doc:  #iterate the document pages
      text = page.get_text(sort=False)  # get plain text (is in UTF-8)
      texto += text

print(texto)

# read the first page of the PDF file and extract the table
# df = tabula.read_pdf(path, pages=1)[0]

# # print the table
# print(df)