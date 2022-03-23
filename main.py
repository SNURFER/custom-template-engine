import sys

import input_loader
from template_store import TemplateStore
from template_engine import TemplateEngine

if __name__ == '__main__':
    arg_num = len(sys.argv)
    template_path = 'input/template'
    if arg_num > 1:
        template_path = sys.argv[1]

    users = input_loader.load()
    template_store = TemplateStore(template_path)
    template_engine = TemplateEngine(template_store, users)

    # pattern input is 'USERS'
    template_engine.gen_code()

    print('===================================================')
    print('================code generate ended================')
    print('===================================================')


