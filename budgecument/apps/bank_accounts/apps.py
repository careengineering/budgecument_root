from django.apps import AppConfig

class BankAccountsConfig(AppConfig):
    name = 'apps.bank_accounts'

    def ready(self):
        import apps.common.signals
