from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import datetime
from .models import *
import json
from django.http import JsonResponse
from coreApp.utils import MissingNumberFinder
from django.views.decorators.csrf import csrf_exempt
#información sobre las compras de dos compañías ficticias que procesan con nosotros.

# Create your views here.
def home(request):#daily_company_totals_repor
    selected_date = None

    date_param = request.GET.get('date')

    if date_param:
        try:
            selected_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            pass

    daily_company_totals = Charges.objects.annotate(
        date=TruncDate('created_at')
    ).values(
        'date', 'company__company_name'
    ).annotate(
        total_amount=Sum('amount')
    ).order_by(
        'date', 'company__company_name'
    )

    if selected_date:
        daily_company_totals = daily_company_totals.filter(date=selected_date)

    context = {
        'report_data': daily_company_totals,
        'title': 'Monto Total Transaccionado por Día y Compañía',
        'selected_date': selected_date,
    }

    return render(request, 'coreApp/home.html', context)

@csrf_exempt 
def find_missing_number_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numbers_list = data.get('numbers', []) 

            finder = MissingNumberFinder(numbers_list)
            
            missing_number = finder.find_missing()

            return JsonResponse({
                'success': True,
                'missing_number': missing_number,
                'message': f"El número faltante es: {missing_number}"
            }, status=200) 

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Formato de petición JSON inválido.'
            }, status=400) 

        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e) 
            }, status=400) 

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ocurrió un error inesperado: {str(e)}'
            }, status=500) 
    else:
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido. Esta API solo acepta peticiones POST.'
        }, status=405) 
