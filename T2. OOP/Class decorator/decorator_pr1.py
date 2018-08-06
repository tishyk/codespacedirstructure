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


class EmployeeCV:
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

    @property
    def requirements_list(self):
        """
        Property which removes empty string from basic requirements list
        and remove spaces before and after each requirement in list
        :return: formatted list of basic requirements
        """
        return list(map(lambda req: req.strip(),
                        filter(lambda requirement: requirement.strip(), self.__Basic_Requirements.split("\n"))))

    @requirements_list.setter
    def requirements_list(self, requirement_key_word=''):
            if requirement_key_word and type(requirement_key_word) == str:
                for requirement in Requirements.split('\n'):
                    if requirement_key_word.lower() in requirement.lower() and \
                                    requirement not in self.__Basic_Requirements:
                        self.__Basic_Requirements = self.__Basic_Requirements + '\n' + requirement
                        break
            else:
                for requirement in Requirements.split('\n'):
                    if requirement not in self.__Basic_Requirements:
                        self.__Basic_Requirements = self.__Basic_Requirements + '\n' + requirement
                        break

    @requirements_list.deleter
    def requirements_list(self):
        self.__Basic_Requirements = EmployeeCV.__Basic_Requirements

    @property
    def responsibilities_list(self):
        return list(map(lambda req: req.strip(),
                        filter(lambda responsibility: responsibility.strip(), self.__Basic_Responsibilities.split("\n"))))

    @responsibilities_list.setter
    def responsibilities_list(self, responsibility_key_word=''):
            if responsibility_key_word and type(responsibility_key_word) == str:
                for responsibility in Responsibilities.split('\n'):
                    if responsibility_key_word.lower() in responsibility.lower() and \
                                    responsibility not in self.__Basic_Responsibilities:
                        self.__Basic_Responsibilities = self.__Basic_Responsibilities + '\n' + responsibility
                        break
            else:
                for responsibility in Responsibilities.split('\n'):
                    if responsibility not in self.__Basic_Responsibilities:
                        self.__Basic_Responsibilities = self.__Basic_Responsibilities + '\n' + responsibility
                        break

    @responsibilities_list.deleter
    def responsibilities_list(self):
        self.__Basic_Responsibilities = EmployeeCV.__Basic_Responsibilities


a = EmployeeCV("John", "Smith")
print(a.requirements_list)
a.requirements_list = 2
a.requirements_list = 'Agile'
a.requirements_list = 'Agile'
a.requirements_list = 'User stories'
print(a.requirements_list)
del a.requirements_list
print(a.requirements_list)

print("\n\n\n")

print(a.responsibilities_list)
a.responsibilities_list = 'plan'
a.responsibilities_list = 'Testing'
a.responsibilities_list = 'delivery'
a.responsibilities_list = 'meetings'
a.responsibilities_list = 'meetings'
print(a.responsibilities_list)
del a.responsibilities_list
print(a.responsibilities_list)
