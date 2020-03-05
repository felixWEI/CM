import os
import datetime


class MyLogger(object):

    def __init__(self):
        self.current_file_path = os.path.abspath(__file__)
        self.logger_path = os.path.join(self.current_file_path.split('Info_Manage')[0], 'Log')

        if not os.path.exists(self.logger_path):
            os.makedirs(self.logger_path)

    def log_info(self, module, message):
        log_file_name = os.path.join(self.logger_path, module+'.log')
        log_format = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file_name, 'a') as file_module:
                file_module.write(log_format+' - '+message+'\n')


    def data_operate_log(self, user, message):
        log_file_name = os.path.join(self.logger_path,'database_operate_history.log')
        log_format = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file_name, 'a') as file_module:
                file_module.write(log_format+' - '+user+' - '+message+'\n')

