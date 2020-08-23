from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, TypeHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, TelegramError

import botButton
from emoji.core import emojize
import botData




commands = ["start", "help", "setup", "welcome", "setRules", "userLeft", "rules", "admin"]  # Bot commands.
buttonRegex = r'^[exp|deleteServiceMsg|kickBots|welcomeRules|welcomeMessage|adminReports|delOldWelcome|userLeftMessage]+$'  # Button callback data regex.
mainMenuRegex = r'^[menu|antiFlood|media|antiSpam|reports|userPermissions]+$'   # Main menu buttons callback regex.


buttonNames = ["Rules", "Delete service messages", "Kick Bots", "Welcome + Rules", "Welcome message", "Admin Report",
               "Delete old Welcome", "User left message"]   # The name of the buttons in the Menu.

# Main menu buttons [name, emoji, callback data].
main_menu = [["Menu", "\U0001F6E0", "menu"],
             ["Anti-flood", "\U0001F46E", "antiFlood"],
             ["Media", "\U0001F4F1", "media"],
             ["Anti-spam", "\U0001F48A", "antiSpam"],
             ["Reports", "\U0001F4E2", "reports"],
             ["User permissions", "\U0001F6B7", "userPermissions"]]

# Main menu buttons [[name, emoji, callback data],[emoji, "", callback data]].
menu_keyboard = [[["Rules", "", "exp"], ["\U0001F534", "", "0"]],
                 [["Delete service messages", "", "deleteServiceMsg"], ["\U0001F534", "", "1"]],
                 [["Kick Bots", "", "kickBots"], ["\U0001F534", "", "2"]],
                 [["Welcome + Rules", "", "welcomeRules"], ["\U0001F534", "", "3"]],
                 [["Welcome message", "", "welcomeMessage"], ["\U0001F534", "", "4"]],
                 [["Admin Report", "", "adminReports"], ["\U0001F534", "", "5"]],
                 [["Delete old Welcome", "", "delOldWelcome"], ["\U0001F534", "", "6"]],
                 [["User left message", "", "userLeftMessage"], ["\U0001F534", "", "7"]],
                 [["", "\U00002796", "-"],["0", "","num"],["", "\U00002795", "+"]],
                 [["Back", "\U0001F519", "back"]]]

def get_user_permission(update, context):
    """
    Checks the permition a user have in the group and return True if the user is admin or creator,
    Else return False.
    :param update:
    :param context:
    :return:
    """
    userStatus = context.bot.get_chat_member(update.message.chat.id, update.effective_user['id'])['status']
    if userStatus in ['creator', 'admin']:
        return True
    return False


