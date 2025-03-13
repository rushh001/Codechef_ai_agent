import groq
import os
from dotenv import load_dotenv

load_dotenv()

def generate_solution(problem_text):
    if not problem_text:
        print("❌ Error: No problem text provided.")
        return None

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ API key not found.")
        return None

    client = groq.Client(api_key=api_key)

    prompt = f"""
    You are a competitive programming assistant. Given a problem statement, generate a Python solution.
    Ensure the solution has a 'main()' function that reads input from stdin and prints the correct output.
    Do not include explanations—just the correct Python code.

    Problem:
    {problem_text}

    Solution:
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )

    solution_code = response.choices[0].message.content

     # Split solution into lines and remove the first and last lines
    solution_lines = solution_code.split("\n")
    if len(solution_lines) > 2:
        solution_code = "\n".join(solution_lines[1:-1])  # Remove first and last line


    # Ensure the response contains a `main()` function
    if "def main():" not in solution_code:
        print("❌ Error: AI-generated code does not contain a main function.")
        return None

    return solution_code
