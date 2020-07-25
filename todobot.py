from telegram.ext import (Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters,
                          PicklePersistence, CallbackQueryHandler, ConversationHandler)
from telegram import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton,
                      InlineKeyboardMarkup, ForceReply)
import telegram.ext
import logging
import datetime
#import schedule
import time
from uuid import uuid4
from _datetime import timedelta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

#NEW 
import os
api_id = 1665385
api_hash = 'cdf2fc6fe9c4ee703e6d1940da92eeb6'
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '1190868363:AAHWra_a4JteryuJBFNhZyAk-lKlMxY3udo'


#################################### STATES ####################################

(FRONT_MENU,
 WORK_MENU,
 GROUP_WORK_MENU,
 GROUP_WORK_TO_DO_LIST_MENU,
 GROUP_WORK_VIEW_TO_DO_LIST_MENU,
 GROUP_WORK_VIEW_INDIVIDUAL_TASK_MENU,
 GROUP_WORK_TO_DO_ADD_TASK_MENU,
 GROUP_WORK_TO_DO_ADD_HEADER_WAITING_INPUT,
 GROUP_WORK_TO_DO_EDIT_INFO_MENU,
 GROUP_WORK_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT,
 GROUP_WORK_TO_DO_EDIT_DEADLINE_WAITING_INPUT,
 GROUP_WORK_TO_DO_EDIT_TASK_STATUS_MENU,
 GROUP_WORK_REMOVE_TASK_MENU,
 GROUP_WORK_REMINDERS_MENU,
 GROUP_WORK_SET_REMINDER_MENU,
 GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED,
 GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT,
 GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT,
 GROUP_WORK_REMINDER_ADD_EVENT_MENU,
 GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT,
 GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU,
 GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT,
 GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT,
 GROUP_WORK_EDIT_TASK,
 GROUP_WORK_REMOVE_REMINDER_MENU,
 MODULE_MENU,
 MODULE_VIEW_MODULES_MENU,
 MODULE_TO_DO_LIST_MENU,
 MODULE_TO_DO_VIEW_TO_DO_LIST_MENU,
 MODULE_TO_DO_VIEW_INDIVIDUAL_TASK_MENU,
 MODULE_TO_DO_ADD_TASK_MENU,
 MODULE_TO_DO_ADD_HEADER_WAITING_INPUT,
 MODULE_TO_DO_EDIT_INFO_MENU,
 MODULE_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT,
 MODULE_TO_DO_EDIT_DEADLINE_WAITING_INPUT,
 MODULE_TO_DO_EDIT_TASK_STATUS_MENU,
 MODULE_REMOVE_TASK_MENU,
 MODULE_ADD_MODULE_WAITING_INPUT,
 MODULE_REMOVE_MODULE_MENU,
 MODULE_REMINDERS_MENU,
 MODULE_SET_REMINDER_MENU,
 MODULE_SET_REMINDER_FOR_TO_DO_LIST_CHOOSE_MODULE,
 MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED,
 MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT,
 MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT,
 MODULE_REMINDER_ADD_EVENT_MENU,
 MODULE_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT,
 MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU,
 MODULE_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT,
 MODULE_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT,
 MODULE_EDIT_TASK,
 MODULE_REMOVE_REMINDER_MENU,
 CCA_MENU,
 CCA_ADD_SESSION_MENU,
 CCA_ADD_SESSION_TITLE_WAITING_INPUT,
 CCA_ADD_SESSION_DETAILS_WAITING_INPUT,
 CCA_ADD_SESSION_DATE_WAITING_INPUT,
 CCA_ADD_SESSION_TIME_WAITING_INPUT,
 CCA_ADD_SESSION_LOCATION_WAITING_INPUT,
 CCA_ADD_SESSION_DEADLINE_WAITING_INPUT,
 CCA_ADD_SESSION_DONE_MENU,
 CCA_USER_SET_REMINDER_WAITING_INPUT,
 CCA_USER_SET_REMINDER_DONE_MENU,
 CCA_VIEW_SESSIONS,
 CCA_REMOVE_SESSION_MENU,
 LEISURE_MENU,
 LEISURE_ADD_SESSION_MENU,
 LEISURE_ADD_SESSION_TITLE_WAITING_INPUT,
 LEISURE_ADD_SESSION_DETAILS_WAITING_INPUT,
 LEISURE_ADD_SESSION_DATE_WAITING_INPUT,
 LEISURE_ADD_SESSION_TIME_WAITING_INPUT,
 LEISURE_ADD_SESSION_LOCATION_WAITING_INPUT,
 LEISURE_ADD_SESSION_DEADLINE_WAITING_INPUT,
 LEISURE_ADD_SESSION_DONE_MENU,
 LEISURE_USER_SET_REMINDER_WAITING_INPUT,
 LEISURE_USER_SET_REMINDER_DONE_MENU,
 LEISURE_VIEW_SESSION,
 LEISURE_REMOVE_SESSION_MENU,
 HELP_MENU,
 HELP_GROUP_WORK_MENU,
 HELP_MODULE_MENU) = range(81)


###################################### BOT ######################################

# takes in a string and adds \ in front of characters that cannot be parsed otherwise
# parameter: string
# returns: string with escapes
def add_escape_to_string(str):
    return str.replace('_', '\_') \
              .replace('[', '\[') \
              .replace(']', '\]') \
              .replace('(', '\(') \
              .replace(')', '\)') \
              .replace('~', '\~') \
              .replace('>', '\>') \
              .replace('#', '\#') \
              .replace('+', '\+') \
              .replace('-', '\-') \
              .replace('=', '\=') \
              .replace('|', '\|') \
              .replace('{', '\{') \
              .replace('}', '\}') \
              .replace('.', '\.') \
              .replace('!', '\!')
              #.replace('*', '\*') \s

def remove_escape_from_string(str):
    return str.replace('\_', '_') \
              .replace('\*', '*') \
              .replace('\[', '[') \
              .replace('\]', ']') \
              .replace('\(', '(') \
              .replace('\)', ')') \
              .replace('\~', '~') \
              .replace('\>', '>') \
              .replace('\#', '#') \
              .replace('\+', '+') \
              .replace('\-', '-') \
              .replace('\=', '=') \
              .replace('\|', '|') \
              .replace('\{', '{') \
              .replace('\}', '}') \
              .replace('\.', '.') \
              .replace('\!', '!')

# print to-do list
# parameter: context
# returns: string with the specified format
def print_to_do_list(context):
    all_tasks_str = ""
    for header,info_dict in context.chat_data['to-do list'].items():
        task_details = ": \n" + info_dict['task details'] if info_dict['task details'] != "_\(empty\)_" else ""
        deadline = "\n\[Deadline: " + info_dict['deadline'] + "\]" if info_dict['deadline'] != "_\(empty\)_" else ""
        status = "\n\[Status: " + info_dict['status'] + "\]" if info_dict['status'] != "_\(empty\)_" else ""
        all_tasks_str = (all_tasks_str + "\n\n📍 " + "*" + header + "*" + task_details + deadline + status)
        #all_tasks_str = (all_tasks_str + "\n\n \-\- " + "*" + header + "*" + task_details + deadline + status)
    return all_tasks_str

def print_individual_task(context, header):
    task_str = ""
    info_dict = context.chat_data['to-do list'][header]

    task_details = ": \n" + info_dict['task details'] if info_dict['task details'] != "_\(empty\)_" else ""
    deadline = "\n\[Deadline: " + info_dict['deadline'] + "\]" if info_dict['deadline'] != "_\(empty\)_" else ""
    status = "\n\[Status: " + info_dict['status'] + "\]" if info_dict['status'] != "_\(empty\)_" else ""

    task_str = (task_str + "\n\n📍 " + "*" + header + "*" + task_details + deadline + status)
    return task_str

#print reminders
#parameter: context
# returns: string with the specified format
def print_reminders(context, category):
    all_reminders=""
    for header in context.chat_data['reminders'][category].keys():
        #if header == 'Reminder for To\-Do List':
        if ('Reminder for ' in header) & ('s To\-Do List' in header):
            date = "\n\[Interval: " + context.chat_data['reminders'][category][header]['interval'] + "\]"
            time = "\n\[Time: " + context.chat_data['reminders'][category][header]['time'] + "\]"
        else:
            # if date is empty, leave as empty else assign format for date
            date = "\n\[Date: " + context.chat_data['reminders'][category][header]['date'] + "\]" if context.chat_data['reminders'][category][header]['date'] != "_\(empty\)_" else ""
            time = "\n\[Time: " + context.chat_data['reminders'][category][header]['time'] + "\]" if context.chat_data['reminders'][category][header]['time'] !=  "_\(empty\)_" else ""
        all_reminders = all_reminders + "\n\n📍 " + "*" + header + "*" + ": " + date + time 
    return all_reminders

# print module's to-do list
# parameter: context
# returns: string with the specified format
def print_module_to_do_list(context, current_module):
    all_tasks_str = ""
    for header,info_dict in context.chat_data['modules'][current_module]['to-do list'].items():
        task_details = ": \n" + info_dict['task details'] if info_dict['task details'] != "_\(empty\)_" else ""
        deadline = "\n\[Deadline: " + info_dict['deadline'] + "\]" if info_dict['deadline'] != "_\(empty\)_" else ""
        status = "\n\[Status: " + info_dict['status'] + "\]" if info_dict['status'] != "_\(empty\)_" else ""
        all_tasks_str = (all_tasks_str + "\n\n📍 " + "*" + header + "*" + task_details + deadline + status)
    return all_tasks_str


def print_module_individual_task(context, current_module, header):
    task_str = ""
    info_dict = context.chat_data['modules'][current_module]['to-do list'][header]

    task_details = ": \n" + info_dict['task details'] if info_dict['task details'] != "_\(empty\)_" else ""
    deadline = "\n\[Deadline: " + info_dict['deadline'] + "\]" if info_dict['deadline'] != "_\(empty\)_" else ""
    status = "\n\[Status: " + info_dict['status'] + "\]" if info_dict['status'] != "_\(empty\)_" else ""

    task_str = (task_str + "\n\n📍 " + "*" + header + "*" + task_details + deadline + status)
    return task_str




################################### CALLBACKS ###################################

# start callback (CommandHandler)
def start(update, context):
    if len(context.chat_data) == 0:
        context.chat_data['current task'] = {}
        context.chat_data['current reminder'] = {}
        context.chat_data['current module'] = ""
        context.chat_data['current cca'] = {}
        context.chat_data['current leisure'] = {}
        context.chat_data['to-do list'] = {}
        context.chat_data['reminders'] = {}
        context.chat_data['reminders']['work'] = {}
        context.chat_data['reminders']['module'] = {}
        context.chat_data['reminders']['cca'] = {}
        context.chat_data['reminders']['leisure'] = {}
        context.chat_data['modules'] = {}
        context.chat_data['cca'] = {}
        context.chat_data['leisure'] = {}

    chat_type = update.message.chat.type

    if chat_type == 'private':
        context.chat_data['chat_type'] = 'private'
    else:
        context.chat_data['chat_type'] = 'group'
    
    update.message.reply_text(text="Eh hello\! I'm the doYourWorkLah bot\!\n\n" +
                                   "If you a bit blur blur hor 🦑,\nsend /help to see what I can do\.\n"
                                   "If you want me to shut up 🤐,\nsend /cancel to stop talking to me\.\n\n" +
                                   "*You better start doing your work ah\! Hurry choose one 😵:*",
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=front_keyboard(context))
    return FRONT_MENU
        
