# -*- coding: utf-8 -*-
from config import dict_factory, TOKEN, CITY, PASSWORD
import logging
import sqlite3
import weather
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Menu Stage
MAIN_MENU, WEATHER, STOPPING, VALIDATE = map(chr, range(4))
# Weather Callback Data
WEATHER_FORECAST, CITY_CHOOSE, DAILY, TYPING, INPUT_CITY_NAME, INPUT_CITY, \
SHOW_RIGHTNOW, WWARNING, QUERY_WEATHER, INPUT_QUERY_NAME = map(chr, range(4, 14))

# Delivery Callback Data
COMPANY, ORDER_NO = map(chr, range(14, 16))

# Main Menu Callback data
END, DELIVERY, MOVIE = map(chr, range(16, 19))

# System control
BACK_MAIN, BACK_WEATHER, START_OVER = map(chr, range(19, 22))

def sql(string):
    conn = sqlite3.connect("bot.sqlite")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute(string)
    conn.commit()
    return res

def validate(update, context):
    user = update.effective_user
    res = sql("select * from user where uid=%d" %(user.id))
    if len(list(res)) == 0:
        update.message.reply_text('兄嘚你要输入密码才能和俺说话噢~~')
        update.message.reply_text('来输个密码：')
        return VALIDATE
    else:
        return start(update, context)

def judgement(update, context):
    if update.message.text == PASSWORD:
        user = update.effective_user
        sql("INSERT INTO user (uid) values ('{}')".format(user.id))
        return start(update, context)
    else:
        update.message.reply_text("大兄嘚密码不对啊，不能和你玩耍！")
        return ConversationHandler.END

def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    buttons = [
            [
                InlineKeyboardButton(text="天气预报", callback_data=str(WEATHER_FORECAST)),
                InlineKeyboardButton(text="查快递", callback_data=str(DELIVERY)),
            ],
            [
                InlineKeyboardButton(text="看电影", callback_data=str(MOVIE)),
                InlineKeyboardButton(text="结束对话", callback_data=str(END)),
            ],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    # Send message with text and appended InlineKeyboard
    text = "俺暂时只会这么多啊！\n如果有什么不满意可以和俺爹提噢！"

    if context.user_data.get(START_OVER):
        context.user_data[START_OVER] = False
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        update.message.reply_photo(
            photo=open('xm.jpeg', 'rb'),
            caption="你来找人家啦？\n俺可以查快递，看美剧并且天气预报噢！",
        )
        update.message.reply_text(text=text, reply_markup=reply_markup,)

    # Tell ConversationHandler that we're in state `FIRST` now
    return MAIN_MENU

def weather_forecast(update, context):
    buttons = [
        [
            InlineKeyboardButton(text="🌈实时天气", callback_data=str(SHOW_RIGHTNOW)),
            InlineKeyboardButton(text="🏠设置城市", callback_data=str(CITY_CHOOSE)),
        ],
        [
            InlineKeyboardButton(text="📆每日预报", callback_data=str(DAILY)),
            InlineKeyboardButton(text="☢天气预警", callback_data=str(WWARNING)),
        ],
        [
            InlineKeyboardButton(text="查询其他城市", callback_data=str(QUERY_WEATHER)),
            InlineKeyboardButton(text="⬅返回", callback_data=str(BACK_MAIN)),
        ]
    ]
    text = "实时天气 -- 获取现在的天气情况\n" \
           "设置城市 -- 设置所在城市\n" \
           "每日预报 -- 每天早上七点定时推送"
    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)

    return WEATHER

