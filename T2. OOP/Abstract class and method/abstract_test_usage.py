from abstract_test import BaseTestAbstract

class BaseTest(BaseTestAbstract):
    def setup(self):
        # check state 1
        # check state 2
        pass

    def run(self):
        # run step 1
        # run step 2
        # run step 3
        pass

    def cleanup(self):
        # revert step 3,2,1
        # clean log
        pass


if __name__ == "__main__":
    test = BaseTest()
