from prompt_toolkit.layout.layout import Layout


from app import app_state
from .list_view import root_container as list_view_root_container, command_buffer as list_view_command_buffer
from .task_view import root_container as task_view_root_container, command_buffer as task_view_command_buffer


main_layout = None

if (not app_state.in_task_view):
   main_layout = Layout(list_view_root_container, focused_element = list_view_root_container)
else:
   main_layout = Layout(task_view_root_container, focused_element = task_view_root_container)