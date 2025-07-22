
class Assignments:
    # Maximum weights for each category
    FORMATIVE_MAX_WEIGHT = 60
    SUMMATIVE_MAX_WEIGHT = 40

    # Initialize assignment with validation and compute weighted grade
    def __init__(self, assignment_name, category, weight, grade):

        # Store the assignment details after validation
        self.assignment_name = assignment_name
        self.validate_category(category)
        self.category = category
        self.validate_weight(weight)
        self.weight = weight
        self.validate_grade(grade)
        self.grade = grade

        # Calculate weighted grade
        self.weighted_grade = (grade * weight) / 100

    # Ensure category is either 'Formative' or 'Summative'
    def validate_category(self, category):

        # Check if the category is either 'Formative' or 'Summative'
        if category not in ['Formative', 'Summative']:
            raise ValueError("Category must be either 'Formative' or 'Summative'")

    # Ensure weight is a valid percentage between 0 and 100
    def validate_weight(self, weight):
        # Check if the weight is between 0 and 100
        if not (0 <= weight <= 100):
            raise ValueError("Weight must be between 0 and 100")

    # Ensure grade is a valid percentage between 0 and 100
    def validate_grade(self, grade):
        # Check if the grade is between 0 and 100
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100")

class Grade_calculator:

    # Initialize lists to hold formative and summative assignments
    def __init__(self):
        self.formative_assignments = []
        self.summative_assignments = []

    # Calculate total weight of assignments in a given category
    def get_category_total_weight(self, category):
        if category == 'Formative':
            return sum(a.weight for a in self.formative_assignments)
        return sum(a.weight for a in self.summative_assignments)

    # Check that adding new weight does not exceed max allowed for category
    def validate_category_weight(self, category, new_weight):
        current_weight = self.get_category_total_weight(category)
        max_weight = Assignments.FORMATIVE_MAX_WEIGHT if category == 'Formative' else Assignments.SUMMATIVE_MAX_WEIGHT
        if (current_weight + new_weight) > max_weight:
            raise ValueError(f"Total {category} weight cannot exceed {max_weight}%. You have {max_weight - current_weight}% left.")

    # Collect and validate all assignment details from user input
    def get_input_from_user(self):
        try:
            # Re-prompt assignment_name if empty
            while True:
                assignment_name = input("\nEnter the assignment (e.g., Group Project, Quiz4): ").strip()
                if assignment_name:
                    break
                print("Assignment name cannot be empty.")

            while True:
                category = input("Enter the category (Formative/Summative): ").strip().capitalize()
                if category in ['Formative', 'Summative']:
                    break
                print("Please enter either 'Formative' or 'Summative'")

            current_weight = self.get_category_total_weight(category)
            max_weight = Assignments.FORMATIVE_MAX_WEIGHT if category == 'Formative' else Assignments.SUMMATIVE_MAX_WEIGHT
            print(f"You have {max_weight - current_weight}% {category} weight left.")

            while True:
                try:
                    weight_input = input("Enter assignment weight (0-100): ").strip()
                    if not weight_input:
                        print("Weight cannot be empty.")
                        continue
                    weight = float(weight_input)
                    self.validate_category_weight(category, weight)
                    if 0 <= weight <= 100:
                        break
                    print("Weight must be between 0 and 100")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            while True:
                try:
                    is_percentage = input("Was this assignment graded out of 100? (yes/no): ").strip().lower()
                    if not is_percentage:
                        print("Please answer with 'yes' or 'no'.")
                        continue
                    if is_percentage in ['yes', 'no']:
                        break
                    print("Please answer with 'yes' or 'no'.")
                except Exception as e:
                    print(f"Invalid input: {e}")

            if is_percentage == 'yes':
                while True:
                    try:
                        grade_input = input("Enter your grade as a percentage (e.g., 85): ").strip()
                        if not grade_input:
                            print("Grade cannot be empty.")
                            continue
                        grade = float(grade_input)
                        if 0 <= grade <= 100:
                            break
                        print("Grade must be between 0 and 100")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                while True:
                    try:
                        raw_input = input("Enter the score you received (e.g., 18): ").strip()
                        if not raw_input:
                            print("Score cannot be empty.")
                            continue
                        raw = float(raw_input)
                        total_input = input("Enter the total marks the assignment was out of (e.g., 20): ").strip()
                        if not total_input:
                            print("Total marks cannot be empty.")
                            continue
                        total = float(total_input)
                        if total <= 0:
                            print("Total must be greater than 0.")
                            continue
                        grade = (raw / total) * 100
                        print(f"Converted grade: {grade:.2f}%")
                        break
                    except ValueError:
                        print("Please enter valid numbers.")

            return Assignments(assignment_name, category, weight, grade)

        except KeyboardInterrupt:
            print("\nInput cancelled by user.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Add a validated assignment to the appropriate list and update progress
    def add_assignment(self, assignment):
        if assignment.category == 'Formative':
            self.formative_assignments.append(assignment)
        else:
            self.summative_assignments.append(assignment)
        self.show_progress()

    # Calculate total weighted grade for a specific category
    def calculate_category_total(self, category):
        if category == 'Formative':
            return sum(a.weighted_grade for a in self.formative_assignments)
        return sum(a.weighted_grade for a in self.summative_assignments)

    # Calculate overall GPA based on total weighted grades
    def calculate_gpa(self):
        total_weighted = sum(a.weighted_grade for a in self.formative_assignments + self.summative_assignments)
        return (total_weighted / 100) * 5 if total_weighted > 0 else 0.0

    # Display current progress and how close user is to passing
    def show_progress(self):
        FORMATIVE_PASS = Assignments.FORMATIVE_MAX_WEIGHT * 0.6
        SUMMATIVE_PASS = Assignments.SUMMATIVE_MAX_WEIGHT * 0.6
        formative_total = self.calculate_category_total('Formative')
        summative_total = self.calculate_category_total('Summative')
        print(f"\n[Progress]")
        print(f"Formative: {formative_total:.2f}/{FORMATIVE_PASS:.2f} needed to pass ({Assignments.FORMATIVE_MAX_WEIGHT} max weight)")
        print(f"Summative: {summative_total:.2f}/{SUMMATIVE_PASS:.2f} needed to pass ({Assignments.SUMMATIVE_MAX_WEIGHT} max weight)")
        if formative_total < FORMATIVE_PASS:
            print(f"You need {FORMATIVE_PASS - formative_total:.2f} more points in Formative to pass.")
        else:
            print("Formative: PASS threshold already met!")
        if summative_total < SUMMATIVE_PASS:
            print(f"You need {SUMMATIVE_PASS - summative_total:.2f} more points in Summative to pass.")
        else:
            print("Summative: PASS threshold already met!")

    # Print a formatted transcript of all assignments and grades
    def display_transcript(self):
        print(f"\n{'='*50}")
        print(f"GRADE TRANSCRIPT")
        print(f"{'='*50}")
        print(f"{'Assignment':<20} {'Category':<10} {'Grade(%)':<10} {'Weight':<10} {'Grade':<10}")
        print("-"*50)
        for assignment in self.formative_assignments:
            print(f"{assignment.assignment_name:<20} {'FA':<10} {assignment.grade:<10.1f} {assignment.weight:<10.1f} {assignment.weighted_grade:<10.2f}")
        for assignment in self.summative_assignments:
            print(f"{assignment.assignment_name:<20} {'SA':<10} {assignment.grade:<10.1f} {assignment.weight:<10.1f} {assignment.weighted_grade:<10.2f}")
        print("-"*50)
        formative_total = self.calculate_category_total('Formative')
        summative_total = self.calculate_category_total('Summative')
        print(f"Formatives ({Assignments.FORMATIVE_MAX_WEIGHT}){' '*30}{formative_total:.2f}")
        print(f"Summatives ({Assignments.SUMMATIVE_MAX_WEIGHT}){' '*30}{summative_total:.2f}")
        gpa = self.calculate_gpa()
        print(f"GPA{' '*41}{gpa:.3f}")
        print(f"{'='*50}")

    # Determine and print whether the user passed or failed based on thresholds
    def determine_pass_fail(self):
        FORMATIVE_PASS = Assignments.FORMATIVE_MAX_WEIGHT * 0.6
        SUMMATIVE_PASS = Assignments.SUMMATIVE_MAX_WEIGHT * 0.6
        formative_total = self.calculate_category_total('Formative')
        summative_total = self.calculate_category_total('Summative')
        print(f"Pass threshold - Formative: {FORMATIVE_PASS:.2f}, Summative: {SUMMATIVE_PASS:.2f}")
        print("")
        if formative_total >= FORMATIVE_PASS and summative_total >= SUMMATIVE_PASS:
            print("Result: PASS (You met the minimum in both categories!)")
        else:
            print("Result: FAIL (You did not meet the minimum in one or both categories.)")
            if formative_total < FORMATIVE_PASS:
                print(f"You needed {FORMATIVE_PASS - formative_total:.2f} more points in Formative.")
            if summative_total < SUMMATIVE_PASS:
                print(f"You needed {SUMMATIVE_PASS - summative_total:.2f} more points in Summative.")

# Main Program
if __name__ == "__main__":
    calculator = Grade_calculator()
    print("\nWelcome to the Grade Calculator!")
    print("Note: Maximum weights - Formative: 60%, Summative: 40%")
    print("To PASS: You need at least 36 points in Formative and 24 in Summative (60% of max possible).\n")
    while True:
        assignment = calculator.get_input_from_user()
        if assignment is None:
            break
        calculator.add_assignment(assignment)
        while True:
            choice = input("\nAdd another assignment? (yes/no): ").strip().lower()
            if not choice:
                print("Please answer 'yes' or 'no'.")
                continue
            if choice in ['yes', 'no']:
                break
            print("Please answer 'yes' or 'no'.")
        if choice != 'yes':
            break
    calculator.display_transcript()
    calculator.determine_pass_fail()