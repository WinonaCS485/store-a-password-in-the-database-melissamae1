import pymysql.cursors
import hashlib, uuid

# Connect to the database
connection = pymysql.connect(host='mrbartucz.com',
                             user='lg6757bu',
                             password='password',
                             db='lg6757bu_PasswordDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:

        # 1. Ask the user to store a password
        userName = input("Create a username: ")
        password = input("Create a password: ")
        print("Adding user to the database...")

        # create a unique salt
        salt = uuid.uuid4().hex 

        print ("password + salt is: " + password + str(salt))

        # create the hashed password
        hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

        print ("the hashed password is: ", hashed_password)

        # 2. Store the salt and hash in database
        sql = "INSERT INTO `UserData` (`userName`, `saltVal`, `hashedPass`) VALUES (%s, %s, %s)"
        print( sql )
        cursor.execute( sql, ((userName,), (salt,), (hashed_password,)) )
        connection.commit()
        

        # 3. Ask the user to enter correct password
        is_correct = False

        #while password is incorrect
        while is_correct == False:

            userName_2 = input("Username: ")
            

            # new SQL!!!!
            # salt_2, hashed_password_2 = cursor[0].execute( "SELECT `saltVal`, `hashedPass` FROM `UserData` WHERE `username`= %s", (userName_2,) )
            sql = "SELECT `saltVal`, `hashedPass` FROM `UserData` WHERE `userName`= %s"

            # execute the SQL command
            cursor.execute( sql, userName_2 )
                
            # get the results
            for result in cursor:
                print (result)
                salt_2 = result['saltVal']
                hashed_password_2 = result['hashedPass']


            attempted_Password = input("Password: ")

            # 4. Tell the user if they are correct or incorrect
            if( hashlib.sha512((attempted_Password + salt_2).encode('utf-8')).hexdigest() == hashed_password ):
                print("Correct!")
                is_correct = True
            else:
                print("ERROR: Password incorrect!")
            
finally:
    connection.close()  
