from abc import ABCMeta, abstractmethod
from sys import stdout as console


class Command(metaclass=ABCMeta):
    """Application Command Interface"""
    name = ""  # Command object name declaration for client usage

    def __init__(self, history, trash):
        self.history = history
        self.trash = trash

    @abstractmethod
    def execute(self) -> None:
        """Method to call and store required action. Client usage"""
        raise NotImplementedError()

    def cancel(self) -> None:
        """Method to revert execute method action and remove it from store. Client usage"""
        raise NotImplementedError()


class RmCommand(Command):
    """ Application rm command description"""
    name = "rm"

    def execute(self) -> None:
        console.write("You are executed \"rm\" command\n")

    def cancel(self) -> None:
        console.write("You are canceled \"rm\" command\n")


class UptimeCommand(Command):
    """ Application uptime command description"""
    name = "uptime"

    def execute(self) -> None:
        console.write("You are executed \"uptime\" command\n")

    def cancel(self) -> None:
        console.write("You are canceled \"uptime\" command\n")


class UndoCommand(Command):
    """ Application undo command description"""
    name = "undo"

    def execute(self) -> None:
        try:
            cmd = self.history.pop()
            self.trash.append(cmd)
            console.write("Undo command \"{0}\"\n".format(cmd.name))
            cmd.cancel()

        except IndexError:
            console.write("ERROR: HISTORY is empty\n")


class RedoCommand(Command):
    """ Application redo command description"""
    name = "redo"

    def execute(self) -> None:
        try:
            cmd = self.trash.pop()
            self.history.append(cmd)
            console.write("Redo command \"{0}\"\n".format(cmd.name))
            cmd.execute()
        except IndexError:
            console.write("ERROR: TRASH is empty\n")


class HistoryCommand(Command):
    """ Application history command description"""
    name = "history"

    def execute(self) -> None:
        i = 0
        for cmd in self.history:
            console.write("{0}: {1}\n".format(i, cmd.name))
            i = i + 1


class ExitCommand(Command):
    """ Application exit command description.
     SessionClosed exception raise """
    name = "exit"

    def execute(self) -> Exception:
        raise SessionClosed("Good bye!")


class ApplicationCommandsFactory():
    """Create command objects for current application page"""

    HISTORY = list()  # Storage of used commands. Undo data
    TRASH = list()  # Storage of commands that were removed from history storage. Redo data

    def main_window_cmds(self):
        """Here is an example of main window available commands"""
        # {'rm': RmCommand(),
        # 'uptime': UptimeCommand(),
        # 'undo':UndoCommand(),
        # 'redo': RedoCommand(),
        # 'history': HistoryCommand(),
        # 'exit': ExitCommand()}
        return {command.name: command(self.__class__.HISTORY, self.__class__.TRASH)
                for command in Command.__subclasses__()}

    def popup_window_cmds(self):
        """Here is an example of popup window available commands"""
        return {'exit': ExitCommand(self.__class__.HISTORY, self.__class__.TRASH)}


class SessionClosed(Exception):
    """ Handling 'exit' command exception """

    def __init__(self, value: Exception):
        self.value = value


# Shell Application client code
def main() -> None:
    commands_storage = ApplicationCommandsFactory()
    MainWindowCommands = commands_storage.main_window_cmds()
    PopUpWindowCommands = commands_storage.popup_window_cmds()

    try:
        while True:
            console.flush()
            console.write("push >> ")

            cmd = input()

            try:
                command = MainWindowCommands[cmd]
                command.execute()
                if (not isinstance(command, UndoCommand) and not
                isinstance(command, RedoCommand) and not
                isinstance(command, HistoryCommand)):
                    commands_storage.TRASH = list()
                    commands_storage.HISTORY.append(command)

            except KeyError:
                console.write("ERROR: Command \"%s\" not found\n" % cmd)

    except SessionClosed as e:
        console.write(e.value)


if __name__ == "__main__":
    main()
