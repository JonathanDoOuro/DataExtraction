import fitz  # Import PyMuPDF module

# Open the PDF file
with fitz.open('data/input/enem2022PV_D1_CD1.pdf') as pdf:
    # Iterate over each page
    for i in range(pdf.page_count):
        page = pdf.load_page(i)

        # Extract the images from the page
        images = page.get_images()

        # Iterate over each image
        for j, image in enumerate(images):
            
            img = pdf.extract_image(image[0])
            
            name = f"data/output/images/image{i+1}_{j+1}.{img['ext']}"
            # Save the image to a file
            with open(name, 'wb') as f:
               f.write(img['image'])