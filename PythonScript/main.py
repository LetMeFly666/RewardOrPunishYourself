'''
Author: LetMeFly
Date: 2022-11-05 17:03:06
LastEditors: LetMeFly
LastEditTime: 2023-02-21 21:54:23
'''
import sqlite3
import time

DBNAME = "LetMeFly_Data.db"
MAX_WHAT_LENGTH = 50  # the maximum length of the name of what you did


def init():
    try:
        conn = sqlite3.connect(DBNAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                what VARCHAR({MAX_WHAT_LENGTH}) NOT NULL,
                when_ VARCHAR(20) NOT NULL,  -- len("2022.10.10 12:00:00")
                score REAL NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE coin (
                total REAL NOT NULL
            );
        """)
        cursor.execute("""
            INSERT INTO coin (total) VALUES (0);
        """)
        conn.commit()
        conn.close()
    except Exception as e:  # 可能是第二次运行，不需要初始化
        print(e)


def main():
    help = """\
+---------+--------------------------+
| Command | Usage                    |
+---------+--------------------------+
| help    | Show how to use          |
+---------+--------------------------+
| add     | Add a log                |
|         | Try `add -help` for more |
+---------+--------------------------+
| show    | Show logs                |
+---------+--------------------------+
| exit    | Quit the system          |
+---------+--------------------------+
""" 
    print(help)
    while True:
        command = input("Please input the command> ")
        commands = command.split()
        if commands[0] == "add":
            addHelp = """\
Usage:
 · You can input `add -help` to see this help
 · You can just input `add` and then you will got a step-by-step instruction
 · You can also input `add "{what}" ["{when}"] {score}` to add one log one line.
Example:
 · add
 · add "Recited 100 words" "2022-12-05 18:38:33" 5
 · add "Played a game for 5mins" -10"""
            if len(commands) == 2 and commands[1] == "-help":
                print("add help:")
                print(addHelp)
                continue
            what, when, score = "Nothing", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 0
            """Parse"""
            if len(commands) == 1:  # add
                while True:
                    whatInputed = input("Please input what you did> ")
                    if len(whatInputed) > MAX_WHAT_LENGTH:
                        print(f"Name too long, you can input {MAX_WHAT_LENGTH} char at most")
                    else:
                        what = whatInputed
                        break
                while True:
                    timeInputed = input("Please input when you did it, with the format of `2022-11-05 19:00:19`(Empty for now)> ")
                    if not timeInputed:
                        break
                    try:
                        when = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timeInputed, "%Y-%m-%d %H:%M:%S"))
                        break
                    except:
                        print("Error format, or you can just input the Enter for now.")
                while True:
                    scoreInputed = input("Just reward or punish yourself! Input the score you get> ")
                    try:
                        score = float(scoreInputed)
                        break
                    except:
                        print("Please input a number")
            else:
                print("Sorry, it's not supported yet.")
                print("Please just input the `add` temporarily")
                continue
            """Execute"""
            conn = sqlite3.connect(DBNAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO log (
                    what,
                    when_,
                    score
                ) VALUES (
                    ?,
                    ?,
                    ?
                );
            """, (what, when, score))
            conn.commit()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE coin SET total = total + {score}")
            conn.commit()
            conn.close()
            print("Log added, use `show` for more")
        elif commands[0] == "show":
            conn = sqlite3.connect(DBNAME)
            cursor = conn.cursor()
            logResult = cursor.execute("""
                SELECT * FROM log;
            """)
            print("(id, what, when, score)")
            print("-----------------------")
            for row in logResult:
                print(row)
            total = 0
            for _ in cursor.execute("""SELECT * FROM coin limit 1;"""):
                total = _[0]
                break
            print("-----------------------")
            print(f"The total score is {total}")
            conn.commit()
            conn.close()
        elif commands[0] == "exit":
            print("Bye~")
            time.sleep(0.5)
            break
        else:
            if commands[0] == "help":
                print("Help:")
            else:
                print("Error command! You can try:")
            print(help)
        



if __name__ == "__main__":
    init()
    main()
