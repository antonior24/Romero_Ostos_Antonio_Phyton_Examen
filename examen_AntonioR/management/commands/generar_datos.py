from django.core.management.base import BaseCommand
from examen_AntonioR.models import Marca, Movil, Banco, Cliente, Votaciones
from faker import Faker
import random

class Command(BaseCommand):
    help = "Genera datos falsos coherentes para el examen"

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')

        # Limpiamos tablas para no duplicar datos en cada ejecución
        Votaciones.objects.all().delete()
        Cliente.objects.all().delete()
        Movil.objects.all().delete()
        Marca.objects.all().delete()
        Banco.objects.all().delete()

        self.stdout.write(self.style.WARNING("Datos anteriores eliminados."))

        # Crear Bancos
        bancos = []
        NOMBRE = ['Caixa', 'BBVA', 'UNICAJA', 'ING']
        for _ in range(10):
            banco = Banco.objects.create(
                numero_cuenta=fake.iban(),
                nombre=random.choice(NOMBRE)
            )
            bancos.append(banco)

        self.stdout.write(self.style.SUCCESS(f"{len(bancos)} bancos creados."))

        # Crear Marcas
        marcas = []
        for _ in range(5):
            marca = Marca.objects.create(nombre=fake.company())
            marcas.append(marca)

        self.stdout.write(self.style.SUCCESS(f"{len(marcas)} marcas creadas."))

        # Crear Móviles
        moviles = []
        for _ in range(15):
            movil = Movil.objects.create(
                modelo=fake.word().capitalize(),
                precio=round(random.uniform(100, 1200), 2),
                stock=random.randint(0, 50),
                marca=random.choice(marcas)
            )
            moviles.append(movil)

        self.stdout.write(self.style.SUCCESS(f"{len(moviles)} móviles creados."))

        # Crear Clientes (uno por banco)
        clientes = []
        for banco in bancos:
            cliente = Cliente.objects.create(
                nombre=fake.name(),
                email=fake.unique.email(),
                banco=banco
            )
            clientes.append(cliente)

        self.stdout.write(self.style.SUCCESS(f"{len(clientes)} clientes creados."))

        # Crear Votaciones (cada cliente vota 1 a 3 móviles)
        votos_total = 0
        for cliente in clientes:
            num_votos = random.randint(1, 3)
            moviles_votados = random.sample(moviles, num_votos)
            for movil in moviles_votados:
                Votaciones.objects.create(
                    cliente=cliente,
                    movil=movil,
                    puntuacion=random.randint(1, 5),
                    comentario=fake.sentence(nb_words=8)
                )
                votos_total += 1

        self.stdout.write(self.style.SUCCESS(f"{votos_total} votaciones creadas correctamente."))
        self.stdout.write(self.style.SUCCESS("✅ Datos generados correctamente con Faker."))
