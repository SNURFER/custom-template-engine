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
        self.__pattern_str: str = ''

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
        if len(self.__pattern_str) == 0 and ch != '<':
            self.__line_str += ch

        # accumulate template data when '<' is started
        elif ch == '<':
            self.__pattern_str += ch

        # once __pattern_str has appended, just append ch to __pattern_str until end of template syntax '>' is found
        elif len(self.__pattern_str) != 0:
            self.__pattern_str += ch

            # read template string <?INPUT?> and generate string with data
            if ch == '>':

                # syntax check.
                # if pattern is not <?INPUT?> flush __pattern_str and append to __line_str.
                if self.__pattern_str[0:2] != '<?' or self.__pattern_str[-2:] != '?>':
                    self.__line_str += self.__pattern_str
                    self.__pattern_str = ''

                # extract value from template variable. format is <?=VARIABLE?>
                elif self.__pattern_str[2] == '=':
                    variable_str = self.__pattern_str[3:-2].strip()
                    key_list = variable_str.split('.')
                    parsed_str = json_walker.find_val(users, key_list[1:])
                    self.__line_str += parsed_str
                    self.__pattern_str = ''

                # for loop mode. format is <? for [variable] in [array] ?>
                elif self.__pattern_str[2:-2].strip().split()[0] == 'for':
                    for_str = self.__pattern_str[2:-2].strip()
                    key_list = for_str.split()[-1].split('.')
                    self.__loop_arr = json_walker.find_arr(users, key_list[1:])
                    self.__loop_flag = True
                    self.__loop_template_str = ''
                    self.__pattern_str = ''

                # error syntax
                else:
                    self.__line_str += '?'
                    self.__pattern_str = ''

        # write line to file immediately when line break character detected
        if self.__line_str[-2:] == '\\n':
            self.__line_str = self.__line_str[:-2]
            self.__f.write(self.__line_str + '\n')
            self.__line_str = ''

    def __write_loop_template(self, ch: str):
        self.__loop_template_str += ch
        if ch == '<':
            self.__pattern_str += ch
        elif ch == '>':
            self.__pattern_str += ch
            inline_str = self.__pattern_str[2:-2].strip()
            if inline_str.find('endfor') != -1:
                self.__loop_flag = False
                self.__loop_template_str = self.__loop_template_str[:-len(self.__pattern_str)]
                # TODO write for loop template str here
                # fixme
                self.__pattern_str = ''
                for item in self.__loop_arr:
                    for ch in self.__loop_template_str:
                        if ch != '\n':
                            self.__write_line(ch, item)
            self.__pattern_str = ''
        elif len(self.__pattern_str) > 0:
            self.__pattern_str += ch
