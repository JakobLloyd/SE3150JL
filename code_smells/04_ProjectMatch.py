"""Find employees who have every skill required by a project."""

# Project matching rules:
#
# - Compare every employee with every project.
#
# - Skill names are not case-sensitive.
#   For example, "Python" and "python"
#   represent the same skill.
#
# - An employee must have every skill
#   required by the project.
#
# - Extra employee skills are allowed.
#
# - An employee is unavailable for a project
#   if any project meeting day appears in
#   the employee's unavailable days.
#
# - An employee may match more than
#   one project.
#
# - A project may match more than
#   one employee.
#
# Return a list of matching pairs.
# Each pair contains the project name
# followed by the employee name.

def find_project_matches(employees, projects):
    matches = []
    for project in projects:
        for employee in employees:
            missing = []
            for required_skill in project["skills"]:
                found = False
                for employee_skill in employee["skills"]:
                    if required_skill.lower() == employee_skill.lower():
                        found = True
                if not found:
                    missing.append(required_skill)
            if not missing:
                conflicts = False
                for project_day in project["meeting_days"]:
                    for unavailable_day in employee["unavailable_days"]:
                        if project_day == unavailable_day:
                            conflicts = True
                if not conflicts:
                    matches.append((project["name"], employee["name"]))
    return matches


if __name__ == "__main__":
    employees = [
        {"name": "Mina", "skills": ["Python", "SQL", "Docker"], "unavailable_days": ["Fri"]},
        {"name": "Owen", "skills": ["SQL", "Excel"], "unavailable_days": ["Tue"]},
        {"name": "Priya", "skills": ["Python", "Docker", "SQL"], "unavailable_days": ["Mon"]},
    ]
    projects = [
        {"name": "Forecasting", "skills": ["Python", "SQL"], "meeting_days": ["Wed"]},
        {"name": "Migration", "skills": ["SQL", "Docker"], "meeting_days": ["Mon"]},
    ]
    print(find_project_matches(employees, projects))


'''
1. Get rid of the nested loops for checking skills and unavailable days.
2. Create another function to handle the for loops for matching employees to projects, which will make the code cleaner and more modular.
3. Only nest for and if loops if needed, otherwise use list comprehensions or generator expressions to make the code more readable.
4. Code is using a lot of lists and dictionaries instead of classes or variables.
5. Check requirements for the project and employee data to make sure they are valid before processing them.

6. In main separate names, skills, and unavailable days into different variables to make it easier to read and understand.
7. In main use a user input function to get employee and project data instead of hardcoding it, which will make the code more flexible and reusable.
8. Return values instead of printing them in the main function to make it easier to test and reuse the code.


'''