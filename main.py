from telebot import types
from pytube import YouTube
import telebot
import ast
import os
from keep_alive import keep_alive
import json
import random
from datetime import datetime
from time import sleep
while True:
  try:
    file = open('permissions.json')
    permissions = json.load(file)
    break
  except:
    key_value = {
      'youtube': True,
      'file_index': True,
      'admins': [],
      'paths': [],
    }
    with open('permissions.json', 'w') as file:
      json.dump(key_value, file)

api = os.environ['api_key']
bot = telebot.TeleBot(api)
global save, m, send_time, active_cap, change_name, name_sender, timer, day
m = None
save = True
active_q = False
active_cap = False
send_time = 0
change_name = False
timer = False
day = datetime.today().day


def is_video(message):
  #bot.send_message(chat_id='5331710167',
  #                 text="{} - {}".format(message.from_user.username,
  #                                       message.from_user.id))
  link = str(message.text)
  if link.startswith('https://youtube.com/shorts/') or link.startswith(
      'http://youtube.com/shorts/'):
    if permissions['youtube'] == True:
      return True
    else:
      bot.reply_to(message=message,
                   text='YouTube Downloader Has Turned Off by Admin')
      return
  else:
    return False


@bot.message_handler(func=is_video)
def start_download(message):
  link = str(message.text)
  try:
    yt = YouTube(link)
  except:
    print("Connection Error")
    bot.send_message(chat_id=message.chat.id, text='Connection Error!')
  else:
    bot.reply_to(message, "Let's Cooking!")
    title = yt.title

    def send_video():
      bot.send_video(chat_id=message.chat.id,
                     video=open(title, 'rb'),
                     supports_streaming=True)

    upload_error = False
    try:
      yt.streams.filter(res="720p",
                        mime_type="video/mp4").first().download(filename=title)
      send_video()
    except:
      try:
        yt.streams.filter(
          res="480p", mime_type="video/mp4").first().download(filename=title)
        send_video()
      except:
        try:
          yt.streams.filter(
            res="360p", mime_type="video/mp4").first().download(filename=title)
          send_video()
        except:
          upload_error = True
    try:
      os.remove(title)
    except:
      return


@bot.message_handler(commands=['farbod'])
def Farbod(message):
  with open('quotes.json') as f:
    Quotes = json.load(f)
  Farbod_Quotes = Quotes["434298733"]
  random.shuffle(Farbod_Quotes)
  quote = Farbod_Quotes[0]
  random_picture_num = random.randint(1, 6)
  bot.send_photo(chat_id=message.chat.id,
                 photo=open('farbod/{}.jpg'.format(random_picture_num), 'rb'),
                 caption='{0}\n\n-Adolf Farbod'.format(quote))


@bot.message_handler(commands=['add_quote'])
def active_get_q(message):
  if permissions['quotes'] == False:
    bot.reply_to(
      message=message,
      text=
      "The Quotes Were Turned Off by Admin or Your Maximum Quotes Limit Were Reached"
    )
    return
  else:
    global active_q
    global userq
    userq = message.from_user.id
    bot.reply_to(message=message, text="نقل قولتان را بفرستید.")
    active_q = True
    return


def is_q(message):
  global active_q, userq
  if active_q == True:
    if userq == message.from_user.id:
      return True
    else:
      return False
  else:
    return False


@bot.message_handler(func=is_q)
def get_q(message):
  global active_q
  file2 = open('quotes.json')
  Quotes = json.load(file2)
  user = message.from_user.id
  quote = message.text
  try:
    Quotes[str(user)].append(quote)
  except:
    Quotes[user] = []
    Quotes[user].append(quote)
  try:
    with open('quotes.txt', 'r+') as qf:
      qf.write(quote + ':::' + Quotes['user_list'][str(user)])
    Quotes['user_quotes'].append(quote + ':::' +
                                 Quotes['user_list'][str(user)])
    bot.reply_to(message=message, text="نقل قولتان دریافت شد.")
    with open('quotes.json', 'w') as file:
      json.dump(Quotes, file)
  except:
    bot.reply_to(
      message,
      'امکان استفاده از نقل قول فعلا برای شما فراهم نیست.لطفا تا آپدیت های بعدی بات منتظر بمانید'
    )
  active_q = False
  return


