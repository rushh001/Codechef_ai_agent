def test_solution(solution_code, test_input):
    if not solution_code:
        print("❌ Error: No solution code provided for testing.")
        return None

    exec_globals = {}
    try:
        exec(solution_code, exec_globals)  # ✅ Execute the generated solution
    except Exception as e:
        print(f"❌ Error executing solution code: {e}")
        return None

    if "main" in exec_globals:
        return exec_globals["main"](test_input)
    else:
        print("❌ Error: No main function found in the solution.")
        return None
