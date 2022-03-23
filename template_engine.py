import json

from template_store import TemplateStore
import json_walker


class TemplateEngine:
    def __init__(self, template_store: TemplateStore, users: json):
        # template file
        self.__template = template_store

        # data file json
        self.__users: json = {'USERS': users}

        # accumulated line string
        # write to file and flush when line break is met
        self.__line_str: str = ''

        # output file descriptor
        self.__f = open("output.txt", "w")

        # accumulated string of template format
        # <? ?>
        self.__pattern_str: str = ''

        # counting nested 'for loop' depth
        self.__loop_counter: int = 0

        # for [variable] in [array]
        # save iterable [array]. type is list because of nested 'for loop'
        self.__loop_arr: [[]] = []

        # save [variable]. type is list because of nested 'for loop'
        self.__loop_var: [] = []

        # accumulated string of inner 'for loop' pattern
        # <? for [variable] in [array] ?>[loop template string]<? endfor ?>
        # type is list because of nested 'for loop'
        self.__loop_template_str: [str] = []

    def __del__(self):
        self.__f.close()

    def gen_code(self):
        for ch in self.__template.get_str():
            # jump to next loop if real line break exists
            # only user written '\n' will move to next line
            if ch != '\n':
                if not self.__loop_counter:
                    self.__write_line(ch, self.__users)
                else:
                    self.__write_loop_template(ch)
        # if template has no line break, write to file at the end.
        if self.__line_str:
            self.__f.write(self.__line_str)

    def __write_line(self, ch: str, data: json):
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
                    parsed_str = json_walker.find_val(data, key_list)
                    self.__line_str += parsed_str
                    self.__pattern_str = ''

                # for loop mode. format is <? for [variable] in [array] ?>
                elif self.__pattern_str[2:-2].strip().split()[0] == 'for':
                    for_str = self.__pattern_str[2:-2].strip()
                    key_list = for_str.split()[-1].split('.')
                    self.__loop_var.append(for_str.split()[1])
                    self.__loop_arr.append(json_walker.find_arr(data, key_list))
                    self.__loop_counter = 1
                    self.__loop_template_str.append('')
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
        self.__loop_template_str[-1] += ch
        if ch == '<':
            self.__pattern_str += ch
        elif ch == '>':
            self.__pattern_str += ch
            variable_str = self.__pattern_str[2:-2].strip()

            if variable_str.split()[0] == 'for':
                self.__loop_counter += 1

            if variable_str == 'endfor':
                self.__loop_counter -= 1
                # write outer 'for loop' first
                if self.__loop_counter == 0:
                    self.__loop_template_str[-1] = self.__loop_template_str[-1][:-len(self.__pattern_str)]
                    self.__pattern_str = ''
                    for item in self.__loop_arr[-1]:
                        for ch in self.__loop_template_str[-1]:
                            if ch != '\n':
                                if not self.__loop_counter:
                                    self.__write_line(ch, {self.__loop_var[-1]: item})
                                else:
                                    self.__write_loop_template(ch)
                    self.__loop_template_str.pop()
                    self.__loop_arr.pop()
                    self.__loop_var.pop()

            self.__pattern_str = ''

        elif len(self.__pattern_str) > 0:
            self.__pattern_str += ch
