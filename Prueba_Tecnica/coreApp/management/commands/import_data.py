import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from coreApp.models import Company, Charges 

class Command(BaseCommand):
    help = 'Importa datos de transacciones desde un archivo CSV a la base de datos Django.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta al archivo CSV de transacciones.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(self.style.SUCCESS(f"Iniciando importación desde: {csv_file_path}"))

        date_formats = ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y-%m-%dT%H:%M:%S', '%Y%m%d')

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                charges_to_create = []
                companies_map = {}

                # --- DEBUGGING: Imprimir los encabezados que DictReader está detectando ---
                self.stdout.write(self.style.NOTICE(f"Encabezados detectados por DictReader: {reader.fieldnames}"))

                with transaction.atomic():
                    for row in reader:
                        # --- DEBUGGING: Imprimir la fila completa tal como la lee DictReader ---
                        self.stdout.write(self.style.NOTICE(f"Fila CSV cruda: {row}"))

                        charge_id = row.get('id', '').strip()
                        company_name_from_csv = row.get('name', '').strip()
                        company_id = row.get('company_id', '').strip()
                        amount_str = row.get('amount', '').strip()
                        status = row.get('status', '').strip()
                        created_at_str = row.get('created_at', '').strip()
                        paid_at_str = row.get('paid_at', '').strip()


                        # Validar campos estrictamente obligatorios antes de procesar

                        if not all([charge_id, company_id]):
                            self.stderr.write(self.style.WARNING(f"Saltando fila con datos incompletos (campos obligatorios): {row}"))
                            continue

                        try:
                            # Manejo más robusto para el monto
                            amount = Decimal('0.00') # Valor por defecto si hay un problema
                            if amount_str.lower() in ['inf', '-inf', 'nan', '']:
                                self.stderr.write(self.style.WARNING(f"Monto '{amount_str}' no es un número válido. Estableciendo a 0.00 para fila '{charge_id}'."))
                            else:
                                try:
                                    amount = Decimal(amount_str)
                                except InvalidOperation:
                                    self.stderr.write(self.style.ERROR(f"Error de conversión de monto '{amount_str}'. Estableciendo a 0.00 para fila '{charge_id}'."))
                                    amount = Decimal('0.00') # Asegura que no detenga la importación
                            
                            created_at = None
                            for fmt in date_formats:
                                try:
                                    created_at = datetime.strptime(created_at_str, fmt).date()
                                    break
                                except ValueError:
                                    pass
                            if created_at is None:
                                raise ValueError(f"Formato de fecha 'created_at' desconocido o vacío: {created_at_str}")

                            paid_at = None
                            if paid_at_str:
                                for fmt in date_formats:
                                    try:
                                        paid_at = datetime.strptime(paid_at_str, fmt).date()
                                        break
                                    except ValueError:
                                        pass
                                if paid_at is None:
                                    self.stderr.write(self.style.WARNING(f"Formato de fecha 'paid_at' desconocido, se establecerá como nulo: {paid_at_str}"))

                        except ValueError as e: # Este catch es ahora principalmente para errores de fecha
                            self.stderr.write(self.style.ERROR(f"Error de formato crítico en fila '{charge_id}': {e} - Fila: {row}"))
                            continue

                        if company_id not in companies_map:
                            inferred_company_name = company_name_from_csv 

                            if company_id == 'cbf1c8b09cd5b549416d49d220a40cbd317f952e': 
                                inferred_company_name = 'MiPasajefy'
                            elif company_id == '8f642dc67fccf861548dfe1c761ce22f795e91f0':
                                inferred_company_name = 'Muebles chidos'
                            else:
                                inferred_company_name = 'Desconocido' 

                            company_obj, created = Company.objects.get_or_create(
                                company_id=company_id,
                                defaults={'company_name': inferred_company_name}
                            )
                            companies_map[company_id] = company_obj
                        else:
                            company_obj = companies_map[company_id]

                        charge_obj = Charges(
                            charge_id=charge_id,
                            company=company_obj,
                            amount=amount,
                            status=status,
                            created_at=created_at,
                            updated_at=paid_at
                        )
                        charges_to_create.append(charge_obj)

                    Charges.objects.bulk_create(charges_to_create, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Importación completada. {len(charges_to_create)} cargos procesados."))

        except FileNotFoundError:
            raise CommandError(f'El archivo CSV "{csv_file_path}" no fue encontrado.')
        except Exception as e:
            raise CommandError(f'Ocurrió un error durante la importación: {e}')