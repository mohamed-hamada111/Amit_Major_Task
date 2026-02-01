class Person:
    """
    Base class that represents any person in the hospital system.
    This class is meant to be inherited by Patient and Staff.
    """

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def view_info(self) -> str:
        """
        Returns basic information about the person.
        """
        return f"Name: {self.name}, Age: {self.age}"


class Staff(Person):
    """
    Represents a staff member in the hospital.
    Inherits common attributes from Person.
    """

    def __init__(self, name: str, age: int, position: str):
        # Call the constructor of the parent class (Person)
        super().__init__(name, age)

        # Staff-specific attribute
        self.position = position

        # This can later be used to link the staff to a department
        self.department = None

    def assign_department(self, department):
        """
        Assigns the staff member to a department.
        This keeps the class flexible and easy to connect later.
        """
        self.department = department

    def view_info(self) -> str:
        """
        Returns detailed information about the staff member.
        Overrides Person.view_info().
        """
        info = f"Name: {self.name}, Age: {self.age}, Position: {self.position}"

        if self.department:
            info += f", Department: {self.department.name}"

        return info
