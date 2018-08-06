Requirements = """Working experience with Firebase, MySQL, Mopub, JSON
Ability to dive into complex problems & find their root cause
Working experience in Jira, Confluence, Android studio, Xcode
Ability to create documentation and report the defects in English
Experience in work with User stories
Practical Experience working in Agile and fast-paced projects"""

Responsibilities = """
Plan test activities and assignments
Testing assigned tasks on mobile and/or web resolutions
Acceptance, regression and smoke testing
Log tests results and document test cases/check lists
Involve in project design/software delivery
Participate in sprint meetings
"""


class EmployeeVC:
    __Basic_Requirements = """
        2+ years experience as a QA Engineer
        2+ years of experience of Mobile Testing
        1+ years experience of testing monetisation tasks
        Ability to design and maintain test cases/checklists/requirements
        Practical experience with API testing
        """

    __Basic_Responsibilities = """
        Design test cases/check lists/User Guides and/or other business documentation
        Testing monetisation partners integrated SDK
        """

    def __init__(self, first, last):
        self.first = first
        self.last = last

    # use property decorator,
    # setter -<-- add one line from Responsibilities
    # deleter -<-- reset do default value
    @property
    def requirements_list(self):
        print("Revert to initial state: {}".format(self.__Basic_Requirements))
        return self.__Basic_Requirements.split("\n")

    @requirements_list.setter
    def requirements_list(self, index):
        self.__Basic_Requirements = self.__Basic_Requirements + '{}\n        '.format(Requirements.split("\n")[index])
        print("Set new value for Basic_Requirements: {}".format(self.__Basic_Requirements))

    @requirements_list.deleter
    def requirements_list(self):
        del self.__Basic_Requirements
        print("Set default value for Basic_Requirements: {}".format(self.__Basic_Requirements))

    # the same
    @property
    def responsibility_list(self):
        print("Default value for Basic_Responsibilities: {}".format(self.__Basic_Responsibilities))
        return self.__Basic_Responsibilities.split("\n")

    @responsibility_list.setter
    def responsibility_list(self, index):
        self.__Basic_Responsibilities = self.__Basic_Responsibilities + '{}\n        '.format(Responsibilities.split("\n")[index])
        print("Set new value for Basic_Responsibilities: {}".format(self.__Basic_Responsibilities))

    @responsibility_list.deleter
    def responsibility_list(self):
        del self.__Basic_Responsibilities
        print("Set default value for Basic_Responsibilities: {}".format(self.__Basic_Responsibilities))


emp1 = EmployeeVC('Vasya', 'Pupkin')
emp1.requirements_list
emp1.requirements_list = 2
emp1.requirements_list = 1
del emp1.requirements_list
emp1.requirements_list

emp1.responsibility_list
emp1.responsibility_list = 2
emp1.responsibility_list = 3
del emp1.responsibility_list