@bot.message_handler(commands=['my_quote'])
def user_quote(message):
  user = message.from_user.id
  with open('quotes.json') as file:
    Quotes = json.load(file)
  if str(user) in Quotes.keys():
    user = str(user)
    user_name = Quotes['user_list'][user]
    user_quotes = Quotes[user]
    random.shuffle(user_quotes)
    bot.send_message(chat_id=message.chat.id,
                     text="{0}\n\n-{1}".format(user_quotes[0], user_name))
  else:
    bot.reply_to(
      message,
      'امکان استفاده از نقل قول فعلا برای شما فراهم نیست.لطفا تا آپدیت های بعدی بات منتظر بمانید'
    )
  return


@bot.message_handler(commands=['random_quote'])
def random_quote(message):
  with open('quotes.json') as f:
    Quotes = json.load(f)
  quotes = Quotes['user_quotes']
  random.shuffle(quotes)
  quote = quotes[0].split(':::')[0]
  user = quotes[0].split(':::')[1]
  bot.send_message(chat_id=message.chat.id,
                   text='{0}\n\n-{1}'.format(quote, user))


def send_random_quote(message):
  if message.chat.type != "private":
    global send_time
    send_time += 1
    if send_time == 10:
      send_time = 0
      return True
    else:
      return False
  else:
    return False


@bot.message_handler(func=send_random_quote)
def send_random_quote(message):
  with open('quotes.json') as f:
    Quotes = json.load(f)
  quotes = Quotes['user_quotes']
  random.shuffle(quotes)
  quote = quotes[0].split(':::')[0]
  user = quotes[0].split(':::')[1]
  bot.send_message(chat_id=message.chat.id,
                   text='{0}\n\n-{1}'.format(quote, user))


@bot.message_handler(commands=['add_file'])
def add_file_start(message):
  if permissions['file_index'] == True:
    global n, save, sender, caption, path, active_cap
    n = 0
    save = False
    sender = message.from_user.username
    if active_cap is False:
      bot.reply_to(
        message=message,
        text=
        "لطفا نامی که میخواهید با آن فایل های مورد نظر را آپلود کنید، ارسال کنید."
      )
      active_cap = True
  else:
    bot.reply_to(message=message, text="File Index Was Turned Off by Admin")


def add_file(message):
  global n, save, sender, caption, path, active_cap
  if save == False:
    if message.from_user.username == sender:
      if active_cap == True:
        return True
  else:
    return False


@bot.message_handler(func=add_file)
def add_files(message):
  global n, save, sender, caption, path, active_cap
  if active_cap == True:
    caption = message.text
    active_cap = False
  save_button = types.InlineKeyboardMarkup()
  save_button.add(
    types.InlineKeyboardButton(text="ذخیره و اتمام آپلود",
                               callback_data="save_{}".format(
                                 str(message.id + 1))))
  bot.reply_to(message=message,
               text='فایل های موردنظر جهت آپلود بفرستید' +
               "\n\nفایل های شما با نام ({}) آپلود می شوند.".format(caption),
               reply_markup=save_button)
  parent_path = 'upload_files/'
  path = os.path.join(parent_path, caption)
  permissions['paths'][caption] = path + '/'
  os.mkdir(path)
  with open('permissions.json', 'w') as file:
    json.dump(permissions, file)


@bot.message_handler(commands=['save'])
def save_files(message):
  if permissions['file_index'] == True:
    print('saved')
    global save
    save = True


@bot.message_handler(content_types=['photo'])
def save__file(message):
  global save, caption, sender, path, n
  if save != True:
    if message.from_user.username == sender:
      photos = message.photo
      photo = photos[-1].file_id
      file_info = bot.get_file(photo)
      down_photo = bot.download_file(file_info.file_path)
      with open(path + '/{}.jpg'.format(n), 'wb') as p:
        p.write(down_photo)
      n += 1
      bot.send_photo(chat_id='5331710167',
                     photo=photos[-1].file_id,
                     caption=caption)
    else:
      return