# front callback (CallbackQueryHandler)
def front(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Eh hello\! I'm the doYourWorkLah bot\!\n\n" +
                                        "If you a bit blur blur hor 🦑,\nsend /help to see what I can do\.\n"
                                        "If you want me to shut up 🤐,\nsend /cancel to stop talking to me\.\n\n" +
                                        "*You better start doing your work ah\! Hurry choose one 😵:*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=front_keyboard(context))
    return FRONT_MENU


# work callback (CallbackQueryHandler)
def work(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose choose: 🥱*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=work_keyboard(context))
    return WORK_MENU


# ---------------------------------WORK > GROUP WORK--------------------------------- #
# group_work callback (CallbackQueryHandler)
def group_work(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Just choose lah: 🥱*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_keyboard())
    return GROUP_WORK_MENU

# ----------------------------WORK > GROUP WORK (TO-DO LIST)---------------------------- #
# group_work_to_do_list callback (CallbackQueryHandler)
def group_work_to_do_list(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick choose one: 😴*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_to_do_list_keyboard())
    return GROUP_WORK_TO_DO_LIST_MENU


def view_to_do_list(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Aiyo just choose something: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_view_to_do_list_keyboard())
    return GROUP_WORK_VIEW_TO_DO_LIST_MENU


# view_entire_to_do_list callback (CallbackQueryHandler)
def view_entire_to_do_list(update, context):
    query = update.callback_query

    if len(context.chat_data['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*📋 __To\-Do List__ 📋*" + print_to_do_list(context),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END


def view_individual_task(update, context):
    query = update.callback_query

    if len(context.chat_data['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Which task do you want to see? 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_view_individual_task_keyboard(context))
        return GROUP_WORK_VIEW_INDIVIDUAL_TASK_MENU


def group_work_view_individual_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    header_without_esc = callback_data.partition('user_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*📝 __Task__ 📝*" + print_individual_task(context, header_with_esc),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    return ConversationHandler.END


# group_work_add_task callback (CallbackQueryHandler)
def group_work_add_task(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Aiyo just choose something: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_add_task_keyboard())
    return GROUP_WORK_TO_DO_ADD_TASK_MENU

# group_work_to_do_add_header callback (CallbackQueryHandler)
def group_work_to_do_add_header(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id,
    #                         text="entered group_work_to_do_add_header block")
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Create a header for your task\!* 👇 \(You cannot use back the same header and it cannot be more than 45 characters ok\!\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Create a header for your task\!* 👇 \(You cannot use back the same header and it cannot be more than 45 characters ok\!\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return GROUP_WORK_TO_DO_ADD_HEADER_WAITING_INPUT

#NEW
# group_work_to_do_add_header_waiting_input callback (MessageHandler)
def group_work_to_do_add_header_waiting_input(update, context):
    # clear context.chat_data['current task'] dictionary
    context.chat_data['current task'].clear()
    header_without_esc = update.message.text
    header_with_esc = add_escape_to_string(header_without_esc)
    # limit header_without_esc to 45 characters
    if len(header_without_esc) <= 45:
        if header_with_esc not in context.chat_data['to-do list']:
            context.chat_data['current task'][header_with_esc] = {'task details':"_\(empty\)_", 'deadline':"_\(empty\)_", 'status':"_\(empty\)_"}
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" +
                                           "📍*Header:* " + header_with_esc + "\n" +
                                           "📜*Task Details:* " + context.chat_data['current task'][header_with_esc]['task details'] + "\n" +
                                           "⏳*Deadline:* " + context.chat_data['current task'][header_with_esc]['deadline'] + "\n" +
                                           "🔘*Status:* " + context.chat_data['current task'][header_with_esc]['status']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=group_work_to_do_edit_info_keyboard())
            return GROUP_WORK_TO_DO_EDIT_INFO_MENU
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Aiyo this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
            group_work_to_do_add_header(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(header_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_to_do_add_header(update, context)

# group_work_to_do_edit_task_details callback (CallbackQueryHandler)
def group_work_to_do_edit_task_details(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick tell me all the details: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    return GROUP_WORK_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT

# group_work_to_do_edit_task_details_waiting_input callback (MessageHandler)
def group_work_to_do_edit_task_details_waiting_input(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id,
    #                         text="entered group_work_to_do_edit_task_details_waiting_input block")
    task_details = update.message.text
    task_details_with_esc = add_escape_to_string(task_details)
    current_header = list(context.chat_data['current task'].keys())[0]
    context.chat_data['current task'][current_header]['task details'] = task_details_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=("*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status']),
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=group_work_to_do_edit_info_keyboard())
    return GROUP_WORK_TO_DO_EDIT_INFO_MENU

# group_work_to_do_edit_deadline callback (CallbackQueryHandler)
def group_work_to_do_edit_deadline(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Faster edit your deadline\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Faster edit your deadline\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return GROUP_WORK_TO_DO_EDIT_DEADLINE_WAITING_INPUT

#NEW
# group_work_to_do_edit_deadline_waiting_input callback (MessageHandler)
def group_work_to_do_edit_deadline_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
    
    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_without_esc = deadline_date_checked + " " + deadline_time_checked
        datetime_object_local = datetime.datetime.strptime(deadline_checked_without_esc, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
        current_datetime_local = datetime.datetime.now()

        if datetime_object_uct < current_datetime_local:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                      text="*Wah jialat your deadline is already over\!* 🤧",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
            group_work_to_do_edit_deadline(update, context)
        else: 
            deadline_checked_with_esc = add_escape_to_string(deadline_checked_without_esc)
            current_header = list(context.chat_data['current task'].keys())[0]
            context.chat_data['current task'][current_header]['deadline'] = deadline_checked_with_esc
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=group_work_to_do_edit_info_keyboard())
            return GROUP_WORK_TO_DO_EDIT_INFO_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your deadline is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_to_do_edit_deadline(update, context)


#NEW
def group_work_to_do_edit_task_status(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose a task status\!:* 😩",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_to_do_edit_task_status_keyboard())
    return GROUP_WORK_TO_DO_EDIT_TASK_STATUS_MENU


#NEW
def group_work_to_do_edit_task_status_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = list(context.chat_data['current task'].keys())[0]
    if callback_data == "haven't do!":
        context.chat_data['current task'][current_header]['status'] = "Paiseh paiseh haven't do yet 😅"
    elif callback_data == "doing!":
        context.chat_data['current task'][current_header]['status'] = "Doing already 💪"
    else:
        context.chat_data['current task'][current_header]['status'] = "Finish liao 😎"
    
    context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                  message_id=query.message.message_id,
                                  text=("*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status']),
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                    reply_markup=group_work_to_do_edit_info_keyboard())
    return GROUP_WORK_TO_DO_EDIT_INFO_MENU



#NEW
# group_work_to_do_done callback (CallbackQueryHandler)
def group_work_to_do_done(update, context):
    query = update.callback_query
    current_datetime = datetime.datetime.now()
    current_header = list(context.chat_data['current task'].keys())[0]

    #if context.chat_data['current task'][current_header]['deadline'] != "_\(empty\)_":
    #    deadline = remove_escape_from_string(context.chat_data['current task'][current_header]['deadline'])
    #    datetime_object_uct = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    #    datetime_object_local = datetime_object_uct - datetime.timedelta(hours = 8)
    
    #    if datetime_object_local < current_datetime:
    #        to_edit = False
    #        context.bot.edit_message_text(chat_id=query.message.chat_id,
    #                                  message_id=query.message.message_id,
    #                                  text="*Aiyo your date and time is already over\!*🙀",
    #                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
    #                                  reply_markup=group_work_to_do_edit_info_keyboard())
    #        return GROUP_WORK_TO_DO_EDIT_INFO_MENU
            
    
    # save stuff in 'current task' to 'to-do list'

    context.chat_data['to-do list'][current_header] = context.chat_data['current task'][current_header]
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*📋 __To\-Do List__ 📋*" + print_to_do_list(context),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return ConversationHandler.END

#group_work_edit_task callback (CallbackQueryHandler)
def group_work_edit_task(update,context):
    query = update.callback_query
    if len(context.chat_data['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Which one you want to edit?:* 😔",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_edit_task_keyboard(context))
        return GROUP_WORK_EDIT_TASK

#NEW
#group_work_edit_task_user_choice callback (CallbackQueryHandler)
def group_work_edit_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('groupwork_edit_task_')[2]
    context.chat_data['current task'].clear()
    context.chat_data['current task'][current_header] = context.chat_data['to-do list'][current_header]
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=("📍*Header:* " + current_header + "\n" +
                                       "📜*Task Details:* " + context.chat_data['to-do list'][current_header]['task details'] + "\n" +
                                       "⏳*Deadline:* " + context.chat_data['to-do list'][current_header]['deadline'] + "\n" +
                                       "🔘*Status:* " + context.chat_data['current task'][current_header]['status']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_to_do_edit_info_keyboard())
    return GROUP_WORK_TO_DO_EDIT_INFO_MENU


# group_work_remove_task callback (CallbackQueryHandler)
def group_work_remove_task(update, context):
    query = update.callback_query
    if len(context.chat_data['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*📋 __To\-Do List__ 📋*" + print_to_do_list(context),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="*Which one you want to remove?:* 🪓",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=group_work_remove_task_keyboard(context))
        return GROUP_WORK_REMOVE_TASK_MENU

# group_work_remove_task_user_choice callback (CallbackQueryHandler)
def group_work_remove_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    header_without_esc = callback_data.partition('user_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    context.chat_data['to-do list'].pop(header_with_esc, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + header_with_esc + "* from the to\-do list liao\. 🥴",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    if len(context.chat_data['to-do list']) == 0:
        context.bot.send_message(chat_id=query.message.chat_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=query.message.chat_id,
                                  text="*📋 __To\-Do List__ 📋*" + print_to_do_list(context),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
        return ConversationHandler.END

# ----------------------------WORK > GROUP WORK (REMINDERS)---------------------------- #
#group_work_reminders callback (CallbackQueryHandler)
def group_work_reminders(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Choose faster can: 💅",
                                  reply_markup=group_work_reminders_keyboard())
    return GROUP_WORK_REMINDERS_MENU

#group_work_view_reminders callback (CallbackQueryHandler)
def group_work_view_reminders(update, context):
    query = update.callback_query

    if len(context.chat_data['reminders']['work']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh you don't have work reminders what\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔 __Reminders__ 🔔*" + print_reminders(context, "work"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END

#group_work_set_reminder callback
def group_work_set_reminder(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="You don't know what 'choose faster' means is it: 💀",
                                  reply_markup=group_work_set_reminder_keyboard())

    return GROUP_WORK_SET_REMINDER_MENU

#group_work_set_reminder_for_to_do_list callback
def group_work_set_reminder_for_to_do_list(update, context):
    query = update.callback_query

    if len(context.chat_data['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END

    else:
        context.chat_data['current reminder for tdl'] = {'time':"_\(empty\)_", 'interval':"_\(empty\)_"}
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Still got some more information to fill in below:* 😈 \(Eh this one cannot leave blank ah\)\n\n" + 
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED #this is the edit menu

def group_work_set_reminder_for_to_do_list_edit_time(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*What time do want me to remind you?* 🥳 \n\(Must be this format ok, don't try to be funny: HH:MM\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*What time do want me to remind you?* 🥳 \n\(Must be this format ok, don't try to be funny: HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT

def group_work_set_reminder_for_to_do_list_edit_time_waiting_input(update, context):
    time = update.message.text
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_checked_with_esc = add_escape_to_string(time_checked)
        context.chat_data['current reminder for tdl']['time'] = time_checked_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Still got some more information to fill in below:* 😈 \(Eh this one cannot leave blank ah\)\n\n" + 
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*You trying to be funny is it, your time is not in the correct format leh\!* 😤",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_to_do_list_edit_time(update, context)

def group_work_set_reminder_for_to_do_list_edit_interval(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Hurry choose the interval between each reminder \(in days\)\.* ⌛️" + "\n"
                                           "\(e\.g\. if you want me to kachiao you with your to\-do list every 2 days, then reply with the number 2\.\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Hurry choose the interval between each reminder \(in days\)\.* ⌛️" + "\n"
                                        "\(e\.g\. if you want me to kachiao you with your to\-do list every 2 days, then reply with the number 2\.\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT

def group_work_set_reminder_for_to_do_list_edit_interval_waiting_input(update, context):
    interval = update.message.text
    try:
        num_of_day = int(interval)
        if num_of_day >= 1:
            if interval == '1':
                context.chat_data['current reminder for tdl']['interval'] = "Every day"
            else:
                context.chat_data['current reminder for tdl']['interval'] = "Every {} days".format(interval)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Still got some more information to fill in below:* 😈 \(Eh this one cannot leave blank ah\)\n\n" + 
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
            return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
        else:
            context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="*Wah your maths need tuition ah, enter an integer greater than or equal to 1 leh\!* 🧑‍🏫",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
            group_work_set_reminder_for_to_do_list_edit_interval(update, context)

    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="*Aiyo enter an integer\!* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_to_do_list_edit_interval(update, context)
  
#callback function for group work > set reminder for to-do list to be sent every X days
def callback_day(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    all_tasks_str = ""
    for header,info_dict in chat_data['to-do list'].items():
        # if date is empty, leave as empty else assign format for date
        if (info_dict['task details'] == "_\(empty\)_") and (info_dict['deadline'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\n📍 " + "*" + header + "*"
        elif (info_dict['task details'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\n📍 " + "*" + header + "*" + "\n\[⏳Deadline: " + info_dict['deadline'] + "\]"
        elif (info_dict['deadline'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\n📍 " + "*" + header + "*" + ": \n" + info_dict['task details']
        else:
            all_tasks_str = all_tasks_str + "\n\n📍 " + "*" + header + "*" + ": \n" + info_dict['task details'] + "\n\[⏳Deadline: " + info_dict['deadline'] + "\]"

    context.bot.send_message(chat_id=chat_id,
                                      text="*📋 __To\-Do List__ 📋*" + all_tasks_str,
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)

def group_work_set_reminder_for_to_do_list_done(update, context):
    query = update.callback_query
    if (context.chat_data['current reminder for tdl']['time'] == "_\(empty\)_") and (context.chat_data['current reminder for tdl']['interval'] == "_\(empty\)_"):
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time and the interval\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    elif context.chat_data['current reminder for tdl']['time'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    elif context.chat_data['current reminder for tdl']['interval'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the interval\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_to_do_list_edit_info_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    else:
        if 'Reminder for To\-Do List' in context.chat_data['reminders']['work']:
            old_job = context.chat_data['reminders']['Reminder for To\-Do List']['job']
            old_job.schedule_removal()
        else:
            context.chat_data['reminders']['work']['Reminder for To\-Do List'] ={}

        context.chat_data['reminders']['work']['Reminder for To\-Do List']['time'] = context.chat_data['current reminder for tdl']['time']
        context.chat_data['reminders']['work']['Reminder for To\-Do List']['date'] = context.chat_data['current reminder for tdl']['interval']
        time_with_esc = context.chat_data['reminders']['work']['Reminder for To\-Do List']['time']
        time = remove_escape_from_string(time_with_esc)
        context.chat_data['reminders']['work']['Reminder for To\-Do List']['interval'] = context.chat_data['current reminder for tdl']['interval']
        interval = context.chat_data['reminders']['work']['Reminder for To\-Do List']['interval']

        num_of_day = 0
        if interval == "Every day":
            num_of_day = 1
        else:
            num_of_day = int(interval[6])

        datetime_object_local = datetime.datetime.strptime(time, '%H:%M')
        datetime_object_uct = datetime_object_local - timedelta(hours = 8)
        time_object_uct = datetime_object_uct.time()

        # need to change from minutes to days
        new_job = context.job_queue.run_repeating(callback_day, timedelta(days=int(num_of_day)), first=time_object_uct, context={'chat_data': context.chat_data, 'chat_id': str(query.message.chat_id)})
        context.chat_data['reminders']['work']['Reminder for To\-Do List']['job'] = new_job

        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                 text="Ok nice nice 💃 A new reminder for your to\-do list has been created\! 😉 I will remind you at *{} {}*\.".format(time, interval.lower()),
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    
#callback group_work_set_reminder_for_event
def group_work_set_reminder_for_event(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Lailai choose choose: 🤪",
                                      reply_markup=group_work_add_event_keyboard())
    return GROUP_WORK_REMINDER_ADD_EVENT_MENU

#group_work_set_reminder_for_event_add_header callback (CallbackQueryHandler)  
def group_work_set_reminder_for_event_add_header(update, context):
    query = update.callback_query
    
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh create a header for your event\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Eh create a header for your event\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT

# group_work_set_reminder_for_event_add_header_waiting_input (MessageHandler)
#state called by group work set reminder for event
def group_work_set_reminder_for_event_add_header_waiting_input(update, context):
    #checks if current reminder dictionary is empty
    # limit header_without_esc to 45 characters
    header_without_esc = update.message.text
    header_with_esc = add_escape_to_string(header_without_esc)
    if len(header_without_esc) > 45:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(header_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_event_add_header(update, context)
    elif header_with_esc in context.chat_data['reminders']['work']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Aiyo this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_event_add_header(update, context)
    else:
        context.chat_data['current reminder'][header_with_esc] = {'date':"_\(empty\)_", 'time':"_\(empty\)_"}
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                           "📍*Header:* " + header_with_esc + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][header_with_esc]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][header_with_esc]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=group_work_set_reminder_for_event_details_keyboard())
    
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU


#callback group_work_set_reminder_for_event_date
def group_work_set_reminder_for_event_date(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                 text="*Eh choose your event date\!* 🤓 \n\(Must be this format ok, don't try to be funny: DD/MM/YYYY\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    return GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT       

def group_work_set_reminder_for_event_add_date_waiting_input(update, context):
    date = update.message.text
    try:
        # check formatting
        date_checked = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        date_with_esc = add_escape_to_string(date_checked)
        current_header = list(context.chat_data['current reminder'].keys())[0]
        context.chat_data['current reminder'][current_header]['date'] = date_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                           "📍*Header:* " + current_header + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][current_header]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][current_header]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=group_work_set_reminder_for_event_details_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Aiyo your date is not in the correct format leh\!* 😒",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_event_date(update, context)

# group_work_set_reminder_for_event_time callback (CallbackQuery Handler)
def group_work_set_reminder_for_event_time(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                 text="*Faster edit your event time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    return GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT

#group_work_set_reminder_for_event_add_time_waiting_input callback (MessageHandler)
def group_work_set_reminder_for_event_add_time_waiting_input(update, context):
    time = update.message.text
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_with_esc = add_escape_to_string(time_checked)
        current_header = list(context.chat_data['current reminder'].keys())[0]
        context.chat_data['current reminder'][current_header]['time'] = time_with_esc
        
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Eh fill in the rest of the information below:*🙄 \(You CANNOT leave the following fields blank\)\n\n" +
                                           "📍*Header:* " + current_header + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][current_header]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][current_header]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=group_work_set_reminder_for_event_details_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*You never read properly is it, your time is not in the correct format\!* 😲",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        group_work_set_reminder_for_event_time(update, context)

def reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_header = context.job.context['header']
    date_with_esc = chat_data['reminders']['work'][current_header]['date']
    time_with_esc = chat_data['reminders']['work'][current_header]['time']
    job_queue = context.job.context['job_queue']
    
    #Job to check if user has clicked snooze / dismiss for the reminder. If user has not clicked any button, default response is dismiss.
    new_job = job_queue.run_once(check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': chat_data, 'job_queue': job_queue, 'header': current_header, 'chat_id': chat_id})
    chat_data['reminders']['work'][current_header]['job'] = new_job
    chat_data['reminders']['work'][current_header]['status'] = "dismiss"

    context.bot.send_message(chat_id= chat_id, 
                             text= ("You have a reminder\! 🥳 \n\n" +
                                    "📍*Event:* " + current_header + "\n" +
                                    "📆*Date:* " + date_with_esc + "\n" +
                                    "⏰*Time:* " + time_with_esc + "\n\n" +
                                    "Please choose either SNOOZE💤 to snooze the reminder for 10 minutes or DISMISS❌ to remove the reminder\!" +"\n" +
                                    "*If you don't choose anything within 10 minutes, then I will just remove your reminder automatically ⏰🔨\.*"),
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=group_work_snooze_reminder_keyboard(current_header))
    #chat_data['reminders'].pop(current_header, None)

#Callback to check if user has clicked snooze/ dismiss or did not click anything for the reminder.
#Snooze feature for one-off event reminders. If user has clicked snooze, reminder is snoozed for 10 minutes and a new reminder for the event will be sent after the 10 minutes from when the reminder is snoozed.
#If user did not click on snooze within 10 minutes, the reminder will have been automatically removed.
#Dimiss feature for one-off event reminders. If user has clicked dismiss, reminder is removed.
def check_reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_header = context.job.context['header']
    job_queue = context.job.context['job_queue']
    now_uct = datetime.datetime.now() 
    if chat_data['reminders']['work'][current_header]['status'] == 'snooze':
        new_job = job_queue.run_once(reminder_callback, now_uct, context={'chat_data': chat_data, 'job_queue': job_queue ,'header': current_header, 'chat_id': chat_id})
        chat_data['reminders']['work'][current_header]['job'] = new_job
    else:
        chat_data['reminders']['work'].pop(current_header, None)
        
 #Callback when users click on the snooze button for reminder.       
def group_work_snooze_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('group_work_snooze_reminder_')[2]
    #If user clicks the snooze keyboard after 10 minutes is up.
    if current_header not in context.chat_data['reminders']['work']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been removed already leh\. 🤷‍♀️",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    else:
        context.chat_data['reminders']['work'][current_header]['status'] = 'snooze'
        old_job = context.chat_data['reminders']['work'][current_header]['job']
        old_job.schedule_removal()
        new_job = context.job_queue.run_once(check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': context.chat_data, 'job_queue': context.job_queue, 'header': current_header, 'chat_id': str(query.message.chat_id)})
        context.chat_data['reminders']['work'][current_header]['job'] = new_job
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been snoozed for 10 minutes\. ⏰💤",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

#Callback when user clicks on dismiss button for reminder.
def group_work_dismiss_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('group_work_dismiss_reminder_')[2]
    old_job = context.chat_data['reminders']['work'][current_header]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['work'].pop(current_header, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been removed\. ⏰🔨😈",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

# group_work_set_reminder_for_event_done callback (CallbackQueryHandler)
def group_work_set_reminder_for_event_done(update, context):
    query = update.callback_query
    current_header = list(context.chat_data['current reminder'].keys())[0]
    current_datetime = datetime.datetime.now()
    

    if (context.chat_data['current reminder'][current_header]['date'] == "_\(empty\)_") and (context.chat_data['current reminder'][current_header]['time'] == "_\(empty\)_"):
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the date and the time\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_event_details_keyboard())
    
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    elif context.chat_data['current reminder'][current_header]['date'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the date\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_event_details_keyboard())
    
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    elif context.chat_data['current reminder'][current_header]['time'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the time\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_event_details_keyboard())
        return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    # check if the given date and time is over
    else:
        #NEW
        date_with_esc = context.chat_data['current reminder'][current_header]['date']
        date_without_esc = remove_escape_from_string(date_with_esc)
        time_with_esc = context.chat_data['current reminder'][current_header]['time']
        time_without_esc = remove_escape_from_string(time_with_esc)
        date_and_time = date_without_esc + " " + time_without_esc
        datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
    
        if datetime_object_uct < current_datetime:
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your date and time is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=group_work_set_reminder_for_event_details_keyboard())
            return GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    # save stuff in 'current reminder' to 'reminders'
        else:
            
            context.chat_data['reminders']['work'][current_header] = context.chat_data['current reminder'][current_header]
            new_job = context.job_queue.run_once(reminder_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'job_queue': context.job_queue, 'header': current_header, 'chat_id': str(query.message.chat_id)})
            context.chat_data['reminders']['work'][current_header]['job'] = new_job
            reminder_status = "dismiss"
            context.chat_data['reminders']['work'][current_header]['status'] = reminder_status
            context.chat_data['current reminder'].clear()
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔 __Reminders__ 🔔*" + print_reminders(context, "work"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
            return ConversationHandler.END

# group_work_remove_reminder callback (CallbackQueryHandler)
def group_work_remove_reminder(update, context):
    query = update.callback_query
    if len(context.chat_data['reminders']['work']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh you have no work reminders leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔 __Reminders__ 🔔*" + print_reminders(context, "work"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="*Faster choose the reminder you want to remove:* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=group_work_remove_reminder_keyboard(context))
    return GROUP_WORK_REMOVE_REMINDER_MENU

# group_work_remove_task_user_choice callback (CallbackQueryHandler)
# need to change the text so that if the to-do list is empty after removing a task, they will say: your to-do list is empty!
def group_work_remove_reminder_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    header_without_esc = callback_data.partition('work_reminder_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    old_job = context.chat_data['reminders']['work'][header_with_esc]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['work'].pop(header_with_esc)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + header_with_esc + "* from reminders liao\. 🥱",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    if len(context.chat_data['reminders']['work']) == 0:
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="*Eh you have no work reminders\!* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    else:
        context.bot.send_message(chat_id=query.message.chat_id,
                              text="*🔔 __Reminders__ 🔔*" + print_reminders(context, "work"),
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=None)
    return ConversationHandler.END


# -------------------------WORK > MODULE (SHOW ALL MODULES -> TO-DO LIST)------------------------- #
def module(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text="*Faster choose choose: 🥱*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_keyboard())
    return MODULE_MENU

def module_view_modules(update, context):
    query = update.callback_query
    if len(context.chat_data['modules']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh you got no modules lah\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo which module do you want to see ah 😪*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_view_modules_keyboard(context))
    return MODULE_VIEW_MODULES_MENU

def module_view_modules_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    module_without_esc = callback_data.partition('viewmod_')[2]
    module_with_esc = add_escape_to_string(module_without_esc)

    context.chat_data['current module'] = module_with_esc
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick choose one: 😴*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_to_do_list_keyboard())
    return MODULE_TO_DO_LIST_MENU

def module_to_do_view_to_do_list(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick choose one: 😴*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_to_do_view_to_do_list_keyboard(context))
    return MODULE_TO_DO_VIEW_TO_DO_LIST_MENU


def module_to_do_view_entire_to_do_list(update, context):
    query = update.callback_query
    module_name = context.chat_data['current module']

    if len(context.chat_data['modules'][module_name]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list for {} is empty leh\! 🤦‍♀️*".format(module_name),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*📋__To\-Do List for {}:__📋*".format(module_name) + print_module_to_do_list(context, module_name),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END


def module_to_do_view_individual_task(update, context):
    query = update.callback_query
    module_name = context.chat_data['current module']

    if len(context.chat_data['modules'][module_name]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 😪*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                       text="*Which task do you want to see\? 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_to_do_view_individual_task_keyboard(context))
        return MODULE_TO_DO_VIEW_INDIVIDUAL_TASK_MENU


def module_to_do_view_individual_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    module_name = context.chat_data['current module']
    header_without_esc = callback_data.partition('user_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*📝__{}'s Task:__📝*".format(module_name) + print_module_individual_task(context, module_name, header_with_esc),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    return ConversationHandler.END



def module_to_do_add_task(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text="*Aiyo just choose something: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_add_task_keyboard(context))
    return MODULE_TO_DO_ADD_TASK_MENU

def module_to_do_add_header(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Create a header for your task\!* 👇 \(Note that no repeats are allowed and there is a 45 character limit\.\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Create a header for your task\!* 👇 \(Note that no repeats are allowed and there is a 45 character limit\.\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return MODULE_TO_DO_ADD_HEADER_WAITING_INPUT

#NEW
def module_to_do_add_header_waiting_input(update, context):
    # clear context.chat_data['current task'] dictionary
    context.chat_data['current task'].clear()
    header_without_esc = update.message.text
    header_with_esc = add_escape_to_string(header_without_esc)
    current_module = context.chat_data['current module']
    # limit header_without_esc to 45 characters
    if len(header_without_esc) <= 45:
        if header_with_esc not in context.chat_data['modules'][current_module]['to-do list']:
            context.chat_data['current task'][header_with_esc] = {'task details':"_\(empty\)_", 'deadline':"_\(empty\)_", 'status':"_\(empty\)_"}
            context.bot.send_message(chat_id=update.effective_chat.id,
                                      text=("*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" +
                                           "📍*Header:* " + header_with_esc + "\n" +
                                           "📜*Task Details:* " + context.chat_data['current task'][header_with_esc]['task details'] + "\n" +
                                           "⏳*Deadline:* " + context.chat_data['current task'][header_with_esc]['deadline'] + "\n" +
                                           "🔘*Status:* " + context.chat_data['current task'][header_with_esc]['status']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_to_do_edit_info_keyboard(context))
            return MODULE_TO_DO_EDIT_INFO_MENU
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Aiyo this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
            module_to_do_add_header(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(header_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_to_do_add_header(update, context)

def module_to_do_edit_task_details(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text="*Quick quick tell me all the details: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    return MODULE_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT

def module_to_do_edit_task_details_waiting_input(update, context):
    task_details = update.message.text
    task_details_with_esc = add_escape_to_string(task_details)
    current_header = list(context.chat_data['current task'].keys())[0]
    context.chat_data['current task'][current_header]['task details'] = task_details_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status'],
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=module_to_do_edit_info_keyboard(context))
    return MODULE_TO_DO_EDIT_INFO_MENU

def module_to_do_edit_deadline(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Faster edit your deadline\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Faster edit your deadline\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return MODULE_TO_DO_EDIT_DEADLINE_WAITING_INPUT

def module_to_do_edit_deadline_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_without_esc = deadline_date_checked + " " + deadline_time_checked
        datetime_object_local = datetime.datetime.strptime(deadline_checked_without_esc, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
        current_datetime_local = datetime.datetime.now()

        if datetime_object_uct < current_datetime_local:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                      text="*Aiyo your date and time is already over\!*🙀",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
            group_work_to_do_edit_deadline(update, context)
        else: 
            deadline_checked_with_esc = add_escape_to_string(deadline_checked_without_esc)
            current_header = list(context.chat_data['current task'].keys())[0]
            context.chat_data['current task'][current_header]['deadline'] = deadline_checked_with_esc
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status'],
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_to_do_edit_info_keyboard(context))
            return MODULE_TO_DO_EDIT_INFO_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your deadline is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_to_do_edit_deadline(update, context)

#NEW
def module_to_do_edit_task_status(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose a task status\!*😩",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_to_do_edit_task_status_keyboard())
    return MODULE_TO_DO_EDIT_TASK_STATUS_MENU


#NEW
def module_to_do_edit_task_status_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = list(context.chat_data['current task'].keys())[0]
    if callback_data == "haven't do!":
        context.chat_data['current task'][current_header]['status'] = "Paiseh paiseh haven't do yet 😅"
    elif callback_data == "doing!":
        context.chat_data['current task'][current_header]['status'] = "Doing already 💪"
    else:
        context.chat_data['current task'][current_header]['status'] = "Finish liao 😎"
    
    context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                  message_id=query.message.message_id,
                                   text="*Still got some more information to fill in below:* 🤡 \(Actually you don't want to fill in also can\)\n\n" + 
                                   "📍*Header:* " + current_header + "\n" +
                                   "📜*Task Details:* " + context.chat_data['current task'][current_header]['task details'] + "\n" +
                                   "⏳*Deadline:* " + context.chat_data['current task'][current_header]['deadline'] + "\n" +
                                   "🔘*Status:* " + context.chat_data['current task'][current_header]['status'],
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                    reply_markup=module_to_do_edit_info_keyboard(context))
    return MODULE_TO_DO_EDIT_INFO_MENU


def module_to_do_done(update, context):
    query = update.callback_query
    current_datetime = datetime.datetime.now()
    current_header = list(context.chat_data['current task'].keys())[0]
    to_edit = True 

    #if context.chat_data['current task'][current_header]['deadline'] != "_\(empty\)_":
    #    deadline = remove_escape_from_string(context.chat_data['current task'][current_header]['deadline'])
    #    datetime_object_uct = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    #    datetime_object_local = datetime_object_uct - datetime.timedelta(hours = 8)
    
    #    if datetime_object_local < current_datetime:
    #        to_edit = False
    #        context.bot.edit_message_text(chat_id=query.message.chat_id,
    #                                  message_id=query.message.message_id,
    #                                  text="*Your date and time is already over\!*",
    #                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
    #                                  reply_markup=module_to_do_edit_info_keyboard(context))
            
    #        return MODULE_TO_DO_EDIT_INFO_MENU
            
    if to_edit:
    # save stuff in 'current task' to 'to-do list'
        current_module = context.chat_data['current module']
        context.chat_data['modules'][current_module]['to-do list'][current_header] = context.chat_data['current task'][current_header]
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*📋__To\-Do List for {}:__📋*".format(current_module) + print_module_to_do_list(context, current_module),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END

def module_edit_task(update,context):
    query = update.callback_query
    current_module = context.chat_data['current module']
    if len(context.chat_data['modules'][current_module]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                     text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Hurry say which one you want to edit:* 😔",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_edit_task_keyboard(context))
        return MODULE_EDIT_TASK

#module_edit_task_user_choice callback (CallbackQueryHandler)
def module_edit_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('module_edit_task_')[2]
    current_module = context.chat_data['current module']
    context.chat_data['current task'].clear()
    context.chat_data['current task'][current_header] = context.chat_data['modules'][current_module]['to-do list'][current_header]
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "📍*Header:* " + current_header + "\n" +
                                       "📜*Task Details:* " + context.chat_data['modules'][current_module]['to-do list'][current_header]['task details'] + "\n" +
                                       "⏳*Deadline:* " + context.chat_data['modules'][current_module]['to-do list'][current_header]['deadline'] + "\n" +
                                        "🔘*Status:* " + context.chat_data['current task'][current_header]['status'],
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_to_do_edit_info_keyboard(context))
    return MODULE_TO_DO_EDIT_INFO_MENU

def module_to_do_remove_task(update, context):
    query = update.callback_query
    current_module = context.chat_data['current module']
    
    if len(context.chat_data['modules'][current_module]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*📋__To\-Do List for {}:__📋*".format(current_module) + print_module_to_do_list(context, current_module),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="*Which one you want to remove?:* 🪓",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=module_remove_task_keyboard(context))
        return MODULE_REMOVE_TASK_MENU

def module_to_do_remove_task_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    header_without_esc = callback_data.partition('removetask_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    current_module = context.chat_data['current module']
    context.chat_data['modules'][current_module]['to-do list'].pop(header_with_esc, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + header_with_esc + "* from {}'s to\-do list liao\. 🥴".format(current_module),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    if len(context.chat_data['modules'][current_module]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Wah your to\-do list is empty leh\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=query.message.chat_id,
                                  text="*📋__To\-Do List for {}:__📋*".format(current_module) + print_module_to_do_list(context, current_module),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
        return ConversationHandler.END



# -------------------------------WORK > MODULE (ADD/REMOVE MODULES)------------------------------- #
def module_add_module(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a module name\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
        return MODULE_ADD_MODULE_WAITING_INPUT
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Eh choose a module name\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return MODULE_ADD_MODULE_WAITING_INPUT

def module_add_module_waiting_input(update, context):
    # clear context.chat_data['current module']
    context.chat_data['current module'] = ""
    module_without_esc = update.message.text
    module_with_esc = add_escape_to_string(module_without_esc)
    # limit module_without_esc to 45 characters
    if len(module_without_esc) <= 45:
        if module_with_esc not in context.chat_data['modules']:
            #context.chat_data['current module'] = module_with_esc
            context.chat_data['modules'][module_with_esc] = {'to-do list':{}}
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Okok I add *{}* liao\! 🤓".format(module_with_esc),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_keyboard())
            #return ConversationHandler.END
            return MODULE_MENU

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Aiyo this module name is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
            module_add_module(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=("*Aiyo this module name exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                       + "*"+ str(len(module_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_add_module(update, context)


def module_remove_module(update, context):
    query = update.callback_query
    
    if len(context.chat_data['modules']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you got no modules\! 😒*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Which one you want to remove?:* 🪓",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_remove_module_keyboard(context))
        return MODULE_REMOVE_MODULE_MENU

def module_remove_module_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    module_without_esc = callback_data.partition('removemod_')[2]
    module_with_esc = add_escape_to_string(module_without_esc)
    context.chat_data['modules'].pop(module_with_esc, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + module_with_esc + "* from your modules liao\. 🥴",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    return ConversationHandler.END


# ------------------------------------WORK > MODULE (REMINDERS)------------------------------------ #
def module_reminders(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Choose faster can: 💅",
                                  reply_markup=module_reminders_keyboard())
    return MODULE_REMINDERS_MENU

def module_view_reminders(update, context):
    query = update.callback_query
    current_module = context.chat_data['current module']

    if len(context.chat_data['reminders']['module']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh you no module reminders what\! 🤦‍♀️*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔__Reminders:__🔔*" + print_reminders(context, "module"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END

def module_set_reminder(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="You don't know what 'choose faster' means is it: 💀",
                                  reply_markup=module_set_reminder_keyboard())

    return MODULE_SET_REMINDER_MENU

def module_set_reminder_for_to_do_list(update, context):
    query = update.callback_query
    if len(context.chat_data['modules']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh you don't have any modules leh\! 🤦‍♀️*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Choose faster can: 😔",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_to_do_list_choose_module_keyboard(context))
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CHOOSE_MODULE

def module_set_reminder_for_to_do_list_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    module_without_esc = callback_data.partition('user_')[2]
    module_with_esc = add_escape_to_string(module_without_esc)
    context.chat_data['current module'] = module_with_esc

    if len(context.chat_data['modules'][module_with_esc]['to-do list']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh your to\-do list for {} is empty leh\! 🤦‍♀️*".format(module_with_esc),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.chat_data['current reminder for tdl'] = {'time':"_\(empty\)_", 'interval':"_\(empty\)_"}
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED #this is the edit menu

def module_set_reminder_for_to_do_list_edit_time(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Faster edit your event time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Faster edit your event time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT

def module_set_reminder_for_to_do_list_edit_time_waiting_input(update, context):
    time = update.message.text
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_checked_with_esc = add_escape_to_string(time_checked)
        context.chat_data['current reminder for tdl']['time'] = time_checked_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="*You never read properly is it, your time is not in the correct format\!* 😲",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_to_do_list_edit_time(update, context)

def module_set_reminder_for_to_do_list_edit_interval(update, context):
    query = update.callback_query
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Hurry choose the interval between each reminder \(in days\)\.* ⌛️" + "\n"
                                           "\(e\.g\. if you want me to kachiao you with your to\-do list every 2 days, then reply with the number 2\.\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Hurry choose the interval between each reminder \(in days\)\.* ⌛️" + "\n"
                                           "\(e\.g\. if you want me to kachiao you with your to\-do list every 2 days, then reply with the number 2\.\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT

def module_set_reminder_for_to_do_list_edit_interval_waiting_input(update, context):
    interval = update.message.text
    try:
        num_of_day = int(interval)
        if num_of_day >= 1:
            if interval == '1':
                context.chat_data['current reminder for tdl']['interval'] = "Every day"
            else:
                context.chat_data['current reminder for tdl']['interval'] = "Every {} days".format(interval)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Still got some more information to fill in below:* 😈 \(Eh this one cannot leave blank ah\)\n\n" + 
                                       "⏰*Time:* " + context.chat_data['current reminder for tdl']['time'] + "\n" +
                                       "📆*Interval:* " + context.chat_data['current reminder for tdl']['interval'],
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
            return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
        else:
            context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="*Wah your maths need tuition ah, enter an integer greater than or equal to 1 leh\!* 🧑‍🏫",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
            module_set_reminder_for_to_do_list_edit_interval(update, context)

    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="*Aiyo enter an integer\!* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_to_do_list_edit_interval(update, context)
  
def module_callback_day(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_module = context.job.context['mod']

    all_tasks_str = ""
    for header,info_dict in chat_data['modules'][current_module]['to-do list'].items():
        # if date is empty, leave as empty else assign format for date
        if (info_dict['task details'] == "_\(empty\)_") and (info_dict['deadline'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\nn📍 " + "*" + header + "*"
        elif (info_dict['task details'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\nn📍 " + "*" + header + "*" + "\n\[Deadline: " + info_dict['deadline'] + "\]"
        elif (info_dict['deadline'] == "_\(empty\)_"):
            all_tasks_str = all_tasks_str + "\n\nn📍 " + "*" + header + "*" + ": \n" + info_dict['task details']
        else:
            all_tasks_str = all_tasks_str + "\n\nn📍 " + "*" + header + "*" + ": \n" + info_dict['task details'] + "\n\[Deadline: " + info_dict['deadline'] + "\]"

    context.bot.send_message(chat_id=chat_id,
                                      text="*📋__To\-Do List for {}:__📋*".format(current_module) + all_tasks_str,
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)

def module_set_reminder_for_to_do_list_done(update, context):
    query = update.callback_query
    current_module = context.chat_data['current module']
    if (context.chat_data['current reminder for tdl']['time'] == "_\(empty\)_") and (context.chat_data['current reminder for tdl']['interval'] == "_\(empty\)_"):
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time and the interval\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    elif context.chat_data['current reminder for tdl']['time'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    elif context.chat_data['current reminder for tdl']['interval'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the interval\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_to_do_list_edit_info_keyboard())
        return MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED
    else:
        if "Reminder for {}'s To\-Do List".format(current_module) in context.chat_data['reminders']['module']:
            old_job = context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['job']
            old_job.schedule_removal()
        else:
            context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)] ={}

        context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['time'] = context.chat_data['current reminder for tdl']['time']
        context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['date'] = context.chat_data['current reminder for tdl']['interval']
        time_with_esc = context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['time']
        time = remove_escape_from_string(time_with_esc)
        context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['interval'] = context.chat_data['current reminder for tdl']['interval']
        interval = context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['interval']

        num_of_day = 0
        if interval == "Every day":
            num_of_day = 1
        else:
            num_of_day = int(interval[6])

        datetime_object_local = datetime.datetime.strptime(time, '%H:%M')
        datetime_object_uct = datetime_object_local - timedelta(hours = 8)
        time_object_uct = datetime_object_uct.time()

        # need to change from minutes to days
        new_job = context.job_queue.run_repeating(module_callback_day, timedelta(days=int(num_of_day)), first=time_object_uct, context={'chat_data': context.chat_data, 'chat_id': str(query.message.chat_id), 'mod' : current_module})
        context.chat_data['reminders']['module']["Reminder for {}'s To\-Do List".format(current_module)]['job'] = new_job

        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Ok can can 🤪 A new reminder for {}'s to\-do list has been created\! 😉 I will remind you at *{} {}*\.".format(current_module, time, interval.lower()),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    

def module_set_reminder_for_event(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Lailai choose choose: 🤪",
                                  reply_markup=module_add_event_keyboard())
    return MODULE_REMINDER_ADD_EVENT_MENU
 
def module_set_reminder_for_event_add_header(update, context):
    query = update.callback_query
    
    if query is not None:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                       text="*Eh create a header for your event\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="*Eh create a header for your event\!* 😪 \(You cannot use back the same header and it cannot be more than 45 characters ah\!\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return MODULE_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT


def module_set_reminder_for_event_add_header_waiting_input(update, context):
    #checks if current reminder dictionary is empty
    # limit header_without_esc to 45 characters
    header_without_esc = update.message.text
    header_with_esc = add_escape_to_string(header_without_esc)
    if len(header_without_esc) > 45:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(header_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_event_add_header(update, context)
    elif header_with_esc in context.chat_data['reminders']['module']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Aiyo this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_event_add_header(update, context)
    else:
        context.chat_data['current reminder'][header_with_esc] = {'date':"_\(empty\)_", 'time':"_\(empty\)_"}
        context.bot.send_message(chat_id=update.effective_chat.id,
                                      text=("*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                           "📍*Header:* " + header_with_esc + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][header_with_esc]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][header_with_esc]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_set_reminder_for_event_details_keyboard())
    
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    

def module_set_reminder_for_event_date(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                 message_id=query.message.message_id,
                                 text="*Eh choose your event date\!* 🤓 \n\(Must be this format ok, don't try to be funny: DD/MM/YYYY\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    return MODULE_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT       

def module_set_reminder_for_event_add_date_waiting_input(update, context):
    date = update.message.text
    try:
        # check formatting
        date_checked = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        date_with_esc = add_escape_to_string(date_checked)
        current_header = list(context.chat_data['current reminder'].keys())[0]
        context.chat_data['current reminder'][current_header]['date'] = date_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                      text=("*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                           "📍*Header:* " + current_header + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][current_header]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][current_header]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_set_reminder_for_event_details_keyboard())
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Aiyo you cannot read is it. Your date is not in the correct format leh\!* 😒",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_event_date(update, context)


def module_set_reminder_for_event_time(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                  message_id=query.message.message_id,
                                 text="*Faster edit your event time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    return MODULE_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT


def module_set_reminder_for_event_add_time_waiting_input(update, context):
    time = update.message.text
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_with_esc = add_escape_to_string(time_checked)
        current_header = list(context.chat_data['current reminder'].keys())[0]
        context.chat_data['current reminder'][current_header]['time'] = time_with_esc
        
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=("*Still got some more information to fill in below:* 👻 \(Eh this one cannot leave blank ah\)\n\n" +
                                           "📍*Header:* " + current_header + "\n" +
                                           "📆*Date:* " + context.chat_data['current reminder'][current_header]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current reminder'][current_header]['time']),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                     reply_markup=module_set_reminder_for_event_details_keyboard())
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*You never read properly is it, your time is not in the correct format\!* 😲",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        module_set_reminder_for_event_time(update, context)

def module_reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_header = context.job.context['header']
    date_with_esc = chat_data['reminders']['module'][current_header]['date']
    time_with_esc = chat_data['reminders']['module'][current_header]['time']
    job_queue = context.job.context['job_queue']

    new_job = context.job_queue.run_once(module_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': chat_data, 'job_queue': job_queue, 'header': current_header, 'chat_id': chat_id})
    chat_data['reminders']['module'][current_header]['job'] = new_job
    chat_data['reminders']['module'][current_header]['status'] = "dismiss"

    context.bot.send_message(chat_id= chat_id, 
                             text= ("You have a reminder\! 🥳 \n\n" +
                                    "📍*Event:* " + current_header + "\n" +
                                    "📆*Date:* " + date_with_esc + "\n" +
                                    "⏰*Time:* " + time_with_esc + "\n\n" +
                                    "Please choose either SNOOZE💤 to snooze the reminder for 10 minutes or DISMISS❌ to remove the reminder\!" +"\n" +
                                    "*If no option is chosen within 10 minutes, then I will just remove your reminder automatically ⏰🔨\.*"),
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=module_snooze_reminder_keyboard(current_header))
    #chat_data['reminders'].pop(current_header)

#Snooze feature for one-off event reminders. If user has clicked snooze, reminder is snoozed for 10 minutes and a new reminder for the event will be sent after the 10 minutes from when the reminder is snoozed.
#If user did not click on snooze within 10 minutes, the reminder will have been automatically removed.
#Dimiss feature for one-off event reminders. If user has clicked dismiss, reminder is removed.
#Callback to check if user has clicked snooze/ dismiss or did not click anything for the reminder.
def module_check_reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_header = context.job.context['header']
    job_queue = context.job.context['job_queue']
    now_uct = datetime.datetime.now()
    if chat_data['reminders']['module'][current_header]['status'] == 'snooze':
        new_job = job_queue.run_once(module_reminder_callback, now_uct, context={'chat_data': chat_data, 'job_queue': job_queue , 'header': current_header, 'chat_id': chat_id})
        chat_data['reminders']['module'][current_header]['job'] = new_job
    else:
        old_job = chat_data['reminders']['module'][current_header]['job']
        old_job.schedule_removal()
        chat_data['reminders']['module'].pop(current_header, None)
        
 #Callback when users click on the snooze button for reminder.       
def module_snooze_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('module_snooze_reminder_')[2]
    #If user clicks the snooze keyboard after 10 minutes is up.
    if current_header not in context.chat_data['reminders']['module']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been removed already leh\. 🤷‍♀️",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    else:
        context.chat_data['reminders']['module'][current_header]['status'] = 'snooze'
        old_job = context.chat_data['reminders']['module'][current_header]['job']
        old_job.schedule_removal()
        new_job = context.job_queue.run_once(module_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': context.chat_data, 'job_queue': context.job_queue, 'header': current_header, 'chat_id': str(query.message.chat_id)})
        context.chat_data['reminders']['module'][current_header]['job'] = new_job
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been snoozed for 10 minutes\. ⏰💤",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

#Callback when user clicks on dismiss button for reminder.
def module_dismiss_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_header = callback_data.partition('module_dismiss_reminder_')[2]
    old_job = context.chat_data['reminders']['module'][current_header]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['module'].pop(current_header, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_header + "* has been removed\. ⏰🔨😈",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

def module_set_reminder_for_event_done(update, context):
    query = update.callback_query
    current_header = list(context.chat_data['current reminder'].keys())[0]
    current_datetime = datetime.datetime.now()
    
    
    if (context.chat_data['current reminder'][current_header]['date'] == "_\(empty\)_") and (context.chat_data['current reminder'][current_header]['time'] == "_\(empty\)_"):
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the date and the time\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_event_details_keyboard())
    
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    elif context.chat_data['current reminder'][current_header]['date'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the date\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_event_details_keyboard())
    
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    elif context.chat_data['current reminder'][current_header]['time'] == "_\(empty\)_":
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh hurry fill in the time\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_event_details_keyboard())
        return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    # check if the given date and time is over
    else:
        #NEW
        date_with_esc = context.chat_data['current reminder'][current_header]['date']
        date_without_esc = remove_escape_from_string(date_with_esc)
        time_with_esc = context.chat_data['current reminder'][current_header]['time']
        time_without_esc = remove_escape_from_string(time_with_esc)
        date_and_time = date_without_esc + " " + time_without_esc
        datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
        
        if datetime_object_uct < current_datetime:
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your date and time is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=module_set_reminder_for_event_details_keyboard())
            return MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU
    # save stuff in 'current reminder' to 'reminders'
        else:
            
            context.chat_data['reminders']['module'][current_header] = context.chat_data['current reminder'][current_header]
            new_job = context.job_queue.run_once(module_reminder_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'job_queue': context.job_queue , 'header': current_header, 'chat_id': str(query.message.chat_id)})
            context.chat_data['reminders']['module'][current_header]['job'] = new_job
            reminder_status = "dismiss"
            context.chat_data['reminders']['module'][current_header]['status'] = reminder_status
            context.chat_data['current reminder'].clear()
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔__Reminders:__🔔*" + print_reminders(context, "module"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
            return ConversationHandler.END


def module_remove_reminder(update, context):
    query = update.callback_query
    if len(context.chat_data['reminders']['module']) == 0:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                     text="*Eh you have no module reminders leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2)
        return ConversationHandler.END
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*🔔__Reminders:__🔔*" + print_reminders(context, "module"),
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=None)
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="*Faster choose the reminder you want to remove:* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=module_remove_reminder_keyboard(context))
    return MODULE_REMOVE_REMINDER_MENU


def module_remove_reminder_user_choice(update, context):
    query = update.callback_query
    callback_data = query.data
    header_without_esc = callback_data.partition('module_reminder_')[2]
    header_with_esc = add_escape_to_string(header_without_esc)
    old_job = context.chat_data['reminders']['module'][header_with_esc]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['module'].pop(header_with_esc)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + header_with_esc + "* from reminders liao\. 🥱",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    if len(context.chat_data['reminders']['module']) == 0:
        context.bot.send_message(chat_id=query.message.chat_id,
                                  text="*Eh you have no module reminders\!* 🥱",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 reply_markup=None)
    else:
        context.bot.send_message(chat_id=query.message.chat_id,
                              text="*🔔__Reminders:__🔔*" + print_reminders(context, "module"),
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=None)
    return ConversationHandler.END



# ------------------------------------CCA------------------------------------ #
#NEW
#CCA callback
def cca(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose choose 🥱 I want to sleep liao*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_keyboard())
    return CCA_MENU

def cca_add_session(update, context):
    context.chat_data['current cca'].clear()
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + "_\(empty\)_" + "\n" +
                                           "📜*Details:* " + "_\(empty\)_" + "\n" +
                                           "📆*Date:* " + "_\(empty\)_" + "\n" +
                                           "⏰*Time:* " + "_\(empty\)_" + "\n" +
                                           "🏫*Location:* " + "_\(empty\)_" + "\n" +
                                           "⏳*Poll Deadline:* " + "_\(empty\)_"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
    return CCA_ADD_SESSION_MENU

def cca_add_session_title(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Create a header for your CCA session\!* 👇 \(Note that no repeats are allowed and there is a 45 character limit\.\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
    return CCA_ADD_SESSION_TITLE_WAITING_INPUT


def cca_add_session_title_waiting_input(update, context):
    title_without_esc = update.message.text
    title_with_esc = add_escape_to_string(title_without_esc)
    if len(title_without_esc) > 45:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                      text=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(title_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_add_session_title(update, context)

  
    elif title_with_esc in context.chat_data['cca']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Eh this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_add_session_title(update, context)
    else:
        context.chat_data['current cca'][title_with_esc] = {'details':"_\(empty\)_", 'date':"_\(empty\)_", 'time':"_\(empty\)_", 'location':"_\(empty\)_", 'deadline':"_\(empty\)_"}
        context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + title_with_esc + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][title_with_esc]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][title_with_esc]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][title_with_esc]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][title_with_esc]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][title_with_esc]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
        
        return CCA_ADD_SESSION_MENU

def cca_add_session_details(update, context):
    query = update.callback_query
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick tell me all the details: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return CCA_ADD_SESSION_DETAILS_WAITING_INPUT

def cca_add_session_details_waiting_input(update, context):
    details_without_esc = update.message.text
    details_with_esc = add_escape_to_string(details_without_esc)
    current_title = list(context.chat_data['current cca'].keys())[0]
    context.chat_data['current cca'][current_title]['details'] = details_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
    return CCA_ADD_SESSION_MENU

def cca_add_session_date(update, context):
    query = update.callback_query
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                       text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text="*Eh choose your CCA date\!* 🤓 \n\(Must be this format ok, don't try to be funny: DD/MM/YYYY\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return CCA_ADD_SESSION_DATE_WAITING_INPUT


def cca_add_session_date_waiting_input(update, context):
    date = update.message.text
  
    try:
        # check formatting
        date_checked = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        date_with_esc = add_escape_to_string(date_checked)
        current_title = list(context.chat_data['current cca'].keys())[0]
        context.chat_data['current cca'][current_title]['date'] = date_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
        return CCA_ADD_SESSION_MENU
         
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Aiyo your date is not in the correct format leh\!* 😒",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_add_session_date(update, context)


def cca_add_session_time(update, context):
    query = update.callback_query
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster edit your CCA time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return CCA_ADD_SESSION_TIME_WAITING_INPUT

def cca_add_session_time_waiting_input(update, context):
    time = update.message.text
  
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_with_esc = add_escape_to_string(time_checked)
        current_title = list(context.chat_data['current cca'].keys())[0]
        context.chat_data['current cca'][current_title]['time'] = time_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
        return CCA_ADD_SESSION_MENU
    
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="*You never read properly is it, your time is not in the correct format\!* 😲",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_add_session_time(update, context)

def cca_add_session_location(update, context):
    query = update.callback_query
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh where you having your CCA ah\! 🏫*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return CCA_ADD_SESSION_LOCATION_WAITING_INPUT


def cca_add_session_location_waiting_input(update, context):
    location_without_esc = update.message.text
    location_with_esc = add_escape_to_string(location_without_esc)
    current_title = list(context.chat_data['current cca'].keys())[0]
    context.chat_data['current cca'][current_title]['location'] = location_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
    return CCA_ADD_SESSION_MENU

def cca_add_session_deadline(update, context):
    query = update.callback_query
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster edit your cut\-off date and time for your CCA poll\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return CCA_ADD_SESSION_DEADLINE_WAITING_INPUT


def cca_add_session_deadline_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
  
    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_with_esc = add_escape_to_string(deadline_date_checked + " " + deadline_time_checked)
        current_title = list(context.chat_data['current cca'].keys())[0]
        context.chat_data['current cca'][current_title]['deadline'] = deadline_checked_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'] + "\n" +
                                            "⏳*Poll Deadline:* " + context.chat_data['current cca'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_add_session_keyboard())
        return CCA_ADD_SESSION_MENU
         
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="*Wah jialat your poll deadline is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_add_session_deadline(update, context)


def update_cca_callback(context):
    current_title = context.job.context['title']
    chat_data = context.job.context['chat_data']
    user_id = context.job.context['user']
    chat_data['cca'].pop(current_title, None)
    if user_id in context.bot_data:
        if 'cca' in context.bot_data[user_id]:
            context.bot_data[user_id]['cca'].pop(current_title, None)


def cca_add_session_done(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    if not context.chat_data['current cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your CCA session first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
        return CCA_ADD_SESSION_MENU

    else:
        current_title = list(context.chat_data['current cca'].keys())[0]
        if context.chat_data['current cca'][current_title]['date'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the date\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
            return CCA_ADD_SESSION_MENU
        

        elif context.chat_data['current cca'][current_title]['time'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
            return CCA_ADD_SESSION_MENU


        elif context.chat_data['current cca'][current_title]['deadline'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the deadline for your CCA poll\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
    
            return CCA_ADD_SESSION_MENU

        else:
            current_datetime = datetime.datetime.now()
            given_date_and_time_string = context.chat_data['current cca'][current_title]['date'] + " " + context.chat_data['current cca'][current_title]['time']
            given_datetime_local = datetime.datetime.strptime(given_date_and_time_string, '%d/%m/%Y %H:%M')
            given_datetime_uct = given_datetime_local - timedelta(hours = 8)
            given_deadline_string = context.chat_data['current cca'][current_title]['deadline']
            given_deadline_local = datetime.datetime.strptime(given_deadline_string, '%d/%m/%Y %H:%M')
            given_deadline_uct = given_deadline_local - timedelta(hours = 8)
        
            if given_datetime_uct < current_datetime:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your date and time is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
                return CCA_ADD_SESSION_MENU

            elif given_deadline_uct < current_datetime:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your deadline for your CCA poll is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
                return CCA_ADD_SESSION_MENU

            elif given_datetime_uct < given_deadline_uct:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh use your brain, your deadline for your poll MUST be earlier than the date and time for your CCA session\! 😠*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_keyboard())
                return CCA_ADD_SESSION_MENU

            else:
                for key, value in context.chat_data['current cca'][current_title].items():
                    if value ==  "_\(empty\)_":
                        context.chat_data['current cca'][current_title][key] = "nil"
        
                context.chat_data['cca'][current_title] = context.chat_data['current cca'][current_title]
        

                details = context.chat_data['current cca'][current_title]['details']

                date_with_esc = context.chat_data['current cca'][current_title]['date']
                time_with_esc = context.chat_data['current cca'][current_title]['time']
                location = context.chat_data['current cca'][current_title]['location']
                deadline = context.chat_data['current cca'][current_title]['deadline']
 
                text = "📍Title : " + current_title + "\n" + "📜Details: " + details + "\n" + "📆Date: " + date_with_esc + "\n" + "⏰Time: " + time_with_esc + "\n" + "🏫Location: " + location + "\n" + "⏳Poll Deadline: " + deadline
                #chat_data['reminders'].pop(current_title, None)
                date_without_esc = remove_escape_from_string(date_with_esc)
                time_without_esc = remove_escape_from_string(time_with_esc)
                date_and_time = date_without_esc + " " + time_without_esc
                datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
                datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
                #Removes cca session when date is passed 
                
                context.job_queue.run_once(update_cca_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'title': current_title, 'user': user_id})
        
            

                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Send poll\? ⌨️",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=cca_add_session_done_keyboard(text))

    
    

def cca_add_session_done_clicked(update, context):
    #text = update.message.text.partition(" ")[2].partition(" ")[2]
    text = update.message.text.split("\n", 1)[1]
    title = text.splitlines()[0]
    user_id = str(update.message.from_user.id)
   
   
    current_title = title.partition(": ")[2]
 
    if 'current cca' not in context.chat_data:
        context.chat_data['current cca'] ={}
        context.chat_data['current cca'][current_title] = {}
        context.chat_data['current cca']['current_title'] = current_title
    else:
        context.chat_data['current cca'][current_title] = {}
        context.chat_data['current cca']['current_title'] = current_title

    context.chat_data['current cca'][current_title]['attending'] ={}
    context.chat_data['current cca'][current_title]['not attending'] = {}
    context.chat_data['current cca'][current_title]['admin'] = user_id
    if user_id not in context.bot_data:
        context.bot_data[user_id] = {}
    
    if 'cca' not in context.bot_data[user_id]:
        context.bot_data[user_id]['cca'] = {}
    
    context.bot_data[user_id]['cca'][current_title] = {}
    context.bot_data[user_id]['cca'][current_title]['attending'] = {}
    context.bot_data[user_id]['cca'][current_title]['not attending'] = {}
 
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text= "*Eh everyone faster choose for this CCA session 🧐: *" + "\n" +  text,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_poll_keyboard("0 0"))


def cca_reminder(update, context):
    to_edit = False
    query = update.callback_query
    text = query.message.text.split("\n", 1)[1]
    #current_title = list(context.chat_data['current cca'].keys())[0]
    current_title = text.splitlines()[0].partition(": ")[2]
    details = text.splitlines()[1].partition(": ")[2]
    date = text.splitlines()[2].partition(": ")[2]
    time = text.splitlines()[3].partition(": ")[2]
    location = text.splitlines()[4].partition(": ")[2]
    deadline = text.splitlines()[5].partition(": ")[2]

    present = datetime.datetime.now()
    date_and_time = date + " " + time
    #NEW
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)

    deadline_object_local = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    deadline_object_uct = deadline_object_local - datetime.timedelta(hours = 8)

    user_id = query.from_user.id
    user_first_name =  query.from_user.first_name if query.from_user.first_name != None else ""
    user_last_name =  query.from_user.last_name if query.from_user.last_name != None else ""
    user_name = user_first_name + " " + user_last_name
    
    if str(user_id) not in context.chat_data['current cca'][current_title]['attending']:
        context.chat_data['current cca'][current_title]['attending'][str(user_id)] = "1"
        admin_user_id = context.chat_data['current cca'][current_title]['admin']
        if 'cca' not in context.user_data:
            context.user_data['cca'] = {}
        if str(user_id) != admin_user_id:
            context.user_data['cca'][current_title] = {'details': details, 'date':date, 'time':time, 'location':location, 'admin' : admin_user_id}
        if current_title in context.bot_data[admin_user_id]['cca']:
            context.bot_data[admin_user_id]['cca'][current_title]['attending'][user_name] = "1"
        to_edit = True   

    context.chat_data['current cca'][current_title]['not attending'].pop(str(user_id), None)
    admin_user_id = context.chat_data['current cca'][current_title]['admin']
    if current_title in context.bot_data[admin_user_id]['cca']:
        context.bot_data[admin_user_id]['cca'][current_title]['not attending'].pop(user_name, None)
    else:
        to_edit = False
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Session has been deleted 🤫')

    attending_num =  len(list(context.chat_data['current cca'][current_title]['attending'].keys()))
    not_attending_num =  len(list(context.chat_data['current cca'][current_title]['not attending'].keys()))
    total_num = str(attending_num) + " " + str(not_attending_num)
    if present > datetime_object_local or present > deadline_object_local:
        to_edit = False
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Poll closed liao 😒')
        
    if to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Eh everyone faster choose for this CCA session 🧐: *" + "\n" +  text,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_poll_keyboard(total_num))
                                                                                            

        context.bot.send_message(chat_id=user_id,
                                text="Lailai choose choose: 🤪" + "\n" + text,
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=cca_user_set_reminder_keyboard())

    

def cca_user_set_reminder(update, context):
    query = update.callback_query
    if query is not None:
    
        query = update.callback_query
        text = query.message.text.split("\n", 1)[1]
        list_of_cca_data = text.splitlines()
        current_title = list_of_cca_data[0].partition(": ")[2]
        if 'reminders' not in context.chat_data:
            context.chat_data['reminders'] = {}
            context.chat_data['reminders']['cca'] ={}
        
        if 'current cca' not in context.chat_data:
            context.chat_data['current cca'] = {} 
        
        if current_title not in context.chat_data['current cca'] or current_title not in context.chat_data['reminders']['cca']:
            details = list_of_cca_data[1].partition(": ")[2]
            date_with_esc = list_of_cca_data[2].partition(": ")[2]
            time_with_esc = list_of_cca_data[3].partition(": ")[2]
            location = list_of_cca_data[4].partition(": ")[2]
            deadline = list_of_cca_data[5].partition(": ")[2]

 

            context.chat_data['current cca'][current_title] = {'details': details, 'date':date_with_esc, 'time':time_with_esc, 'location':location, 'deadline': deadline}
            context.chat_data['current cca']['current_title'] = current_title
            context.chat_data['reminders']['cca'][current_title] = {'details': details, 'date':date_with_esc, 'time':time_with_esc, 'location':location, 'deadline': deadline}
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text="*Faster choose a date and time for your CCA reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
            
        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text="*Faster choose a date and time for your CCA reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)


    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Faster choose a date and time for your CCA reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
  
    return  CCA_USER_SET_REMINDER_WAITING_INPUT

def cca_user_set_reminder_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
    current_datetime = datetime.datetime.now()

    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_with_esc = add_escape_to_string(deadline_date_checked + " " + deadline_time_checked)
        datetime_object_local = datetime.datetime.strptime(deadline_checked_with_esc, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)

        if datetime_object_uct < current_datetime:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your date and time is already over\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
            cca_user_set_reminder(update, context)
    
        else:
        #current_title = list(context.chat_data['current cca'].keys())[0]
            current_title = context.chat_data['current cca']['current_title']
            context.chat_data['current cca'][current_title]['deadline'] = deadline_checked_with_esc
            context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="*Okok hurry confirm this reminder for: *" + "\n" 
                                      "📍*Title : *" + current_title + "\n"
                                      "📆*Date: *" + deadline_date_checked + "\n" 
                                      "⏰*Time: *" + deadline_time_checked,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_user_set_reminder_done_keyboard())
        
            return CCA_USER_SET_REMINDER_DONE_MENU

    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your date and time is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        cca_user_set_reminder(update, context)



def cca_callback(context):
    chat_id = context.job.context['chat_id']
    current_title = context.job.context['title']
    chat_data = context.job.context['chat_data']
    details = chat_data['reminders']['cca'][current_title]['details']
    date_with_esc = chat_data['reminders']['cca'][current_title]['date']
    time_with_esc = chat_data['reminders']['cca'][current_title]['time']
    location = chat_data['reminders']['cca'][current_title]['location']
    job_queue = context.job.context['job_queue']
    user_data = context.job.context['user_data']
    #chat_data['reminders'].pop(current_title, None)
    #chat_data['current cca'].clear()
   
    new_job = context.job_queue.run_once(cca_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': chat_data, 'user_data': user_data, 'job_queue': job_queue, 'title': current_title, 'chat_id': chat_id})
    chat_data['reminders']['cca'][current_title]['job'] = new_job
    user_data['reminders']['cca'][current_title]['job'] = new_job
    chat_data['reminders']['cca'][current_title]['status'] = "dismiss"

    context.bot.send_message(chat_id= chat_id, 
                                         text= ("You have a reminder\! 🥳 \n\n" +
                                             "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n\n" +
                                    "Please choose either SNOOZE💤 to snooze the reminder for 10 minutes or DISMISS❌ to remove the reminder\!" +"\n" +
                                    "*If no option is chosen within 10 minutes, reminder will be removed automatically\.*"),
                                        parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                        reply_markup= cca_snooze_reminder_keyboard(current_title))

#Callback to check if user has clicked snooze/ dismiss or did not click anything for the reminder.
#Snooze feature for one-off event reminders. If user has clicked snooze, reminder is snoozed for 10 minutes and a new reminder for the event will be sent after the 10 minutes from when the reminder is snoozed.
#If user did not click on snooze within 10 minutes, the reminder will have been automatically removed.
#Dimiss feature for one-off event reminders. If user has clicked dismiss, reminder is removed.
def cca_check_reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_title = context.job.context['title']
    job_queue = context.job.context['job_queue']
    user_data = context.job.context['user_data']
    now_uct = datetime.datetime.now() 
    if chat_data['reminders']['cca'][current_title]['status'] == 'snooze':
        new_job = job_queue.run_once(cca_callback, now_uct, context={'chat_data': chat_data, 'user_data': user_data, 'job_queue': job_queue , 'title': current_title, 'chat_id': chat_id})
        chat_data['reminders']['cca'][current_title]['job'] = new_job
        user_data['reminders']['cca'][current_title]['job'] = new_job
    else:
        old_job = chat_data['reminders']['cca'][current_title]['job']
        old_job.schedule_removal()
        chat_data['reminders']['cca'].pop(current_title, None)
        user_data['reminders']['cca'].pop(current_title, None)
        
 #Callback when users click on the snooze button for reminder.       
def cca_snooze_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('cca_snooze_reminder_')[2]
    #If user clicks the snooze keyboard after 10 minutes is up.
    if current_title not in context.chat_data['reminders']['cca']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_title + "* has been removed already leh\. 🤷‍♀️",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    else:
        context.chat_data['reminders']['cca'][current_title]['status'] = 'snooze'
        old_job = context.chat_data['reminders']['cca'][current_title]['job']
        old_job.schedule_removal()
        old_job = context.user_data['reminders']['cca'][current_title]['job']
        old_job.schedule_removal()
        new_job = context.job_queue.run_once(cca_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': context.chat_data, 'job_queue': context.job_queue, 'user_data': context.user_data, 'title': current_title, 'chat_id': str(query.message.chat_id)})
        context.chat_data['reminders']['cca'][current_title]['job'] = new_job
        context.user_data['reminders']['cca'][current_title]['job'] = new_job
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_title + "*  has been snoozed for 10 minutes\. ⏰💤",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

#Callback when user clicks on dismiss button for reminder.
def cca_dismiss_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('cca_dismiss_reminder_')[2]
    old_job = context.chat_data['reminders']['cca'][current_title]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['cca'].pop(current_title, None)
    context.user_data['reminders']['cca'].pop(current_title, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_title + "*  has been removed\. ⏰🔨😈",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)


def cca_user_set_reminder_confirm(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id

    #current_title = list(context.chat_data['current cca'].keys())[0]
    current_title = context.chat_data['current cca']['current_title']
    deadline_checked_with_esc = context.chat_data['current cca'][current_title]['deadline']
    date_and_time = remove_escape_from_string(deadline_checked_with_esc)
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
    
    
    #context.chat_data['cca'][current_title] = {'details': details_with_space, 'date':date_with_esc, 'time':time_with_esc, 'location':location_with_space}
    new_job = context.job_queue.run_once(cca_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'user_data': context.user_data, 'job_queue': context.job_queue, 'title': current_title, 'chat_id': str(chat_id)})
    context.chat_data['reminders']['cca'][current_title]['job'] = new_job
    if 'reminders' not in context.user_data:
        context.user_data['reminders'] = {}
    if 'cca' not in context.user_data['reminders']:
        context.user_data['reminders']['cca'] = {}

    context.user_data['reminders']['cca'][current_title] = {}
    context.user_data['reminders']['cca'][current_title]['job'] = new_job
    reminder_status = "dismiss"
    context.chat_data['reminders']['cca'][current_title]['status'] = reminder_status
       
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                text="*Yay a Reminder for your CCA has been set\! 😋*" +  "\n" 
                                     "*Note that if you click on Not Attending for the poll before the poll deadline, the reminder you previously set will be automatically removed\.*" + "\n\n"
                                    "📍*Title :* " + current_title + "\n" 
                                    "📜*Details:* " + context.chat_data['current cca'][current_title]['details'] + "\n" 
                                    "📆*Date:* " + context.chat_data['current cca'][current_title]['date'] + "\n"
                                    "⏰*Time:* " + context.chat_data['current cca'][current_title]['time'] + "\n" +
                                    "🏫*Location:* " + context.chat_data['current cca'][current_title]['location'],
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
   


def not_attending_cca(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    text = query.message.text.split("\n", 1)[1]
    #current_title = list(context.chat_data['current cca'].keys())[0]
    current_title = text.splitlines()[0].partition(": ")[2]
    to_edit = False
    date = text.splitlines()[2].partition(": ")[2]
    time = text.splitlines()[3].partition(": ")[2]
    deadline = text.splitlines()[5].partition(": ")[2]
    present = datetime.datetime.now()
    date_and_time = date + " " + time
    #NEW
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)

    deadline_object_local = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    deadline_object_uct = deadline_object_local - datetime.timedelta(hours = 8)

    user_id = query.from_user.id
    user_first_name =  query.from_user.first_name if query.from_user.first_name != None else ""
    user_last_name =  query.from_user.last_name if query.from_user.last_name != None else ""
    user_name = user_first_name + " " + user_last_name
    admin_user_id = context.chat_data['current cca'][current_title]['admin']
    if str(user_id) not in context.chat_data['current cca'][current_title]['not attending']:
        context.chat_data['current cca'][current_title]['not attending'][str(user_id)] = "1"
        #admin_user_id = context.chat_data['current cca'][current_title]['admin']
        if 'cca' in context.user_data:
            context.user_data['cca'].pop(current_title, None)
        if current_title in context.bot_data[admin_user_id]['cca']:
            context.bot_data[admin_user_id]['cca'][current_title]['not attending'][user_name] = "1"
        to_edit = True   
     
    if present > datetime_object_uct or present > deadline_object_uct:
        to_edit = False
        #context.bot_data[admin_user_id]['cca'].pop(current_title, None)
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Poll closed liao 😒')
        
    if str(user_id) in context.chat_data['current cca'][current_title]['attending']:
        if 'reminders' in context.user_data:
            if 'cca' in context.user_data['reminders']:
                if current_title in context.user_data['reminders']['cca']:
                    old_job = context.user_data['reminders']['cca'][current_title]['job'] 
                    old_job.schedule_removal()
       

    context.chat_data['current cca'][current_title]['attending'].pop(str(user_id), None)
    if current_title in context.bot_data[admin_user_id]['cca']:
        context.bot_data[admin_user_id]['cca'][current_title]['attending'].pop(user_name, None)
    else:
        to_edit = False
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Session has been deleted 🤫')
    attending_num =  len(list(context.chat_data['current cca'][current_title]['attending'].keys()))
    not_attending_num =  len(list(context.chat_data['current cca'][current_title]['not attending'].keys()))
    total_num = str(attending_num) + " " + str(not_attending_num)
    
    if to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Eh everyone faster choose for this CCA session 🧐: *" + "\n" +  text,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_poll_keyboard(total_num))

def cca_view_sessions(update, context):
    query = update.callback_query
    to_edit = True
    if 'cca' in context.user_data:
        if len(context.user_data['cca'])!= 0:
            to_edit = False

    if len(context.chat_data['cca']) == 0 and to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh why you no CCA session\!* 😔 Your social life aiyo",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose one to see\!* 😩",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=cca_view_sessions_keyboard(context))

        return CCA_VIEW_SESSIONS

def cca_view_session_clicked_admin(update, context):
    query = update.callback_query
    callback_data = query.data
    cca_session = callback_data.partition('view_cca_admin')[2]
    user_id = str(query.from_user.id)
    details = context.chat_data['cca'][cca_session]['details']
    date_with_esc = context.chat_data['cca'][cca_session]['date']
    time_with_esc = context.chat_data['cca'][cca_session]['time']
    location = context.chat_data['cca'][cca_session]['location']
    deadline = context.chat_data['cca'][cca_session]['deadline']
    to_edit = False
    if user_id in context.bot_data:
        if 'cca' in context.bot_data[user_id]:
            if cca_session in context.bot_data[user_id]['cca']:
                list_of_attendees = list(context.bot_data[user_id]['cca'][cca_session]['attending'].keys())
                list_of_non_attendees = list(context.bot_data[user_id]['cca'][cca_session]['not attending'].keys())
                attendees_string = ', '.join(map(str, list_of_attendees))
                non_attendees_string = ', '.join(map(str, list_of_non_attendees))
                to_edit = True
        

    if to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=  "📍*Title:* " + cca_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n" +
                                           "⏳*Poll Deadline:* " + deadline + "\n" + 
                                            "🌈*Attending: *" + attendees_string + "\n"
                                            "☔*Not Attending: *" + non_attendees_string,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                    text=  "📍*Title:* " + cca_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n" +
                                           "⏳*Poll Deadline:* " + deadline,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

def cca_view_session_clicked_user(update, context):
    query = update.callback_query
    callback_data = query.data
    cca_session = callback_data.partition('view_cca_user')[2]
    details = context.user_data['cca'][cca_session]['details']
    date_with_esc = context.user_data['cca'][cca_session]['date']
    time_with_esc = context.user_data['cca'][cca_session]['time']
    location = context.user_data['cca'][cca_session]['location']
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text=  "📍*Title:* " + cca_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)


def cca_remove_session(update, context):
    query = update.callback_query
    to_edit = True
    present = datetime.datetime.now()

    if 'cca' in context.user_data:
        for header in context.user_data['cca']:
            admin_user_id = context.user_data['cca'][header]['admin']
            date = context.user_data['cca'][header]['date']
            time = context.user_data['cca'][header]['time']
            date_and_time = date + " " + time
            datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
            datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
            if present > datetime_object_uct:
                if header not in context.bot_data[admin_user_id]['cca']:
                    context.user_data['cca'].pop(header)

        if len(context.user_data['cca'])!= 0:
            to_edit = False

    

    if len(context.chat_data['cca']) == 0 and to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh why you no CCA session\!* 😔 Your social life aiyo",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                             message_id=query.message.message_id,
                             text="*Which one you want to remove?:* 🪓",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=cca_remove_session_keyboard(context))

    return CCA_REMOVE_SESSION_MENU


def cca_remove_session_admin(update, context):
    query = update.callback_query
    callback_data = query.data
    user_id = str(query.from_user.id)
    current_title = callback_data.partition('remove_cca_admin')[2]
    context.chat_data['cca'].pop(current_title, None)
    if user_id in context.bot_data:
        if 'cca' in context.bot_data[user_id]:
            context.bot_data[user_id]['cca'].pop(current_title, None)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + current_title + "* from your CCA sessions liao\. 🥴 Your poll for this CCA will be closed too",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    
    
    return ConversationHandler.END

def cca_remove_session_user(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('remove_cca_user')[2]
    context.user_data['cca'].pop(current_title, None)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + current_title + "* from your CCA sessions liao\. 🥴",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    
    
    return ConversationHandler.END

# --------------------------------LEISURE ACTIVITY-------------------------------- #
#NEW
#leisure callback
def leisure(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster choose choose 🥱 Can let me rest or not ah*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_keyboard())
    return LEISURE_MENU

def leisure_add_session(update, context):
    context.chat_data['current leisure'].clear()
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                             "📍*Title :* " + "_\(empty\)_" + "\n" +
                                           "📜*Details:* " + "_\(empty\)_" + "\n" +
                                           "📆*Date:* " + "_\(empty\)_" + "\n" +
                                           "⏰*Time:* " + "_\(empty\)_" + "\n" +
                                           "🏫*Location:* " + "_\(empty\)_" + "\n" +
                                           "⏳*Poll Deadline:* " + "_\(empty\)_"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
    return LEISURE_ADD_SESSION_MENU

def leisure_add_session_title(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Create a header for your leisure activity\!* 👇 \(Note that no repeats are allowed and there is a 45 character limit\.\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
    return LEISURE_ADD_SESSION_TITLE_WAITING_INPUT


def leisure_add_session_title_waiting_input(update, context):
    title_without_esc = update.message.text
    title_with_esc = add_escape_to_string(title_without_esc)
    if len(title_without_esc) > 45:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     ttext=("*Aiyo this header exceeds the maximum number of characters leh\!* 😱" + "\n\(Current number of characters: "
                                           + "*"+ str(len(title_without_esc)) + "*" + "\)" + "\n*Choose another one\!*"),
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_add_session_title(update, context)

  
    elif title_with_esc in context.chat_data['leisure']:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="*Eh this header is already taken\! 😱 Choose another one\!*",
                                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_add_session_title(update, context)
    else:
        context.chat_data['current leisure'][title_with_esc] = {'details':"_\(empty\)_", 'date':"_\(empty\)_", 'time':"_\(empty\)_", 'location':"_\(empty\)_", 'deadline':"_\(empty\)_"}
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , 📆date, ⏰time and ⏳poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + title_with_esc + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][title_with_esc]['details'] + "\n" +
                                            "📆*Date:* " + context.chat_data['current leisure'][title_with_esc]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][title_with_esc]['time'] + "\n" +
                                            "🏫*Location:* " + context.chat_data['current leisure'][title_with_esc]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][title_with_esc]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
        
        return LEISURE_ADD_SESSION_MENU

def leisure_add_session_details(update, context):
    query = update.callback_query
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Quick quick tell me all the details: 😪*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return LEISURE_ADD_SESSION_DETAILS_WAITING_INPUT

def leisure_add_session_details_waiting_input(update, context):
    details_without_esc = update.message.text
    details_with_esc = add_escape_to_string(details_without_esc)
    current_title = list(context.chat_data['current leisure'].keys())[0]
    context.chat_data['current leisure'][current_title]['details'] = details_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , date, time and poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
    return LEISURE_ADD_SESSION_MENU

def leisure_add_session_date(update, context):
    query = update.callback_query
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh choose your leisure activity date\!* 🤓 \n\(Must be this format ok, don't try to be funny: DD/MM/YYYY\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return LEISURE_ADD_SESSION_DATE_WAITING_INPUT


def leisure_add_session_date_waiting_input(update, context):
    date = update.message.text
  
    try:
        # check formatting
        date_checked = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        date_with_esc = add_escape_to_string(date_checked)
        current_title = list(context.chat_data['current leisure'].keys())[0]
        context.chat_data['current leisure'][current_title]['date'] = date_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , date, time and poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
        return LEISURE_ADD_SESSION_MENU
         
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Aiyo why your date not in the correct format\!* 😒",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_add_session_date(update, context)


def leisure_add_session_time(update, context):
    query = update.callback_query
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster edit your leisure activity time\!*😒\n\(Die die must be this format ah: HH:MM\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return LEISURE_ADD_SESSION_TIME_WAITING_INPUT

def leisure_add_session_time_waiting_input(update, context):
    time = update.message.text
  
    try:
        # check formatting
        time_checked = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')
        time_with_esc = add_escape_to_string(time_checked)
        current_title = list(context.chat_data['current leisure'].keys())[0]
        context.chat_data['current leisure'][current_title]['time'] = time_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , date, time and poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
        return LEISURE_ADD_SESSION_MENU
    
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*You never read properly is it, your time is not in the correct format\!* 😲",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_add_session_time(update, context)

def leisure_add_session_location(update, context):
    query = update.callback_query
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh where you having your leisure activity ah\! 🏫*",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return LEISURE_ADD_SESSION_LOCATION_WAITING_INPUT


def leisure_add_session_location_waiting_input(update, context):
    location_without_esc = update.message.text
    location_with_esc = add_escape_to_string(location_without_esc)
    current_title = list(context.chat_data['current leisure'].keys())[0]
    context.chat_data['current leisure'][current_title]['location'] = location_with_esc
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , date, time and poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
    return LEISURE_ADD_SESSION_MENU

def leisure_add_session_deadline(update, context):
    query = update.callback_query
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Faster edit your cut\-off date and time for your leisure activity poll\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
        return LEISURE_ADD_SESSION_DEADLINE_WAITING_INPUT


def leisure_add_session_deadline_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_with_esc = add_escape_to_string(deadline_date_checked + " " + deadline_time_checked)
        current_title = list(context.chat_data['current leisure'].keys())[0]
        context.chat_data['current leisure'][current_title]['deadline'] = deadline_checked_with_esc
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text=("*Eh hurry fill in the rest of the information below: * \(MUST fill up the 📍Title , date, time and poll cut\-off ah\)\n\n" +
                                           "📍*Title :* " + current_title + "\n" +
                                          "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" +
                                           "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n" +
                                           "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                           "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'] + "\n" +
                                           "⏳*Poll Deadline:* " + context.chat_data['current leisure'][current_title]['deadline']),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_add_session_keyboard())
        return LEISURE_ADD_SESSION_MENU
         
    
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your poll deadline is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_add_session_deadline(update, context)



def update_leisure_callback(context):
    current_title = context.job.context['title']
    chat_data = context.job.context['chat_data']
    user_id = context.job.context['user']
    chat_data['leisure'].pop(current_title, None)
    if user_id in context.bot_data:
        if 'leisure' in context.bot_data[user_id]:
            context.bot_data[user_id]['leisure'].pop(current_title, None)


def leisure_add_session_done(update, context):
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    if not context.chat_data['current leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh choose a header for your leisure activity first leh\! 🤔*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
        return LEISURE_ADD_SESSION_MENU

    else:
        current_title = list(context.chat_data['current leisure'].keys())[0]
        if context.chat_data['current leisure'][current_title]['date'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                     text="*Why you never fill in the date\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
            return LEISURE_ADD_SESSION_MENU
        

        elif context.chat_data['current leisure'][current_title]['time'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the time\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
            return LEISURE_ADD_SESSION_MENU

        elif context.chat_data['current leisure'][current_title]['deadline'] == "_\(empty\)_":
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Why you never fill in the deadline for your leisure activity poll\!* 😡",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
    
            return LEISURE_ADD_SESSION_MENU

        else:
            current_datetime = datetime.datetime.now()
            given_date_and_time_string = context.chat_data['current leisure'][current_title]['date'] + " " + context.chat_data['current leisure'][current_title]['time']
            given_datetime_local = datetime.datetime.strptime(given_date_and_time_string, '%d/%m/%Y %H:%M')
            given_datetime_uct = given_datetime_local - timedelta(hours = 8)
            given_deadline_string = context.chat_data['current leisure'][current_title]['deadline']
            given_deadline_local = datetime.datetime.strptime(given_deadline_string, '%d/%m/%Y %H:%M')
            given_deadline_uct = given_deadline_local - timedelta(hours = 8)
        
            if given_datetime_uct < current_datetime:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your date and time is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
                return LEISURE_ADD_SESSION_MENU

            elif given_deadline_uct < current_datetime:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Aiyo your deadline for your leisure activity poll is already over leh\!* 😠",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
                return LEISURE_ADD_SESSION_MENU

            elif given_datetime_uct < given_deadline_uct:
                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="*Eh use your brain, your deadline for your poll MUST be earlier than the date and time for your leisure activity\! 😠*",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_keyboard())
                return LEISURE_ADD_SESSION_MENU
        
            else:
                for key, value in context.chat_data['current leisure'][current_title].items():
                    if value ==  "_\(empty\)_":
                        context.chat_data['current leisure'][current_title][key] = "nil"
        
                context.chat_data['leisure'][current_title] = context.chat_data['current leisure'][current_title]
        

                details = context.chat_data['current leisure'][current_title]['details']

                date_with_esc = context.chat_data['current leisure'][current_title]['date']
                time_with_esc = context.chat_data['current leisure'][current_title]['time']
                location = context.chat_data['current leisure'][current_title]['location']
                deadline = context.chat_data['current leisure'][current_title]['deadline']
 
                text = "📍Title : " + current_title + "\n" + "📜Details: " + details + "\n" + "📆Date: " + date_with_esc + "\n" + "⏰Time: " + time_with_esc + "\n" + "🏫Location: " + location + "\n" + "⏳Poll Deadline: " + deadline
                #chat_data['reminders'].pop(current_title, None)

                date_without_esc = remove_escape_from_string(date_with_esc)
                time_without_esc = remove_escape_from_string(time_with_esc)
                date_and_time = date_without_esc + " " + time_without_esc
                datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
                datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
                #Removes leisure session when date is passed 
                context.job_queue.run_once(update_leisure_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'title': current_title, 'user': user_id})


                context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text="Send poll\? ⌨️",
                                      parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                      reply_markup=leisure_add_session_done_keyboard(text))

    
    

def leisure_add_session_done_clicked(update, context):
    #text = update.message.text.partition(" ")[2].partition(" ")[2]
    text = update.message.text.split("\n", 1)[1]
    title = text.splitlines()[0]
    user_id = str(update.message.from_user.id)
   
    current_title = title.partition(": ")[2]
 
    if 'current leisure' not in context.chat_data:
        context.chat_data['current leisure'] ={}
        context.chat_data['current leisure'][current_title] = {}
        context.chat_data['current leisure']['current_title'] = current_title
    else:
        context.chat_data['current leisure'][current_title] = {}
        context.chat_data['current leisure']['current_title'] = current_title

    context.chat_data['current leisure'][current_title]['attending'] ={}
    context.chat_data['current leisure'][current_title]['not attending'] = {}
    context.chat_data['current leisure'][current_title]['admin'] = user_id
    if user_id not in context.bot_data:
        context.bot_data[user_id] = {}
    
    if 'leisure' not in context.bot_data[user_id]:
        context.bot_data[user_id]['leisure'] = {}
    
    context.bot_data[user_id]['leisure'][current_title] = {}
    context.bot_data[user_id]['leisure'][current_title]['attending'] = {}
    context.bot_data[user_id]['leisure'][current_title]['not attending'] = {}
 
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text= "*Eh everyone faster choose for this leisure activity 🧐: *" + "\n" +  text + "\n"
                                  "🌈*Attending: *",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_poll_keyboard("0 0"))


def leisure_reminder(update, context):
    to_edit = False
    query = update.callback_query
    text = query.message.text.split("\n", 1)[1]
    #current_title = list(context.chat_data['current leisure'].keys())[0]
    current_title = text.splitlines()[0].partition(": ")[2]
    details = text.splitlines()[1].partition(": ")[2]
    date = text.splitlines()[2].partition(": ")[2]
    time = text.splitlines()[3].partition(": ")[2]
    location = text.splitlines()[4].partition(": ")[2]
    deadline = text.splitlines()[5].partition(": ")[2]
    
    present = datetime.datetime.now()
    date_and_time = date + " " + time
    #NEW
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
    
    deadline_object_local = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    deadline_object_uct = deadline_object_local - datetime.timedelta(hours = 8)

    user_id = query.from_user.id
    user_first_name = query.from_user.first_name
    user_first_name =  query.from_user.first_name if query.from_user.first_name != None else ""
    user_last_name =  query.from_user.last_name if query.from_user.last_name != None else ""
    user_name = user_first_name + " " + user_last_name

    if str(user_id) not in context.chat_data['current leisure'][current_title]['attending']:
        context.chat_data['current leisure'][current_title]['attending'][str(user_id)] = user_first_name
        admin_user_id = context.chat_data['current leisure'][current_title]['admin']
        if 'leisure' not in context.user_data:
            context.user_data['leisure'] = {}
        if str(user_id) != admin_user_id:
            context.user_data['leisure'][current_title] = {'details': details, 'date':date, 'time':time, 'location':location, 'admin': admin_user_id}
        if current_title in context.bot_data[admin_user_id]['leisure']:
            context.bot_data[admin_user_id]['leisure'][current_title]['attending'][user_name] = "1"
        to_edit = True   

    context.chat_data['current leisure'][current_title]['not attending'].pop(str(user_id), None)
    admin_user_id = context.chat_data['current leisure'][current_title]['admin']
    
    if current_title in context.bot_data[admin_user_id]['leisure']:
        context.bot_data[admin_user_id]['leisure'][current_title]['not attending'].pop(user_name, None)
    else:
        to_edit = False
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Session has been deleted 🤫')

    attending_num =  len(list(context.chat_data['current leisure'][current_title]['attending'].keys()))
    not_attending_num =  len(list(context.chat_data['current leisure'][current_title]['not attending'].keys()))
    total_num = str(attending_num) + " " + str(not_attending_num)
    if present > datetime_object_uct or present > deadline_object_uct:
        to_edit = False
        #context.bot_data[admin_user_id]['leisure'].pop(current_title, None)
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Poll closed liao 😒')
        
    if to_edit:
        text = "\n".join(text.split("\n")[:-1])
        list_of_attendees = list(context.chat_data['current leisure'][current_title]['attending'].values())
        attendees_string = ', '.join(map(str, list_of_attendees))
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Eh everyone faster choose for this leisure activity 🧐: *" + "\n" +  text + "\n"
                                  "🌈*Attending: *" + attendees_string,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_poll_keyboard(total_num))
                                                                                            

        context.bot.send_message(chat_id=user_id,
                                text="Lailai choose choose: 🤪" + "\n" + text,
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=leisure_user_set_reminder_keyboard())

    

def leisure_user_set_reminder(update, context):
    query = update.callback_query
    if query is not None:
    
        query = update.callback_query
        text = query.message.text.split("\n", 1)[1]
        list_of_leisure_data = text.splitlines()
        current_title = list_of_leisure_data[0].partition(": ")[2]
        if 'reminders' not in context.chat_data:
            context.chat_data['reminders'] = {}
            context.chat_data['reminders']['leisure'] ={}
        
        if 'current leisure' not in context.chat_data:
            context.chat_data['current leisure'] = {}
        
        if current_title not in context.chat_data['current leisure'] or current_title not in context.chat_data['reminders']['leisure']:
            details = list_of_leisure_data[1].partition(": ")[2]
            date_with_esc = list_of_leisure_data[2].partition(": ")[2]
            time_with_esc = list_of_leisure_data[3].partition(": ")[2]
            location = list_of_leisure_data[4].partition(": ")[2]
            deadline = list_of_leisure_data[5].partition(": ")[2]

 

            context.chat_data['current leisure'][current_title] = {'details': details, 'date':date_with_esc, 'time':time_with_esc, 'location':location, 'deadline': deadline}
            context.chat_data['current leisure']['current_title'] = current_title
            context.chat_data['reminders']['leisure'][current_title] = {'details': details, 'date':date_with_esc, 'time':time_with_esc, 'location':location, 'deadline': deadline}
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text="*Faster choose a date and time for your leisure activity reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id,
                                    message_id=query.message.message_id,
                                    text="*Faster choose a date and time for your leisure activity reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)


    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Faster choose a date and time for your leisure activity reminder\!* 🙄 \n\(Die die must follow this format: \nDD/MM/YYYY HH:MM\)",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
  
    return  LEISURE_USER_SET_REMINDER_WAITING_INPUT

def leisure_user_set_reminder_waiting_input(update, context):
    deadline = update.message.text
    deadline_date = deadline.partition(' ')[0]
    deadline_time = deadline.partition(' ')[2]
    current_datetime = datetime.datetime.now()

    try:
        # check formatting
        deadline_date_checked = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').strftime('%d/%m/%Y')
        deadline_time_checked = datetime.datetime.strptime(deadline_time, '%H:%M').strftime('%H:%M')
        deadline_checked_with_esc = add_escape_to_string(deadline_date_checked + " " + deadline_time_checked)
        datetime_object_local = datetime.datetime.strptime(deadline_checked_with_esc, '%d/%m/%Y %H:%M')
        datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)

        if datetime_object_uct < current_datetime:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your date and time is already over\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
            leisure_user_set_reminder(update, context)

        else:
        #current_title = list(context.chat_data['current leisure'].keys())[0]
            current_title = context.chat_data['current leisure']['current_title']
            context.chat_data['current leisure'][current_title]['deadline'] = deadline_checked_with_esc
            context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="*Okok hurry confirm this reminder for: *" + "\n" 
                                      "📍*Title : *" + current_title + "\n"
                                      "📆*Date: *" + deadline_date_checked + "\n" 
                                      "⏰*Time: *" + deadline_time_checked,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_user_set_reminder_done_keyboard())
        
            return LEISURE_USER_SET_REMINDER_DONE_MENU

    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="*Wah jialat your date and time is in the wrong format leh\!* 🤧",
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
        leisure_user_set_reminder(update, context)



def leisure_callback(context):
    chat_id = context.job.context['chat_id']
    current_title = context.job.context['title']
    chat_data = context.job.context['chat_data']
    details = chat_data['reminders']['leisure'][current_title]['details']
    date_with_esc = chat_data['reminders']['leisure'][current_title]['date']
    time_with_esc = chat_data['reminders']['leisure'][current_title]['time']
    location = chat_data['reminders']['leisure'][current_title]['location']
    job_queue = context.job.context['job_queue']
    user_data = context.job.context['user_data']
    #chat_data['reminders'].pop(current_title, None)
    #chat_data['current leisure'].clear()
   
    new_job = context.job_queue.run_once(leisure_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': chat_data, 'user_data': user_data, 'job_queue': job_queue, 'title': current_title, 'chat_id': chat_id})
    chat_data['reminders']['leisure'][current_title]['job'] = new_job
    user_data['reminders']['leisure'][current_title]['job'] = new_job
    chat_data['reminders']['leisure'][current_title]['status'] = "dismiss"

    context.bot.send_message(chat_id= chat_id, 
                                          text= ("You have a reminder\! 🥳 \n\n" +
                                             "📍*Title :* " + current_title + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n\n" +
                                    "Please choose either SNOOZE💤 to snooze the reminder for 10 minutes or DISMISS❌ to remove the reminder\!" +"\n" +
                                    "*If no option is chosen within 10 minutes, reminder will be removed automatically\.*"),
                                        parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                        reply_markup=leisure_snooze_reminder_keyboard(current_title))

#Callback to check if user has clicked snooze/ dismiss or did not click anything for the reminder.
#Snooze feature for one-off event reminders. If user has clicked snooze, reminder is snoozed for 10 minutes and a new reminder for the event will be sent after the 10 minutes from when the reminder is snoozed.
#If user did not click on snooze within 10 minutes, the reminder will have been automatically removed.
#Dimiss feature for one-off event reminders. If user has clicked dismiss, reminder is removed.
def leisure_check_reminder_callback(context):
    chat_id = context.job.context['chat_id']
    chat_data = context.job.context['chat_data']
    current_title = context.job.context['title']
    job_queue = context.job.context['job_queue']
    user_data = context.job.context['user_data']
    now_uct = datetime.datetime.now()
    if chat_data['reminders']['leisure'][current_title]['status'] == 'snooze':
        new_job = job_queue.run_once(leisure_callback, now_uct, context={'chat_data': chat_data, 'user_data': user_data, 'job_queue': job_queue , 'title': current_title, 'chat_id': chat_id})
        chat_data['reminders']['leisure'][current_title]['job'] = new_job
        user_data['reminders']['leisure'][current_title]['job'] = new_job
    else:
        old_job = chat_data['reminders']['leisure'][current_title]['job']
        old_job.schedule_removal()
        chat_data['reminders']['leisure'].pop(current_title, None)
        user_data['reminders']['leisure'].pop(current_title, None)

 #Callback when users click on the snooze button for reminder.       
def leisure_snooze_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('leisure_snooze_reminder_')[2]
    #If user clicks the snooze keyboard after 10 minutes is up.
    if current_title not in context.chat_data['reminders']['leisure']:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                 text="*Reminder for " + current_title + "* has been removed already leh\. 🤷‍♀️",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    else:
        context.chat_data['reminders']['leisure'][current_title]['status'] = 'snooze'
        old_job = context.chat_data['reminders']['leisure'][current_title]['job']
        old_job.schedule_removal()
        old_job = context.user_data['reminders']['leisure'][current_title]['job']
        old_job.schedule_removal()
        new_job = context.job_queue.run_once(leisure_check_reminder_callback, datetime.timedelta(minutes=1), context={'chat_data': context.chat_data, 'user_data': context.user_data, 'job_queue': context.job_queue, 'title': current_title, 'chat_id': str(query.message.chat_id)})
        context.chat_data['reminders']['leisure'][current_title]['job'] = new_job
        context.user_data['reminders']['leisure'][current_title]['job'] = new_job
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_title + "*  has been snoozed for 10 minutes\. ⏰💤",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)

#Callback when user clicks on dismiss button for reminder.
def leisure_dismiss_reminder(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('leisure_dismiss_reminder_')[2]
    old_job = context.chat_data['reminders']['leisure'][current_title]['job']
    old_job.schedule_removal()
    context.chat_data['reminders']['leisure'].pop(current_title, None)
    context.user_data['reminders']['cca'].pop(current_title, None)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Reminder for " + current_title + "*  has been removed\. ⏰🔨😈",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)


def leisure_user_set_reminder_confirm(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    #current_title = list(context.chat_data['current leisure'].keys())[0]
    current_title = context.chat_data['current leisure']['current_title']
    deadline_checked_with_esc = context.chat_data['current leisure'][current_title]['deadline']
    date_and_time = remove_escape_from_string(deadline_checked_with_esc)
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
   
    #context.chat_data['leisure'][current_title] = {'details': details_with_space, 'date':date_with_esc, 'time':time_with_esc, 'location':location_with_space}
    new_job = context.job_queue.run_once(leisure_callback, datetime_object_uct, context={'chat_data': context.chat_data, 'user_data': context.user_data, 'job_queue': context.job_queue, 'title': current_title, 'chat_id': str(chat_id)})
    context.chat_data['reminders']['leisure'][current_title]['job'] = new_job
    if 'reminders' not in context.user_data:
        context.user_data['reminders'] = {}
    if 'leisure' not in context.user_data['reminders']:
        context.user_data['reminders']['leisure'] ={}

    context.user_data['reminders']['leisure'][current_title] = {}
    context.user_data['reminders']['leisure'][current_title]['job'] = new_job
    reminder_status = "dismiss"
    context.chat_data['reminders']['leisure'][current_title]['status'] = reminder_status

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                text="*Yay a Reminder for your leisure activity has been set\! 😋*" +  "\n" 
                                    "*Note that if you click on Not Attending for the poll before the poll deadline, the reminder you previously set will be automatically removed\.*" + "\n\n"
                                     "📍*Title :* " + current_title + "\n" 
                                    "📜*Details:* " + context.chat_data['current leisure'][current_title]['details'] + "\n" 
                                    "📆*Date:* " + context.chat_data['current leisure'][current_title]['date'] + "\n"
                                    "⏰*Time:* " + context.chat_data['current leisure'][current_title]['time'] + "\n" +
                                    "🏫*Location:* " + context.chat_data['current leisure'][current_title]['location'],
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
   


def not_attending_leisure(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    text = query.message.text.split("\n", 1)[1]
    #current_title = list(context.chat_data['current leisure'].keys())[0]
    current_title = text.splitlines()[0].partition(": ")[2]
    to_edit = False
    date = text.splitlines()[2].partition(": ")[2]
    time = text.splitlines()[3].partition(": ")[2]
    deadline = text.splitlines()[5].partition(": ")[2]

    present = datetime.datetime.now()
    date_and_time = date + " " + time
    #NEW 
    datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
    datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)

    deadline_object_local = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
    deadline_object_uct = deadline_object_local - datetime.timedelta(hours = 8)
    
    user_id = query.from_user.id
    user_first_name =  query.from_user.first_name if query.from_user.first_name != None else ""
    user_last_name =  query.from_user.last_name if query.from_user.last_name != None else ""
    user_name = user_first_name + " " + user_last_name
    admin_user_id = context.chat_data['current leisure'][current_title]['admin']
    if str(user_id) not in context.chat_data['current leisure'][current_title]['not attending']:
        context.chat_data['current leisure'][current_title]['not attending'][str(user_id)] = "1"
        if 'leisure' in context.user_data:
                context.user_data['leisure'].pop(current_title, None)
        if current_title in context.bot_data[admin_user_id]['leisure']:
            context.bot_data[admin_user_id]['leisure'][current_title]['not attending'][user_name] = "1"
        to_edit = True   
     
    if present > datetime_object_local or present > deadline_object_local:
        to_edit = False
        #context.bot_data[admin_user_id]['leisure'].pop(current_title, None)
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Poll closed liao 😒')
        
    if str(user_id) in context.chat_data['current leisure'][current_title]['attending']:
        if 'reminders' in context.user_data:
            if 'leisure' in context.user_data['reminders']:
                if current_title in context.user_data['reminders']['leisure']:
                    old_job = context.user_data['reminders']['leisure'][current_title]['job'] 
                    old_job.schedule_removal()
       

    context.chat_data['current leisure'][current_title]['attending'].pop(str(user_id), None)
    if current_title in context.bot_data[admin_user_id]['leisure']:
        context.bot_data[admin_user_id]['leisure'][current_title]['attending'].pop(user_name, None)
    else:
        to_edit = False
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= 'Session has been deleted 🤫')
    
    attending_num =  len(list(context.chat_data['current leisure'][current_title]['attending'].keys()))
    not_attending_num =  len(list(context.chat_data['current leisure'][current_title]['not attending'].keys()))
    total_num = str(attending_num) + " " + str(not_attending_num)
    
    if to_edit:
        text = "\n".join(text.split("\n")[:-1])
        list_of_attendees = list(context.chat_data['current leisure'][current_title]['attending'].values())
        attendees_string = ', '.join(map(str, list_of_attendees))
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= "*Eh everyone faster choose for this leisure activity 🧐: *" + "\n" +  text + "\n"
                                  "🌈*Attending: *" + attendees_string,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_poll_keyboard(total_num))


def leisure_view_session(update, context):
    query = update.callback_query
    to_edit = True
    if 'leisure' in context.user_data:
        if len(context.user_data['leisure'])!= 0:
            to_edit = False

    if len(context.chat_data['leisure']) == 0 and to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh why you no leisure activity\!* 😔 Your social life aiyo",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text="*Faster choose one to see\!* 😩",
                                   parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=leisure_view_session_keyboard(context))

        return LEISURE_VIEW_SESSION

def leisure_view_session_clicked_admin(update, context):
    query = update.callback_query
    callback_data = query.data
    leisure_session = callback_data.partition('view_leisure_admin')[2]
    user_id = str(query.from_user.id)
    details = context.chat_data['leisure'][leisure_session]['details']
    date_with_esc = context.chat_data['leisure'][leisure_session]['date']
    time_with_esc = context.chat_data['leisure'][leisure_session]['time']
    location = context.chat_data['leisure'][leisure_session]['location']
    deadline = context.chat_data['leisure'][leisure_session]['deadline']
    to_edit = False
    if user_id in context.bot_data:
        if 'leisure' in context.bot_data[user_id]:
            if leisure_session in context.bot_data[user_id]['leisure']:
                list_of_attendees = list(context.bot_data[user_id]['leisure'][leisure_session]['attending'].keys())
                list_of_non_attendees = list(context.bot_data[user_id]['leisure'][leisure_session]['not attending'].keys())
                attendees_string = ', '.join(map(str, list_of_attendees))
                non_attendees_string = ', '.join(map(str, list_of_non_attendees))
                to_edit = True
        

    if to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=  "📍*Title:* " + leisure_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n" +
                                           "⏳*Poll Deadline:* " + deadline + "\n" + 
                                            "🌈*Attending: *" + attendees_string + "\n"
                                            "☔*Not Attending: *" + non_attendees_string,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text=  "📍*Title:* " + leisure_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n" +
                                           "⏳*Poll Deadline:* " + deadline,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

                                                                                          
def leisure_view_session_clicked_user(update, context):
    query = update.callback_query
    callback_data = query.data
    leisure_session = callback_data.partition('view_leisure_user')[2]
    details = context.user_data['leisure'][leisure_session]['details']
    date_with_esc = context.user_data['leisure'][leisure_session]['date']
    time_with_esc = context.user_data['leisure'][leisure_session]['time']
    location = context.user_data['leisure'][leisure_session]['location']
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                   text=  "📍*Title:* " + leisure_session + "\n" +
                                           "📜*Details:* " + details + "\n" +
                                           "📆*Date:* " + date_with_esc + "\n" +
                                           "⏰*Time:* " + time_with_esc + "\n" +
                                           "🏫*Location:* " + location + "\n" +
                                           "⏳*Poll Deadline:* " + deadline,
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)


def leisure_remove_activity(update, context):
    query = update.callback_query
    to_edit = True
    present = datetime.datetime.now()
    if 'leisure' in context.user_data:
        for header in context.user_data['leisure']:
            admin_user_id = context.user_data['leisure'][header]['admin']
            date = context.user_data['leisure'][header]['date']
            time = context.user_data['leisure'][header]['time']
            date_and_time = date + " " + time
            datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
            datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
            if present > datetime_object_local:
                if header not in context.bot_data[admin_user_id]['leisure']:
                    context.user_data['leisure'].pop(header)

        if len(context.user_data['leisure'])!= 0:
            to_edit = False

    if len(context.chat_data['leisure']) == 0 and to_edit:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="*Eh why you no leisure activity\!* 😔 Your social life aiyo",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                             message_id=query.message.message_id,
                             text="*Which one you want to remove?:* 🪓",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             reply_markup=leisure_remove_activity_keyboard(context))

        return LEISURE_REMOVE_SESSION_MENU

# group_work_remove_task_user_choice callback (CallbackQueryHandler)
def leisure_remove_activity_admin(update, context):
    query = update.callback_query
    callback_data = query.data
    user_id = str(query.from_user.id)
    current_title = callback_data.partition('remove_leisure_admin')[2]
    context.chat_data['leisure'].pop(current_title, None)
    if user_id in context.bot_data:
        if 'leisure' in context.bot_data[user_id]:
            context.bot_data[user_id]['leisure'].pop(current_title, None)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Okok I removed *" + current_title + "* from your leisure activities liao\. 🥴 Your poll for this activity will be closed too\.",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    
    
    return ConversationHandler.END

def leisure_remove_activity_user(update, context):
    query = update.callback_query
    callback_data = query.data
    current_title = callback_data.partition('remove_leisure_user')[2]
    context.user_data['leisure'].pop(current_title, None)
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                 text="Okok I removed *" + current_title + "* from your leisure activities liao\. 🥴",
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=None)
    
    
    return ConversationHandler.END
 



##TESTING
#def sendmypoll(update, context):
#    header = update.message.text.partition(' ')[2].partition(' ')[2]
#    context.bot.send_message(chat_id=update.effective_chat.id,
#                                 text="this is my poll name: " + header,
#                                 reply_markup=work_keyboard())
#    #actual thing can be to use the header to send the actual poll itself

# ------------------------------------HELP------------------------------------ #

def help(update, context):
    chat_type = update.message.chat.type

    if chat_type == 'private':
        context.chat_data['chat_type'] = 'private'

        update.message.reply_text(text=add_escape_to_string("Hello hello! You are a bit blur about what’s going on right? Nevermind, come, I explain to you!" + "\n\n"
                                                            "The first thing that you may be wondering is *“why would I ever use this bot leh?”* and this is why." + "\n\n" 
                                                            "You are a uni student and I want to believe you very hardworking 😏 but sometimes ah, there is way *too much work* and you damn shag, you honestly cannot even remember what and when your labs or projects are due! 😩" + "\n"
                                                            "It’s ok, I get it, that’s why I’m here! 😜"  + "\n\n"
                                                            "So ah, within a private chat with moi (this doYourWorkLah bot lah), there are 3 main sections: *Work*, *CCA* and *Leisure Activity*" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "There is a *Work* section that allows you to:" + "\n"
                                                            "📍 input the modules you are taking" + "\n"
                                                            "📍 create individual to-do lists for each module to consolidate tasks for each module" + "\n\n"
                                                            "Aiyo I know you can already do this in other note apps but I haven’t talk finish mah! Still got some more! Sometimes, things just slip out of your mind but you can trust me to remind you!" + "\n\n" 
                                                            "You can:" + "\n"
                                                            "📍 set reminders for your specific module to-do lists and for individual events or tasks." + "\n\n"
                                                            "If you want to know more about the specific functions of this *Work* section, click on the *Work* button below! 👇" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "There is a *CCA* section that allows you to:" + "\n"
                                                            "📍 create a CCA session with all of its details and send it to a group chat to collect attendance" + "\n"
                                                            "📍 allow attendees to have the option to set a reminder for the CCA session" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "There is a *Leisure Activity* section that allows you to:" + "\n"
                                                            "📍 create a leisure activity event with all of its details and send it to a group chat to collect attendance" + "\n"
                                                            "📍 allow attendees to have the option to set a reminder for the event" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "There is also a *Snooze* function. 😴 If you want to learn more about it ah, click on the *Snooze* button ok?" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "Ok lah, that’s all from me! 🥳 If you want to know more, just choose below ok?" + "\n\n" 
                                                            "Just remember, *YOU BETTER DO YOUR WORK AH!* 🤡"),
                                                            parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                                            reply_markup=help_keyboard(context))
  

    else:
        context.chat_data['chat_type'] = 'group'
 
        update.message.reply_text(text=add_escape_to_string("Hello hello! You are a bit blur about what’s going on right? Nevermind, come, I explain to you!" + "\n\n"
                                    "The first thing that you may be wondering is *“why would I ever use this bot leh?”* and this is why." + "\n\n" 
                                    "You added me into this group for a reason, you have group projects!" + "\n\n"
                                    "*Eh* and I’m not pointing fingers ah but *sOMeBodY* 😳 always seems to not know what they are supposed to do or isn’t very motivated to do it. 🤭 Or maybe your group just needs a place to organise all the tasks that need to be done." + "\n\n" 
                                    "So let me be the bad guy lah ok, I’ll do *all the nagging for you!* 🤬" + "\n\n"
                                    "*What this bot can do that existing reminder/calendar/note apps fail to do* is to allow for collaboration and I know that the first thing that any group does in NUS is to create a *Telegram group* lah huh so 🐤two birds in one stone leh! So just use it lah! 😉" + "\n\n"
                                    "So ah, within a group chat with moi (this doYourWorkLah bot lah), there is only 1 main section called *Work*." + "\n\n"
                                    "__________________________" + "\n\n"
                                    "The *Work* section that takes you into the *Group Work* section, which allows all members to:" + "\n\n"
                                    "📍 add tasks into a consolidated to-do list" + "\n"
                                    "📍 set reminders for the to-do list & for individual events" + "\n\n"
                                    "If you want to know more about the specific functions of this *Work* section, click on the *Work* button below! 👇" + "\n\n"
                                     "__________________________" + "\n\n"
                                    "There is also a *Snooze* function. 😴 If you want to learn more about it ah, click on the *Snooze* button ok?" + "\n\n"
                                    "Ok lah, that’s all from me! 🥳 If you still want to know more, *click* the buttons below!🤡"),
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              reply_markup=help_keyboard(context))
    return HELP_MENU

def help_return_menu(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text='*Which one do you want to know more about ah?* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_keyboard(context))
    
    return HELP_MENU

def help_snooze_return_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='*Which one do you want to know more about ah?* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_keyboard(context))
    
    return HELP_MENU

def help_snooze(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= add_escape_to_string("So let me tell you more about the *Snooze* function ah. 😴" + "\n\n"
                                    "Sometimes you suddenly get a reminder of something that you need to complete but you are in the *middle of something else* and you know that if you ignore the reminder, *you will confirm forget.* 🙃" + "\n\n"
                                    "So, the snooze function allows you to:" + "\n\n"
                                    "📍 snooze the reminder for 10min before reminding you again" + "\n"
                                    "📍 keep snoozing until you dismiss the reminder" + "\n\n"
                                     "__________________________" + "\n\n"
                                      "Okok I talk finish liao, faster go do your work! 🤧"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"Instructions_Snooze.jpg", 'rb'))
    chat_type = context.chat_data['chat_type']

    if chat_type == 'private':
        help_cca_and_leisure_return_menu(update, context)
    else:
        help_snooze_return_menu(update, context)

def help_group_work(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text='*Which one do you want to know more about ah?* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_group_work_keyboard())
    
    return HELP_GROUP_WORK_MENU

def help_group_work_return_menu(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='*What else do you want to know ah* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_group_work_keyboard())
    
    return HELP_GROUP_WORK_MENU


def help_group_work_to_do_list(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= add_escape_to_string("I’m gonna help your group get their shit together, here we go!🤜🤛" + "\n\n"
                                        "So ah, this is a section called *Work*. When you click it, it becomes *Group Work*. Then, you need to click it one more time and there will be damn a lot of things you can do. 🤩" + "\n\n" 
                                        "Okok I know you are getting a bit sian and you are thinking “wah why need to click so many times one” but stay with me ok? 🥺" + "\n\n"
                                        "__________________________" + "\n\n"
                                        "Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                        "After clicking *Group Work*, you will be able to go to the *To-Do List* section, where you can:" + "\n\n"
                                        "📍 *View to-do list* that can be edited by anyone in the group" + "\n"
                                        "       💡You can either *View entire to-do list* or just *View individual task*" + "\n\n"
                                        "📍 *Add new task* into the to-do list" + "\n"
                                        "       💡Fill up fields like *header, task details, deadline and task status*" + "\n\n"
                                        "📍 *Edit task* that you already have in the to-do list" + "\n\n"
                                        "📍 *Remove existing task* in the to-do list"  + "\n\n"
                                         "__________________________" + "\n\n"
                                        "Okok I talk finish liao, faster go do your work! 🤧"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"C:\Users\65968\Documents\murmuring-ocean-40072\Instructions_Group_Work_1.jpg", 'rb'))
    help_group_work_return_menu(update, context)


def help_group_work_reminders(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text= add_escape_to_string("I’m gonna help your group get their shit together, here we go!🤜🤛" + "\n\n"
                                        "So ah, this is a section called *Work*. When you click it, it becomes *Group Work*. Then, you need to click it one more time and there will be damn a lot of things you can do. 🤩" + "\n\n" 
                                        "Okok I know you are getting a bit sian and you are thinking “wah why need to click so many times one” but stay with me ok? 🥺" + "\n\n"
                                        "__________________________" + "\n\n"
                                        "Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                        "After clicking *Group Work*, there is also a *Reminders* section which allows you to:" + "\n\n"
                                        "📍 *View reminders* you have already set" + "\n\n"
                                        "📍 *Set a reminder*" + "\n"
                                        "       💡You can set a reminder either *For To-Do List* to be sent to the group chat at a customisable interval and timing or *For Individual Events*, like a meeting or a presentation" + "\n\n"
                                        "📍 *Remove a reminder*" + "\n\n"
                                        "So you can *make sure that* that person who *isn’t very motivated* to do his tasks is *bombarded* with the to-do list all the time *until he gets his part done!* 😏" + "\n\n"
                                        "__________________________" + "\n\n"
                                        "Okok I talk finish liao, faster go do your work! 🤧"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"C:\Users\65968\Documents\murmuring-ocean-40072\Instructions_Group_Work_2.jpg", 'rb'))
    help_group_work_return_menu(update, context)


def help_module(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=add_escape_to_string("Wah, not bad ah, you really want to be organised! Very good, I help you! 😘" + "\n\n"
                                                            "So ah, this is a section called *Work*. When you click it, it becomes *Module*. Then, you need to click it one more time and there will be damn a lot of things you can do. 🤩 " + "\n\n"
                                                            "Okok I know you are getting a bit sian and you are thinking “wah why need to click so many times one” but stay with me ok? 🥺" + "\n\n"
                                                            "After clicking *Module*, you will be able to *Add, Remove, View and Edit Modules*. Oh ya, you can also set *Reminders* in the *Reminders* section." + "\n\n"
                                                            "Very cool right? Sooo which one do you want to know more about ah?" + "\n" 
                                                            "Just choose one first ok 🤧"),
                                                            parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                                            reply_markup=help_module_keyboard())
    return HELP_MODULE_MENU


def help_module_return_menu(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='*What else do you want to know ah* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_module_keyboard())
    
    return HELP_MODULE_MENU

def help_module_view_and_edit_module(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=add_escape_to_string("Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                                            "After clicking *Module*, you will be able to *View and edit modules*, where you can:" + "\n"
                                                            "📍 view the list of modules you currently have" + "\n\n"
                                                            "You can then pick a specific module you want to look at and:" + "\n\n"
                                                            "📍 *View to-do list* for that specific module" + "\n"
                                                            "       💡You can either *View entire to-do list* of the module or just *View individual task*" + "\n\n"
                                                            "📍 *Add new task* into the module’s to-do list" + "\n"
                                                            "       💡Fill up fields like *header, task details, deadline and task status*" + "\n\n" 
                                                            "📍 *Edit task* that you already have in your module’s to-do list" + "\n\n"
                                                            "📍 *Remove existing task* in your module’s to-do list" + "\n\n"
                                                            "Clicking *Module* also allows you to:" + "\n"
                                                            "📍 *Add new module*" + "\n"
                                                            "📍 *Remove existing module*" + "\n"
                                                            "📍 Go into the *Reminders* section" + "\n\n"
                                                            "That way you confirm plus chop will remember all the tasks that you need to complete! 🤓" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "Okok I talk finish liao, faster go do your work! 🤧"),
                                                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
                                  
    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fimage&psig=AOvVaw1oKIXfwjJEf1Deit1i2-JS&ust=1595803888664000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIDb2P2-6eoCFQAAAAAdAAAAABAD", 'rb'))
    help_module_return_menu(update, context)

def help_module_reminders(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=add_escape_to_string("Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                                            "This *Reminders* section allows you to:" + "\n\n"
                                                            "📍 *View reminders* you have already set"  + "\n\n"
                                                            "📍 *Set a reminder*"  + "\n"
                                                            "       💡You can set a reminder either *For To-Do List* of a specific module to be sent to you at a customisable interval and timing or *For Individual Events*, like a meeting or a presentation"  + "\n\n"
                                                            "📍 *Remove a reminder*"  + "\n\n"
                                                            "That way you confirm plus chop will remember all the tasks that you need to complete! 🤓" + "\n\n"
                                                            "__________________________" + "\n\n"
                                                            "Okok I talk finish liao, faster go do your work! 🤧"),
                                                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"C:\Users\65968\Documents\murmuring-ocean-40072\Instructions_Module_2.jpg", 'rb'))
    help_module_return_menu(update, context)

def help_cca_and_leisure_return_menu(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='*What else do you want to know ah* 😩',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                  reply_markup=help_keyboard(context))
    

    return HELP_MENU

def help_cca(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=add_escape_to_string("Wah look at you being in charge of your CCA sessions! 😎" + "\n\n"
                                  "Sometimes ah, it’s just *so mafan* to try to layout all the details of the CCA session and collect the attendance of your CCA mates in a clean and concise way.😖" + "\n"
                                  "People just keep copy and pasting *the same message* so many times aiyo! So, i can help you with that 😉" + "\n\n"
                                  "Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                  "After clicking *CCA*, you will be able to *Add new CCA session* by:" + "\n\n"
                                  "📍 Filling in the *session title, details, date, time, location and poll cut-off date and time*"  + "\n\n"
                                  "📍 Sending poll to desired group chat to take attendance" + "\n" 
                                  "     💡Make sure I am also a member of that group chat 😘" + "\n"
                                  "     💡Group chat members will no longer be able to click on the poll after the poll cut-off date and time is over" + "\n" 
                                  "     💡Name of the attendees will not be visible here"  + "\n\n"
                                  "📍 Sending attendees a *private message* to set a reminder for the CCA session"  + "\n\n"
                                  "You can also:" + "\n"
                                  "📍* View CCA session* to see who is attending 😊 and who isn’t 🤨"  + "\n"
                                  "📍 *Remove CCA session* to remove past CCA sessions or remove a CCA session with incorrect information"  + "\n\n"
                                  "This process will no longer be a headache anymore! 🥳"),
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)

    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"C:\Users\65968\Documents\murmuring-ocean-40072\Instructions_CCA.jpg", 'rb'))
    help_cca_and_leisure_return_menu(update, context)                                

def help_leisure(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=add_escape_to_string("Okok you have studied enough liao, TIME TO PARTYY! 🤙 Or you just want to jio your friends to watch a movie also can lah." + "\n\n" 
                                  "*But there are always people who say they can come, then suddenly cannot come, then suddenly can come again and you really don’t know if the person is going to show up or not.* 😭" + "\n\n"
                                  "So this bot can allow your friend to just update their attendance when they want to *(before the poll cut-off date and time of course lah)* and you can have a *quick* glance of everyone who is going to be there! 🎉" + "\n\n"
                                  "Pssst we also send reminders to those friends who blur blur one and forget when you all hanging out🐙" + "\n\n"
                                  "Eh you see below got images right, so you can refer to the images below for clearer illustration if the words are making you even more blur." + "\n\n"
                                  "After clicking *Leisure Activity*, you will be able to *Add new leisure activity* by:" + "\n\n"
                                  "📍 Filling in the *activity title, details, date, time, location and poll cut-off date and time*" + "\n\n"
                                  "📍 Sending poll to desired group chat to take attendance" + "\n" 
                                  "     💡Make sure I am also a member of that group chat 😘" + "\n" 
                                  "     💡Group chat members will no longer be able to click on the poll after the poll cut-off date and time is over" + "\n" 
                                  "     💡Name of the attendees will be visible here" + "\n\n"
                                  "📍 Sending attendees a private message to set a reminder for the activity" + "\n\n"
                                  "📍 See the updated list of attendees in the group chat" + "\n\n"
                                  "You can also:" + "\n"
                                  "📍* View leisure activity* to see the details and attendance" + "\n"
                                  "📍 *Remove leisure activity* to remove past activities or remove an activity with incorrect information" + "\n\n"
                                  "Have fun! 🥳 *BUT MAKE SURE YOU STUDY FIRST AH* 🤡"),
                                   parse_mode=telegram.ParseMode.MARKDOWN_V2)

    context.bot.send_photo(chat_id=query.message.chat_id, photo=open(r"C:\Users\65968\Documents\murmuring-ocean-40072\Instructions_Leisure_Activity.jpg", 'rb'))
    help_cca_and_leisure_return_menu(update, context)

def resetall(update, context):
    context.chat_data.clear()
    update.message.reply_text(text="*All data has been cleared from the bot\!*",
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return ConversationHandler.END

def cancel(update, context):
    #user = update.message.from_user
    #logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('*Bye\!*',
                               parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return ConversationHandler.END

def help_done(update, context):
    query = update.callback_query
    
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text='*Bye\!*',
                                  parse_mode=telegram.ParseMode.MARKDOWN_V2)
    return ConversationHandler.END

#To log errors caused by Updates
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)




#################################### KEYBOARDS ####################################

# Associated callback: start & main
# Flow: Front
def front_keyboard(context):
    #header = "just a trial"
    if context.chat_data['chat_type'] == 'private':

        keyboard = [[InlineKeyboardButton('Work', callback_data='work!')],
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                [InlineKeyboardButton('CCA', callback_data='cca!')],
                [InlineKeyboardButton('Leisure Activity', callback_data='leisure!')]]
        return InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [[InlineKeyboardButton('Work', callback_data='work!')]]
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                #[InlineKeyboardButton('CCA', callback_data='cca!')],
                #[InlineKeyboardButton('Leisure Activity', callback_data='leisure!')]]
        return InlineKeyboardMarkup(keyboard)


# -------------------------------------------WORK------------------------------------------- #
# Associated callback: work
# Flow: Front > Work
def work_keyboard(context):
    if context.chat_data['chat_type'] == 'private':
        
        keyboard = [[InlineKeyboardButton('Module', callback_data='module!')],
                [InlineKeyboardButton('<< Back', callback_data='front!')]]
        return InlineKeyboardMarkup(keyboard)

    else:

        keyboard = [[InlineKeyboardButton('Group Work', callback_data='group_work!')],
                #[InlineKeyboardButton('Module', callback_data='module!')],
                [InlineKeyboardButton('<< Back', callback_data='front!')]]
        return InlineKeyboardMarkup(keyboard)

# -------------------------------------WORK > GROUP WORK------------------------------------- #
# Associated callback: group_work
# Flow: Front > Work > Group Work
def group_work_keyboard():
    keyboard = [[InlineKeyboardButton('To-Do List', callback_data='group_work_to_do_list!')],
                [InlineKeyboardButton('Reminders', callback_data='group_work_reminders!')],
                [InlineKeyboardButton('<< Back', callback_data='work!')]]
    return InlineKeyboardMarkup(keyboard)

# Associated callback: group_work_to_do_list
# Flow: Front > Work > Group Work > To-Do List
def group_work_to_do_list_keyboard():
    keyboard = [[InlineKeyboardButton('View to-do list', callback_data='view_to_do_list!')],
                [InlineKeyboardButton('Add new task', callback_data='group_work_add_task!')],
                [InlineKeyboardButton('Edit task', callback_data='group_work_edit_task!')],
                [InlineKeyboardButton('Remove existing task', callback_data='group_work_remove_task!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work!')]]
    return InlineKeyboardMarkup(keyboard)

def group_work_view_to_do_list_keyboard():
    keyboard = [[InlineKeyboardButton('View entire to-do list', callback_data='view_entire_to_do_list!')],
                [InlineKeyboardButton('View individual task', callback_data='view_individual_task!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work_to_do_list!')]]
    return InlineKeyboardMarkup(keyboard)

def group_work_view_individual_task_keyboard(context):
    keyboard = []
    for header in context.chat_data['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='user_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)


## Associated callback: group_work_add_task
# Flow: Front > Work > Group Work > To-Do List > Add new task
def group_work_add_task_keyboard():
    keyboard = [[InlineKeyboardButton('Add header', callback_data='group_work_to_do_add_header!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work_to_do_list!')]]
    return InlineKeyboardMarkup(keyboard)

# Associated callback: group_work_to_do_add_header_waiting_input, group_work_to_do_edit_task_details_waiting_input, group_work_to_do_edit_deadline_waiting_input
# Flow: Front > Work > Group Work > To-Do List > Add new task > Add header >
#       "Please input header" > User input
def group_work_to_do_edit_info_keyboard():
    keyboard = [[InlineKeyboardButton('Edit task details', callback_data='group_work_to_do_edit_task_details!'),
                 InlineKeyboardButton('Edit deadline', callback_data='group_work_to_do_edit_deadline!')],
                 
                [InlineKeyboardButton('Edit task status', callback_data='group_work_to_do_edit_task_status!'),
                 InlineKeyboardButton('Done', callback_data='group_work_to_do_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='group_work_to_do_list!')]]
    return InlineKeyboardMarkup(keyboard)

#NEW
def group_work_to_do_edit_task_status_keyboard():
    keyboard = [[InlineKeyboardButton("Paiseh haven't do yet 😅", callback_data="haven't do!")],
                [InlineKeyboardButton("Doing already 💪", callback_data="doing!")],
                [InlineKeyboardButton("Finish liao 😎", callback_data='finish!')]]
    return InlineKeyboardMarkup(keyboard)


# Associated callback: group_work_remove_task
# Flow: Front > Work > Group Work > To-Do List > Remove existing task
# Note: limit callback_data length to 50 characters (5 for prefix + 45 for header without escapes)
def group_work_remove_task_keyboard(context):
    keyboard = []
    for header in context.chat_data['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='user_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

## Associated callback: group_work_reminders
# Flow: Front > Work > Group Work > Reminders
def group_work_reminders_keyboard():
    keyboard = [[InlineKeyboardButton('View reminders', callback_data='group_work_view_reminders!')],
                [InlineKeyboardButton('Set a reminder', callback_data='group_work_set_reminder!')],
                [InlineKeyboardButton('Remove a reminder', callback_data='group_work_remove_reminder!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work!')]]
    return InlineKeyboardMarkup(keyboard)


## Associated callback: group_work_set_reminder
# Flow: Front > Work > Group Work > Reminders > Set a reminder
def group_work_set_reminder_keyboard():
    keyboard = [[InlineKeyboardButton('For To-Do List', callback_data='group_work_set_reminder_for_to_do_list!')],
                [InlineKeyboardButton('For Individual Events', callback_data='group_work_set_reminder_for_event!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work_reminders!')]]
    return InlineKeyboardMarkup(keyboard)

def group_work_set_reminder_for_to_do_list_edit_info_keyboard():
    keyboard = [[InlineKeyboardButton('Edit time', callback_data='group_work_set_reminder_for_to_do_list_time!'),
                 InlineKeyboardButton('Edit interval', callback_data='group_work_set_reminder_for_to_do_list_interval!')],
                 
                [InlineKeyboardButton('Done', callback_data='group_work_set_reminder_for_to_do_list_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='group_work_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)

## Associated callback: group_work_set_reminder_for_event
#  Flow: Front > Work > Group Work > Reminders > Set a reminder > For individual events
def group_work_add_event_keyboard():
    keyboard = [[InlineKeyboardButton('Add header', callback_data='group_work_set_reminder_for_event_add_header!')],
                [InlineKeyboardButton('<< Back', callback_data='group_work_reminders!')]]
    return InlineKeyboardMarkup(keyboard)

## Associated callback: group_work_set_reminder_for_event_clicked
# Flow: Front > Work > Group Work > Reminders > Set a reminder > For individual events > Add header
def group_work_set_reminder_for_event_details_keyboard():
    keyboard = [[InlineKeyboardButton('Edit date', callback_data='group_work_set_reminder_for_event_date!'),
                 InlineKeyboardButton('Edit time', callback_data='group_work_set_reminder_for_event_time!')],
                 
                [InlineKeyboardButton('Done', callback_data='group_work_set_reminder_for_event_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='group_work_reminders!')]]             
    return InlineKeyboardMarkup(keyboard)

def group_work_edit_task_keyboard(context):
    keyboard = []
    for header in context.chat_data['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='groupwork_edit_task_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

def group_work_snooze_reminder_keyboard(header):
    keyboard = [[InlineKeyboardButton('Snooze', callback_data='group_work_snooze_reminder_' + header)],
                [InlineKeyboardButton('Dismiss', callback_data='group_work_dismiss_reminder_' + header)]]
    return InlineKeyboardMarkup(keyboard)

## Associated callback: group_work_set_reminder_for_event_clicked
# Flow: Front > Work > Group Work > Reminders > Remove a reminder
def group_work_remove_reminder_keyboard(context):
    keyboard = []
    for header in context.chat_data['reminders']['work']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='work_reminder_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

# -------------------------------------WORK > MODULE------------------------------------- #
## Associated callback: module
# Flow: Front > Work > Module
def module_keyboard():
    keyboard = [[InlineKeyboardButton('View and edit modules', callback_data='module_view_modules!')],
                [InlineKeyboardButton('Add new module', callback_data='module_add_module!')],
                [InlineKeyboardButton('Remove existing module', callback_data='module_remove_module!')],
                [InlineKeyboardButton('Reminders', callback_data='module_reminders!')],
                [InlineKeyboardButton('<< Back', callback_data='work!')]]
    return InlineKeyboardMarkup(keyboard)

## Associated callback: module_view_modules
# Flow: Front > Work > Module > View all modules
def module_view_modules_keyboard(context):
    keyboard = []
    for module_name in context.chat_data['modules']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(module_name), callback_data='viewmod_' + remove_escape_from_string(module_name))])
    return InlineKeyboardMarkup(keyboard)

## Associated callback: module_to_do_list
# Flow: Front > Work > Module > View all modules > arbitrary module name
def module_to_do_list_keyboard():
    keyboard = [[InlineKeyboardButton('View to-do list', callback_data='module_to_do_view_to_do_list!')],
                [InlineKeyboardButton('Add new task', callback_data='module_to_do_add_task!')],
                [InlineKeyboardButton('Edit task', callback_data='module_to_do_edit_task!')],
                [InlineKeyboardButton('Remove existing task', callback_data='module_to_do_remove_task!')],
                [InlineKeyboardButton('<< Back', callback_data='module_view_modules!')]]
    return InlineKeyboardMarkup(keyboard)

def module_to_do_view_to_do_list_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = [[InlineKeyboardButton('View entire to-do list', callback_data='module_to_do_view_entire_to_do_list!')],
                [InlineKeyboardButton('View individual task', callback_data='module_to_do_view_individual_task!')],
                [InlineKeyboardButton('<< Back', callback_data='viewmod_' + remove_escape_from_string(module_name))]]
    return InlineKeyboardMarkup(keyboard)

def module_to_do_view_individual_task_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = []
    for header in context.chat_data['modules'][module_name]['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='user_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

## Associated callback: module_to_do_list
# Flow: Front > Work > Module > View all modules > arbitrary module name > Add new task
def module_add_task_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = [[InlineKeyboardButton('Add header', callback_data='module_to_do_add_header!')],
                [InlineKeyboardButton('<< Back', callback_data='viewmod_' + remove_escape_from_string(module_name))]]
    return InlineKeyboardMarkup(keyboard)

def module_to_do_edit_info_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = [[InlineKeyboardButton('Edit task details', callback_data='module_to_do_edit_task_details!'),
                 InlineKeyboardButton('Edit deadline', callback_data='module_to_do_edit_deadline!')],
                 
                [InlineKeyboardButton('Edit task status', callback_data='module_to_do_edit_task_status!'),
                 InlineKeyboardButton('Done', callback_data='module_to_do_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='viewmod_' + remove_escape_from_string(module_name))]]
    return InlineKeyboardMarkup(keyboard)

def module_to_do_edit_task_status_keyboard():
    keyboard = [[InlineKeyboardButton("Paiseh haven't do yet 😅", callback_data="haven't do!")],
                [InlineKeyboardButton("Doing already 💪", callback_data="doing!")],
                [InlineKeyboardButton("Finish liao 😎", callback_data='finish!')]]
    return InlineKeyboardMarkup(keyboard)

def module_edit_task_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = []
    for header in context.chat_data['modules'][module_name]['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='module_edit_task_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

def module_remove_task_keyboard(context):
    module_name = context.chat_data['current module']
    keyboard = []
    for header in context.chat_data['modules'][module_name]['to-do list']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='removetask_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

def module_remove_module_keyboard(context):
    keyboard = []
    for header in context.chat_data['modules']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='removemod_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)



def module_reminders_keyboard():
    keyboard = [[InlineKeyboardButton('View reminders', callback_data='module_view_reminders!')],
                [InlineKeyboardButton('Set a reminder', callback_data='module_set_reminder!')],
                [InlineKeyboardButton('Remove a reminder', callback_data='module_remove_reminder!')],
                [InlineKeyboardButton('<< Back', callback_data='module!')]]
    return InlineKeyboardMarkup(keyboard)


def module_set_reminder_keyboard():
    keyboard = [[InlineKeyboardButton('For To-Do List', callback_data='module_set_reminder_for_to_do_list!')],
                [InlineKeyboardButton('For Individual Events', callback_data='module_set_reminder_for_event!')],
                [InlineKeyboardButton('<< Back', callback_data='module_reminders!')]]
    return InlineKeyboardMarkup(keyboard)

def module_set_reminder_for_to_do_list_choose_module_keyboard(context):
    keyboard = []
    for header in context.chat_data['modules']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='user_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)

def module_set_reminder_for_to_do_list_edit_info_keyboard():
    keyboard = [[InlineKeyboardButton('Edit time', callback_data='module_set_reminder_for_to_do_list_time!'),
                 InlineKeyboardButton('Edit interval', callback_data='module_set_reminder_for_to_do_list_interval!')],
                 
                [InlineKeyboardButton('Done', callback_data='module_set_reminder_for_to_do_list_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='module_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)


def module_add_event_keyboard():
    keyboard = [[InlineKeyboardButton('Add header', callback_data='module_set_reminder_for_event_add_header!')],
                [InlineKeyboardButton('<< Back', callback_data='module_reminders!')]]
    return InlineKeyboardMarkup(keyboard)


def module_set_reminder_for_event_details_keyboard():
    keyboard = [[InlineKeyboardButton('Edit date', callback_data='module_set_reminder_for_event_date!'),
                 InlineKeyboardButton('Edit time', callback_data='module_set_reminder_for_event_time!')],
                 
                [InlineKeyboardButton('Done', callback_data='module_set_reminder_for_event_done!')],
                 
                [InlineKeyboardButton('<< Back', callback_data='module_reminders!')]]             
    return InlineKeyboardMarkup(keyboard)

def module_snooze_reminder_keyboard(header):
    keyboard = [[InlineKeyboardButton('Snooze', callback_data='module_snooze_reminder_' + header)],
                [InlineKeyboardButton('Dismiss', callback_data='module_dismiss_reminder_' + header)]]
    return InlineKeyboardMarkup(keyboard)

def module_remove_reminder_keyboard(context):
    keyboard = []
    for header in context.chat_data['reminders']['module']:
        keyboard.append([InlineKeyboardButton(remove_escape_from_string(header), callback_data='module_reminder_' + remove_escape_from_string(header))])
    return InlineKeyboardMarkup(keyboard)


# -------------------------------------CCA------------------------------------- #
def cca_keyboard():
    keyboard = [[InlineKeyboardButton('Add new CCA session', callback_data='cca_add_session!')],
                [InlineKeyboardButton('View CCA session', callback_data='cca_view_session!')],
                [InlineKeyboardButton('Remove CCA session', callback_data='cca_remove_session!')],
                [InlineKeyboardButton('<< Back', callback_data='front!')]]
    return InlineKeyboardMarkup(keyboard)

def cca_add_session_keyboard():
    keyboard = [[InlineKeyboardButton('Edit session title', callback_data='cca_add_session_title!'), 
                InlineKeyboardButton('Edit session details', callback_data='cca_add_session_details!')],
                 [InlineKeyboardButton('Edit date', callback_data='cca_add_session_date!'),
                 InlineKeyboardButton('Edit time', callback_data='cca_add_session_time!')],
                 [InlineKeyboardButton('Edit location', callback_data='cca_add_session_location!'),
                 InlineKeyboardButton('Edit poll cut-off time and date', callback_data='cca_add_session_deadline!')],
                 [InlineKeyboardButton('Done', callback_data='cca_add_session_done!'),     
                InlineKeyboardButton('<< Back', callback_data='cca!')]]
    return InlineKeyboardMarkup(keyboard)

def cca_add_session_done_keyboard(text):
    keyboard = [[InlineKeyboardButton('Please choose a chat to send the poll to', switch_inline_query='/sendCCApoll' + "\n" + text)]]
    return InlineKeyboardMarkup(keyboard)

def cca_poll_keyboard(total_num):
    attending_num = total_num.partition(" ")[0]
    not_attending_num = total_num.partition(" ")[2]
    keyboard = [[InlineKeyboardButton('Attending: ' + attending_num , callback_data='attending_cca')],
                [InlineKeyboardButton('Not Attending: ' + not_attending_num, callback_data='not_attending_cca!')]]
    return InlineKeyboardMarkup(keyboard)

def cca_user_set_reminder_keyboard():
    keyboard =  [[InlineKeyboardButton('Edit date and time for reminder', callback_data='cca_user_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)

def cca_user_set_reminder_done_keyboard():
    keyboard =  [[InlineKeyboardButton('Confirm', callback_data='cca_user_set_reminder_confirm!')],
                [InlineKeyboardButton('<< Back', callback_data='cca_user_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)

def cca_snooze_reminder_keyboard(header):
    keyboard = [[InlineKeyboardButton('Snooze', callback_data='cca_snooze_reminder_' + header)],
                [InlineKeyboardButton('Dismiss', callback_data='cca_dismiss_reminder_' + header)]]
    return InlineKeyboardMarkup(keyboard)

def cca_view_sessions_keyboard(context):
    keyboard = []
    present = datetime.datetime.now()
    for header in context.chat_data['cca']:
        keyboard.append([InlineKeyboardButton(header, callback_data='view_cca_admin' + header)])
    if 'cca' in context.user_data:
        for header in context.user_data['cca']:
            admin_user_id = context.user_data['cca'][header]['admin']
            date = context.user_data['cca'][header]['date']
            time = context.user_data['cca'][header]['time']
            date_and_time = date + " " + time
            datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
            datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
            if present < datetime_object_local:
                if header in context.bot_data[admin_user_id]['cca']:
                    keyboard.append([InlineKeyboardButton(header, callback_data='view_cca_user' + header)])
            else:
                context.user_data['cca'].pop(header)

    return InlineKeyboardMarkup(keyboard)

def cca_remove_session_keyboard(context):
    keyboard = []
    for header in context.chat_data['cca']:
        keyboard.append([InlineKeyboardButton(header, callback_data='remove_cca_admin' + header)])
   
    for header in context.user_data['cca']:
        keyboard.append([InlineKeyboardButton(header, callback_data='remove_cca_user' + header)])
    
    keyboard.append([InlineKeyboardButton('<< Back', callback_data='cca!')])
    return InlineKeyboardMarkup(keyboard)




# -------------------------------------LEISURE ACTIVITY------------------------------------- #
def leisure_keyboard():
    keyboard = [[InlineKeyboardButton('Add new leisure activity', callback_data='leisure_add_session!')],
                [InlineKeyboardButton('View leisure activity', callback_data='leisure_view_session!')],
                [InlineKeyboardButton('Remove leisure activity', callback_data='leisure_remove_session!')],
                [InlineKeyboardButton('<< Back', callback_data='front!')]]
    return InlineKeyboardMarkup(keyboard)

def leisure_add_session_keyboard():
    keyboard = [[InlineKeyboardButton('Edit activity title', callback_data='leisure_add_session_title!'),
                 InlineKeyboardButton('Edit activity details', callback_data='leisure_add_session_details!')],
                 [InlineKeyboardButton('Edit date', callback_data='leisure_add_session_date!'),
                 InlineKeyboardButton('Edit time', callback_data='leisure_add_session_time!')],
                 [InlineKeyboardButton('Edit location', callback_data='leisure_add_session_location!'),
                 InlineKeyboardButton('Edit poll cut-off time and date', callback_data='leisure_add_session_deadline!')],
                 [InlineKeyboardButton('Done', callback_data='leisure_add_session_done!'),     
                InlineKeyboardButton('<< Back', callback_data='leisure!')]]
    return InlineKeyboardMarkup(keyboard)

def leisure_add_session_done_keyboard(text):
    keyboard = [[InlineKeyboardButton('Please choose a chat to send the poll to', switch_inline_query='/sendLeisurepoll' + "\n" + text)]]
    return InlineKeyboardMarkup(keyboard)

def leisure_poll_keyboard(total_num):
    attending_num = total_num.partition(" ")[0]
    not_attending_num = total_num.partition(" ")[2]
    keyboard = [[InlineKeyboardButton('Attending: ' + attending_num , callback_data='attending_leisure')],
                [InlineKeyboardButton('Not Attending: ' + not_attending_num, callback_data='not_attending_leisure!')]]
    return InlineKeyboardMarkup(keyboard)

def leisure_user_set_reminder_keyboard():
    keyboard =  [[InlineKeyboardButton('Edit date and time for reminder', callback_data='leisure_user_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)

def leisure_user_set_reminder_done_keyboard():
    keyboard =  [[InlineKeyboardButton('Confirm', callback_data='leisure_user_set_reminder_confirm!')],
                [InlineKeyboardButton('<< Back', callback_data='leisure_user_set_reminder!')]]
    return InlineKeyboardMarkup(keyboard)

def leisure_snooze_reminder_keyboard(header):
    keyboard = [[InlineKeyboardButton('Snooze', callback_data='leisure_snooze_reminder_' + header)],
                [InlineKeyboardButton('Dismiss', callback_data='leisure_dismiss_reminder_' + header)]]
    return InlineKeyboardMarkup(keyboard)

def leisure_view_session_keyboard(context):
    keyboard = []
    present = datetime.datetime.now()
    for header in context.chat_data['leisure']:
        keyboard.append([InlineKeyboardButton(header, callback_data='view_leisure_admin' + header)])
    if 'leisure' in context.user_data:
        for header in context.user_data['leisure']:
            admin_user_id = context.user_data['leisure'][header]['admin']
            date = context.user_data['leisure'][header]['date']
            time = context.user_data['leisure'][header]['time']
            date_and_time = date + " " + time
            datetime_object_local = datetime.datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')
            datetime_object_uct = datetime_object_local - datetime.timedelta(hours = 8)
            if present < datetime_object_local:
                if header in context.bot_data[admin_user_id]['leisure']:
                    keyboard.append([InlineKeyboardButton(header, callback_data='view_leisure_user' + header)])
            else:
                context.user_data['leisure'].pop(header)
    return InlineKeyboardMarkup(keyboard)

def leisure_remove_activity_keyboard(context):
    keyboard = []
    present = datetime.datetime.now()
    for header in context.chat_data['leisure']:
        keyboard.append([InlineKeyboardButton(header, callback_data='remove_leisure_admin' + header)])
    
    for header in context.user_data['leisure']:
        keyboard.append([InlineKeyboardButton(header, callback_data='remove_leisure_user' + header)])
            
    keyboard.append([InlineKeyboardButton('<< Back', callback_data='leisure!')])
    return InlineKeyboardMarkup(keyboard)

# -------------------------------------HELP------------------------------------- #
'''
def help_keyboard(context):
    if context.chat_data['chat_type'] == 'private':

        keyboard = [[InlineKeyboardButton('Work', callback_data='help_work_module!')],
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                [InlineKeyboardButton('CCA', callback_data='help_cca!')],
                [InlineKeyboardButton('Leisure Activity', callback_data='help_leisure!')],
                [InlineKeyboardButton('Snooze Feature', callback_data='help_snooze!')]]
        return InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [[InlineKeyboardButton('Work', callback_data='help_work_group_work!')],
                    [InlineKeyboardButton('Snooze Feature', callback_data='help_snooze!')]]
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                #[InlineKeyboardButton('CCA', callback_data='cca!')],
                #[InlineKeyboardButton('Leisure Activity', callback_data='leisure!')]]
        return InlineKeyboardMarkup(keyboard)
'''

def help_keyboard(context):
    if context.chat_data['chat_type'] == 'private':

        keyboard = [[InlineKeyboardButton('Work', callback_data='help_module!')],
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                [InlineKeyboardButton('CCA', callback_data='help_cca!')],
                [InlineKeyboardButton('Leisure Activity', callback_data='help_leisure!')],
                [InlineKeyboardButton('Snooze Feature', callback_data='help_snooze!')],
                [InlineKeyboardButton('Done',callback_data='help_done!')]]
        return InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [[InlineKeyboardButton('Work', callback_data='help_group_work!')],
                    [InlineKeyboardButton('Snooze', callback_data='help_snooze!')],
                    [InlineKeyboardButton('Done',callback_data='help_done!')]]
                    #[InlineKeyboardButton('Snooze Feature', callback_data='help_snooze!')]]
                 #[InlineKeyboardButton('CCA', switch_inline_query='/sendmypoll ' + header)], ##TESTING
                #[InlineKeyboardButton('CCA', callback_data='cca!')],
                #[InlineKeyboardButton('Leisure Activity', callback_data='leisure!')]]
        return InlineKeyboardMarkup(keyboard)

def help_group_work_keyboard():
        keyboard = [[InlineKeyboardButton('To-do list', callback_data='help_group_work_to_do_list!')],
                    [InlineKeyboardButton('Reminders', callback_data='help_group_work_reminders!')],
                    [InlineKeyboardButton('Back', callback_data='help!')],
                    [InlineKeyboardButton('Done',callback_data='help_done!')]]
          
  
        return InlineKeyboardMarkup(keyboard)

def help_module_keyboard():
        keyboard = [[InlineKeyboardButton('View and Edit modules', callback_data='help_module_view_and_edit_module!')],
                    [InlineKeyboardButton('Reminders', callback_data='help_module_reminders!')],
                    [InlineKeyboardButton('Back', callback_data='help!')],
                    [InlineKeyboardButton('Done',callback_data='help_done!')]]
          
  
        return InlineKeyboardMarkup(keyboard)
################################### MAIN ###################################

def main():

    #user_persistence = PicklePersistence(filename ='user_file')

    updater = Updater(token='1190868363:AAHWra_a4JteryuJBFNhZyAk-lKlMxY3udo',
                      #persistence=user_persistence,
                      use_context=True)

    
    convo_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            #name_of_menu: [all the buttons on the menu], what you return should be what matches with the keyboard
            FRONT_MENU: [CallbackQueryHandler(work, pattern='work!'),
                         CallbackQueryHandler(cca, pattern='cca!'),
                         CallbackQueryHandler(leisure, pattern='leisure!')
                         ],
            WORK_MENU: [CallbackQueryHandler(group_work, pattern='group_work!'),
                        CallbackQueryHandler(module, pattern='module!'),
                        CallbackQueryHandler(front, pattern='front!')],
            GROUP_WORK_MENU: [CallbackQueryHandler(group_work_to_do_list, pattern='group_work_to_do_list!'),
                              CallbackQueryHandler(group_work_reminders, pattern='group_work_reminders!'),
                              CallbackQueryHandler(work, pattern='work!')],
            GROUP_WORK_TO_DO_LIST_MENU: [CallbackQueryHandler(view_to_do_list, pattern='view_to_do_list!'),
                                         CallbackQueryHandler(group_work_add_task, pattern='group_work_add_task!'),
                                         CallbackQueryHandler(group_work_edit_task, pattern='group_work_edit_task!'),
                                         CallbackQueryHandler(group_work_remove_task, pattern='group_work_remove_task!'),
                                         CallbackQueryHandler(group_work, pattern='group_work!')],
            GROUP_WORK_VIEW_TO_DO_LIST_MENU: [CallbackQueryHandler(view_entire_to_do_list, pattern='view_entire_to_do_list!'),
                                              CallbackQueryHandler(view_individual_task, pattern='view_individual_task!'),
                                              CallbackQueryHandler(group_work_to_do_list, pattern='group_work_to_do_list!')],
            GROUP_WORK_VIEW_INDIVIDUAL_TASK_MENU: [CallbackQueryHandler(group_work_view_individual_task_user_choice, pattern='user_')],
            GROUP_WORK_TO_DO_ADD_TASK_MENU:[CallbackQueryHandler(group_work_to_do_add_header, pattern='group_work_to_do_add_header!'),
                                            CallbackQueryHandler(group_work_to_do_list, pattern='group_work_to_do_list!')],
            GROUP_WORK_TO_DO_ADD_HEADER_WAITING_INPUT: [MessageHandler(Filters.text, group_work_to_do_add_header_waiting_input)],
            #NEW
            GROUP_WORK_TO_DO_EDIT_INFO_MENU: [CallbackQueryHandler(group_work_to_do_edit_task_details, pattern='group_work_to_do_edit_task_details!'),
                                              CallbackQueryHandler(group_work_to_do_edit_deadline, pattern='group_work_to_do_edit_deadline!'),
                                              CallbackQueryHandler(group_work_to_do_edit_task_status, pattern='group_work_to_do_edit_task_status!'),
                                              CallbackQueryHandler(group_work_to_do_done, pattern='group_work_to_do_done!'),
                                              CallbackQueryHandler(group_work_to_do_list, pattern='group_work_to_do_list!')],
            GROUP_WORK_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT: [MessageHandler(Filters.text, group_work_to_do_edit_task_details_waiting_input)],
            GROUP_WORK_TO_DO_EDIT_DEADLINE_WAITING_INPUT: [MessageHandler(Filters.text, group_work_to_do_edit_deadline_waiting_input)],
            #NEW
            GROUP_WORK_TO_DO_EDIT_TASK_STATUS_MENU: [CallbackQueryHandler(group_work_to_do_edit_task_status_user_choice, pattern="haven't do!"),
                                                     CallbackQueryHandler(group_work_to_do_edit_task_status_user_choice, pattern="doing!"),
                                                     CallbackQueryHandler(group_work_to_do_edit_task_status_user_choice, pattern="finish!")],
            GROUP_WORK_REMOVE_TASK_MENU: [CallbackQueryHandler(group_work_remove_task_user_choice, pattern='user_')],
            GROUP_WORK_REMINDERS_MENU: [CallbackQueryHandler(group_work_view_reminders, pattern='group_work_view_reminders!'),
                                              CallbackQueryHandler(group_work_set_reminder, pattern='group_work_set_reminder!'),
                                              CallbackQueryHandler(group_work_remove_reminder, pattern='group_work_remove_reminder!'),
                                              CallbackQueryHandler(group_work, pattern='group_work!')],
            GROUP_WORK_SET_REMINDER_MENU: [CallbackQueryHandler(group_work_set_reminder_for_to_do_list, pattern='group_work_set_reminder_for_to_do_list!'),
                                            CallbackQueryHandler(group_work_set_reminder_for_event, pattern='group_work_set_reminder_for_event!'),
                                            CallbackQueryHandler(group_work_reminders, pattern='group_work_reminders!')],
            GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_CLICKED: [CallbackQueryHandler(group_work_set_reminder_for_to_do_list_edit_time, pattern='group_work_set_reminder_for_to_do_list_time!'),
                                                             CallbackQueryHandler(group_work_set_reminder_for_to_do_list_edit_interval, pattern='group_work_set_reminder_for_to_do_list_interval!'),
                                                             CallbackQueryHandler(group_work_set_reminder_for_to_do_list_done, pattern='group_work_set_reminder_for_to_do_list_done!'),
                                                             CallbackQueryHandler(group_work_set_reminder, pattern='group_work_set_reminder!')],
            GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT: [MessageHandler(Filters.text, group_work_set_reminder_for_to_do_list_edit_time_waiting_input)],
            GROUP_WORK_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT:[MessageHandler(Filters.text, group_work_set_reminder_for_to_do_list_edit_interval_waiting_input)],
            GROUP_WORK_REMINDER_ADD_EVENT_MENU:[CallbackQueryHandler(group_work_set_reminder_for_event_add_header, pattern='group_work_set_reminder_for_event_add_header!')],
            GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT: [MessageHandler(Filters.text, group_work_set_reminder_for_event_add_header_waiting_input)],
            GROUP_WORK_SET_REMINDER_FOR_EVENT_DETAILS_MENU: [CallbackQueryHandler(group_work_set_reminder_for_event_date, pattern='group_work_set_reminder_for_event_date!'),
                                                      CallbackQueryHandler(group_work_set_reminder_for_event_time, pattern='group_work_set_reminder_for_event_time!'),
                                                      CallbackQueryHandler(group_work_set_reminder_for_event_done, pattern='group_work_set_reminder_for_event_done!'),
                                                      CallbackQueryHandler(group_work_reminders, pattern='group_work_reminders!')],
            GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT: [MessageHandler(Filters.text, group_work_set_reminder_for_event_add_date_waiting_input)],
            GROUP_WORK_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT: [MessageHandler(Filters.text, group_work_set_reminder_for_event_add_time_waiting_input)],
            GROUP_WORK_EDIT_TASK: [CallbackQueryHandler(group_work_edit_task_user_choice, pattern='groupwork_edit_task_')],
            GROUP_WORK_REMOVE_REMINDER_MENU: [CallbackQueryHandler(group_work_remove_reminder_user_choice, pattern='reminder_')],
            MODULE_MENU: [CallbackQueryHandler(module_view_modules, pattern='module_view_modules!'),
                          CallbackQueryHandler(module_add_module, pattern='module_add_module!'),
                          CallbackQueryHandler(module_remove_module, pattern='module_remove_module!'),
                          CallbackQueryHandler(module_reminders, pattern='module_reminders!'),
                          CallbackQueryHandler(work, pattern='work!')],
            MODULE_VIEW_MODULES_MENU: [CallbackQueryHandler(module_view_modules_user_choice, pattern='viewmod_')],
            MODULE_TO_DO_LIST_MENU: [CallbackQueryHandler(module_to_do_view_to_do_list, pattern='module_to_do_view_to_do_list!'),
                                     CallbackQueryHandler(module_to_do_add_task, pattern='module_to_do_add_task!'),
                                     CallbackQueryHandler(module_edit_task, pattern='module_to_do_edit_task!'),
                                     CallbackQueryHandler(module_to_do_remove_task, pattern='module_to_do_remove_task!'),
                                     CallbackQueryHandler(module_view_modules, pattern='module_view_modules!')],
            MODULE_TO_DO_VIEW_TO_DO_LIST_MENU: [CallbackQueryHandler(module_to_do_view_entire_to_do_list, pattern='module_to_do_view_entire_to_do_list'),
                                                CallbackQueryHandler(module_to_do_view_individual_task, pattern='module_to_do_view_individual_task!'),
                                                CallbackQueryHandler(module_view_modules_user_choice, pattern='viewmod_')],
            MODULE_TO_DO_VIEW_INDIVIDUAL_TASK_MENU: [CallbackQueryHandler(module_to_do_view_individual_task_user_choice, pattern='user_')],
            MODULE_TO_DO_ADD_TASK_MENU: [CallbackQueryHandler(module_to_do_add_header, pattern='module_to_do_add_header!'),
                                         CallbackQueryHandler(module_view_modules_user_choice, pattern='viewmod_')],
            MODULE_TO_DO_ADD_HEADER_WAITING_INPUT: [MessageHandler(Filters.text, module_to_do_add_header_waiting_input)],
            #NEW
            MODULE_TO_DO_EDIT_INFO_MENU: [CallbackQueryHandler(module_to_do_edit_task_details, pattern='module_to_do_edit_task_details!'),
                                          CallbackQueryHandler(module_to_do_edit_deadline, pattern='module_to_do_edit_deadline!'),
                                          CallbackQueryHandler(module_to_do_edit_task_status, pattern='module_to_do_edit_task_status!'),
                                          CallbackQueryHandler(module_to_do_done, pattern='module_to_do_done!'),
                                          CallbackQueryHandler(module_view_modules_user_choice, pattern='viewmod_')],
            MODULE_TO_DO_EDIT_TASK_DETAILS_WAITING_INPUT: [MessageHandler(Filters.text, module_to_do_edit_task_details_waiting_input)],
            MODULE_TO_DO_EDIT_DEADLINE_WAITING_INPUT: [MessageHandler(Filters.text, module_to_do_edit_deadline_waiting_input)],
            #NEW
            MODULE_TO_DO_EDIT_TASK_STATUS_MENU: [CallbackQueryHandler(module_to_do_edit_task_status_user_choice, pattern="haven't do!"),
                                                 CallbackQueryHandler(module_to_do_edit_task_status_user_choice, pattern="doing!"),
                                                 CallbackQueryHandler(module_to_do_edit_task_status_user_choice, pattern="finish!")],
            MODULE_REMOVE_TASK_MENU: [CallbackQueryHandler(module_to_do_remove_task_user_choice, pattern='removetask_')],
            MODULE_ADD_MODULE_WAITING_INPUT: [MessageHandler(Filters.text, module_add_module_waiting_input)],
            MODULE_EDIT_TASK: [CallbackQueryHandler(module_edit_task_user_choice, pattern='module_edit_task_')],
            MODULE_REMOVE_MODULE_MENU: [CallbackQueryHandler(module_remove_module_user_choice, pattern='removemod_')],
            MODULE_REMINDERS_MENU: [CallbackQueryHandler(module_view_reminders, pattern='module_view_reminders!'),
                                    CallbackQueryHandler(module_set_reminder, pattern='module_set_reminder!'),
                                    CallbackQueryHandler(module_remove_reminder, pattern='module_remove_reminder!'),
                                    CallbackQueryHandler(module, pattern='module!')],
            MODULE_SET_REMINDER_MENU: [CallbackQueryHandler(module_set_reminder_for_to_do_list, pattern='module_set_reminder_for_to_do_list!'),
                                       CallbackQueryHandler(module_set_reminder_for_event, pattern='module_set_reminder_for_event!'),
                                       CallbackQueryHandler(module_reminders, pattern='module_reminders!')],
            MODULE_SET_REMINDER_FOR_TO_DO_LIST_CHOOSE_MODULE: [CallbackQueryHandler(module_set_reminder_for_to_do_list_user_choice, pattern='user_')],
            MODULE_SET_REMINDER_FOR_TO_DO_LIST_CLICKED: [CallbackQueryHandler(module_set_reminder_for_to_do_list_edit_time, pattern='module_set_reminder_for_to_do_list_time!'),
                                                         CallbackQueryHandler(module_set_reminder_for_to_do_list_edit_interval, pattern='module_set_reminder_for_to_do_list_interval!'),
                                                         CallbackQueryHandler(module_set_reminder_for_to_do_list_done, pattern='module_set_reminder_for_to_do_list_done!'),
                                                         CallbackQueryHandler(module_set_reminder, pattern='module_set_reminder!')],
            MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_TIME_WAITING_INPUT: [MessageHandler(Filters.text, module_set_reminder_for_to_do_list_edit_time_waiting_input)],
            MODULE_SET_REMINDER_FOR_TO_DO_LIST_EDIT_INTERVAL_WAITING_INPUT:[MessageHandler(Filters.text, module_set_reminder_for_to_do_list_edit_interval_waiting_input)],
            MODULE_REMINDER_ADD_EVENT_MENU:[CallbackQueryHandler(module_set_reminder_for_event_add_header, pattern='module_set_reminder_for_event_add_header!')],
            MODULE_SET_REMINDER_FOR_EVENT_ADD_HEADER_WAITING_INPUT: [MessageHandler(Filters.text, module_set_reminder_for_event_add_header_waiting_input)],
            MODULE_SET_REMINDER_FOR_EVENT_DETAILS_MENU: [CallbackQueryHandler(module_set_reminder_for_event_date, pattern='module_set_reminder_for_event_date!'),
                                                      CallbackQueryHandler(module_set_reminder_for_event_time, pattern='module_set_reminder_for_event_time!'),
                                                      CallbackQueryHandler(module_set_reminder_for_event_done, pattern='module_set_reminder_for_event_done!'),
                                                      CallbackQueryHandler(module_reminders, pattern='module_reminders!')],
            MODULE_SET_REMINDER_FOR_EVENT_ADD_DATE_WAITING_INPUT: [MessageHandler(Filters.text, module_set_reminder_for_event_add_date_waiting_input)],
            MODULE_SET_REMINDER_FOR_EVENT_ADD_TIME_WAITING_INPUT: [MessageHandler(Filters.text, module_set_reminder_for_event_add_time_waiting_input)],
            MODULE_REMOVE_REMINDER_MENU: [CallbackQueryHandler(module_remove_reminder_user_choice, pattern='reminder_')],
            CCA_MENU: [CallbackQueryHandler(cca_add_session, pattern='cca_add_session!'),
                        CallbackQueryHandler(cca_view_sessions, pattern='cca_view_session!'),
                        CallbackQueryHandler(cca_remove_session, pattern='cca_remove_session!'),
                        CallbackQueryHandler(front, pattern='front!')],
            CCA_ADD_SESSION_MENU: [CallbackQueryHandler(cca_add_session_title, pattern='cca_add_session_title!'),
                                    CallbackQueryHandler(cca_add_session_details, pattern='cca_add_session_details!'),
                                    CallbackQueryHandler(cca_add_session_date, pattern='cca_add_session_date!'),
                                    CallbackQueryHandler(cca_add_session_time, pattern='cca_add_session_time!'),
                                    CallbackQueryHandler(cca_add_session_location, pattern='cca_add_session_location!'),
                                    CallbackQueryHandler(cca_add_session_deadline, pattern='cca_add_session_deadline!'),
                                    CallbackQueryHandler(cca_add_session_done, pattern='cca_add_session_done!'),
                                    CallbackQueryHandler(cca, pattern='cca!')],
            CCA_ADD_SESSION_TITLE_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_title_waiting_input)],
            CCA_ADD_SESSION_DETAILS_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_details_waiting_input)],
            CCA_ADD_SESSION_DATE_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_date_waiting_input)],
            CCA_ADD_SESSION_TIME_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_time_waiting_input)],
            CCA_ADD_SESSION_LOCATION_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_location_waiting_input)],
            CCA_ADD_SESSION_DEADLINE_WAITING_INPUT: [MessageHandler(Filters.text, cca_add_session_deadline_waiting_input)],
            CCA_VIEW_SESSIONS: [CallbackQueryHandler(cca_view_session_clicked_admin, pattern='view_cca_admin'),
                                CallbackQueryHandler(cca_view_session_clicked_user, pattern='view_cca_user')],
            CCA_REMOVE_SESSION_MENU: [CallbackQueryHandler(cca_remove_session_admin, pattern='remove_cca_admin'),
                                      CallbackQueryHandler(cca_remove_session_user, pattern='remove_cca_user'),
                                      CallbackQueryHandler(cca, pattern='cca!')],
            LEISURE_MENU: [CallbackQueryHandler(leisure_add_session, pattern='leisure_add_session!'),
                            CallbackQueryHandler(leisure_view_session, pattern='leisure_view_session!'),
                            CallbackQueryHandler(leisure_remove_activity, pattern='leisure_remove_session!'),
                        CallbackQueryHandler(front, pattern='front!')],
            LEISURE_ADD_SESSION_MENU: [CallbackQueryHandler(leisure_add_session_title, pattern='leisure_add_session_title!'),
                                    CallbackQueryHandler(leisure_add_session_details, pattern='leisure_add_session_details!'),
                                    CallbackQueryHandler(leisure_add_session_date, pattern='leisure_add_session_date!'),
                                    CallbackQueryHandler(leisure_add_session_time, pattern='leisure_add_session_time!'),
                                    CallbackQueryHandler(leisure_add_session_location, pattern='leisure_add_session_location!'),
                                    CallbackQueryHandler(leisure_add_session_deadline, pattern='leisure_add_session_deadline!'),
                                    CallbackQueryHandler(leisure_add_session_done, pattern='leisure_add_session_done!'),
                                    CallbackQueryHandler(leisure, pattern='leisure!')],
            LEISURE_ADD_SESSION_TITLE_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_title_waiting_input)],
            LEISURE_ADD_SESSION_DETAILS_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_details_waiting_input)],
            LEISURE_ADD_SESSION_DATE_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_date_waiting_input)],
            LEISURE_ADD_SESSION_TIME_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_time_waiting_input)],
            LEISURE_ADD_SESSION_LOCATION_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_location_waiting_input)],
            LEISURE_ADD_SESSION_DEADLINE_WAITING_INPUT: [MessageHandler(Filters.text, leisure_add_session_deadline_waiting_input)],
            LEISURE_VIEW_SESSION: [CallbackQueryHandler(leisure_view_session_clicked_admin, pattern='view_leisure_admin'),
                                   CallbackQueryHandler(leisure_view_session_clicked_user, pattern='view_leisure_user')],
            LEISURE_REMOVE_SESSION_MENU: [CallbackQueryHandler(leisure_remove_activity_admin, pattern='remove_leisure_admin'),
                                        CallbackQueryHandler(leisure_remove_activity_user, pattern='remove_leisure_user'),
                                          CallbackQueryHandler(leisure, pattern='leisure!')]

        },

        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True
    )


    cca_convo_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(cca_user_set_reminder, pattern='cca_user_set_reminder!')],

        states={
                CCA_USER_SET_REMINDER_WAITING_INPUT: [MessageHandler(Filters.text, cca_user_set_reminder_waiting_input)],
                CCA_USER_SET_REMINDER_DONE_MENU: [CallbackQueryHandler(cca_user_set_reminder_confirm, pattern='cca_user_set_reminder_confirm!'),
                                                    CallbackQueryHandler(cca_user_set_reminder, pattern='cca_user_set_reminder!')]
        },
        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True
    )

    leisure_convo_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(leisure_user_set_reminder, pattern='leisure_user_set_reminder!')],

        states={
                LEISURE_USER_SET_REMINDER_WAITING_INPUT: [MessageHandler(Filters.text, leisure_user_set_reminder_waiting_input)],
                LEISURE_USER_SET_REMINDER_DONE_MENU: [CallbackQueryHandler(leisure_user_set_reminder_confirm, pattern='leisure_user_set_reminder_confirm!'),
                                                    CallbackQueryHandler(leisure_user_set_reminder, pattern='leisure_user_set_reminder!')]
        },
        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True
    )

    help_convo_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help)],

        states={
                HELP_MENU: [CallbackQueryHandler(help_group_work, pattern='help_group_work!'),
                            CallbackQueryHandler(help_module, pattern='help_module!'),
                            CallbackQueryHandler(help_cca, pattern='help_cca!'),
                            CallbackQueryHandler(help_leisure, pattern='help_leisure!'),
                            CallbackQueryHandler(help_snooze, pattern='help_snooze!'),
                            CallbackQueryHandler(help_done, pattern='help_done!')],
                HELP_GROUP_WORK_MENU: [CallbackQueryHandler(help_group_work_to_do_list, pattern='help_group_work_to_do_list!'),
                                        CallbackQueryHandler(help_group_work_reminders, pattern='help_group_work_reminders!'),
                                        CallbackQueryHandler(help_return_menu, pattern='help!'),
                                        CallbackQueryHandler(help_done, pattern='help_done!')],
                HELP_MODULE_MENU:[CallbackQueryHandler(help_module_view_and_edit_module, pattern='help_module_view_and_edit_module!'),
                                  CallbackQueryHandler(help_module_reminders, pattern='help_module_reminders!'),
                                  CallbackQueryHandler(help_return_menu, pattern='help!'),
                                  CallbackQueryHandler(help_done, pattern='help_done!')]

        },
        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True
    )
    updater.dispatcher.add_handler(convo_handler)
    updater.dispatcher.add_handler(cca_convo_handler)
    updater.dispatcher.add_handler(leisure_convo_handler)
    updater.dispatcher.add_handler(help_convo_handler)

    #NEW (Remember to change this to the name of our new bot at the end)
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('@reminderExampleBot /sendCCApoll' + "\n"), cca_add_session_done_clicked)) ##TESTING
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('@reminderExampleBot /sendLeisurepoll' + "\n"), leisure_add_session_done_clicked))
    updater.dispatcher.add_handler(CallbackQueryHandler(group_work_snooze_reminder, pattern='group_work_snooze_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(group_work_dismiss_reminder, pattern='group_work_dismiss_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(module_snooze_reminder, pattern='module_snooze_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(module_dismiss_reminder, pattern='module_dismiss_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(cca_snooze_reminder, pattern='cca_snooze_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(cca_dismiss_reminder, pattern='cca_dismiss_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(leisure_snooze_reminder, pattern='leisure_snooze_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(leisure_dismiss_reminder, pattern='leisure_dismiss_reminder_'))
    updater.dispatcher.add_handler(CallbackQueryHandler(cca_reminder, pattern='attending_cca'))
    updater.dispatcher.add_handler(CallbackQueryHandler(not_attending_cca, pattern='not_attending_cca!'))
    updater.dispatcher.add_handler(CallbackQueryHandler(leisure_reminder, pattern='attending_leisure'))
    updater.dispatcher.add_handler(CallbackQueryHandler(not_attending_leisure, pattern='not_attending_leisure!'))

    #updater.dispatcher.add_handler(MessageHandler(Filters.regex('@kyl_py_newofficial_bot /sendmypoll '), sendmypoll)) ##TESTING

    updater.dispatcher.add_handler(CommandHandler('resetall', resetall))

    updater.dispatcher.add_error_handler(error)


    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook('https://murmuring-ocean-40072.herokuapp.com/' + TOKEN)
    
    #updater.start_polling()
    updater.idle()





if __name__ == '__main__':
    main()
