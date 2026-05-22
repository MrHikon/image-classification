# ── GRADING FUNCTIONS ──────────────────────────────────────

def get_grade_and_point(score):
    # Convert a score to a letter grade and grade point
    # using the Nigerian university grading system
    if   70 <= score <= 100: return "A", 5
    elif 60 <= score <= 69:  return "B", 4
    elif 50 <= score <= 59:  return "C", 3
    elif 45 <= score <= 49:  return "D", 2
    elif 40 <= score <= 44:  return "E", 1
    elif  0 <= score <= 39:  return "F", 0
    else:                    return None, None   # Score is outside valid range

# ── INPUT VALIDATION HELPERS ───────────────────────────────

def get_valid_score(course_name):
    # Keep asking until the user enters an integer between 0 and 100
    while True:
        raw = input(f"  Score for {course_name}: ").strip()
        if raw.isdigit() and 0 <= int(raw) <= 100:
            return int(raw)
        print("  Score must be a whole number between 0 and 100.")

def get_valid_credit():
    # Keep asking until the user enters a credit unit between 1 and 6
    while True:
        raw = input("  Credit unit       : ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 6:
            return int(raw)
        print("  Credit unit must be between 1 and 6.")

# ── DISPLAY FUNCTIONS ──────────────────────────────────────

def display_table(records):
    # Print all courses in a formatted table
    # WP = Weighted Points (grade_point x credit_unit)
    print("\n" + "=" * 54)
    print("            STUDENT RESULT SHEET")
    print("=" * 54)
    print(f"  {'Course':<22}{'Score':>6}{'Credit':>7}{'Grade':>6}{'WP':>8}")
    print("  " + "-" * 50)

    for r in records:
        # Calculate weighted points for this course
        wp = r["grade_point"] * r["credit"]
        print(f"  {r['course']:<22}{r['score']:>6}{r['credit']:>7}{r['grade']:>6}{wp:>8}")

    print("  " + "-" * 50)

def calculate_gpa(records):
    # GPA formula: total weighted points divided by total credit units
    total_wp = sum(r["grade_point"] * r["credit"] for r in records)
    total_cr = sum(r["credit"] for r in records)

    # Avoid division by zero in case no courses were entered
    return total_wp / total_cr if total_cr else 0.0

# ── MAIN PROGRAM ───────────────────────────────────────────

def run_gpa_calculator():
    print("=" * 54)
    print("       STUDENT GPA CALCULATOR")
    print("  70-100=A(5) | 60-69=B(4) | 50-59=C(3)")
    print("  45-49=D(2)  | 40-44=E(1) | 0-39=F(0)")
    print("=" * 54)

    student_name = input("\n  Student name   : ").strip()
    matric_no    = input("  Matric number  : ").strip()

    # List of dictionaries — each dictionary holds one course's details
    records = []

    print("\n  Enter courses. Type 'done' when finished.\n")

    while True:
        course = input("  Course name (or 'done'): ").strip()

        # Stop collecting courses when user types done
        if course.lower() == "done":
            if not records:
                print("  Enter at least one course.")
                continue
            break

        if not course:
            print("  Course name cannot be empty.")
            continue

        score        = get_valid_score(course)
        credit       = get_valid_credit()
        grade, point = get_grade_and_point(score)

        # Store all details for this course as a dictionary in the list
        records.append({
            "course":      course,
            "score":       score,
            "credit":      credit,
            "grade":       grade,
            "grade_point": point
        })

        print(f"  >> Grade: {grade}  |  Points: {point}\n")

    # Display the full result table
    display_table(records)

    # Calculate and display the final GPA
    gpa          = calculate_gpa(records)
    total_credits = sum(r["credit"] for r in records)
    total_wp      = sum(r["grade_point"] * r["credit"] for r in records)

    print(f"\n  Student : {student_name}  |  Matric: {matric_no}")
    print(f"  Total Credits     : {total_credits}")
    print(f"  Total Grade Points: {total_wp}")
    print(f"\n  *** FINAL GPA     : {gpa:.2f} ***")

    # Convert GPA to a class of degree
    if   gpa >= 4.50: remark = "First Class"
    elif gpa >= 3.50: remark = "Second Class Upper"
    elif gpa >= 2.50: remark = "Second Class Lower"
    elif gpa >= 1.50: remark = "Third Class"
    else:             remark = "Fail"

    print(f"  Class of Degree   : {remark}")
    print("=" * 54)

# ── ENTRY POINT ────────────────────────────────────────────
run_gpa_calculator()