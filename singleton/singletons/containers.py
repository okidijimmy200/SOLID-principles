# from http import client
# from dependency_injector import providers, containers
# from email_client import EmailClient
# from email_reader import EmailReader


# class Configs(containers.DeclarativeContainer):
#     config = providers.Configuration('config')

# class Client(containers.DeclarativeContainer):
#     '''This class is a container defining all kinds of clients. 
#     EmailClient is created with a singleton provider, asserting a single instance of this class, and defining its dependency on the config objec'''
#     email_client = providers.Singleton(EmailClient, Configs.config)

# class Readers(containers.DeclarativeContainer):
#     email_reader = providers.Factory(EmailReader, client=Client.email_client)

from dependency_injector import providers, containers
from email_client import EmailClient
from email_reader import EmailReader

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    # other configs
    
class Clients(containers.DeclarativeContainer):
    email_client = providers.Singleton(EmailClient, Configs.config)
    # other clients
    
class Readers(containers.DeclarativeContainer):
    email_reader = providers.Factory(EmailReader, client=Clients.email_client)
    # other readers