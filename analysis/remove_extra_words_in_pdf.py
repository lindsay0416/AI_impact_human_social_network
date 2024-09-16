import fitz  # PyMuPDF

# Load the PDF file
input_pdf_path = "images/topic_step15.pdf"
output_pdf_path = "images/topic_step15_cleaned.pdf"

doc = fitz.open(input_pdf_path)

# Loop through each page to find and remove highlighted text
for page_num in range(doc.page_count):
    page = doc[page_num]
    # Iterate through all annotations on the page
    annot = page.first_annot
    while annot:
        # Check if the annotation is a highlight
        if annot.type[0] == 8:  # Annotation type 8 is Highlight
            # Remove the highlight annotation
            page.delete_annot(annot)
        annot = annot.next  # Move to the next annotation

# Save the modified PDF without highlighted text
doc.save(output_pdf_path)
doc.close()

output_pdf_path
