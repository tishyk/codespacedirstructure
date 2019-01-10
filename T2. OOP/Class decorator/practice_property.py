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

    # use property decorator,
    # setter -<-- add all Responsibilities
    # deleter -<-- reset do default value
    def requirements_list(self):
        print("Revert to initial state:{}".format(self.__Basic_Requirements))
        return self.__Basic_Requirements.split("\n")

    # the same
    def responsibility_list(self):
        return self.__Basic_Responsibilities.split("\n")