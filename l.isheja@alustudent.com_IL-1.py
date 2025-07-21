# -----------------------------
# Grade Generator Calculator (Single Student Version)
# -----------------------------
# NOTE: The assignment requests comparison to an "average" grade. In a real classroom, this would be the class average.
# For this individual lab, we use a fixed threshold (e.g., 50) for each category, as only one student's data is available.
# All error handling and input validation is included for robustness.

class Assignments:
    # Maximum weights for each category
    FORMATIVE_MAX_WEIGHT = 60
    SUMMATIVE_MAX_WEIGHT = 40

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

    def validate_category(self, category):
        # Check if the category is either 'Formative' or 'Summative'
        if category not in ['Formative', 'Summative']:
            raise ValueError("Category must be either 'Formative' or 'Summative'")

    def validate_weight(self, weight):
        # Check if the weight is between 0 and 100
        if not (0 <= weight <= 100):
            raise ValueError("Weight must be between 0 and 100")

    def validate_grade(self, grade):
        # Check if the grade is between 0 and 100
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100")

# -----------------------------
# Grade Calculator Class (Single Student)
# -----------------------------
class Grade_calculator:
    def __init__(self):
        # Initialize lists to store assignments
        self.formative_assignments = []
        self.summative_assignments = []

    def get_category_total_weight(self, category):
        # Calculate total weight for a category
        if category == 'Formative':
            return sum(a.weight for a in self.formative_assignments)
        return sum(a.weight for a in self.summative_assignments)

    def validate_category_weight(self, category, new_weight):
        # Check if adding new weight would exceed category limit
        current_weight = self.get_category_total_weight(category)
        if category == 'Formative' and (current_weight + new_weight) > Assignments.FORMATIVE_MAX_WEIGHT:
            raise ValueError(f"Total Formative weight cannot exceed {Assignments.FORMATIVE_MAX_WEIGHT}%")
        elif category == 'Summative' and (current_weight + new_weight) > Assignments.SUMMATIVE_MAX_WEIGHT:
            raise ValueError(f"Total Summative weight cannot exceed {Assignments.SUMMATIVE_MAX_WEIGHT}%")

    def get_input_from_user(self):
        # Collect assignment details from user with robust error handling
        try:
            assignment_name = input("\nEnter the assignment (e.g, Group Project, Quiz4): ").strip()
            if not assignment_name:
                raise ValueError("Assignment name cannot be empty.")
            # Get and validate category
            while True:
                category = input("Enter the category (Formative/Summative): ").strip()
                if category in ['Formative', 'Summative']:
                    break
                print("Please enter either 'Formative' or 'Summative'")
            # Get and validate weight
            while True:
                try:
                    weight_input = input("Enter assignment weight (0-100): ").strip()
                    if not weight_input:
                        raise ValueError("Weight cannot be empty.")
                    weight = float(weight_input)
                    self.validate_category_weight(category, weight)
                    if 0 <= weight <= 100:
                        break
                    print("Weight must be between 0 and 100")
                except ValueError as e:
                    print(f"Invalid input: {e}")
            # Get and validate grade
            while True:
                try:
                    grade_input = input("Enter grade received (0-100): ").strip()
                    if not grade_input:
                        raise ValueError("Grade cannot be empty.")
                    grade = float(grade_input)
                    if 0 <= grade <= 100:
                        break
                    print("Grade must be between 0 and 100")
                except ValueError as e:
                    print(f"Invalid input: {e}")
            # Create and return a new assignment
            return Assignments(assignment_name, category, weight, grade)
        except KeyboardInterrupt:
            print("\nInput cancelled by user.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def add_assignment(self, assignment):
        # Add assignment to the appropriate category list
        if assignment.category == 'Formative':
            self.formative_assignments.append(assignment)
        else:
            self.summative_assignments.append(assignment)

    def calculate_category_total(self, category):
        # Calculate total weighted grade for a category
        if category == 'Formative':
            return sum(a.weighted_grade for a in self.formative_assignments)
        return sum(a.weighted_grade for a in self.summative_assignments)

    def calculate_gpa(self):
        # Calculate GPA out of 5
        total_weighted = sum(a.weighted_grade for a in self.formative_assignments + self.summative_assignments)
        return (total_weighted / 100) * 5 if total_weighted > 0 else 0.0

    def display_transcript(self):
        # Display student's transcript
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

    def determine_pass_fail(self, min_required=50):
        # Determine pass/fail for the student based on fixed minimum threshold
        formative_total = self.calculate_category_total('Formative')
        summative_total = self.calculate_category_total('Summative')
        if formative_total >= min_required and summative_total >= min_required:
            print("Result: PASS (You met the minimum in both categories!)")
        else:
            print("Result: FAIL (You did not meet the minimum in one or both categories.)")

# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":
    # Start the grade calculator for a single student
    calculator = Grade_calculator()
    print("\nWelcome to the Grade Calculator!")
    print("Note: Maximum weights - Formative: 60%, Summative: 40%")
    print(" ")
    while True:
        assignment = calculator.get_input_from_user()
        if assignment is None:
            break
        calculator.add_assignment(assignment)
        choice = input("\nAdd another assignment? (yes/no): ").lower()
        if choice != 'yes':
            break
    # Display transcript and pass/fail result
    calculator.display_transcript()
    calculator.determine_pass_fail()
