from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects_images/')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title if self.title else f"Project {self.pk}"

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-created']


class Company(models.Model):
    company_id = models.CharField(max_length=24, unique=True, primary_key=True)
    company_name = models.CharField(max_length=130, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_id})" if self.company_name else f"Company {self.company_id}"

    class Meta:
        verbose_name = "Compañía"
        verbose_name_plural = "Compañías"


class Charges(models.Model):
    charge_id = models.CharField(max_length=24, unique=True, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='charges')
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=30)
    created_at = models.DateField()
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Cargo {self.charge_id} de {self.company.company_name} - ${self.amount:.2f}"

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['-created_at']
