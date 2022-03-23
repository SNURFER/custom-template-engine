class TemplateStore:
    def __init__(self, template_path: str):
        self.__f = open(template_path)
        self.__template_str = ''.join(self.__f.readlines())

    def __del__(self):
        self.__f.close()

    def get_str(self) -> str:
        return self.__template_str
