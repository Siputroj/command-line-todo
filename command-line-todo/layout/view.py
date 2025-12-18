from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, ConditionalContainer
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.filters import Condition

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

def get_task_view_content():
   app_state.get_selected_list_data()
   current_list_tasks = app_state.current_list_tasks
   list_name = current_list_tasks.name if current_list_tasks else "Error"
   selector = app_state.task_view_selection_index

   fragments = []

   # Header
   fragments.append(('bg:#2A4D69 bold', f'   {list_name} '))
   fragments.append(('', '\n'))

   if not current_list_tasks or not current_list_tasks.tasks:
      fragments.append(('', '   (List is empty. Type "add" below to add a task.)'))
      return FormattedText(fragments)
   
   for i, item in enumerate(current_list_tasks.tasks):
      is_selected = (i == selector)

      index = f"{i + 1}."
      status = "[x]" if item.is_completed else "[ ]"
      desc_style = 'fg:green bold' if item.is_completed else 'fg:red'
      indicator = ' ➤ ' if is_selected else '   '

      line_style = 'bg:#5CB3FF fg:black' if is_selected else ''
      fragments.append((line_style, f' {index:<3} {indicator} {status} '))
      fragments.append((desc_style, item.description))
      fragments.append(('', '\n'))

   if fragments and fragments[-1][1] == '\n':
      fragments.pop()

   return FormattedText(fragments)

task_view_control = FormattedTextControl(
   text = get_task_view_content,
   focusable = True
)

shortcut_list_view_content = FormattedText([
   ('fg:#FFA500 bg:#36454F bold', '   Commands'),
   ('', '\n\n'),
   ('fg:#00FF00 bold', '   In Menu View:'),
   ('', '\n'),
   ('', '   <C-A>:         Add New List\n'),
   ('', '   <Up/Down>:     Navigate\n'),
   ('', '   <Enter>:       Open List\n\n'),
   ('fg:#00FF00 bold', '   In Task View:'),
   ('', '\n'),
   ('', '   add <task>:    Add Task\n'),
   ('', '   toggle <id>:   Mark Done\n'),
   ('', '   <Esc>:         Go Back\n\n'),
   ('', '   <C-C/C-Q>: Quit App'),
])

shortcut_control = FormattedTextControl(
   text = shortcut_list_view_content,
   focusable = False
)

# command line
command_buffer = Buffer(name = "command_input")
command_control = BufferControl(buffer = command_buffer)


list_view_pane = Frame(
      body = Window(content = list_view_control, always_hide_cursor = True),
      title="TO-DO LIST"
   )

task_view_pane = Frame(
      body = Window(content = task_view_control, always_hide_cursor = True),
      title="TO-DO LIST"
   )

shortcuts_pane = Frame(
   body = Window(content = shortcut_control, always_hide_cursor = True),
   title = "KEYBOARD SHORTCUTS",
   width = 40
)

in_task_view = Condition(lambda: app_state.in_task_view)
in_list_view = Condition(lambda: not app_state.in_task_view)

list_task_shortcut_view = VSplit([
   ConditionalContainer(
      content = list_view_pane,
      filter = in_list_view
   ),
   ConditionalContainer(
      content = task_view_pane,
      filter = in_task_view
   ),
   shortcuts_pane
])

root_container = HSplit([
   list_task_shortcut_view,
   Window(height = 1, char = '-', style = 'fg:#AAAAAA'),
   Window(
      content = command_control,
      height = 1,
      style = 'bg:#5CB3FF fg:black'
   )
])

main_layout = Layout(root_container, focused_element = list_view_control)

