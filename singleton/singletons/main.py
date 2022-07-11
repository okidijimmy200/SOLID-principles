# from containers import Readers, Client, Configs

# if __name__ == '__main__':
#     Configs.config.override({
#         'domain_name': 'imap.gmail.com',
#         'email_address': 'test@gmail.com',
#         'password': 'test123',
#         'mailbox': 'Inbox'
#     })
#     email_reader = Readers.email_reader()
#     print(email_reader.read('(SUBJECT TestSubject)'))

from containers import Readers, Clients, Configs

if __name__ == "__main__":
    Configs.config.override({
        "domain_name": "imap.gmail.com",
        "email_address": "YOUR_EMAIL_ADDRESS",
        "password": "YOUR_PASSWORD",
        "mailbox": "INBOX"
    })
    email_reader = Readers.email_reader()
    print(email_reader.read('(SUBJECT TestSubject)'))