import datetime


def error_level(level):
    def decorator(logman):
        def wrapper(self, message):
            logman(self, '{} {}: {}\n'.format(level, datetime.datetime.now(), message))

        return wrapper

    return decorator


class Logger:
    __slots__ = ['name', 'file']

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open('{}_log.txt'.format(self.name), 'a+')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    @error_level('INFO')
    def info(self, message):
        self.file.write(message)

    @error_level('WARNING')
    def warning(self, message):
        self.file.write(message)

    @error_level('ERROR')
    def error(self, message):
        self.file.write(message)

    @error_level('CRITICAL')
    def critical(self, message):
        self.file.write(message)


with Logger('hometask') as logger:
    logger.info('Student opened PyCharm')
    logger.info('Creating custom logger class')
    logger.warning('User adding slots to class Logger')
    logger.info('Create decorator method for log level')
    logger.error('Typing some code')
    logger.critical('Commits changes to repository')
    logger.critical('On the way to lesson')
