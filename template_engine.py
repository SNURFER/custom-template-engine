import json

from template_store import TemplateStore
import json_walker


class TemplateEngine:
    def __init__(self, template_store: TemplateStore, users: json):
        # template file
        self.__template = template_store

        # data file json
        self.__users: json = users

        # accumulated line string
        # write to file and flush when line break is met
        self.__line_str: str = ''

        # output file descriptor
        self.__f = open("output.txt", "w")

        # accumulated string of template format
        # <? ?>
        self.__deque: str = ''

        self.__loop_flag: bool = False
        self.__loop_arr: [] = []
        self.__loop_template_str: str = ''

    def __del__(self):
        self.__f.close()

    def gen_code(self):
        for ch in self.__template.get_str():
            # jump to next loop if real line break exists
            # only user written '\n' will move to next line
            if ch != '\n':
                if not self.__loop_flag:
                    self.__write_line(ch, self.__users)
                else:
                    self.__write_loop_template(ch)

    def gen_code_user(self):
        for user in self.__users:
            for ch in self.__template.get_str():
                # jump to next loop if real line break exists
                # only user written '\n' will move to next line
                if ch != '\n':
                    if not self.__loop_flag:
                        self.__write_line(ch, user)
                    else:
                        self.__write_loop_template(ch)

    def __write_line(self, ch: str, users: json):
        if len(self.__deque) == 0 and ch != '<':
            self.__line_str += ch

        # accumulate template data when '<' is started
        elif ch == '<':
            self.__deque += ch

        # once deque has appended, just append ch to deque until end of template syntax '>' is found
        elif len(self.__deque) != 0:
            self.__deque += ch

            # read template string <?[input]?> and generate string with data
            if ch == '>':

                # deque syntax check. if the text is not <?[input]?> reset deque and append to __line_str
                if self.__deque[0:2] != '<?' or self.__deque[-2:] != '?>':
                    self.__line_str += ''.join(self.__deque)
                    self.__deque = ''

                # extract value from inline template. format is <?=[input]?>
                elif self.__deque[2] == '=':
                    input_str = self.__deque[3:-2].strip()
                    key_list = input_str.split('.')
                    parsed_str = json_walker.find_val(users, key_list[1:])
                    self.__line_str += parsed_str
                    self.__deque = ''

                # for loop mode. format is <? for [variable] in [array] ?>
                else:
                    input_str = self.__deque[2:-2].strip()
                    key_list = input_str.split()[-1].split('.')
                    self.__loop_arr = json_walker.find_arr(users, key_list[1:])
                    self.__loop_flag = True
                    self.__loop_template_str = ''
                    self.__deque = ''

        # write line to file immediately when line break character detected
        if self.__line_str[-2:] == '\\n':
            self.__line_str = self.__line_str[:-2]
            self.__f.write(self.__line_str + '\n')
            self.__line_str = ''

    def __write_loop_template(self, ch: str):
        self.__loop_template_str += ch
        if ch == '<':
            self.__deque += ch
        elif ch == '>':
            self.__deque += ch
            inline_str = self.__deque[2:-2].strip()
            if inline_str.find('endfor') != -1:
                self.__loop_flag = False
                self.__loop_template_str = self.__loop_template_str[:-len(self.__deque)]
                # TODO write for loop template str here
                # fixme
                self.__deque = ''
                for item in self.__loop_arr:
                    for ch in self.__loop_template_str:
                        if ch != '\n':
                            self.__write_line(ch, item)
            self.__deque = ''
        elif len(self.__deque) > 0:
            self.__deque += ch
