from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.styles import Style


from layout.view import main_layout
from key_bindings import kb

kb2 = KeyBindings


def main():

   application = Application(
      layout = main_layout,
      key_bindings = kb, 
      full_screen = True,
   )
   application.run()
   

if __name__ == '__main__':
   main()
