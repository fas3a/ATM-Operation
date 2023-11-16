# register
#   -email, first name, last name, password

# login

import random
from bank_database import Database, AuthDatabase, UpdateAccountBalance

# user_database = {}
# for user_details in user_database.values():
#     userFirstName = user_details[0]
#     userLastName = user_details[1]
#     userEmail = user_details[2]


def init():
    isTheOperationTrue = False

    while isTheOperationTrue == False:
        try:
            user_option = int(input('Do you have an account 1-Yes or 2-No? '))
        except ValueError:
            print('wrong entry, kindly input 1-Yes or 2-No')
            init()

        if user_option == 1:
            isTheOperationTrue = True
            login()
        elif user_option == 2:
            isTheOperationTrue = True
            print('Kindly register: ')
            register()
        else:
            print('Wrong Option')


def register():
    first_name = input('First name: ')
    last_name = input('Last name: ')
    email = input('Email Address: ')
    password = input('Your password: ')
    customerId = 2

    account_number = account_no_generation()    # account no generated

    print(f'{first_name}, congratulations Your registration is complete and your account no is {account_number}')

    # user_database[account_number] = [first_name, last_name, email, password]    # Add user details to database

    # [first_name, Last_name, email, password] = customer_details

    save_database = Database(account_number, first_name, last_name, email, password, customerId)    # save to an Excel database
    save_database.save_to_excel()

    login()


def login():
    print('Please Input your account no and password details to login: ')

    # user_details = user_database.values()

    isLoginSuccessful = False
    while not isLoginSuccessful:
        global accountNoFromUser, pswdFromUser

        accountNoFromUser = input('Your account no: ')

        while not verify_account_no(accountNoFromUser):
            login()
        else:
            pswdFromUser = input('Your password: ')

        # Calling the authentication class from bank_database.py
        authDatabase = AuthDatabase(int(accountNoFromUser), pswdFromUser)
        if authDatabase.authFromDatabase():
            print('You\'ve Logged in Successfully')
            isLoginSuccessful = True

            bankOperation(authDatabase.get_user_name())

        else:
            print(f'Either your account no or password is wrong, pls try again')

        # This is saved to a temporary database array called user_database
        #
        # accountNoFromUser = int(input('Your account no: '))
        # if accountNoFromUser in user_database.keys():
        #     print('user name found')
        #     pswdFromUser = input('Your password: ')
        #
        #     for user_details in user_database.values():
        #         if pswdFromUser == user_details[3]:
        #             print('it is successful')
        #             bankOperation()
        #             isLoginSuccessful = True
        #         else:
        #             print(f'password wrong, it is {user_details[3]}')
        #
        #             login()
        # else:
        #     print('user not found')

def account_no_generation():
    account_no = random.randint(111111111, 999999999)
    return account_no


def bankOperation(user_from_database):
    print('********** BANK OPERATION *********')
    print(f'You are welcome {user_from_database}')

    user_operation_option = input('''
  Press (1) - check account balance
        (2) - Withdrawal
        (3) - logout
        (4) - quit \n''')

    if int(user_operation_option) == 1:
        check_account_balance()
    elif int(user_operation_option) == 2:
        withdrawal()
    elif int(user_operation_option) == 3:
        logout()
    elif int(user_operation_option) == 4:
        quit()
    else:
        print('Kindly choose the write option')
        bankOperation()


def check_account_balance():
    authDatabase = AuthDatabase(int(accountNoFromUser), pswdFromUser)
    print(f'your account balance is NGN {authDatabase.get_user_account_balance()}')
    user_to_continue = input('Do you want to perform another transaction 1-yes or 2-no: ')

    if int(user_to_continue) == 1:
        bankOperation(authDatabase.get_user_name())
    else:
        exit()


def withdrawal():
    authDatabase = AuthDatabase(int(accountNoFromUser), pswdFromUser)
    user_account_balance = authDatabase.get_user_account_balance()
    user_withdraw_amount = int(input('How much do you want to withdraw?: '))

    try:

        if user_withdraw_amount > user_account_balance:
            print(f'You Account balance is not sufficient. your current account balance is '
                  f'{user_account_balance}')
            withdrawal()
        elif user_withdraw_amount <= user_account_balance:
            user_new_account_balance = user_account_balance - user_withdraw_amount
            print(f'You have successfully withdrawn NGN {user_withdraw_amount} and your balance is NGN '
                  f'{user_new_account_balance}')

            authDatabase = UpdateAccountBalance(user_new_account_balance, int(accountNoFromUser), pswdFromUser)
            authDatabase.update_account_balance()

            user_to_continue = input('Do you want to perform another transaction 1-yes or 2-no: ')

            if int(user_to_continue) == 1:
                bankOperation(authDatabase.get_user_name())
            else:
                print(f'Thank you for banking with us!')
                exit()
    except ValueError:
        print('You have inputted wrong amount, kindly try again')
        exit()


def logout():
    user_logout_option = input('Are you sure yes or no: ')
    if user_logout_option.lower() == 'yes':
        init()
    else:
        pass


def verify_account_no(accountNoFromUser):
    if accountNoFromUser:
        if len(str(accountNoFromUser)) == 9:
            try:
                int(accountNoFromUser)
                return True
            except ValueError:
                print('Account no must be integers only')
                return False
        else:
            print('Account Number must be 9 digits')
            return False
    else:
        print('Account number cannot be empty, pls try again')
        return False


init()