class peaceMakerBot:

    def __init__(self, bot_token):
        self.updater = Updater(bot_token, use_context=True)
        self.dp = self.updater.dispatcher
        self.main_keyboard = []
        self.menu_keyboard_list = []
        self.menu_button = []
        self.welcome_message = None
        self.rule_message = None
        self.old_welcome_message = None
        self.userLeftMessage = None
        self.init_handlers()
        self.init_main_keyboard()
        self.init_menu_keyboard()
        # Start the bot
        self.updater.start_polling()
        self.updater.idle()

    def init_handlers(self):
        """
        Initialize handlers for bot commands and for callback query.
        :return:
        """
        # Bot command handlers.
        self.dp.add_handler(CommandHandler(command=commands[0], callback=self.start, filters=Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[1], callback=self.help_command, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[2], callback=self.show_main_keyboard, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[3], callback=self.set_welcome, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[4], callback=self.set_rules, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[5], callback=self.set_left_user_message, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[6], callback=self.show_rules, filters=~Filters.private))
        self.dp.add_handler(CommandHandler(command=commands[7], callback=self.report_to_admin, filters=~Filters.private))
        # Callback query handlers.
        self.dp.add_handler(CallbackQueryHandler(self.choose_menu_handler, pattern=mainMenuRegex))
        self.dp.add_handler(CallbackQueryHandler(self.button_info, pattern=buttonRegex))
        self.dp.add_handler(CallbackQueryHandler(self.menu_button_callback, pattern=r'^[0-9|back|+|-]+$'))
        # Service message handlers.
        self.dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, self.user_join_handler))
        self.dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, self.user_left_handler))


    def start(self, update, context):
        # ToDO: Send the user a bot user guide
        pass

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text("Help!")

    def set_welcome(self, update, context):
        """Set the new welcome message."""
        if not get_user_permission(update, context):
            return
        self.welcome_message = update.message.text.replace("/welcome ", "")
        if '$title' in self.welcome_message:
            self.welcome_message = self.welcome_message.replace("$title", update.effective_chat["title"])
        update.message.reply_text("Welcome message has been set {0}".format(emojize('\U0001F44F')))

    def set_rules(self, update, context):
        """Set the new rules of the group."""
        if not get_user_permission(update, context):
            return
        self.rule_message = update.message.text.replace("/setRules ", "")
        update.message.reply_text("Rules has been set {0}".format(emojize('\U0001F44F')))

    def set_left_user_message(self, update, context):
        """Set a message for user that leaving the group"""
        if not get_user_permission(update, context):
            return
        self.userLeftMessage = update.message.text.replace("/userLeft ", "")
        update.message.reply_text("User left message has been set {0}".format(emojize('\U0001F44F')))

    def show_rules(self, update, context):
        """Shows the group rules"""
        if self.rule_message is not None:
            if self.menu_button[0][1].state:
                context.bot.send_message(chat_id=update.effective_user["id"], text=self.rule_message)
            else:
                update.message.reply_text(self.rule_message)

    def report_to_admin(self, update, context):
        """Under construction"""
        count = 0
        usr=""
        adminList = context.bot.get_chat_administrators(update.message.chat["id"])
        print(adminList)
        for admin in adminList:
            print(admin)
            if not admin.user["is_bot"]:
                count += 1

                print(admin.user.username)
                usr = "@" + admin.user.username


            context.bot.send_message(chat_id=update.message.chat.id,text=usr)
            context.bot.send_message(chat_id=update.message.chat.id, text="Alert sent to {0} Admins".format(count))



    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Bot Commands^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def init_main_keyboard(self):
        """
        Initializing the main keyboard.
        :return:
        """
        if len(self.main_keyboard) == 0:
            button = botButton.botButton()
            for btn in main_menu:
                keyboard = button.init_button(btn[0], btn[1], btn[2]).get_button()
                self.main_keyboard.append([keyboard])

    def init_menu_keyboard(self):
        """
        Initializing the menu keyboard, The menu keyboard depends on the menu_keyboard button list.
        :return:
        """

        for btns in menu_keyboard:
            button_row = []
            for btn in btns:
                button_row.append(btn)
            number_of_buttons = len(button_row)
            if number_of_buttons == 1:
                button1 = botButton.botButton()
                keyboard1 = button1.init_button(button_row[0][0], button_row[0][1], button_row[0][2])
                self.menu_button.append(keyboard1)
                self.menu_keyboard_list.append([keyboard1.get_button()])
            if number_of_buttons == 2:
                button1 = botButton.botButton()
                button2 = botButton.botButton()
                keyboard1 = button1.init_button(button_row[0][0], button_row[0][1], button_row[0][2])
                keyboard2 = button2.init_button(button_row[1][0], button_row[1][1], button_row[1][2])
                keyboard1 = [keyboard1,keyboard2]
                self.menu_button.append(keyboard1)
                self.menu_keyboard_list.append([keyboard1[0].get_button(), keyboard1[1].get_button()])
            if number_of_buttons == 3:
                button1 = botButton.botButton()
                button2 = botButton.botButton()
                button3 = botButton.botButton()
                keyboard1 = button1.init_button(button_row[0][0], button_row[0][1], button_row[0][2])
                keyboard2 = button2.init_button(button_row[1][0], button_row[1][1], button_row[1][2])
                keyboard3 = button3.init_button(button_row[2][0], button_row[2][1], button_row[2][2])
                keyboard1 = [keyboard1, keyboard2, keyboard3]
                self.menu_button.append(keyboard1)
                self.menu_keyboard_list.append([keyboard1[0].get_button(), keyboard1[1].get_button(), keyboard1[2].get_button()])


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Initialization^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def show_main_keyboard(self, update, context):
        """
        Send the main keyboard to the user (admin)
        :param update:
        :param context:
        :return:
        """
        if get_user_permission(update, context):
            text = "Hello {0}, I am {1} and I'll help you manage and enforce your group rules," \
                   "Please select an option"
            context.bot.send_message(chat_id=update.effective_user["id"],
                                     text=text.format(update.effective_user["first_name"],
                                                      context.bot.first_name),
                                     reply_markup=InlineKeyboardMarkup(self.main_keyboard))

    def show_menu_keyboard(self,update, context):
        """
        Send the menu keyboard to the user (admin)
        :param update:
        :param context:
        :return:
        """
        try:
            query = update.callback_query
            text = "Click the buttons on the left to get details about each option" \
                   "\nOR\nClick the buttons on the right to turn On/Of the option"
            context.bot.edit_message_text(chat_id=query.message.chat.id,
                                          message_id=query.message.message_id,
                                          text=text
                                          ,reply_markup=InlineKeyboardMarkup(self.menu_keyboard_list))
        except TelegramError as err:
            print(err)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Show and Print^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def choose_menu_handler(self, update, context):
        query = update.callback_query
        if query.data == "menu":
            self.show_menu_keyboard(update, context)

    def button_info(self, update, context):
        query = update.callback_query
        text = botData.button_info(query.data)
        context.bot.answer_callback_query(query["id"], text=text, show_alert=True)

    def menu_button_callback(self, update, context):
        """
        The main callback method calls other handler depending on the callback query data.
        :param update:
        :param context:
        :return:
        """

        query = update.callback_query
        print(query)
        text = "Hello {0}, I am {1} and I'll help you manage and enforce your group rules," \
               "Please select an option"
        if query.data == "back":
            context.bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                          text=text.format(update.effective_user["first_name"],
                                                           context.bot.first_name),
                                          reply_markup=InlineKeyboardMarkup(self.main_keyboard))
        elif query.data == "9":
            self.rules_button_ahandler(update, context)

        elif query.data == "+" or query.data == "-":
            self.menu_button[8][1].set_button_count(query.data)
            self.show_menu_keyboard(update, context)



        else:
            index = int(query.data)
            self.menu_button[index][1].change_button_state_on_off()
            self.show_menu_keyboard(update, context)
            context.bot.answer_callback_query(query["id"], "{0} is {1}"
                                              .format(self.menu_button[index][0].button.text,
                                                      "On" if self.menu_button[index][1].
                                                      state == True else "Off"),
                                              short_alert=True)

    def user_join_handler(self, update, context):
        """
        Activated when a new user joins the group,
        1. In case the new user is a bot and it is not allowed to add bots to the group,
        The bot will kick the new bot user from the group.
        2. If a welcome message exists it will be displayed in the group according to the pattern of the saved messages.
        3. If there are saved rules , they will be displayed to the user below the Welcome message
        if the Welcome message exists.
        4. If there are saved rules and a Welcome message does not exist, only the rules will be displayed to the user.
        5. Remove the service messages if flag is True

        Args:
            :param update: This object represents an incoming update.
            :param context: This is a context object passed to the callback called by telegram.ext.Handler
        :return:
        """
        chatId = update.message.chat["id"]
        if update.message.new_chat_members[0]["is_bot"] and self.menu_button[2][1].state == True:
            # User is bot and bots don't allowed.
            # Kick the bot user.
            # Send warning message to the user that added the bot.
            context.bot.kick_chat_member(update.message.chat.id, update.message.new_chat_members[0]["id"])
            context.bot.send_message(chat_id=chatId, text="Adding bots to the group is not allowed.")
            return
        # If welcome message is On.
        if self.menu_button[4][1].state:
            if self.old_welcome_message is not None and self.menu_button[6][1].state == True:
                context.bot.delete_message(self.old_welcome_message.chat["id"], self.old_welcome_message["message_id"])
            if self.welcome_message is not None:

                # Welcome message exists
                # If the substring '$name' is in welcome message replace it with the new users name.
                # If rules exists add them to the welcome message.
                # Send a welcome and/or rules message in the group.
                if "$name" in self.welcome_message:
                    print(update.message.new_chat_members[0]["first_name"])
                    self.welcome_message = self.welcome_message.replace('$name', update.message.new_chat_members[0]["first_name"])
                if self.menu_button[3][1].state:
                    button = botButton.botButton()
                    keyboard = button.init_button("Rules", "", "9").get_button()
                    print(keyboard)
                    self.welcome_message = "{0}".format(self.welcome_message)
                self.old_welcome_message = context.bot.send_message(chat_id=chatId, text=self.welcome_message,
                                                                    reply_markup=InlineKeyboardMarkup([[keyboard]]))
            if self.rule_message is not None and self.welcome_message is None:
                # If rules exists and welcome message does not exists Send The rules in the group.
                self.old_welcome_message = context.bot.send_message(chat_id=chatId, text=self.welcome_message)
            # If remove service messages flag set to on, all service messages wi be deleted.
        self.remove_service_message(update, context)

    def user_left_handler(self, update, context):
        if self.userLeftMessage is not None:
            if self.menu_button[7][1].state:
                context.bot.send_message(update.message.left_chat_member["id"], text=self.userLeftMessage)
        self.remove_service_message(update, context)


    def remove_service_message(self, update, context):
        """
        Delete service messages from the group
        :param update:
        :param context:
        :return:
        """
        if self.menu_button[1][1].state:
            context.bot.delete_message(update.message.chat["id"], update.message["message_id"])

    def rules_button_ahandler(self, update, context):
        """
        Sends the group Rules.
        :param update:
        :param context:
        :return:
        """
        context.bot.send_message(chat_id=update.effective_user["id"], text=self.rule_message)


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Handlers^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^





temp = peaceMakerBot("Your bot token here!")
