import collections
import json

from template_store import TemplateStore
import json_walker


# TODO syntax check
# This engine writes every individual user data to template.
# Assume that USERS and USER template inputs do not exist in the same file.
class UserEngine:
    def __init__(self, template_store: TemplateStore, users: json):
        self.template = template_store
        self.users: json = users
        self.line_str: str = ''
        self.f = open("output.txt", "w")
        self.deque: str = ''

    def __del__(self):
        self.f.close()

    def gen_code(self):
        for user in self.users:
            for ch in self.template.get_str():
                # jump to next loop if real line break exists
                # only user written '\n' will move to next line
                if ch != '\n':
                    self.write_line(ch, user)

    def write_line(self, ch: str, user: json):
        if len(self.deque) == 0 and ch != '<':
            self.line_str += ch

        # accumulates template data when '<' is started
        elif ch == '<':
            self.deque += ch
        # once deque has appended, just append ch to deque until end of template syntax '>' is found
        elif len(self.deque) != 0:
            self.deque += ch
            # read the inline template input <?[input]?> and generate string with user data
            if ch == '>':
                inline_str = self.deque[3:-2].strip()
                inline_list = inline_str.split('.')
                parsed_str = json_walker.find_val(user, inline_list[1:])
                self.line_str += parsed_str
                self.deque = ''

        # write line to file immediately when line break character detected
        if self.line_str[-2:] == '\\n':
            self.line_str = self.line_str[:-2]
            self.f.write(self.line_str + '\n')
            self.line_str = ''


