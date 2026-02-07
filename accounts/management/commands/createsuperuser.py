"""
Custom createsuperuser command that enforces only ONE superuser
and properly handles the unique_id field
"""
from django.core.management.base import CommandError
from django.contrib.auth.management.commands.createsuperuser import Command as SuperuserCommand
from accounts.models import CustomUser


class Command(SuperuserCommand):
    help = 'Create a superuser with ADMIN role (Only ONE superuser allowed)'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Add unique_id as a command line argument
        parser.add_argument(
            '--unique_id',
            dest='unique_id',
            default=None,
            help='Specifies the unique ID (Roll No / Employee ID) for the superuser.',
        )

    def handle(self, *args, **options):
        # Check if a superuser already exists
        existing_superuser = CustomUser.objects.filter(is_superuser=True).first()
        
        if existing_superuser:
            raise CommandError(
                f'\n❌ ERROR: A superuser already exists!\n'
                f'   Username: {existing_superuser.username}\n'
                f'   Email: {existing_superuser.email}\n'
                f'   Unique ID: {existing_superuser.unique_id}\n'
                f'   Created: {existing_superuser.created_at}\n\n'
                f'Only ONE superuser is allowed in this system.\n'
                f'The superuser has ADMIN role with full system access.\n\n'
                f'To create additional admin users, login as the superuser and use:\n'
                f'  - Admin Dashboard > User Management > Create User\n'
                f'  - Set role to "ADMIN" for admin privileges\n'
            )
        
        # Get unique_id from options or prompt for it
        unique_id = options.get('unique_id')
        database = options.get('database')
        
        # If not provided via command line and not in non-interactive mode, prompt for it
        if not unique_id and not options.get('interactive', True) is False:
            unique_id = input('Unique ID (Roll No / Employee ID): ')
        
        # If still no unique_id, use username as default
        if not unique_id:
            unique_id = options.get('username', 'ADMIN001')
        
        # Store unique_id in options so it gets passed to create_superuser
        options['unique_id'] = unique_id
        
        # Proceed with superuser creation
        self.stdout.write(self.style.SUCCESS('\n✅ Creating the FIRST and ONLY superuser...\n'))
        self.stdout.write(self.style.WARNING('This superuser will have ADMIN role with full system access.\n'))
        
        # Get username, email, password from options or prompt
        username = options.get('username')
        email = options.get('email')
        
        if not username:
            username = input('Username: ')
        if not email:
            email = input('Email address: ')
        
        # Get password
        password = None
        if not options.get('interactive', True) is False:
            import getpass
            while password is None:
                password = getpass.getpass('Password: ')
                password2 = getpass.getpass('Password (again): ')
                if password != password2:
                    self.stderr.write("Error: Your passwords didn't match.")
                    password = None
                    continue
                if password.strip() == '':
                    self.stderr.write("Error: Blank passwords aren't allowed.")
                    password = None
                    continue
        
        # Create the superuser
        try:
            user_data = {
                'username': username,
                'email': email,
                'unique_id': unique_id,
            }
            
            user = CustomUser._default_manager.db_manager(database).create_superuser(
                **user_data,
                password=password
            )
            
            self.stdout.write(self.style.SUCCESS('\n✅ Superuser created successfully!'))
            self.stdout.write(self.style.SUCCESS(f'   Username: {user.username}'))
            self.stdout.write(self.style.SUCCESS(f'   Email: {user.email}'))
            self.stdout.write(self.style.SUCCESS(f'   Unique ID: {user.unique_id}'))
            self.stdout.write(self.style.SUCCESS(f'   Role: {user.role}'))
            self.stdout.write(self.style.SUCCESS('   Access: Full system access\n'))
            
        except Exception as e:
            raise CommandError(f'Error creating superuser: {e}')
