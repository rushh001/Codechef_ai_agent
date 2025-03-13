from scraper import get_daily_easy_problem
from parser import parse_problem
from ai_solver import generate_solution
from tester import test_solution
from submitter import submit_solution
from notifier import send_email
from utils import log_solved_problem

def main():
    problem_name, problem_link = get_daily_easy_problem()
    problem_text = parse_problem(problem_link)
    solution_code = generate_solution(problem_text)

       # Print the generated solution
    print("\n🔹 AI-Generated Solution:\n")
    print(solution_code)
    print("\n🔹 End of Solution 🔹\n")

    # test_result = test_solution(solution_code, "5\n1 2 3 4 5")  # Sample test input
    # print("Test Result:", test_result)

    submission_status = submit_solution(problem_link, solution_code)
    
    log_solved_problem(problem_name, submission_status)
    send_email("CodeChef Problem Solved", f"Today's problem {problem_name} has been solved and submitted!", "mzhusain2002@gmail.com")

if __name__ == "__main__":
    main()
