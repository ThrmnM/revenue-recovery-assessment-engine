from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

filename = "reports/Revenue_Recovery_Report.pdf"

c = canvas.Canvas(filename, pagesize=letter)

c.setFont("Helvetica-Bold", 20)
c.drawString(72, 750, "Revenue Recovery Assessment")

c.setFont("Helvetica", 14)
c.drawString(72, 710, "Company: Elite Gate & Fence Services")

c.drawString(72, 680, "Revenue Recovery Score: 60/100")

c.drawString(72, 640, "Revenue Leaks Identified:")

c.drawString(100, 610, "• Missed Calls")
c.drawString(100, 590, "• Delayed Quotes")
c.drawString(100, 570, "• Poor Communication")
c.drawString(100, 550, "• Technician Scheduling")

c.drawString(72, 500, "Recommendations:")

c.drawString(
    100,
    470,
    "• Install AI Receptionist and Missed Call Text Back."
)

c.drawString(
    100,
    450,
    "• Automate Quote Follow-Ups."
)

c.drawString(
    100,
    430,
    "• Implement Technician ETA Notifications."
)

c.save()

print(f"PDF created: {filename}")