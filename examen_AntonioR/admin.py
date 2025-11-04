from django.contrib import admin

from .models import Videojuego, Plataforma, Estudio, VideojuegoPlataformas, Sede, Analisis


admin.site.register(Videojuego)
admin.site.register(Plataforma)
admin.site.register(Estudio)
admin.site.register(VideojuegoPlataformas)
admin.site.register(Sede)
admin.site.register(Analisis)
