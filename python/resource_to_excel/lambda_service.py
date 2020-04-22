import math
class c_lambda:
    def __init__(self, c_lambda):
        self.c_lambda = c_lambda

    def describe_lambda_info(self):

        lambda_list = self.c_lambda.list_functions()
        result = []

        for lambda_info in lambda_list['Functions']:

            fun_name = lambda_info['FunctionName']
            runtime = lambda_info['Runtime']
            description = lambda_info['Description']
            handler = lambda_info['Handler']
            timeout = lambda_info['Timeout']
            u_description = ''

            result.append((fun_name, description, runtime, handler, timeout, u_description))

        return result