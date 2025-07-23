from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm

def generate_salary_pdf(
    output_path: Path,
    employee_dict: dict,
    predicted_salary: float,
    model_r2: float,
    comparison_text: str,
    suggestions_text: str,
    title: str = "Smart Salary AI - Salary Report",
):
    output_path = Path(output_path)
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.HexColor("#00ffe5"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30*mm, height - 30*mm, title)

    # Employee details
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30*mm, height - 45*mm, "Employee Input")
    c.setFont("Helvetica", 12)
    y = height - 55*mm
    for k, v in employee_dict.items():
        c.drawString(32*mm, y, f"{k}: {v}")
        y -= 7*mm

    # Predicted salary
    y -= 5*mm
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#00e6ac"))
    c.drawString(30*mm, y, f"Predicted Salary: ₹{int(predicted_salary):,}")
    y -= 10*mm

    # Model R2
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.white)
    c.drawString(30*mm, y, f"Model R² Score: {model_r2:.4f}")
    y -= 10*mm

    # Comparison
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30*mm, y, "Role Comparison")
    y -= 7*mm
    c.setFont("Helvetica", 12)
    for line in comparison_text.split("\n"):
        c.drawString(32*mm, y, line)
        y -= 6*mm

    # Suggestions
    y -= 5*mm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30*mm, y, "Career Suggestions")
    y -= 7*mm
    c.setFont("Helvetica", 12)
    for line in suggestions_text.split("\n"):
        c.drawString(32*mm, y, line)
        y -= 6*mm

    c.showPage()
    c.save()
    return output_path
