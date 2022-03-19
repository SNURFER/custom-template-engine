import input_loader
from template_store import TemplateStore
from user_engine import UserEngine

if __name__ == '__main__':
    users = input_loader.load()
    template_store = TemplateStore()

    if template_store.user_mode():
        # user engine
        # should print all users with template
        user_engine = UserEngine(template_store, users)
        user_engine.gen_code()
    else:
        # users engine
        pass


