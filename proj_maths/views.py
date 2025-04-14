from django.shortcuts import render, redirect
from django.core.cache import cache
from . import physics_work

def index(request):
    return render(request, "index.html")

def problems_list(request):
    problems = physics_work.get_problems_for_table()
    return render(request, "problems_list.html", context={"problems": problems})

def add_problem(request):
    return render(request, "problem_add.html")

def send_problem(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_problem = request.POST.get("new_problem", "")
        new_solution = request.POST.get("new_solution", "").replace(";", ",")
        difficulty = request.POST.get("difficulty", "medium")
        
        context = {"user": user_name}
        if len(new_solution) == 0:
            context["success"] = False
            context["comment"] = "Solution must not be empty"
        elif len(new_problem) == 0:
            context["success"] = False
            context["comment"] = "Problem must not be empty"
        else:
            context["success"] = True
            context["comment"] = "Your problem was added"
            physics_work.write_problem(new_problem, new_solution, difficulty)
        
        return render(request, "problem_request.html", context)
    else:
        return add_problem(request)

def solve_problem(request):
    problems = physics_work.get_problems_for_table()
    problem_id = request.GET.get('problem_id')
    if problem_id:
        try:
            problem_id = int(problem_id)
            selected_problem = problems[problem_id-1]
            context = {
                "problems": problems,
                "selected_problem": {
                    "id": problem_id,
                    "text": selected_problem[1],
                    "difficulty": selected_problem[3],
                    "dimension": selected_problem[4] if len(selected_problem) > 4 else ""
                }
            }
            return render(request, "problem_solve.html", context)
        except (IndexError, ValueError):
            pass
    return render(request, "problem_solve.html", {"problems": problems})

def check_solution(request):
    if request.method == "POST":
        problem_id = int(request.POST.get("problem_id"))
        user_answer = request.POST.get("user_answer", "")
        
        is_correct = physics_work.check_answer(problem_id, user_answer)
        problem = physics_work.get_problems_for_table()[problem_id-1]
        
        return render(request, "solution_result.html", {
            "correct": is_correct,
            "problem_id": problem_id,
            "problem_text": problem[1],
            "user_answer": user_answer,
            "correct_answer": problem[2]  # The solution from database
        })
    else:
        return solve_problem(request)

def show_stats(request):
    stats = physics_work.get_problems_stats()
    
    # Calculate percentages for progress bars
    total = stats["total_problems"]
    stats.update({
        "solved_percentage": (stats["solved"] / total) * 100 if total else 0,
        "unsolved_percentage": (stats["unsolved"] / total) * 100 if total else 0,
        "not_attempted_percentage": (stats["not_attempted"] / total) * 100 if total else 0,
    })
    
    return render(request, "stats.html", {"stats": stats})
