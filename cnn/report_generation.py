from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views import View
from reportlab.pdfgen import canvas

class PDFGeneratorView(View):
    def get(self, request):
        # Prepare data
        data = {
            "image1" : {
                "back-dents" : 40,
                "broken-head-or-tail-lamp": 20,
                "front-dents": 10,
                "glas-shatter": 5,
                "no-damage": 5,
                "scratches": 10,
                "side-dents": 10
            },
            "image2" : {
                "back-dents" : 40,
                "broken-head-or-tail-lamp": 20,
                "front-dents": 10,
                "glas-shatter": 5,
                "no-damage": 5,
                "scratches": 10,
                "side-dents": 10
            },

        }

        # Render the PDF template
        template = get_template('pdf_template.html')
        rendered_template = template.render({'data': data})

        # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        p = canvas.Canvas(response)

        # Draw images
        image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg']
        x, y = 50, 600
        for image_path in image_paths:
            p.drawImage(image_path, x, y, width=200, height=150)
            y -= 200

        # Draw text
        x, y = 50, 500
        for key, value in data.items():
            p.drawString(x, y, f'{key}: {value}')
            y -= 20

        # Save the PDF
        p.showPage()
        p.save()

        return response
