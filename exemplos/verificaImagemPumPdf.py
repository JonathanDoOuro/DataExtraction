import fitz

path = "data/input/f12022Q_X.pdf"

doc = fitz.open(path)

x = doc.load_page(3).get_xobjects()

print(x)
