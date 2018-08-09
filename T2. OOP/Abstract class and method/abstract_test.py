from abc import ABC, abstractmethod

class BaseTestAbstract(ABC):
    @abstractmethod
    def setup(self):
        # Set test precondition, check requirements
        pass

    @abstractmethod
    def run(self):
        #
        pass

    @abstractmethod
    def cleanup(self):
        """
        Convenience method for setting the current state do initial.
        """

    def clear_logs(self):
        """
        Clear all logs in the local directory
        """

    def _pass(self):
        """
        Convenience method for setting the current results object to PASS.
        """

    def _fail(self):
        """
        Convenience method for setting the current results object to FAIL.
        """


