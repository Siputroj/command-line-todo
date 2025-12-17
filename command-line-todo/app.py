from typing import List, Generator
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import List as DBList, Task as DBTask, get_db

class ToDoApp:

   selected_list_id: int | None = None
   menu_selection_index: int = 0
   in_task_view: bool = False                   # check if current tab is task view 
   adding_new_list: bool = False                # which cursor to focus on, the command line or the choice


   def _get_db_session(self) -> Generator[Session, None, None]:
      return get_db()
   

   # LISTS Operations
   def get_all_lists(self) -> List[DBList]:     # list of DBList object
      with next(self._get_db_session()) as db:
         return db.query(DBList).order_by(DBList.name).all()
      
   
   def add_new_list(self, name:str) -> bool:
      try:
         with next(self._get_db_session) as db:
            # check if name already exist
            if db.query(DBList).filter(func.lower(DBList.name) == func.lower(name)).first():
               return False
         
         new_list = DBList(name = name)
         db.add(new_list)
         db.commit()

         # get the updated list of ToDoLists
         all_lists = self.get_all_lists()
         self.menu_selection_index = len(all_lists) - 1
         return True
      except:
         return False
      

   def select_list_by_index(self, index: int):
      all_lists = self.get_all_lists()
      if 0 <= index < len(all_lists):
         self.selected_list_id = all_lists[index].id
         self.menu_selection_index = index

   
   def get_selected_list_data(self) -> DBList | None:
      if self.selected_list_id is None:
         return None

      with next(self._get_db_session()) as db:
         return db.query(DBList).filter(DBList.id == self.selected_list_id).first()
      



   # TASKS Operation
   def add_new_task(self, description: str):
      if self.selected_list_id is None:
         return
         
      with next(self._get_db_session()) as db:
         new_task = DBTask(description = description, list_id = self.selected_list_id)
         db.add(new_task)
         db.commit()

   def toggle_task_complete(self, task_index: int):
      selected_list = self.get_selected_list_data()
      # if no selected lists or selected lists has no tasks
      if not selected_list or not selected_list.tasks:
         return
      
      if 0 <= task_index < len(selected_list.tasks):
         task_to_toggle = selected_list.tasks[task_index]
         
         with next(self._get_db_session()) as db:
            db_task = db.query(DBTask).get(task_to_toggle.id)
            db_task.completed = not db_task.completed
            db.commit()


app_state = ToDoApp()
      

   


