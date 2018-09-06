from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        # signals are imported, so that they are defined and can be used
        import accounts.signal_handler
