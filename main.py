import input_loader
from template_store import TemplateStore
from template_engine import TemplateEngine

if __name__ == '__main__':
    users = input_loader.load()
    template_store = TemplateStore()

    template_engine = TemplateEngine(template_store, users)
    if template_store.user_mode():
        # should print all users with template
        # input is USER and generate every USER in data.json
        template_engine.gen_code_user()
    else:
        # general template engine
        # input is USERS
        template_engine.gen_code()
        pass


