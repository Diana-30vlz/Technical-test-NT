from django.db import models

# Create your models here.
from django.db import models

class Company(models.Model):
    company_id = models.CharField(max_length=40, unique=True, primary_key=True)
    company_name = models.CharField(max_length=130, blank=True, null=True)

    def __str__(self): 
        return f"{self.company_name}"

    class Meta:
        verbose_name = "Compañía"
        verbose_name_plural = "Compañías"


class Charges(models.Model):
    charge_id = models.CharField(max_length=40, unique=True, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='charges')
    amount = models.DecimalField(max_digits=200, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=30,blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.charge_id} de {self.company.company_name}"

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['-created_at']