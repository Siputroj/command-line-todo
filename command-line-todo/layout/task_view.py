from prompt_toolkit.layout.containers import HSplit, Window, VSplit, ConditionalContainer
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.buffer import Buffer

# Import the state object from the models file
# TODO: Might need to move this together with list_view and do ConditionalContainer instead
from app import app_state

def get_task_view_content():
   current_list_tasks = app_state.get_selected_list_data()
   list_name = current_list_tasks.name if current_list_tasks else "Error"
   selector = app_state.task_view_selection_index

   lines = [f'   <style bg="#2A4D69" bold>{list_name} </style>\n']

   if not current_list_tasks or not current_list_tasks.tasks:
      lines.append('   (List is empty. Type "add" below to add a task.)')
      return '\n'.join(lines)
   
   for i, item in enumerate(current_list_tasks.tasks):
      is_selected = (i == selector)

      index = f"{i + 1}."
      status = "[x]" if item.is_completed else "[ ]"
      style = 'style="fg:green;bold"' if item.is_completed else 'style="fg:red"'
      indicator = ' ➤ ' if is_selected else '   '
      lines.append(f' {index:<3} {indicator} {status} <{style}> {item.description} </{style}>') 

   return '/n'.join(lines)

task_view_control = FormattedTextControl(
   text = get_task_view_content,
   focusable = True
)

shortcut_task_view_content = """
   
   <C-A>:         Add New Task
   <Up/Down>:     Navigate
   <Enter>:       Mark Done/Undone
   <Esc>:         Go Back to List Menu

   <C-C/C-Q>: Quit App
"""
shortcut_control = FormattedTextControl(
   text = shortcut_task_view_content,
   focusable = False
)

command_buffer = Buffer(name = "command_input")
command_control = BufferControl(buffer = command_buffer)


task_command_view_pane = HSplit([
   Frame(
      body = Window(content = task_view_control, always_hide_cursor = True),
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
   task_command_view_pane,
   shortcuts_pane
])

