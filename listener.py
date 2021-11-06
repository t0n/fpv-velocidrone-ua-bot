# import json
# import logging
# import telegram
# from telegram import Update, Chat, ChatMember, ParseMode, ForceReply
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#
# from constants import RENAME_PLAYER_TEMPLATE
# from db import get_all_daily_results, update_daily_results
# from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
#
#
# logging.basicConfig(filename='log.txt', filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     # datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
# logging.getLogger('telegram').setLevel(logging.ERROR)
#
#
# def empty_message(update, context):
#     """
#     Empty messages could be status messages, so we check them if there is a new
#     group member, someone left the chat or if the bot has been added somewhere.
#     """
#
#     if update.message.chat.id in [TELEGRAM_CHAT_MESSAGE_ID, ]:
#
#         if update.message.new_chat_members:
#             for new_member in update.message.new_chat_members:
#                 # Bot was added to a group chat
#                 if new_member.username == BOTNAME:
#                     return introduce(update, context)
#                 # Another user joined the chat
#                 else:
#                     return welcome(update, context, new_member)
#
#         # # Someone left the chat
#         # elif update.message.left_chat_member is not None:
#         #     if update.message.left_chat_member.username != BOTNAME:
#         #         return goodbye(update, context)
#
#
# def reply(update, context):
#     """
#     Empty messages could be status messages, so we check them if there is a new
#     group member, someone left the chat or if the bot has been added somewhere.
#     """
#
#     print(update)
#     print(f'update.message {update.message}')
#     print(f'update.channel_post {update.channel_post}')
#     print(f'update.channel_post.chat {update.channel_post.chat}')
#     print(f'update.channel_post.chat.id {update.channel_post.chat.id}')
#
#     TELEGRAM_CHAT_MESSAGE_ID = ''
#     # TELEGRAM_CHAT_MESSAGE_ID = ''
#     if update.channel_post.chat.id in [TELEGRAM_CHAT_MESSAGE_ID, ]:
#
#         print('>>> chat OK')
#
#         if 'test'.lower() in update.channel_post.text.lower():
#             print('>>> message OK')
#             update.channel_post.reply_markdown_v2(f'it works! {update.effective_user.mention_markdown_v2()}',
#                                              reply_markup=ForceReply(selective=True),)
#             print('>>> replied!')
#
#         # # Someone left the chat
#         # elif update.message.left_chat_member is not None:
#         #     if update.message.left_chat_member.username != BOTNAME:
#         #         return goodbye(update, context)
#
#
# def main():
#     logging.info("Listener script started!")
#
#     bot = telegram.Bot('')
#     logging.debug(bot)
#
#     updater = Updater("", workers=10, use_context=True)
#
#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher
#
#     # Keep track of which chats the bot is in
#     # dispatcher.add_handler(CommandHandler("slava_ukraini", show_chats))
#
#     # dispatcher.add_handler(MessageHandler(Filters.status_update, empty_message))
#     dispatcher.add_handler(MessageHandler(Filters.text, reply))
#
#     # Start the Bot
#     # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
#     # To reset this, simply pass `allowed_updates=[]`
#     updater.start_polling(timeout=1, clean=True)
#
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()
#
#
# if __name__ == "__main__":
#     main()
