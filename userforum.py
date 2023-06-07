import sqlite3
import traceback
import logging


RESET = "\033[0m"       # Reset all formatting
RED = "\033[31m"        # Red text
GREEN = "\033[32m"      # Green text
YELLOW = "\033[33m"     # Yellow text
BLUE = "\033[34m"       # Blue text
MAGENTA = "\033[35m"    # Magenta text
CYAN = "\033[36m"       # Cyan text
WHITE = "\033[37m"      # White text

def get_db_connection():
    conn = sqlite3.connect("./users.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table():
    conn, cursor = get_db_connection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            utype TEXT DEFAULT "USER"
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            username TEXT NOT NULL,
            title_post TEXT NOT NULL,
            description_post TEXT NOT NULL,
            FOREIGN KEY(category_id) REFERENCES category(category_id)
        )
    ''')
    conn.commit()
    conn.close()




def register():
    
    conn, cursor = get_db_connection()
    create_table()
    username = input(RED + "Enter a username: ")
    password = input("Enter a password: ")
    email = input("Enter your email: " + RESET)

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different username.")
        return

    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

    print(GREEN + "Registration successful." + RESET)

logged_in_user = None
user_id, username, password, email, utype = None, None, None, None, None

def login():
    
    conn, cursor = get_db_connection()
    create_table()
    global user_id
    global username
    global password
    global email 
    global utype
    username = input(RED + "Enter your username: ")
    password = input("Enter your password: " + RESET)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        global logged_in_user
        logged_in_user = True
        user_id, username, password, email, utype=user
        print(GREEN + "Login successful." + RESET)
        while True:
            if ((utype == "ADMIN") and (logged_in_user == True)):
                printmenu("ADMIN")
                adminchoice = input(CYAN + "Enter Your Choice: " + RESET)
                adminmenu(adminchoice)
            elif ((utype == "USER") and (logged_in_user == True)):
                printmenu("USER")
                userchoice = input(CYAN + "Enter Your Choice: " + RESET)
                usermenu(userchoice)       
    else:
        print(RED + "Invalid username or password." + RESET)

def printmenu(utypemenu):
    if utypemenu == "ADMIN":
            print("--------------------------")
            print("|1. Create Category.     |")
            print("|2. View Category.       |")
            print("|3. Delete Category.     |")
            print("|4. Edit Category.       |")
            print("|5. Delete Post.         |")
            print("|6. Edit UserType.       |")
            print("|7. Logout.              |")
            print("--------------------------")
    elif utypemenu == "USER":
            print("----------------------------")
            print("|1. View All Categories.   |")
            print("|2. Post in Category.      |")
            print("|3. View Category Posts.   |")
            print("|4. Search Post with title.|")
            print("|5. Logout.                |")
            print("----------------------------")       
def usermenu(selection):
    if selection == "1":
        viewCategory()
    elif selection == "2":
        postCategory()
    elif selection == "3":
        viewPosts()
    elif selection == "4":
        searchPost()
    elif selection == "5":
        logout()
    else: 
        print("Invalid Choice!")
        return True

def adminmenu(selection):
    if selection == "1":
        createCategory()
    elif selection == "2":
        viewCategory()
    elif selection == "3":
        delCategory()
    elif selection == "4":
        editCategory()
    elif selection == "5":
        delPost()
    elif selection == "6":
        editUserType()
    elif selection == "7":
        logout()
    else: 
        print("Invalid Choice!")
        return True

def createCategory():
    
    titlecat = input("Enter the Title of New Category: ")
    descriptioncat = input("Enter The Description of New Category: ")
    create_category(
        titlecat,
        descriptioncat
    )

def create_category(titlecat, descriptioncat):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("INSERT INTO category (title, description) VALUES (?, ?)",
                       (titlecat, descriptioncat))
        conn.commit()
        print(GREEN + "Category Created" + RESET)
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()

def searchPost(): 
    
    conn, cursor = get_db_connection()
    rows = []
    try:
        term=input("Enter the Search TERM: ")
        cursor.execute(f"SELECT * FROM posts WHERE title_post LIKE '%{term}%' OR description_post LIKE '%{term}%'")
        rows = cursor.fetchall()
        if(rows==[]):
            print(RED + "Nothing Found"+ RESET)
        for row in rows:
            print(YELLOW + "---------------------------------------------------------" + RESET)
            print(f"POST ID - {row[0]}                  AUTHOR - {row[2]}")
            print(f"POST TITLE: {row[3]}")
            print(MAGENTA + f"{row[4]}" + RESET)
            print(YELLOW + "---------------------------------------------------------" + RESET)
            
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows  
def postCategory():
    
    conn, cursor = get_db_connection()
    try:
        viewCategory()
        global username
        cat_id = input("Enter the Category ID: ")
        title_post = input("Enter the Title of Post: ")
        description_post = input("Enter The Description of Post: ")
        cursor.execute("INSERT INTO posts (category_id, username, title_post, description_post) VALUES (?, ?, ?, ?)",
                       (cat_id, username, title_post, description_post))
        conn.commit()
        print(GREEN + "Posted Successfully!" + RESET)
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()

def viewCategory():
    
    conn, cursor = get_db_connection()
    rows = []
    try:
        cursor.execute("select * from category")
        rows = cursor.fetchall()
        for row in rows:
            print(YELLOW + "---------------------------------------------------------" + RESET)
            print(f"Category ID - {row[0]}                  ")
            print(f"TITLE: {row[1]}")
            print(f"Description: {row[2]}")
            print(YELLOW + "---------------------------------------------------------\n" + RESET)
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows
def delPost():
    
    conn, cursor = get_db_connection()
    try:
        viewPosts()
        post_id=input("Post ID you want to Delete: ")
        cursor.execute(
            f"delete from posts where post_id={post_id}"
        )
        conn.commit()
        print(GREEN + "Post Deleted" + RESET)
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    
def delCategory():
    
    conn, cursor = get_db_connection()
    try:
        viewCategory()
        catid=input("Input the Category ID you want to Delete? ");
        cursor.execute(
            f"delete from category where category_id={catid}"
        )
        conn.commit()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()

def editCategory():
    
    conn, cursor = get_db_connection()
    try:
        viewCategory()
        catid=input("Input the Category ID you want to Edit? ");
        title=input("New Title? ");
        desc=input("New Description? ");
        cursor.execute(
                f"update category set description='{desc}', title='{title}' where category_id={catid}"
            )
        conn.commit()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
        
def editUserType():
    
    conn, cursor = get_db_connection()
    try:
        allUsers()
        user_id=input("Enter User ID: ")
        utype_changed=input("Enter UType[ADMIN/USER]: ")
        utype_changed=utype_changed.upper()
        cursor.execute(
                f"update users set utype='{utype_changed}' where id={user_id}"
            )
        conn.commit()
        print(GREEN + "UserType Changed Successfully"+ RESET)
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()


def allUsers(): 
    
    conn, cursor = get_db_connection()
    rows = []
    try:
        term=input("USER Type[ADMIN, USER]: ")
        if term=="ADMIN":
            cursor.execute(f"SELECT * FROM users WHERE utype = '{term}'")
        elif term=="USER":
            cursor.execute(f"SELECT * FROM users WHERE utype = '{term}'")
        else:
            cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if(rows==[]):
            print(RED + "Nothing Found"+ RESET)
        for row in rows:
            print(YELLOW + "---------------------------------------------------------" + RESET)
            print(f"USER ID - {row[0]}                  USER NAME - {row[1]}")
            print(MAGENTA + f" USER TYPE - {row[4]}" + RESET)
            print(YELLOW + "---------------------------------------------------------" + RESET)
            
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows  

def viewPosts():
    
    conn, cursor = get_db_connection()
    rows = []
    try:
        viewCategory()
        cat_id=input("Which Category, Enter ID?")
        cursor.execute(f"select * from posts where category_id={cat_id}")
        rows = cursor.fetchall()
        for row in rows:
            print(YELLOW + "---------------------------------------------------------" + RESET)
            print(f"POST ID - {row[0]}                  AUTHOR - {row[2]}")
            print(RED + f"POST TITLE: {row[3]}" + RESET)
            print(MAGENTA + f"{row[4]}" + RESET)
            print(YELLOW + "---------------------------------------------------------" + RESET)
            
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows   

def logout():
    global logged_in_user
    logged_in_user=False
    global user_id
    global username
    global password
    global email 
    global utype
    user_id, username, password, email, utype=None,None,None,None,None
    main()

def main():
    while True:
        print(CYAN + "Welcome to Team Motohead Forums!" + RESET)
        choice = input("Enter " + YELLOW  + "r" + RESET + " to Register\nEnter " + YELLOW + "l" + RESET + " to login\nInput: ")
        if choice.lower() == 'r':
            register()
        elif choice.lower() == 'l':
            login()
        else:
            break
main()