@bot.message_handler(content_types=['document'])
def save__document(message):
  global save, caption, sender, path, n
  if save != True:
    if message.chat.username == sender:
      file_name = message.document.file_name
      file_info = bot.get_file(message.document.file_id)
      downloaded_file = bot.download_file(file_info.file_path)
      with open(path + '/{}.pdf'.format(n), 'wb') as file:
        file.write(downloaded_file)
      n += 1
      bot.send_document(chat_id='5331710167',
                        document=file_name,
                        caption=caption)
    else:
      return


@bot.message_handler(commands=['delete'])
def delete_file(message):
  for admin in permissions['admins']:
    if message.from_user.id == admin:
      try:
        number = str(message.text).split(' ')[1]
      except:
        bot.reply_to(message=message, text="So Where is Number?")
        return
      paths = {}
      c = 1
      for key in permissions['paths'].keys():
        paths[c] = key
        c += 1

      folder = paths[int(number)]
      folder_path = permissions["paths"][folder]
      for file in os.listdir(folder_path):
        os.remove(folder_path + file)
      del permissions["paths"][folder]
      os.rmdir(folder_path)
      bot.reply_to(message=message, text="The File Deleted Successfully")
      with open('permissions.json', 'w') as file:
        json.dump(permissions, file)
      break
    else:
      bot.reply_to(message=message, text="OnlyAdmins!")


@bot.message_handler(commands=['get'])
def send_files(message):
  global paths
  markup = types.InlineKeyboardMarkup()
  paths = {}
  c = 1
  text = ""
  for key in permissions['paths'].keys():
    markup.add(
      types.InlineKeyboardButton(text=key, callback_data=str([str(c), key])))
    text += '\n' + '/' + str(c) + ' : ' + key
    paths[c] = key
    c += 1

  bot.send_message(chat_id=message.chat.id,
                   text='یکی از فایل های آپلود شده را انتخاب کنید:',
                   reply_markup=markup)


def is_file(message):
  if str(message.text).startswith('/'):
    tag = str(message.text).split('@')[0]
    try:
      number = int(str(''.join(tag[1::])))
      if len(permissions['paths'].keys()) >= number:
        return True
    except:
      return False
  else:
    return False


