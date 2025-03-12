from PIL import Image
from reportlab.pdfgen import canvas

# File names – ensure these files are in the same directory as the script.
template_image = "two_column_template_page-0001.jpg"
vocab_file = "egp1_vokabeln-semikolon.txt"
output_pdf = "vocab_output.pdf"

# Open the template image to get its dimensions.
with Image.open(template_image) as img:
    page_width, page_height = img.size

# Create a PDF canvas with the page size matching the template image.
c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))

# Read the vocabulary file and parse each line into (German, English) tuples.
vocabs = []
with open(vocab_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(";")
            if len(parts) >= 2:
                german = parts[0].strip()
                english = parts[1].strip()
                vocabs.append((german, english))

# ---------------------------
# Spacing and Layout Variables
# ---------------------------
vocabs_per_page = 24  # Number of vocabulary pairs per page.

# Vertical layout settings:
top_margin = 183  # Distance from the top edge of the page for the first row.
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

# ---------------------------
# Generate PDF Pages
# ---------------------------
for i in range(0, len(vocabs), vocabs_per_page):
    # Draw the template image as the background for the current page.
    c.drawImage(template_image, 0, 0, width=page_width, height=page_height)

    # Reapply the font settings on each new page.
    c.setFont(font_name, font_size)

    # Get the vocabulary pairs for the current page.
    page_vocabs = vocabs[i : i + vocabs_per_page]

    # Draw each vocabulary pair on its corresponding row.
    for j, (german, english) in enumerate(page_vocabs):
        y = page_height - top_margin - j * row_spacing
        c.drawString(left_column_x, y, german)
        c.drawString(right_column_x, y, english)

    # Finish the current page.
    c.showPage()

# Save the resulting PDF.
c.save()
print("PDF created successfully:", output_pdf)
