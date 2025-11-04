from django.shortcuts import render
from .models import Movil, Votaciones, Cliente, Banco, Videojuego
from django.db.models import Avg
from django.db.models import Q
from django.views.defaults import page_not_found

# Create your views here.
def home(request):
    return render(request, 'examen_AntonioR/home.html')

def ultimo_voto(request, movil_id):
    votaciones = Votaciones.objects.select_related('cliente', 'movil')
    votaciones = Votaciones.objects.filter(movil__id=movil_id).order_by('-fecha_votacion')
    votaciones = votaciones.all()

    #votaciones = Votaciones.objects.raw('''
    #   SELECT * FROM examen_AntonioR_votaciones v
    #   INNER JOIN examen_AntonioR_movil m ON v.movil_id = m.id
    #   INNER JOIN examen_AntonioR_cliente c ON v.cliente_id = c.id
    #   WHERE m.id = %s
    #   ORDER BY v.fecha_votacion DESC
    #   , [movil_id])[:51]

    return render(request, 'examen_AntonioR/ultimo_voto.html' , {'votaciones': votaciones})

def votos_bajos(request, cliente_id):
    votaciones = (
        Votaciones.objects
        .select_related('cliente', 'movil')
        .filter(cliente__id=cliente_id, puntuacion__lt=3)
        .all()
    )

    #votaciones = Votaciones.objects.raw('''
    #   SELECT * FROM examen_AntonioR_votaciones v
    #   INNER JOIN examen_AntonioR_movil m ON v.movil_id = m.id
    #   INNER JOIN examen_AntonioR_cliente c ON v.cliente_id = c.id
    #   WHERE c.id = %s AND v.puntuacion < 3
    #   ORDER BY v.fecha_votacion ASC
    #   , [cliente_id])[:19]

    return render(request, 'examen_AntonioR/votos_bajos.html' , {'votaciones': votaciones})

def clientes_sin_votos(request):
    from .models import Cliente
    clientes = (
        Cliente.objects
        .filter(votaciones_movil__isnull=True)
        .all()
    )
    
    #clientes = Cliente.objects.raw('''
    #   SELECT * FROM examen_AntonioR_cliente c
    #   LEFT JOIN examen_AntonioR_votaciones v ON c.id = v.cliente_id
    #   WHERE v.id IS NULL
    #   ''')
    
    return render(request, 'examen_AntonioR/clientes_sin_votos.html', {'clientes': clientes})

def cuentas_bancarias(request):
    cuentas = (
        Banco.objects
        .filter(nombre__in=['CaixaBank', 'Unicaja'], cliente_banco__nombre__icontains='Juan')
        .all()
    )
    
    #cuentas = Banco.objects.raw('''
    #   SELECT b.* FROM examen_AntonioR_banco b
    #   INNER JOIN examen_AntonioR_cliente c ON b.id = c.banco_id
    #   WHERE b.nombre IN ('CaixaBank', 'Unicaja') AND c.nombre LIKE %s
    #   ''', ['%Juan%'])
    
    return render(request, 'examen_AntonioR/cuentas_bancarias.html', {'cuentas': cuentas})

def votos_altos_con_cuenta(request):

    votaciones = (
        Votaciones.objects
        .select_related('cliente', 'movil')
        .filter(puntuacion=5, fecha_votacion__gte='2023-01-01', cliente__banco__isnull=False)
        .all()
    )
    
    #votaciones = Votaciones.objects.raw('''
    #   SELECT v.* FROM examen_AntonioR_votaciones v
    #   INNER JOIN examen_AntonioR_cliente c ON v.cliente_id = c.id
    #   INNER JOIN examen_AntonioR_banco b ON c.banco_id = b.id
    #   WHERE v.puntuacion = 5 AND v.fecha_votacion >= '2023-01-01' AND b.id IS NOT NULL
    #   ''')

    return render(request, 'examen_AntonioR/votos_altos_con_cuenta.html', {'votaciones': votaciones})

def modelos_media_alta(request):
    modelos = (
        Votaciones.objects
        .select_related('cliente')
        .select_related('movil')
        .annotate(media_votacion=Avg('puntuacion'))
        .filter(media_votacion__gt=2.5)
        .all()
    )
    #modelos = Votaciones.objects.raw('''
     #   SELECT m.id, m.modelo, AVG(v.puntuacion) as media_votacion
      #  FROM examen_AntonioR_votaciones v
       # INNER JOIN examen_AntonioR_movil m ON v.movil_id = m.id
        #GROUP BY m.id, m.modelo
        #HAVING AVG(v.puntuacion) > 2.5
    #''')
    
    return render(request, 'examen_AntonioR/modelos_media_alta.html', {'modelos': modelos})

def mostrar_nuevos(request):
    #    SELECT 
    #    V.*,E.*,VP.*,P.*
    #FROM 
    #    videojuego V
    #INNER JOIN 
     #   estudio E ON V.estudio_desarrollo_id = E.id
    #INNER JOIN 
     #   sede S ON E.id = S.estudio_id
    #LEFT JOIN 
    #    videojuego_plataformas VP ON V.id = VP.videojuego_id
    #LEFT JOIN
    #    plataforma P ON VP.plataforma_id = P.id
    #LEFT JOIN
    #    analisis A ON V.id = A.videojuego_id
    #WHERE 
    #    V.titulo LIKE '%Fantasy%' 
    #    AND S.pais LIKE '%Unidos%';
    
    videos = (
        Videojuego.objects
        .select_related('estudio_desarrollo')
        .prefetch_related('plataformas')
        .filter(
            Q(titulo__icontains='Fantasy') &
            Q(estudio_desarrollo__estudio_sedes__pais__icontains='Unidos')
        )
        .all()
    )

    return render(request, 'examen_AntonioR/mostrar_nuevos.html', {'videojuegos': videos})



def mi_error_404(request, exception=None):
    return render(request, 'examen_AntonioR/errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'examen_AntonioR/errores/500.html', None, None, 500)

def mi_error_403(request, exception=None):
    return render(request, 'examen_AntonioR/errores/403.html', None, None, 403)

def mi_error_400(request, exception=None):
    return render(request, 'examen_AntonioR/errores/400.html', None, None, 400)