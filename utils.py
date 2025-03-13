import datetime

def log_solved_problem(problem_name, status):
    with open("logs/solved_problems.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {problem_name} - {status}\n")
