from django.core.management.base import BaseCommand
from django.conf import settings
from cartas.models import Buff, Efecto


class Command(BaseCommand):
    help = 'Carga la configuración inicial de Buffs y Efectos desde variables de entorno'

    def handle(self, *args, **options):
        config = settings.CARD_EDITOR_CONFIG

        # Cargar Buffs desde configuración
        buffs_disponibles = config.get('AVAILABLE_BUFFS', [])
        for buff_name in buffs_disponibles:
            buff, created = Buff.objects.get_or_create(
                name=buff_name,
                defaults={
                    'description': f'Buff: {buff_name}',
                    'atributos': []  # Se deben llenar manualmente o con otro script
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Buff "{buff_name}" creado')
                )
            else:
                self.stdout.write(f'  Buff "{buff_name}" ya existe')

        # Cargar Efectos desde configuración
        efectos_disponibles = config.get('AVAILABLE_EFFECTS', [])
        for efecto_name in efectos_disponibles:
            efecto, created = Efecto.objects.get_or_create(
                name=efecto_name,
                defaults={
                    'description': f'Efecto: {efecto_name}',
                    'atributos': []  # Se deben llenar manualmente o con otro script
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Efecto "{efecto_name}" creado')
                )
            else:
                self.stdout.write(f'  Efecto "{efecto_name}" ya existe')

        self.stdout.write(
            self.style.SUCCESS('\n✓ Configuración cargada exitosamente')
        )
        self.stdout.write(
            self.style.WARNING(
                '\nNOTA: Los atributos de Buffs y Efectos deben ser definidos '
                'manualmente en Django Admin con estructura: [{"nombre": str, "tipo": str}, ...]'
            )
        )
