import math
class glue:
    def __init__(self, glue, type):
        self.glue = glue
        self.type = type

    def describe_glue_info(self):
        #data base 정보 가져오기
        glue_database_list = self.glue.get_databases()

        print('-------glue---------')
        #print(glue_database_list)

        for glue_database_info in glue_database_list['DatabaseList']:
            glue_database_list = self.glue.get_tables(DatabaseName=glue_database_info['Name'])

            print(glue_database_list)

        #lambda_list = self.glue.get_tables()
        result = []

        # for lambda_info in glue_database_list['Functions']:
        #
        #     fun_name = lambda_info['FunctionName']
        #     runtime = lambda_info['Runtime']
        #     description = lambda_info['Description']
        #     handler = lambda_info['Handler']
        #     timeout = lambda_info['Timeout']
        #     u_description = ''
        #
        #     result.append((fun_name, description, runtime, handler, timeout, u_description))

        return result