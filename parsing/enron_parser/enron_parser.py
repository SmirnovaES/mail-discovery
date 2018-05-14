import mails_table
import users_table


class Parser:

    def __init__(self, file_name):
        self.file_name = file_name

    def create_database(self):
        mails_table.create_mails_table(self.file_name)
        users_table.create_users_table(self.file_name)


"""parser = Parser('/home/david/почта/enron/emails.csv')
parser.create_database()"""
