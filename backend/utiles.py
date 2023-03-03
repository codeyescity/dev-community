from passlib.context import CryptContext
from dbhelper import runSQL, runSQL_return_id

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def estimate_task_complexity(tasks, task):
    needed_times_sum = 0
    for t in tasks: needed_times_sum += t['task_needed_time']
    task_complexity = task['task_needed_time'] / needed_times_sum
    return task_complexity
 
def estimate_needed_time(task_progress, dif_sd_sp):
    if task_progress == 0: return dif_sd_sp
    task_needed_time = 100 * dif_sd_sp / task_progress
    return task_needed_time

def estimate_project_progress(project_id):
    tasks = runSQL("""SELECT * FROM tasks WHERE project_id = %s""", (project_id,))
    project_progress = 0
    for task in tasks: project_progress += task['task_progress'] * estimate_task_complexity(tasks, task)
    runSQL_return_id("""UPDATE projects SET project_progress = %s WHERE project_id = %s""", (project_progress,project_id))
    return project_progress

    