from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from emoji.core import emojize



# Buttons and their indexes
strToIndex = {"Rules": 0, "Delete service messages": 1, "Kick Bots": 2, "Welcome + Rules": 3, "Welcome message": 4,
              "Admin Report": 5, "Delete old Welcome": 6, "User left message":7}
buttonNames = ["Rules", "Delete service messages", "Kick Bots", "Welcome + Rules", "Welcome message", "Admin Report",
               "Delete old Welcome", "User left message"]

# Buttons states
menuButtonState = [True, True, True, True, True, True, True, True, True, True]
emojiButtonState = ['\U0001F7E2', '\U0001F7E2', '\U0001F7E2', '\U0001F7E2', '\U0001F7E2', '\U0001F7E2', '\U0001F7E2']


def button_info(data):
    text = ""
    if data == "exp":
        text = "'When someone uses the command: '/rules.'\n'" \
              " 'On: The bot will answer in a private message.\n'" \
               "Off: The bot will answer in the group."
        return text
    if data == "deleteServiceMsg":
        text = "On: deletes all service messages in the group."
    if data == "kickBots":
        text = "On: Kicks all bots joining the group."
    if data == "welcomeRules":
        text = "If welcome message is on, It will include the rules button that will send the user the rules in a private message."
    if data == "welcomeMessage":
        text = "If welcome message is on, Shows a welcome message for each new user."
    if data == "adminReports":
        text = "On: Users can report a message using the /admin command."

    if data == "delOldWelcome":
        text = "On: Each time a Welcome message is sent, previously Welcome messages will be deleted."
    if data == "userLeftMessage":
        text = "On: sends a message to the user who just left the group,\nIf Off:The message will not be sent.\n" \
               "Message need to be set with the /userLeft Command!"
    if data == "userLeftMessage":
        text = "On: If userLeft message is set, Sends the message to a user that just left the channel.\n" \
               "Off: Don't send a userLeft message."
    return text
