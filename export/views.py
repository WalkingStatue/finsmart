from analysis.views import CashFlowChartView, WalletsOverviewView, SpendingTrendsView, Budget_Utilization
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.http import HttpResponse,HttpRequest
from django.contrib.staticfiles import finders
from transactions.models import Transaction
from reportlab.lib.pagesizes import letter
from django.test import RequestFactory
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from .forms import DateRangeForm
from weasyprint import HTML, CSS
from django.conf import settings
from urllib.parse import quote
import csv
import os

class ExportTransactionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        return render(request, 'export/export.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if form.is_valid():
            print("Form is valid, processing data...")

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            transactions = Transaction.objects.filter(
                account__user=self.request.user, 
                transaction_date__date__range=(start_date, end_date))

            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': f'attachment; filename={quote("transactions.csv")}'}
            )

            writer = csv.writer(response)
            writer.writerow(['Wallet', 'Transaction Type', 'Amount', 'Description', 'Category', 'Transaction Date', 'Budget', 'Goal'])

            for transaction in transactions:
                category_name = transaction.category.name if transaction.category else 'N/A'
                writer.writerow([
                    transaction.wallet.name,
                    transaction.transaction_type,
                    transaction.amount,
                    transaction.description,
                    category_name,
                    transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
                    transaction.budget,
                    transaction.goal,
                ])

            return response
        else:
            print(f"Form errors: {form.errors}")
        return render(request, 'export/export.html', {'form': form})

class ExportTransactionsPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        return render(request, 'export/export.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            transactions = Transaction.objects.filter(
                account__user=request.user,
                transaction_date__date__range=(start_date, end_date))

            response = HttpResponse(content_type='application/pdf')
            filename = f"transactions_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

           
            doc = SimpleDocTemplate(response, pagesize=letter)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='TitleCustom', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica-Bold', textColor=colors.navy))
            styles.add(ParagraphStyle(name='CustomHeading', parent=styles['Heading2'], fontSize=14, alignment=TA_LEFT, spaceAfter=12, fontName='Helvetica-Bold', textColor=colors.darkgreen))
            styles.add(ParagraphStyle(name='NormalIndent', parent=styles['Normal'], firstLineIndent=20, spaceBefore=6, spaceAfter=6, textColor=colors.black))
            styles.add(ParagraphStyle(name='UserInfo', parent=styles['Normal'], fontSize=12, spaceBefore=6, spaceAfter=6))

            story = []

            story.append(Paragraph("FinSmart Statement", styles['TitleCustom']))
            story.append(Spacer(1, 12))

            # Statement Period Section
            story.append(Paragraph("Statement Period", styles['CustomHeading']))
            statement_period = f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}"
            story.append(Paragraph(statement_period, styles['UserInfo']))
            story.append(Spacer(1, 12))

            # User Information Section
            story.append(Paragraph("User Information", styles['CustomHeading']))
            user_info_text = f"Username: {request.user.username}<br/>Name: {request.user.first_name} {request.user.last_name}<br/>Currency: INR"
            story.append(Paragraph(user_info_text, styles['UserInfo']))
            story.append(Spacer(1, 12))

            # Initialize debit and credit totals
            total_debit = 0
            total_credit = 0

            # Table of Transactions
            transaction_data = [['Description', 'Date', 'Wallet', 'Debit', 'Credit', 'Category', 'Budget', 'Goal']]  # Header row

            for transaction in transactions:
                if transaction.transaction_type == 'debit':
                    total_debit += transaction.amount
                elif transaction.transaction_type == 'credit':
                    total_credit += transaction.amount
                
                category_name = transaction.category.name if transaction.category else 'N/A'
                transaction_row = [
                    Paragraph(transaction.description, styles['Normal']),
                    Paragraph(transaction.transaction_date.strftime('%Y-%m-%d'), styles['Normal']),
                    Paragraph(transaction.wallet.name if transaction.wallet else 'N/A', styles['Normal']),
                    Paragraph(f'{transaction.amount:.2f}' if transaction.transaction_type == 'debit' else '', styles['Normal']),
                    Paragraph(f'{transaction.amount:.2f}' if transaction.transaction_type == 'credit' else '', styles['Normal']),
                    Paragraph(category_name, styles['Normal']),
                    Paragraph(str(transaction.budget) if transaction.budget else 'N/A', styles['Normal']),
                    Paragraph(str(transaction.goal) if transaction.goal else 'N/A', styles['Normal']),
                ]
                transaction_data.append(transaction_row)
            spacer_row = [Paragraph(' ', styles['Normal']) for _ in range(8)]  # Adjust the range if your table has a different number of columns
            transaction_data.append(spacer_row)
                    # Adding the total row, ensuring each cell is properly formatted
            total_row = [
                Paragraph('Total', styles['Normal']),  # 'Total' label in the first column, adjust column index as needed
                Paragraph('', styles['Normal']),  # Empty cell
                Paragraph('', styles['Normal']),  # Empty cell
                Paragraph(f'{total_debit:.2f}', styles['Normal']),  # Debit total
                Paragraph(f'{total_credit:.2f}', styles['Normal']),  # Credit total
                Paragraph('', styles['Normal']),  # Empty cell
                Paragraph('', styles['Normal']),  # Empty cell
                Paragraph('', styles['Normal']),  # Empty cell
            ]
            transaction_data.append(total_row)

            # Create and style the table
            table_style = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2D3748')),  # Using bg-gray-800 equivalent
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),  # Keeping the text color for the header
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),  # Center alignment for all cells
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),  # Bold font for the header
                ('BOTTOMPADDING', (0,0), (-1,0), 12),  # Padding below the header
                ('FONTSIZE', (0,0), (-1,-1), 9),  # Font size for all cells
                ('LINEBELOW', (0,0), (-1,-2), 1, colors.HexColor('#AAAAAA')),  # Line below each row except the last one
                ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#FFFFFF')),  # Background for body rows
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#DDDDDD')),  # Background for the total row
                ('TOPPADDING', (0,-1), (-1,-1), 5),  # Padding above the total row
                ('BOTTOMPADDING', (0,-1), (-1,-1), 5),  # Padding below the total row
            ])
            
            table = Table(transaction_data,colWidths = [130, 65, 70, 65, 65, 70, 65, 65])
            table.setStyle(table_style)
            story.append(table)

            # Build the PDF document with the table
            doc.build(story)
            return response
        else:
            print(f"Form errors: {form.errors}")
            return render(request, 'export/export.html', {'form': form})
