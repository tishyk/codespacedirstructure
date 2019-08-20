class Cat():
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.known_tricks = ['granny', 'kitty']

    def show_trick(self, trick):
        if trick in self.known_tricks:
            print(f"Cat show trick {trick}")
        else:
            print('meow..?')

    def remember_trick(self, trick):
        self.known_tricks.append(trick)
        print(f"Cat knows a new trick {trick}")
        return trick


class Robot():
    @staticmethod
    def search_memo(memo_str):
        found_memo = ""
        print('Memos database connection..')
        for memo in Memo.MEMOS.values():
            if memo_str in memo:
                print("Memo found. Exit DB")
                found_memo = memo
                break
        return found_memo

    @staticmethod
    def add_memo(memo):
        ok = False
        print("Check database memo record")
        if Memo.MEMOS.setdefault(Memo.COUNT - 1, memo) != memo:
            print("Database memo record conflict found!")
            print("Solve db record conflict method execution")
        else:
            ok = True
        return ok

    @staticmethod
    def show_memos():
        for memo in Memo.MEMOS:
            print(memo)

class Memo():
    MEMOS = {0: """National Centre for Nuclear Robotics is unique
             in working on practical problems with industry,
             while simultaneously generating the highest calibre of 
             cutting-edge academic research – exemplified by 
             this landmark paper.""",
             1: "granny is comming",
             2: "kitty kitty kitty"}
    COUNT = 3

    @classmethod
    def add_memo(cls, memo):
        cls.MEMOS[cls.COUNT - 1] = memo

    @classmethod
    def get_memo(cls, id):
        return cls.MEMOS.get(id, '')

class RoboCat():
    def __init__(self, serial, country):
        self.country = country
        self.serial = serial