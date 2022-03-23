import input_loader
from template_store import TemplateStore
from template_engine import TemplateEngine

if __name__ == '__main__':
    users = input_loader.load()
    template_store = TemplateStore()

    template_engine = TemplateEngine(template_store, users)

    # pattern input is 'USERS'
    template_engine.gen_code()

    print('===================================================')
    print('================code generate ended================')
    print('===================================================')


