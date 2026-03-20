from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from datetime import datetime
from config import CURRENCY, APP_NAME


def generate_bill_pdf(bill_data, filename="bill.pdf", customer_name="", bill_id=""):
    """
    Generate a professional pharmacy bill PDF
    
    Args:
        bill_data: List of dicts with 'name', 'quantity', 'price'
        filename: Output filename
        customer_name: Customer name for the bill
        bill_id: Bill ID/reference number
    """
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=6,
        alignment=0  # Left
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.white,
        alignment=1  # Center
    )
    
    # Header
    title = Paragraph(f"💊 {APP_NAME}", title_style)
    elements.append(title)
    
    subtitle = Paragraph("Professional Pharmacy Bill", subtitle_style)
    elements.append(subtitle)
    
    # Bill Info
    bill_info = f"""
    <b>Bill ID:</b> {bill_id} | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>Customer:</b> {customer_name or 'Walk-in Customer'}
    """
    elements.append(Paragraph(bill_info, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Prepare table data
    table_data = [['Medicine', 'Qty', f'Unit Price ({CURRENCY})', f'Total ({CURRENCY})']]
    
    total_amount = 0
    for item in bill_data:
        item_total = item["quantity"] * item["price"]
        total_amount += item_total
        
        table_data.append([
            item["name"],
            str(item["quantity"]),
            f"{item['price']:.2f}",
            f"{item_total:.2f}"
        ])
    
    # Add totals row
    table_data.append(['', '', 'TOTAL:', f"{total_amount:.2f}"])
    
    # Create table
    table = Table(table_data, colWidths=[3*inch, 0.8*inch, 1.2*inch, 1.2*inch])
    
    # Style table
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body rows
        ('ALIGN', (0, 1), (0, -2), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -2), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8F9FA')]),
        ('GRID', (0, 0), (-1, -2), 1, colors.HexColor('#E0E0E0')),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
        ('TOPPADDING', (0, 1), (-1, -2), 8),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F0F0F0')),
        ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (0, -1), (-1, -1), 1, colors.HexColor('#0066CC')),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer = Paragraph(
        "<i>Thank you for your purchase! This is an automated invoice. For queries, contact our pharmacy.</i>",
        styles['Normal']
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    return filename