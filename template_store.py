class TemplateStore:
    def __init__(self):
        self.__f = open('input/template')
        self.__template_lines = self.__f.readlines()
        self.__template_str = ''.join(self.__template_lines)
        # "USER" does not have full information of iterating each user data
        # this is for exceptional case handling(template input has only "USER" not "USERS")
        self.__user_input = self.__template_str.find('USERS.') == -1

    def __del__(self):
        self.__f.close()

    def user_mode(self) -> bool:
        return self.__user_input

    def get_str(self) -> str:
        return self.__template_str
