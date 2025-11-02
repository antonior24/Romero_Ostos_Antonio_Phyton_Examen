from django.contrib import admin
from .models import Marca, Movil, Votaciones, Cliente, Banco

# Register your models here.
admin.site.register(Marca)
admin.site.register(Movil)
admin.site.register(Votaciones)
admin.site.register(Cliente)
admin.site.register(Banco)
