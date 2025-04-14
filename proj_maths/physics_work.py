import json
from pathlib import Path

def get_problems_for_table():
    problems = []
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:  # Skip header
            # Split line and ensure we have exactly 5 values
            parts = line.strip().split(";")
            if len(parts) < 5:
                parts += [''] * (5 - len(parts))  # Fill missing columns with empty strings
            term, definition, difficulty, dimension, explanation = parts[:5]
            problems.append([cnt, term, definition, difficulty, dimension])
            cnt += 1
    return problems


def get_problem_by_id(problem_id):
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # Skip header
        if 1 <= problem_id <= len(lines):
            problem, solution, difficulty = lines[problem_id-1].strip().split(";")
            return {
                "id": problem_id,
                "problem": problem,
                "solution": solution,
                "difficulty": difficulty
            }
    return None

def write_problem(new_problem, new_solution, difficulty):
    new_line = f"{new_problem};{new_solution};{difficulty}"
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        existing = [l.strip("\n") for l in f.readlines()]
        title = existing[0]
        old_problems = existing[1:]
    
    problems_sorted = old_problems + [new_line]
    problems_sorted.sort()
    new_problems = [title] + problems_sorted
    with open("./data/problems.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_problems))

def check_answer(problem_id, user_answer):
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]
        if problem_id > len(lines):
            return False
        problem_data = lines[problem_id-1].strip().split(";")
        correct_answer = float(problem_data[1])
        try:
            user_num = float(user_answer)
            is_correct = abs(user_num - correct_answer) < 0.001
            update_user_progress(problem_id, is_correct)
            return is_correct
        except ValueError:
            return False


def get_problems_stats():
    progress = get_user_progress()
    stats = {
        "total_problems": 0,
        "solved": len(progress["solved"]),
        "unsolved": len(progress["unsolved"]),
        "not_attempted": 0,
        "progress_percentage": 0,
    }
    
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        stats["total_problems"] = len(f.readlines()) - 1  # exclude header
    
    stats["not_attempted"] = stats["total_problems"] - stats["solved"] - stats["unsolved"]
    if stats["total_problems"] > 0:
        stats["progress_percentage"] = round((stats["solved"] / stats["total_problems"]) * 100)
    
    return stats

def get_user_progress():
    progress_file = Path("./data/user_progress.json")
    if not progress_file.exists():
        return {"solved": [], "unsolved": []}
    with open(progress_file, "r", encoding="utf-8") as f:
        return json.load(f)

def update_user_progress(problem_id, is_correct):
    progress = get_user_progress()
    
    # Remove from both lists if exists
    progress["solved"] = [pid for pid in progress["solved"] if pid != problem_id]
    progress["unsolved"] = [pid for pid in progress["unsolved"] if pid != problem_id]
    
    # Add to appropriate list
    if is_correct:
        progress["solved"].append(problem_id)
    else:
        progress["unsolved"].append(problem_id)
    
    # Save updated progress
    with open("./data/user_progress.json", "w", encoding="utf-8") as f:
        json.dump(progress, f)

def get_problem_by_id(problem_id):
    with open("./data/problems.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # Skip header
        if 1 <= problem_id <= len(lines):
            problem, solution, difficulty = lines[problem_id-1].strip().split(";")
            return {
                "id": problem_id,
                "problem": problem,
                "solution": solution,
                "difficulty": difficulty
            }
    return None