@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
  global save, sender, timer
  data = call.data
  if data.startswith("save"):
    print(sender, call.from_user.username)
    if call.from_user.username == sender:
      save = True
      print('saved')
      message_code = data.split('_')[1]
      bot.answer_callback_query(callback_query_id=call.id,
                                show_alert=True,
                                text="فایل های شما با موفقیت آپلود شد!")
      bot.delete_message(chat_id=call.message.chat.id,
                         message_id=int(message_code))
      bot.send_message(chat_id=call.message.chat.id,
                       text="فایل های شما دریافت شدند. باتشکر از شما")
    else:
      bot.answer_callback_query(
        callback_query_id=call.id,
        show_alert=True,
        text="داداش فقط کسی که داره آپلود میکنه میتونه ذخیره کنه")
  elif data.startswith('T-'):
    qj= open("permissions.json", "rb")
    quiz_board = json.load(qj)
    quiz_board["quiz"][str(call.from_user.id)][1] += 1
    with open("permissions.json", "w") as file:
      json.dump(quiz_board, file)
    #bot.answer_callback_query(callback_query_id=call.id,
    #                          show_alert=True,
    #                          text="گزینه انتخابی شما درست است!")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=int(data.split('-')[2]), text="@{}\n✅ آزمون شما به پایان رسید \n\n سوال: {} \n\nجواب درست:{} ✅️\n جواب شما: {} ✅️\n\n شما 1 امتیاز دریافت می کنید".format(call.from_user.username, call.message.text, data.split('-')[1], data.split('-')[1]))
    timer = False
  elif data.startswith('F-'):
    #bot.answer_callback_query(
    #  callback_query_id=call.id,
    #  show_alert=True,
    #  text="گزینه انتخابی شما نادرست است! گزینه درست {} می باشد!".format(
    #    data.split('-')[1]))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=int(data.split('-')[2]), text="@{}\n❌️ آزمون شما به پایان رسید \n\n سوال: {} \n\nجواب درست:{} ☑️\n جواب شما: {} ❌️\n\n شما امتیازی دریافت نمی کنید".format(call.from_user.username,call.message.text, data.split('-')[1], data.split('-')[3]))
    timer = False
  else:
    data = ast.literal_eval(call.data)
    bot.answer_callback_query(
      callback_query_id=call.id,
      show_alert=True,
      text="اکنون فایل (های) {} را در پیویتان یا در همین چت ارسال میکنم.".
      format(data[1]))
    tag = data[0]

    global paths
    paths = {}
    c = 1
    for key in permissions['paths'].keys():
      paths[c] = key
      c += 1
    key = paths[int(tag)]
    path = permissions['paths'][key]
    try:
      bot.send_message(chat_id=call.from_user.id, text=data[1])
      for file in os.listdir(path):
        with open(path + file, "rb") as photo:
          bot.send_document(chat_id=call.from_user.id, document=photo)
    except:
      bot.send_message(chat_id=call.message.chat.id, text=data[1])
      for file in os.listdir(path):
        with open(path + file, "rb") as photo:
          bot.send_document(chat_id=call.message.chat.id, document=photo)


@bot.message_handler(func=is_file)
def send_files2(message):
  tag = str(message.text).split('@')[0]
  global paths
  paths = {}
  c = 1
  for key in permissions['paths'].keys():
    paths[c] = key
    c += 1
  number = int(str(''.join(tag[1::])))
  key = paths[number]
  path = permissions['paths'][key]
  bot.send_message(chat_id=message.chat.id, text="در حال ارسال فایل ها...")
  for file in os.listdir(path):
    with open(path + file, "rb") as photo:
      bot.send_document(chat_id=message.chat.id, document=photo)
  bot.delete_message(message.chat.id, message.message_id + 1)


@bot.message_handler(commands=['change_name'])
def get_custom_title(message):
  global change_name, name_sender
  bot.reply_to(message=message, text="لطفا لقب مورد نظر خود را بفرستید")
  change_name = True
  name_sender = message.from_user.username


def is_change_name(message):
  global change_name, name_sender
  if change_name == True:
    if message.from_user.username == name_sender:
      return True
  else:
    return False


@bot.message_handler(func=is_change_name)
def change_custom_title(message):
  global change_name
  try:
    bot.promote_chat_member(chat_id=message.chat.id,
                            user_id=message.from_user.id,
                            can_change_info=False,
                            can_post_messages=True,
                            can_edit_messages=True,
                            can_delete_messages=False,
                            can_invite_users=True,
                            can_restrict_members=False,
                            can_pin_messages=True,
                            can_promote_members=False,
                            is_anonymous=False,
                            can_manage_chat=False,
                            can_manage_video_chats=False,
                            can_manage_voice_chats=False,
                            can_manage_topics=False)
    bot.set_chat_administrator_custom_title(chat_id=message.chat.id,
                                            user_id=message.from_user.id,
                                            custom_title=message.text)
  except:
    bot.reply_to(message=message,
                 text="احتمالا دسترسی لازم برای تغییر لقب شما را ندارم.")
  else:
    bot.reply_to(message=message,
                 text="لقب شما با موفقیت به {} تغییر یافت".format(
                   message.text))
  change_name = False


