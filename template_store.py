# this approach should be verified again
# "USER" does not have full information of iterating each user data
class TemplateStore:
    def __init__(self):
        f = open('input/template')
        self.template_lines = f.readlines()
        self.template_str = ''.join(self.template_lines)
        # TODO FIXME
        self.user_input = self.template_str.find('USERS.') == -1

    def user_mode(self) -> bool:
        return self.user_input

    def get_str(self) -> str:
        return self.template_str
