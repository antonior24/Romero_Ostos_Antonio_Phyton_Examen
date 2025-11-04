from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelos de tienda de móviles

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Many to One con Marca, y relacion many to one con Votaciones

class Movil(models.Model):
    modelo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='marca_movil')

    def __str__(self):
        return f"{self.modelo} - {self.marca.nombre}"

class Banco(models.Model):
    NOMBRE = [
        ('BBVA', 'BBVA'),
        ('Santander', 'Santander'),
        ('CaixaBank', 'CaixaBank'),
        ('Bankia', 'Bankia'),
        ('Sabadell', 'Sabadell'),
    ]
    
    numero_cuenta = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50, choices=NOMBRE, default='BBVA')

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    banco = models.OneToOneField(Banco, on_delete=models.CASCADE, related_name='cliente_banco')
    votaciones_movil = models.ManyToManyField(Movil, through='Votaciones', related_name='cliente_votaciones', blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Votaciones, para los comentarios y valoraciones de los móviles

class Votaciones(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    movil = models.ForeignKey(Movil, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)
    fecha_votacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Puntuación: {self.puntuacion}"
    
# Modelos de videojuegos

class Plataforma(models.Model):
    nombre = models.CharField(max_length=50)
    Fabricante = [
        ('Sony', 'Sony'),
        ('Microsoft', 'Microsoft'),
        ('Nintendo', 'Nintendo'),
        ('PC', 'PC'),
        ('Apple', 'Apple'),
    ]
    fabricante = models.CharField(max_length=50, choices=Fabricante, default='Estados Unidos')

    def __str__(self):
        return self.nombre
    
class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    estudio_desarrollo = models.ForeignKey('Estudio', on_delete=models.CASCADE, related_name='estudio_videojuegos')
    plataformas = models.ManyToManyField(Plataforma, through='VideojuegoPlataformas', related_name='videojuegos')
    ventas_estimadas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Estudio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Sede(models.Model):
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE, related_name='estudio_sedes')
    PAIS = [
        ('Estados Unidos', 'Estados Unidos'),
        ('Reino Unido', 'Reino Unido'),
        ('Japón', 'Japón'),
        ('Canadá', 'Canadá'),
        ('Alemania', 'Alemania'),
        ('España', 'España'),
    ]
    pais = models.CharField(max_length=50, choices=PAIS, default='Estados Unidos')

class VideojuegoPlataformas(models.Model):
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.videojuego.titulo}"

#SELECT 
 #   V.*,E.*,VP.*,P.*
#FROM 
 #   videojuego V
#INNER JOIN 
   # videojuego_plataformas VP ON V.id = VP.videojuego_id
#INNER JOIN 
  #  plataforma P ON VP.plataforma_id = P.id
#INNER JOIN
  #  analisis A ON V.id = A.videojuego_id
#INNER JOIN 
  #  estudio E ON V.estudio_desarrollo_id = E.id
#LEFT JOIN
 #   sede S ON E.id = S.estudio_id
#WHERE 
#    P.fabricante LIKE 'Sony' 
 #   OR p.nombre LIKE ‘%Play Station%’ 
 #   AND A.puntuacion > 75
#LIMIT 3

class Analisis(models.Model):
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE, related_name='analisis_videojuego')
    puntuacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    review = models.TextField()
    anyo_publicacion = models.DateField( null=True, blank=True)

    def __str__(self):
        return f"Análisis de {self.videojuego.titulo} - Puntuación: {self.puntuacion}"
    
#SELECT 
#    V.*
#FROM 
#    videojuego V
#LEFT JOIN 
#    videojuego_plataformas VP ON V.id = VP.videojuego_id
#WHERE 
#    VP.id IS NULL
#ORDER BY v.ventas_estimadas DESC