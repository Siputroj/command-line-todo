from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText

from app import app_state

def get_list_view_content():
   fragments = []

   # Header bar
   fragments.append(('bg:#2A4D69 fg:white bold', '   Select a To-Do List '))
   fragments.append(('', '\n'))

   all_lists = app_state.get_all_lists()
   selector = app_state.list_view_selection_index

   if not all_lists:
      fragments.append(('fg:#999999', '   Press CTRL + A to add new To-Do List'))
      return FormattedText(fragments)
   
   for i, list in enumerate(all_lists):
      is_selected = (i == selector)
      indicator = ' ➤ ' if is_selected else '   '
      task_count = len(list.tasks)

      style = 'bg:#5CB3FF fg:black' if is_selected else 'fg:#CCCCCC'
      fragments.append((style, f'{indicator} {list.name} ({task_count})'))
      fragments.append(('', '\n'))

   # drop the trailing newline for a cleaner render
   if fragments and fragments[-1][1] == '\n':
      fragments.pop()

   return FormattedText(fragments)
   

list_view_control = FormattedTextControl(
   text = get_list_view_content,
   focusable = True
)

shortcut_list_view_content = """

   <C-A>:      Add New List
   <Up/Down>:  Navigate
   <Enter>:    Open List

   <C-C/C-Q>:  Quit App
"""

shortcut_control = FormattedTextControl(
   text = shortcut_list_view_content,
   focusable = False
)

command_buffer = Buffer(name = "command_input")
command_control = BufferControl(buffer = command_buffer)


list_command_view_pane = HSplit([
   Frame(
      body = Window(content = list_view_control, always_hide_cursor = True),
      title="TO-DO LIST"
   ),

   Window(height = 1, char = '~', style = 'fg:#AAAAAA'),
   
   # this is for the command line
   Window(
      content  = command_control,
      height = 1,
      style = 'bg:#5CB3FF fg:black'
   ),
])

shortcuts_pane = Frame(
   body = Window(content = shortcut_control, always_hide_cursor = True),
   title = "KEYBOARD SHORTCUTS",
   width = 40
)


root_container = VSplit([
   list_command_view_pane,
   shortcuts_pane
])
