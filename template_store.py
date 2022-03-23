class TemplateStore:
    def __init__(self):
        self.__f = open('input/template')
        self.__template_str = ''.join(self.__f.readlines())

    def __del__(self):
        self.__f.close()

    def get_str(self) -> str:
        return self.__template_str
