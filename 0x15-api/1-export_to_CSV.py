import requests
import csv

def get_employee_todo_list(employee_id):
    url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve employee data for id {employee_id}")
    employee_data = response.json()
    employee_name = employee_data["username"]

    url = f"https://jsonplaceholder.typicode.com/todos?userId={employee_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve TODO list data for employee {employee_id}")
    todo_list_data = response.json()

    total_tasks = len(todo_list_data)
    completed_tasks = sum(task["completed"] for task in todo_list_data)

    print(f"Employee {employee_name} is done with tasks ({completed_tasks}/{total_tasks}):")
    filename = f"{employee_id}.csv"
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in todo_list_data:
            task_id = task["id"]
            task_title = task["title"]
            task_status = "complete" if task["completed"] else "incomplete"
            writer.writerow([employee_id, employee_name, task_status, task_title])
            if task["completed"]:
                print(f"\t{task['title']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py EMPLOYEE_ID")
        sys.exit(1)
    employee_id = int(sys.argv[1])
    get_employee_todo_list(employee_id)
