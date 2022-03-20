import json

from template_store import TemplateStore
import json_walker


# TODO syntax check
# This engine writes every individual user data to template.
# Assume that USERS and USER template inputs do not exist in the same file.
class TemplateEngine:
    def __init__(self, template_store: TemplateStore, users: json):
        self.template = template_store
        self.users: json = users
        self.line_str: str = ''
        self.f = open("output.txt", "w")
        self.deque: str = ''

        self.loop_flag: bool = False
        self.loop_arr: [] = []
        self.loop_template_str: str = ''

    def __del__(self):
        self.f.close()

    def gen_code(self):
        for ch in self.template.get_str():
            # jump to next loop if real line break exists
            # only user written '\n' will move to next line
            if ch != '\n':
                if not self.loop_flag:
                    self.write_line(ch, self.users)
                else:
                    self.write_loop_template(ch)

    def write_line(self, ch: str, users: json):
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
                if self.deque[2] == '=':
                    # access directly to data
                    inline_str = self.deque[3:-2].strip()
                    inline_list = inline_str.split('.')
                    parsed_str = json_walker.find_val(users, inline_list[1:])
                    self.line_str += parsed_str
                    self.deque = ''

                else:
                    # for loop mode
                    inline_str = self.deque[2:-2].strip()
                    inline_list = inline_str.split(' ')
                    inline_list2 = inline_list[-1].split('.')
                    self.loop_arr = json_walker.find_arr(users, inline_list2[1:])
                    self.loop_flag = True
                    self.loop_template_str = ''
                    self.deque = ''

        # write line to file immediately when line break character detected
        if self.line_str[-2:] == '\\n':
            self.line_str = self.line_str[:-2]
            self.f.write(self.line_str + '\n')
            self.line_str = ''

    def write_loop_template(self, ch: str):
        self.loop_template_str += ch
        if ch == '<':
            self.deque += ch
        elif ch == '>':
            self.deque += ch
            inline_str = self.deque[2:-2].strip()
            if inline_str.find('endfor') != -1:
                self.loop_flag = False
                self.loop_template_str = self.loop_template_str[:-len(self.deque)]
                # TODO write for loop template str here
                # fixme
                self.deque = ''
                for item in self.loop_arr:
                    for ch in self.loop_template_str:
                        if ch != '\n':
                            self.write_line(ch, item)

            self.deque = ''
        elif len(self.deque) > 0:
            self.deque += ch
