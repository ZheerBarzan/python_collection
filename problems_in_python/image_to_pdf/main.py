import fpdf
from fpdf import FPDF

pdf = FPDF()

imagelist = ["ferrari.jpg", "mustang.jpg"]
for image in imagelist:
    pdf.add_page()
    pdf.image(image, 0, 0, 210, 297)

pdf.output("output.pdf", "F")
