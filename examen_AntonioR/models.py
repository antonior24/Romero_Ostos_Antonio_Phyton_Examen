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