from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import telegram
from emoji.core import emojize

x = [["Menu", "\U0001F6E0", "menu"],
     ["Anti-flood", "\U0001F46E", "antiFlood"],
     ["Media", "\U0001F4F1", "media"],
     ["Anti-spam", "\U0001F48A", "antiSpam"],
     ["Reports", "\U0001F4E2", "reports"],
     ["User permissions", "\U0001F6B7", "userPermissions"]]


class botButton(telegram.InlineKeyboardButton):

    def __init__(self):
        super()
        self.button = None
        self.menu = []
        self.state = False
        self.count = 0
        self.info = None

    def init_button(self, button_name, button_emoji, button_callback_data):
        """
        Creating a single button object.
        :param button_name: The name of the button.
        :param button_emoji: The emoji on the button.
        :param button_callback_data: The callback data of the button.
        :return: self -> Class botButton object.
        """
        self.button = InlineKeyboardButton(text="{0}{1}".format(button_name if button_name != "" else "",
                                                                emojize(button_emoji) if button_emoji != "" else ""),
                                           callback_data=button_callback_data)
        if button_name.isnumeric():
            self.count = int(button_name)
        return self

    def get_button(self):
        """
        :return: The InlineKeyboardButton Object.
        """
        return self.button

    def change_button_state_on_off(self):
        """
        Change the button state to On or Off.
        On: The emoji will be green.
        Off: The emoji will be red.
        :return:
        """
        if self.state:
            self.state = False
            self.button.text = '\U0001F534'
        elif not self.state:
            self.state = True
            self.button.text = '\U0001F7E2'

    def set_button_count(self, action):
        """
        Increase or decrease the number on the button (for digit buttons).
        :param action: Plus or Minus character.
        :return:
        """
        if action == "+":
            self.count += 1
            self.button.text = self.count
        elif action == "-":
            if self.count >= 1:
                self.count -= 1
                self.button.text = self.count


    def get_button_count(self):
        """
        Returns the Integer value on the button text (for digit buttons).
        :return: Integer value of the button text.
        """
        return self.count

    def set_button_info(self, info):
        """
        :param info: Information (string) about the button such as functionality of the button.
        :return:
        """
        self.info = info

    def get_button_info(self):
        """
        :return: Information (string) about the button such as functionality of the button.
        """
        return self.info

    def get_button_state(self):
        """
        :return: The state of the button, True or False.
        """
        return self.state

    def change_three_button_state(self, state):
        pass

# temp = botButton()
# temp.init_button("2", "", "menu")
# print(temp.get_button()[0])
