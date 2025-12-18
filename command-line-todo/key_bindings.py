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
list_view_focused = Condition(lambda: main_layout.has_focus(list_view_control)) & in_list_view

task_buffer_focused = Condition(lambda: main_layout.has_focus(command_buffer)) & in_task_view
task_view_focused = Condition(lambda: main_layout.has_focus(task_view_control)) & in_task_view


# Navigation for ListView
@kb.add("up", filter = in_list_view & list_view_focused)
def _(event):
   app_state.list_view_selection_index = max(0, app_state.list_view_selection_index - 1)
   event.app.invalidate()
   
@kb.add("down", filter = in_list_view & list_view_focused)
def _(event):
   list_count = len(app_state.get_all_lists())
   if list_count > 0:
      app_state.list_view_selection_index = min(list_count - 1, app_state.list_view_selection_index + 1)
      event.app.invalidate()

@kb.add("i", filter = in_list_view & list_view_focused)
def _(event):
   event.app.layout.focus(command_buffer)


@kb.add("enter", filter = in_list_view & list_view_focused)
@kb.add("right", filter = in_list_view & list_view_focused)
def _(event):
   all_lists = app_state.get_all_lists()
   if all_lists:
      app_state.select_list_by_index(app_state.list_view_selection_index)
      app_state.get_selected_list_data()
      app_state.in_task_view = True

      event.app.invalidate()
      event.app.layout.focus(task_view_control)

      




# Navigation for TaskView
@kb.add("up", filter = in_task_view & task_view_focused)
def _(event):
   app_state.task_view_selection_index = max(0, app_state.task_view_selection_index - 1)
   event.app.invalidate()
   
@kb.add("down", filter = in_task_view & task_view_focused)
def _(event):
   task_count = len(app_state.current_list_tasks.tasks)
   if task_count > 0:
      app_state.task_view_selection_index = min(task_count - 1, app_state.task_view_selection_index + 1)
      event.app.invalidate()

@kb.add("i", filter = in_task_view & task_view_focused)
def _(event):
   event.app.layout.focus(command_buffer)

@kb.add("left", filter = in_task_view & task_view_focused)
def _(event):
   
   app_state.in_task_view = False
   event.app.layout.focus(list_view_control)
   event.app.invalidate()
   
   # reset task list and pointer
   app_state.current_list_tasks = None
   app_state.selected_list_id = None
   app_state.task_view_selection_index = 0



@kb.add("enter", filter = in_task_view & task_view_focused)
@kb.add("right", filter = in_task_view & task_view_focused)
def _(event):
   if app_state.current_list_tasks:
      app_state.toggle_task_complete(app_state.task_view_selection_index)

      event.app.invalidate()



# Command line
# there is a delay in the escape key button
@kb.add("escape", filter = list_buffer_focused | task_buffer_focused)
def _(event):
   if (app_state.in_task_view):
      event.app.layout.focus(task_view_control)
   else:
      event.app.layout.focus(list_view_control)
   event.app.invalidate()

# ListView command line
@kb.add("enter", filter = in_list_view & list_buffer_focused)
def _(event):
   name = command_buffer.text.strip()

   # clear the command line
   command_buffer.text = ''

   if not name:
      return
   
   app_state.add_new_list(name)
   event.app.layout.focus(list_view_control)
   event.app.invalidate()

# TaskView command line
@kb.add("enter", filter = in_task_view & task_buffer_focused)
def _(event):
   task_name = command_buffer.text.strip()

   command_buffer.text = ''

   if not task_name:
      return
   
   app_state.add_new_task(task_name)
   event.app.invalidate()