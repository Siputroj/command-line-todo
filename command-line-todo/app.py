from typing import List, Generator
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func

from database import List as DBList, Task as DBTask, get_db

class ToDoApp:

   selected_list_id: int | None = None
   list_view_selection_index: int = 0
   current_list_tasks: List | None = None
   task_view_selection_index: int = 0
   in_task_view: bool = False                   # check if current tab is task view or list_view


   def _get_db_session(self) -> Generator[Session, None, None]:
      return get_db()
   

   # LISTS Operations
   # TODO: 
   # might want to just store this as a variable instead of having to call it multiple times
   
   def get_all_lists(self) -> List[DBList]:     # list of DBList object
      with next(self._get_db_session()) as db:
         return db.query(DBList).options(selectinload(DBList.tasks)).order_by(DBList.name).all()
      
   
   def add_new_list(self, name:str) -> bool:
      try:
         with next(self._get_db_session()) as db:
            # check if name already exist
            if db.query(DBList).filter(func.lower(DBList.name) == func.lower(name)).first():
               return False
         
         new_list = DBList(name = name)
         db.add(new_list)
         db.commit()

         return True
      except:
         return False
      

   def select_list_by_index(self, index: int):
      all_lists = self.get_all_lists()
      if 0 <= index < len(all_lists):
         # converting index to id
         self.selected_list_id = all_lists[index].id
         self.list_view_selection_index = index

   
   def get_selected_list_data(self) -> DBList | None:
      if self.selected_list_id is None:
         return None

      with next(self._get_db_session()) as db:
         self.current_list_tasks = (db.query(DBList)
                                    .options(selectinload(DBList.tasks))
                                    .filter(DBList.id == self.selected_list_id)
                                    .first())
      



   # TASKS Operation    
   def add_new_task(self, description: str):
      if self.selected_list_id is None:
         return
         
      with next(self._get_db_session()) as db:
         new_task = DBTask(description = description, list_id = self.selected_list_id)
         db.add(new_task)
         db.commit()

   
   def toggle_task_complete(self, task_index: int):
      if not self.current_list_tasks:
         return
      
      if 0 <= task_index < len(self.current_list_tasks.tasks):
         task_to_toggle = self.current_list_tasks.tasks[task_index]
         
         with next(self._get_db_session()) as db:
            db_task = db.query(DBTask).get(task_to_toggle.id)
            db_task.is_completed = not db_task.is_completed
            db.commit()


app_state = ToDoApp()
      

   


