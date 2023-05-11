import fitz
import tabula

path = f'exemplos/gabarito_2022_DIVULGA.pdf'

doc = fitz.open(path)  # open document
texto = ''
for page in doc:  #iterate the document pages
      text = page.get_text(sort=False)  # get plain text (is in UTF-8)
      texto += text

# with open("exemplos/teste.txt", "w") as file:
#       file.write(texto)

page_numbers = "1-3" 

table = tabula.read_pdf(path, pages=page_numbers)[0]


print(table)