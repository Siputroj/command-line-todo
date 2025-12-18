from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition

from app import app_state
from layout.view import main_layout, list_view_control, task_view_control, command_buffer

kb = KeyBindings()


@kb.add('c-c')
@kb.add('c-q')
def exit_(event):
   """
   Exit application
   """
   event.app.exit()

# Focus helpers
in_task_view = Condition(lambda: app_state.in_task_view)
in_list_view = Condition(lambda: not app_state.in_task_view)


list_buffer_focused = Condition(lambda: main_layout.has_focus(command_buffer)) & in_list_view
list_control_focused = Condition(lambda: main_layout.has_focus(list_view_control)) & in_list_view

task_buffer_focused = Condition(lambda: main_layout.has_focus(command_buffer)) & in_task_view
task_control_focused = Condition(lambda: main_layout.has_focus(list_view_control)) & in_task_view


# Navigation for ListView
@kb.add("up", filter=in_list_view & list_control_focused)
def _(event):
   app_state.list_view_selection_index = max(0, app_state.list_view_selection_index - 1)
   event.app.invalidate()
   
@kb.add("down", filter=in_list_view & list_control_focused)
def _(event):
   list_count = len(app_state.get_all_lists())
   if list_count > 0:
      app_state.list_view_selection_index = min(list_count - 1, app_state.list_view_selection_index + 1)
      event.app.invalidate()

@kb.add("i", filter=in_list_view & list_control_focused)
def _(event):
   event.app.layout.focus(command_buffer)


@kb.add("enter", filter=in_list_view & list_control_focused)
def _(event):
   all_lists = app_state.get_all_lists()
   if all_lists:
      app_state.select_list_by_index(app_state.list_view_selection_index)
      app_state.in_task_view = True

      event.app.invalidate()
      event.app.layout.focus(task_view_control)

      

@kb.add("enter", filter=in_list_view & list_buffer_focused)
def _(event):
   name = command_buffer.text.strip()
   # clear the command line
   command_buffer.text = ''

   if not name:
      return
   
   app_state.add_new_list(name)
   event.app.layout.focus(list_view_control)
   event.app.invalidate()
