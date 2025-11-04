from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ultimo_voto/<int:movil_id>/', views.ultimo_voto, name='ultimo_voto'),
    path('votos_bajos/<int:cliente_id>/', views.votos_bajos, name='votos_bajos'),
    #Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo:
    path('clientes_sin_votos/', views.clientes_sin_votos, name='clientes_sin_votos'),
    #Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”
    path('cuentas_bancarias/', views.cuentas_bancarias, name='cuentas_bancarias'),
    # Obtener los votos de los usuarios que hayan votado a partir del 2023 con una puntuación numérica igual a 5  y que tengan asociada una cuenta bancaria.
    path('votos_altos_con_cuenta/', views.votos_altos_con_cuenta, name='votos_altos_con_cuenta'),
    # Obtener todos los modelos principales que tengan una media de votaciones mayor del 2,5:
    path('modelos_media_alta/', views.modelos_media_alta, name='modelos_media_alta'),
    
    path('mostrar_nuevos/', views.mostrar_nuevos, name='mostrar_nuevos'),
    path('buscar_fabricante/', views.buscar_fabricante, name='buscar_fabricante'),
    path('videojuegos_sin_plataforma/', views.videojuegos_sin_plataforma, name='videojuegos_sin_plataforma'),
    path('analisis_estudio/<int:estudio_id>/', views.analisis_estudio, name='analisis_estudio'),
    path('videojuegos_estudio_media/<int:estudio_id>/', views.videojuegos_estudio_media, name='videojuegos_estudio_media'),
]