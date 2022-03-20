import input_loader
from template_store import TemplateStore
from user_engine import UserEngine
from template_engine import TemplateEngine

if __name__ == '__main__':
    users = input_loader.load()
    template_store = TemplateStore()

    if template_store.user_mode():
        # user engine
        # should print all users with template
        user_engine = UserEngine(template_store, users)
        user_engine.gen_code()
    else:
        # general template engine
        # input is USERS
        users_engine = TemplateEngine(template_store, users)
        users_engine.gen_code()
        pass


