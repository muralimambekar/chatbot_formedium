class report:
    def report(state):
        # Report generation
        fileName = 'report.pdf'
        
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.pagesizes import letter
        
        pdf = SimpleDocTemplate(
            fileName,
            pagesize=letter
        )
        
        
        from reportlab.platypus import Table
        table = Table(state)
        
        # add style
        from reportlab.platypus import TableStyle
        from reportlab.lib import colors
        
        style = TableStyle([
            ('BACKGROUND', (0,0), (5,0), colors.green),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(2,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ])
        table.setStyle(style)
        
        # 2) Alternate backgroud color
        rowNumb = len(state)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.burlywood
            else:
                bc = colors.beige
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
        
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),
            ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )
        table.setStyle(ts)
        # adding date
        from datetime import datetime
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        preventive="To prevent the spread of COVID-19:<br /> Clean your hands often. Use soap and water, or an alcohol-based hand rub.<br /> Maintain a safe distance from anyone who is coughing or sneezing.<br /> Don’t touch your eyes, nose or mouth.<br /> Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.<br /> Stay home if you feel unwell.<br /> If you have a fever, a cough, and difficulty breathing, seek medical attention. Call in advance.<br /> Follow the directions of your local health authority. "
        from reportlab.lib.styles import getSampleStyleSheet
        sample_style_sheet = getSampleStyleSheet()
        items = []
        from reportlab.platypus import Paragraph
        paragraph_1 = Paragraph("Latest updates on COVID-19 cases in India", sample_style_sheet['Heading2'])
        paragraph_2 = Paragraph("Retrived at: "+ dt_string,sample_style_sheet['BodyText'])
        paragraph_3 = Paragraph(preventive,sample_style_sheet['BodyText'])
        items.append(paragraph_1)
        items.append(paragraph_2)
        items.append(table)
        items.append(paragraph_3)
        pdf.build(items)    
        return None
        

