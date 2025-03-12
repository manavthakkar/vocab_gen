from io import BytesIO

import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas


def generate_pdf(vocab_text):
    # Parse vocabulary file contents.
    vocabs = []
    for line in vocab_text.splitlines():
        line = line.strip()
        if line:
            parts = line.split(";")
            if len(parts) >= 2:
                german = parts[0].strip()
                english = parts[1].strip()
                vocabs.append((german, english))

    # Load the background template image.
    with Image.open("background.jpg") as img:
        page_width, page_height = img.size

    # Create a BytesIO buffer to store the PDF.
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # ---------------------------
    # Spacing and Layout Variables
    # ---------------------------
    vocabs_per_page = 24  # Number of vocabulary pairs per page.

    # Vertical layout settings:
    top_margin = (
        183  # Distance from the top edge of the page for the first row.
    )
    row_spacing = 56  # Vertical distance between rows.

    # Horizontal layout settings:
    left_margin = 115  # Starting x-position for the left (German) column.
    column_gap = (
        20  # Additional gap from the center for the right (English) column.
    )

    # Determine x-coordinates for each column.
    left_column_x = left_margin
    right_column_x = (page_width / 2) + column_gap

    # Font settings:
    font_name = "Helvetica"
    font_size = 25

    # Generate each page.
    for i in range(0, len(vocabs), vocabs_per_page):
        # Draw the background image on the current page.
        c.drawImage(
            "background.jpg",
            0,
            0,
            width=page_width,
            height=page_height,
        )

        # Reapply font settings (needed after showPage).
        c.setFont(font_name, font_size)

        # Get the vocabulary pairs for the current page.
        page_vocabs = vocabs[i : i + vocabs_per_page]

        # Write each vocab pair on its row.
        for j, (german, english) in enumerate(page_vocabs):
            y = page_height - top_margin - j * row_spacing
            c.drawString(left_column_x, y, german)
            c.drawString(right_column_x, y, english)

        # End the current page.
        c.showPage()

    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# ---------------------------
# Streamlit App Interface
# ---------------------------
st.title("Vocabulary PDF Generator")

# File uploader for the vocabulary text file.
uploaded_file = st.file_uploader(
    "Upload your vocabulary text file (semicolon-separated):", type=["txt"]
)

# Text input for the output PDF file name.
pdf_filename = st.text_input("Enter output PDF file name:", "Episode_1")

# If a file is uploaded and a file name is provided...
if uploaded_file is not None and pdf_filename:
    # Read and decode the uploaded file.
    file_content = uploaded_file.read().decode("utf-8")

    if st.button("Generate PDF"):
        with st.spinner("Generating PDF..."):
            pdf_bytes = generate_pdf(file_content)
        st.success("PDF generated successfully!")
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
        )
