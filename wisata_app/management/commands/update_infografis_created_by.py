from django.core.management.base import BaseCommand
from wisata_app.models import Infografis, Master_User

class Command(BaseCommand):
    help = 'Update existing infografis records with created_by field'

    def handle(self, *args, **kwargs):
        # Get the first super admin user
        super_admin = Master_User.objects.filter(role='super_admin').first()
        
        if not super_admin:
            self.stdout.write(self.style.ERROR('No super admin user found!'))
            return
            
        # Update all infografis records that don't have created_by
        updated = Infografis.objects.filter(created_by__isnull=True).update(created_by=super_admin)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated} infografis records')) 