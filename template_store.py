class TemplateStore:
    def __init__(self):
        self.__f = open('input/template')
        self.__template_lines = self.__f.readlines()
        self.__template_str = ''.join(self.__template_lines)
        # TODO FIXME
        # this approach should be verified again
        # "USER" does not have full information of iterating each user data
        self.__user_input = self.__template_str.find('USERS.') == -1

    def __del__(self):
        self.__f.close()

    def user_mode(self) -> bool:
        return self.__user_input

    def get_str(self) -> str:
        return self.__template_str
