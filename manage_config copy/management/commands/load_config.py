from django.core.management.base import BaseCommand
from django.conf import settings
from cards.models import Buff, Effect


class Command(BaseCommand):
    help = 'Loads the initial configuration of Buffs and Effects from environment variables'

    def handle(self, *args, **options):
        config = settings.CARD_EDITOR_CONFIG

        # Load Buffs from configuration
        available_buffs = config.get('AVAILABLE_BUFFS', [])
        for buff_name in available_buffs:
            buff, created = Buff.objects.get_or_create(
                name=buff_name,
                defaults={
                    'description': f'Buff: {buff_name}',
                    'attributes': []  # Must be filled in manually or with another script
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Buff "{buff_name}" created')
                )
            else:
                self.stdout.write(f'  Buff "{buff_name}" already exists')

        # Load Effects from configuration
        available_effects = config.get('AVAILABLE_EFFECTS', [])
        for effect_name in available_effects:
            effect, created = Effect.objects.get_or_create(
                name=effect_name,
                defaults={
                    'description': f'Effect: {effect_name}',
                    'attributes': []  # Must be filled in manually or with another script
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Effect "{effect_name}" created')
                )
            else:
                self.stdout.write(f'  Effect "{effect_name}" already exists')

        self.stdout.write(
            self.style.SUCCESS('\n✓ Configuration loaded successfully')
        )
        self.stdout.write(
            self.style.WARNING(
                '\nNOTE: Buff and Effect attributes must be defined '
                'manually in Django Admin with structure: [{"name": str, "type": str}, ...]'
            )
        )