@bot.message_handler(commands=['quiz'])
def send_quiz(message):
  global timer, day
  timer = True
  
  qjp = open('permissions.json', 'rb')
  qj = json.load(qjp)
  quiz_board = qj['quiz']
  if not str(day) in quiz_board.keys():
    quiz_board[day] = {}
  if str(message.from_user.id) in quiz_board[str(day)].keys():
    if quiz_board[str(day)][str(message.from_user.id)] == 3:
      bot.send_message(chat_id= message.chat.id, text="@{}\n شما حداکثر ظرفیت سوالات خود را (3/3) استفاده کردید! فردا دوباره سر بزنید.".format(message.from_user.username))
      return
  if not str(message.from_user.id) in quiz_board[str(day)].keys():
    quiz_board[day][message.from_user.id] = 1
  else:
    quiz_board[str(day)][str(message.from_user.id)] += 1 
  if not str(message.from_user.id) in quiz_board.keys():
    quiz_board[message.from_user.id] = [message.from_user.first_name, 0]
  q_j = open('questions.json')
  qq = json.load(q_j)
  question = list(qq.keys())[random.randint(1, 200)]
  quiz_options = types.InlineKeyboardMarkup()
  quiz_options.row_width = 2
  while True:
    for option, value in qq[question].items():
      if value == True:
        op = option 
        break
    break
  for option, value in qq[question].items():
    if value == True:
      quiz_options.add(
        types.InlineKeyboardButton(text=option,
                                   callback_data='T-{}-{}'.format(op, message.id+1)))
    else:
      quiz_options.add(
        types.InlineKeyboardButton(text=option,
                                   callback_data='F-{}-{}-{}'.format(op, message.id+1, option)))

  bot.send_message(chat_id=message.chat.id,
                   text=question + "\n\n زمان باقی مانده: 15",
                   reply_markup=quiz_options)
  with open("permissions.json", 'w') as file:
    qj["quiz"] = quiz_board
    json.dump(qj , file)
  for i in range(14, 0, -1):
    if timer == False:
      break
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.id + 1,
                          text=question + "\n\n⏳️ زمان باقی مانده: {}".format(i),
                          reply_markup=quiz_options)
    sleep(1)
    if i == 1:
      bot.edit_message_text(chat_id=message.chat.id,
                            message_id=message.id + 1,
                            text=" زمان شما به پایان رسید. ⌛️")

@bot.message_handler(commands=["leaderboard"])
def send_quiz_leaderboard(message):
  text = "جدول رتبه بندی بازیکنان: \n"
  table = {}
  with open("permissions.json", "rb") as file:
    q = json.load(file)
    board = q["quiz"]
    for k, v in board.items():
      if len(k) > 2:
        table[v[0]] = v[1]
  print(table)
  
  for k, v in table.items():
    text += str(k) + ' : ' + str(v) + '\n' + '----------------' + "\n"
  bot.send_message(chat_id=message.chat.id, text=text)
@bot.message_handler(content_types=["text"])
def changing_permissions(message): 
  for admin_id in permissions['admins']:
    if message.from_user.id == admin_id:
      code = str(message.text)
      if code == '00':
        permissions["youtube"] = False
        bot.reply_to(message=message,
                     text='The YouTube DownLoader Has Turned Off.')
        break
      elif code == '01':
        permissions["youtube"] = True
        bot.reply_to(message=message,
                     text='The YouTube DownLoader Has Turned On.')
        break
      elif code == '10':
        permissions["file_index"] = False
        bot.reply_to(message=message, text='The File Indexer Has Turned Off.')
        break
      elif code == '11':
        permissions["file_index"] = True
        bot.reply_to(message=message, text='The File Indexer Has Turned On.')
        break
      elif code == '20':
        permissions["quotes"] = False
        bot.reply_to(message=message, text='The Quotes Has Turned Off.')
      elif code == '21':
        permissions["quotes"] = True
        bot.reply_to(message=message, text='The Quotes Has Turned On.')
      elif code == '404':
        bot.send_message(chat_id=message.chat.id, text="GoodBye")
        bot.leave_chat(message.chat.id)
        break
      else:
        return
  with open('permissions.json', 'w') as file:
    json.dump(permissions, file)


keep_alive()
bot.infinity_polling(timeout=10, long_polling_timeout=5)