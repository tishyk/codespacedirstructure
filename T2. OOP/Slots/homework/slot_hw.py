#! usr/bin/python

# Create class ChatView with all necessary parent classes that can be used.
# create UsersView parent class for ChatView. Use slots variable for User class parent of UsersView class.
# for example username, user_id, status, user_device (PC, Android, Mac ..), last joining etc.
# Chat window get from chat.gif

class User:
    __slots__ = ['username', 'user_id', 'status', '_user_device', 'last_joining'] # TODO: Q: Мені не вдалось лишили у слотах і у проперті user_device, довелось називати по різному. Чи правильно я зробив чи є інший підхід для використання однієї і тієї самої змінної у проперті і слотах?
    __user_devices = ['PC', "Android", 'Mac']

    def __init__(self):
        self._user_device = None
    # slots

    @property
    def user_device(self):
        return self._user_device

    @user_device.setter
    def user_device(self, usr_device):
        if usr_device in self.__user_devices:
            self._user_device = usr_device
        else:
            raise ValueError(f"Possible values are: {[x for x in self.__user_devices]}, but {usr_device} was given") # TODO: Q: Чи правильно таким чином оброблювати некоректне значення? Чи є правильніший підхід? Зараз я отримую значення спочатку один в один, а потім вже з підставленими значеннями - чи є можливість отримати одразу повідомлення з проставленими значеннями (це ж f стрінга)? Чи це відображається безпосередньо рядок який зарайзив ексепшен і з цим нічого не вдіяти?

    @user_device.deleter
    def user_device(self):
        self._user_device = None


class UsersView(User):
    pass
# ...

#class ChatView(UsersView, OptionView, MessageView, MessageSenderView, LogView):
    #pass

user1 = User()
user1.user_device = 'PC'
print(user1.user_device)
del user1.user_device

print(user1.user_device)
user1.user_device = 'PC1'
