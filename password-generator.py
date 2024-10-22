import string
import plac
import random

MINIMUM_LENGTH = 12

def check_password_rules(password):
    if (len(password) < MINIMUM_LENGTH):
        raise RuntimeError('password too short, must be at least {} characters long'.format(MINIMUM_LENGTH))
    
    # must contain only
    valid_chars = set(string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits)
    password_set = set(password)
    if not (password_set.issubset(valid_chars)):
        raise RuntimeError('password contains an invalid character, password is: {}'.format(password))
    
    # must have at least one of each of the categories
    lower_case = set(string.ascii_lowercase)
    upper_case = set(string.ascii_uppercase)
    digits = set(string.digits)
    special_chars = set(string.punctuation)

    if not bool(special_chars & password_set):
        raise RuntimeError('password {} does not contain at least one special character'.format(password))
    
    if not bool(digits & password_set):
        raise RuntimeError('password {} does not containat least one digit'.format(password))
    
    if not bool(lower_case & password_set):
        raise RuntimeError('password {} does not containat least one lower case character'.format(password))
    
    if not bool(upper_case & password_set):
        raise RuntimeError('password {} does not containat least one upper case character'.format(password))


def check_password_unique(password):
    # load previous passwords from file
    with open("password-file.txt", "r+") as f:
        previous_pws = set(f.read().split())
        print(previous_pws)
        # check new password is not in set
        if (password in previous_pws):
            raise RuntimeError('password {} has been used before'.format(password))

    # write the new password to the file
    with open('password-file.txt', 'a') as file:
        file.write(password + '\n')


@plac.opt('password', help="the user generate password - will be checked against the rules")
@plac.flg('randompw', help="if set then a random password will be generated")
def main(password, randompw = False) :
    """
    A program to generate passwords - default behaviour is to request a password from the user

    """

    if (randompw):
        pw_characters = random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation,
                                       k=MINIMUM_LENGTH)
        password = ''.join(pw_characters)
    
    check_password_rules(password)

    check_password_unique(password)

    print('your password is: {}'.format(password))



if __name__ == '__main__':
    plac.call(main)
