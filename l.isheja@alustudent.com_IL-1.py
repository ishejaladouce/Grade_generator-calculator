class Assignments:
    def __init__(self, assignment_name, category, weight, grade):
        """
        Initialize a new assignment with validation.
        
        Parameters:
            name (str): The name of the assignment (e.g., 'Group Project', 'Quiz4')
            category (str): Either 'Formative' or 'Summative'
            weight (float): The percentage weight of this assignment (0-100)
            grade (float): The grade received on this assignment (0-100)
        """

        #store the assignment deatails after validation
        self.assignment_name = assignment_name
        self.validate_category(category)
        self.category = category
        self.validate_weight(weight)
        self.weight = weight
        self.validate_grade(grade)
        self.grade = grade

    def validate_category(self, category):
            # check if the category is either 'Formative' or 'Summative'

            if category not in ['Formative', 'Summative']:
                raise ValueError("Category must be either 'Formative' or 'Summative'")

    def validate_weight(self, weight):
            #check if the weight is between 0 and 100
            if not (0 <= weight <= 100):
                raise ValueError("Weight must be between 0 and 100")

    def validate_grade(self, grade):
            #check if the grades are between 0 and 100
            if not (0<= grade <= 100):
                raise ValueError("Grades must be between 0 and 100")

#create  a class(Grade_calculator) that will handle all our calculations and user interactions.
class Grade_calculator:
    def __init__(self):
        #initialize empty lists to store assignments
        self.formative_assignments = [] #store formative assignments
        self.summative_assignments = [] #store summative assignments

    #get input from user
    def get_input_from_user(self):
        try:
            #get the assignment name
            assignment_name = input("\nEnter the assignment  (e.g, Group Project, Quiz4): ")

            #get and validate category
            while True:
                category = input("Enter the category (Formative/Summative): ")
                if category in ['Formative', 'Summative']:
                    break
                print("Please enter either 'Formative' or 'Summative'")

            #get and validate weigt 
            while True:
                try:
                    weight = float(input("Enter assignment weight (0-100): "))
                    if 0<= weight <= 100:
                        break
                    print("Weight must be between 0 and 100")
                except ValueError:
                    print("Please enter a valid number")

            #get and validate grade
            while True:
                try:
                    grade = float(input("Enter grade received (0-100):"))
                    if 0 <= grade <= 100:
                        break
                    print("Grade must be between 0 and 100")
                except ValueError:
                    print("Please enter a valid number")

            #create and return a new assignment
            return Assignments(assignment_name, category, weight, grade)
        except KeyboardInterrupt:
            print("\ncancelled by user")
            return None

    def add_assignment(self, assignment):
        #Add a new assigment to the appropriate category list
        if assignment.category == 'Formative':
            self.formative_assignments.append(assignment)
        else:
            self.summative_assignments.append(assignment)

    def calculate_category_totals(self):
        """ 
        Calculate the total weighted grade for each category.
        Return a turple: (formative_total, summative__total)
        """
        formative_total = sum ((a.grade * a.weight / 100) for a in self.formative_assignments)
        summative_total = sum ((a.grade * a.weight / 100) for a in self.summative_assignments)
        return formative_total, summative_total

    def calculate_gpa(self):
        # Calculate the overall GPA out of 5 based on all assignments and return the GPA as a float
        all_assignments = self.formative_assignments + self.summative_assignments
        if not all_assignments:
            return 0.0
        total_weighted_grade = sum((a.grade * a.weight / 100) for a in all_assignments)
        total_weight = sum(a.weight for a in all_assignments)
        if total_weight == 0:
            return 0.0
        gpa = (total_weighted_grade / total_weight) * 5
        return gpa


#Main function to run the grade calculator
if __name__ == "__main__":
    calculator = Grade_calculator()
    print("\nWelcome to the Grade Calculator!")
    print(" ")

    while True:
        #Get assignment deatils
        assignment = calculator.get_input_from_user()
        if assignment is None: #User cancelled
            break

        #Add assignment to appropriate list
        calculator.add_assignment(assignment)

        #Ask if user wants to another assigment
        choice = input("\nAdd another assignment? (yes/no): ").lower()
        if choice != 'yes':
            break

    #After input, calculate and display category totals
    formative_total, summative_total = calculator.calculate_category_totals()
    print(f"\nFormative Category Total: {formative_total:.2f}")
    print(f"Summative Category Total: {summative_total:.2f}")

    #calculate and display GPA
    gpa = calculator.calculate_gpa()
    print(f"\nYour GPA (out of 5): {gpa:.2f}")
