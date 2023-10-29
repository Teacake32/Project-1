import pandas as pd
import sqlite3


def create_songs_database():
  df = pd.read_csv('songs.csv')
  df.column = df.columns.str.strip()
  conn = sqlite3.connect('song.db')
  df.to_sql('song_databse', conn, if_exists='replace')
  conn.close()

create_songs_database()

password = ""
username = ""
selected_artist = ""
selected_genre = ""

def create_account ():
  password_check = False
  global password
  global username
  global selected_artist
  global selected_genre
  username = input("Please enter a Username for Musically: ")
  while password_check is False:
      password = input("Enter a Password more than 12 Characters: ")
      if len(password) < 12:
        print("InValid Password")
        password_check = False
      else:
        print ("Valid Password")
        selected_artist = input("Please enter a preferred artist: ")
        selected_genre = input("Please enter a preferred genre: ")
        password_check = True

  return (password, username,selected_artist,selected_genre)

create_account()
print (username)
print (password)
print (selected_artist)
print(selected_genre)

def store_logins(username, password,selected_artist,selected_genre):
  conn = sqlite3.connect('login.db')
  cur = conn.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS login_database (
                username text, 
                password text,
				preferred_artist text,
				preferred_genre text
                )''')

  cur.execute('''INSERT INTO login_database
                 VALUES (:username,:password,:preferred_artist,:preferred_genre);''', {'username': username, 'password': password, 'preferred_artist': selected_artist, 'preferred_genre': selected_genre})
  conn.commit()
  conn.close()

store_logins(username, password, selected_artist, selected_genre)


print ("welcome" + username + "to the playlist database")
print ("powered by SQLITE3")

def sign_in():
  username_input = input("please enter your username: ")
  password_input = input("please enter your password: ")
  conn = sqlite3.connect('login.db')
  cur = conn.cursor()

  cur.execute('SELECT * FROM login_database')
  database = cur.fetchall()
  for i in database:
    username_check = i[1]
    password_check = i[2]

    if username_check != username_input and password_check != password_input:
      print("password or username is not valid")
      print("This program will force quite")
      print("----------------------------------")
      exit()
    else:
      print("username and password correct")
      print("-------------------------------")




def alphabet_sort ():
  conn = sqlite3.connect('song.db')
  cur = conn.cursor()
  cur.execute('SELECT "Song Name", "Artist", "Time (seconds)" FROM "song.db" ORDER BY "Song Name" ASC')
  my_data = cur.fetchall()
  for i in my_data:
    print(i)
  conn.commit()
  conn.close()



def timed_playlist():
  selected_time = int(input("How long do you want this playlist to be in Minutes?"
                            "enter this as just a number e.g 10: "))
  playlist_name = input("What is this playlist called?: ")
  total_time = 0
  conn = sqlite3.connect('song.db')
  cur = conn.cursor()
  while total_time < 10:
    random_song = cur.execute('SELECT "Song Name", "Artist", "Genre", "Time (seconds)" ORDER BY RANDOM() LIMIT 1')

def genre_playlist():
  selected_genre = input("please enter a selected genre: ")
  selected_genre = selected_genre.capitalize()
  conn = sqlite3.connect('song.db')
  cur = conn.cursor()
  playlist_name = input("what is this playlist called: ")
  cur.execute("CREATE VIEW '" + str(playlist_name) +"' AS SELECT * FROM 'song.db' WHERE Genre = '" + str(selected_genre) + "' ORDER BY RANDOM() LIMIT 5")
  conn.commit()
  conn.close()


def pick_artist_textfile():
  selected_artist = input("What artist do you want to select: ")
  conn = sqlite3.connect('song.db')
  cur = conn.cursor()
  cur.execute("CREATE VIEW IF NOT EXISTS'" + str(selected_artist) +"' AS SELECT * FROM 'song.db' WHERE Artist = '" + str(selected_artist) + "' ")
  my_data = cur.fetchall()
  f = open(selected_artist,"w")
  for i in my_data:
    f.write(my_data)
    print (my_data)
  f.close()
  conn.commit()
  conn.close()


print ("Welcome to the playlist menu" + username)
print("""Commands for the Playlsit are
      Alphabetical list of all the songs in our deck - press 1 
      Create a playlist from all songs in our deck based on a genre - press 2
      Create a text file of an artists songs - press 3 
      Create a playlist from a specified time - press 4 
      """)
program_check = False
while program_check == False:
  number_input = int(input("Enter your option: "))
  if number_input == 1:
    alphabet_sort()
    program_decide = input("would you like to continue to another option, yes or no: ").lower()
    if program_decide == "yes":
      program_check = False
    else:
      program_check = True
  elif number_input == 2:
    genre_playlist()
    program_decide = input("would you like to continue to another option, yes or no: ").lower()
    if program_decide == "yes":
      program_check = False
    else:
      program_check = True
  elif number_input == 3:
    pick_artist_textfile()
    program_decide = input("would you like to continue to another option, yes or no: ").lower()
    if program_decide == "yes":
      program_check = False
    else:
      program_check = True
  elif number_input == 4:
   timed_playlist()
   program_decide = input("would you like to continue to another option, yes or no: ").lower()
   if program_decide == "yes":
    program_check = False
   else:
    program_check = True









print("SYSTEM EXIT")
print("--------------------------------")