def show_rightnow(update, context):
    user = update.effective_user
    res = sql("select * from user where uid=%d" % (user.id))
    res = res.fetchall()[0]
    if res['city_code'] == None:
        text = "啊呀呀！\n" \
               "大兄嘚你还没有设置城市呢！\n" \
               "是否需要现在设置呢？"
        buttons = [[InlineKeyboardButton(text="设置城市", callback_data=str(CITY_CHOOSE)),
                    InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]]

    else:
        text = weather.rightNow(res['city'])
        buttons = [[InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)

    return WEATHER

def weather_warning(update, context):
    return

def city_choose(update, context):
    user = update.effective_user
    res = sql("select * from user where uid=%d" %(user.id))
    res = res.fetchall()[0]
    if res['city_code'] == None:
        text = "请输入你所在的城市名称噢！\n\n" \
               "例如：\n" \
               "    深圳市\n" \
               "    北京市朝阳区\n" \
               "    苏州市昆山市\n\n" \
               "港澳地区请输入：\n" \
               "    香港\n" \
               "    香港沙田区\n" \
               "    澳门嘉模堂区"
        buttons = [
            [InlineKeyboardButton(text="点击输入城市（地区）", callback_data=str(TYPING))],
            [InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]
        ]

    else:
        text = "❤️🧡💛💚💙💜\n\n" \
               "大兄嘚！\n" \
               "你已经设置过城市了哦！\n\n" \
               "当前城市：{}\n\n" \
               "是否需要修改呢？".format(res['city'])
        buttons = [[InlineKeyboardButton(text="修改城市", callback_data=str(TYPING)),
                    InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)

    return WEATHER

def end_weather(update, context):
    """End weather forecast and back to main menu"""
    context.user_data[START_OVER] = True
    start(update, context)

    return BACK_MAIN

def back_to_weather(update, context):
    """Back to weather menu"""
    weather_forecast(update, context)

    return WEATHER

def delivery(update, context):
    """Set Delivery Menu"""
    text = "请输入快递名称和快递单号。"
    buttons = [
        [
            InlineKeyboardButton(text="公司", callback_data=str(COMPANY)),
            InlineKeyboardButton(text="单号", callback_data=str(ORDER_NO))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)

    return MAIN_MENU

def stop(update, context):
    """Stop Conversation In Main Menu"""
    if update.callback_query is None:
        update.message.reply_text('大兄Dei~下次再来玩啊~~')

    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='大兄Dei~下次再来玩啊~~')

    return ConversationHandler.END

def stop_in_submenu(update, context):
    """Stop Conversation In Sub Menu"""
    if update.callback_query is None:
        update.message.reply_text('大兄Dei~下次再来玩啊~~')

    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text='大兄Dei~下次再来玩啊~~')

    return STOPPING


def ask_input_city_name(update, context):
    """Ask user to input the city name"""
    text = "输入城市名称："
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return INPUT_CITY_NAME

def save_city_name(update, context):
    user = update.effective_user
    city_name = update.message.text
    right_now = weather.rightNow(city_name)
    if right_now == None:
        text = "啊呀呀，没有找到你输入的城市呀\n请检查你的输入是否符合规范！\n例如：深圳市或者深圳市福田区"

    else:
        city_code = CITY.get(city_name)
        sql("update user set city='{}', city_code={} where uid={}".format(city_name,city_code,user.id))
        text = "🎉🎉🎉🎉🎉🎉\n设置成功啦！\n\n" + right_now
    buttons = [[InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=reply_markup)

    return BACK_WEATHER

def ask_query_weather(update, context):
    """Ask user to input the city name"""
    text = "请输入你想查询的城市名称："
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return INPUT_QUERY_NAME

def return_weather_res(update, context):
    """Return query weather result"""
    city_name = update.message.text
    right_now = weather.forecastAll(city_name)
    if right_now == None:
        text = "啊呀呀，没有找到你输入的城市呀\n请检查你的输入是否符合规范！\n例如：深圳市或者深圳市福田区"

    else:
        text = "🎉🎉🎉🎉🎉🎉\n查询成功！\n\n" + right_now
    buttons = [[InlineKeyboardButton(text="返回", callback_data=str(BACK_WEATHER))]]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=reply_markup)

    return BACK_WEATHER

def error(update, context):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Error "%s"', context.error)

def main():
    # REQUEST_KWARGS = {'proxy_url': 'http://127.0.0.1:10808'}
    # request_kwargs = REQUEST_KWARGS
    updater = Updater(token=TOKEN, use_context=True)

    # save input
    save_input = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(ask_input_city_name, pattern='^'+str(TYPING)+'$'),
            CallbackQueryHandler(ask_query_weather, pattern='^'+str(QUERY_WEATHER)+'$')
        ],
        states={
            INPUT_CITY_NAME: [MessageHandler(Filters.text, save_city_name)],
            INPUT_QUERY_NAME: [MessageHandler(Filters.text, return_weather_res)]
        },
        fallbacks=[
            CallbackQueryHandler(back_to_weather, pattern='^'+str(BACK_WEATHER)+'$'),
            CommandHandler('stop', stop_in_submenu),
        ],
        map_to_parent={
            BACK_WEATHER: WEATHER,
            STOPPING: STOPPING
        }
    )

    # set weather forecast menu
    conv_weather = ConversationHandler(
        entry_points=[CallbackQueryHandler(weather_forecast, pattern='^'+str(WEATHER_FORECAST)+'$')],
        states={
            WEATHER: [
                CallbackQueryHandler(city_choose, pattern='^'+str(CITY_CHOOSE)+'$'),
                CallbackQueryHandler(show_rightnow, pattern='^'+str(SHOW_RIGHTNOW)+'$'),
                save_input,
            ],
        },
        fallbacks=[
            CommandHandler('stop', stop_in_submenu),
            CallbackQueryHandler(end_weather, pattern='^'+str(BACK_MAIN)+'$'),
            CallbackQueryHandler(back_to_weather, pattern='^'+str(BACK_WEATHER)+'$')
        ],
        map_to_parent={
            # back to main menu
            BACK_MAIN: MAIN_MENU,
            # stop from sub menu
            STOPPING: ConversationHandler.END
        }
    )

    # set main menu
    conv_description = ConversationHandler(
        entry_points=[CommandHandler('start', validate)],
        states={
            VALIDATE: [MessageHandler(Filters.text, judgement)],
            MAIN_MENU: [
                conv_weather,
                CallbackQueryHandler(delivery, pattern='^'+str(DELIVERY)+'$')
            ],

        },
        fallbacks=[
            CommandHandler('stop', stop),
            CallbackQueryHandler(stop, pattern='^'+str(END)+'$')]
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(conv_description)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
