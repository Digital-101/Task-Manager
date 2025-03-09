from task_client.openapi_client.api.default_api import DefaultApi
from task_client.openapi_client.configuration import Configuration
from task_client.openapi_client.api_client import ApiClient

# Set up the API client
configuration = Configuration(host="http://localhost:5000/api")
api_client = ApiClient(configuration)
api_instance = DefaultApi(api_client)

# Create a new task
new_task = {
    'title': 'Buy groceries',
    'description': 'Milk, Bread, Eggs',
    'completed': False
}
created_task = api_instance.create_task(new_task)
print("Created Task:", created_task)

# Get all tasks
tasks = api_instance.get_tasks()
print("All Tasks:", tasks)

# Get a task by ID
task_id = created_task['id']
task = api_instance.get_task(task_id)
print("Task by ID:", task)

# Delete the task
api_instance.delete_task(task_id)
print(f"Task {task_id} deleted.")