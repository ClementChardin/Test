from joueur import rang_new

def rang_armee(arm, carte):
    if arm == 'K':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('^')
        elif carte['valeur'] in (4, 5):
            return rang_new('<')
        elif carte['valeur'] in (6, 7):
            return rang_new('^^')
        elif carte['valeur'] in (8, 9):
            return rang_new('<<')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'EST':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('^')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<')
        elif carte['valeur'] in (7, 8):
            return rang_new('^^')
        elif carte['valeur'] == 9:
            return rang_new('<<<')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'ARA':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('^')
        elif carte['valeur'] in (4, 5):
            return rang_new('<')
        elif carte['valeur'] in (6, 7):
            return rang_new('^^')
        elif carte['valeur'] in (8, 9):
            return rang_new('<<')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'EMP':
        if carte['valeur'] in (1, 2, 3, 4):
            return rang_new('>')
        elif carte['valeur'] in (5, 6, 7, 8):
            return rang_new('^')
        elif carte['valeur'] in (9, ):
            return rang_new('<<')
        elif carte['valeur'] in (10,):
            return rang_new('^^')
        elif carte['valeur'] == 11:
            return rang_new('x')
        elif carte['valeur'] == 12:
            return rang_new('*')
        elif carte['valeur'] == 13:
            return rang_new('xx')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'CHS':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5):
            return rang_new('<')
        elif carte['valeur'] in (6, 7):
            return rang_new('^')
        elif carte['valeur'] in (8, 9):
            return rang_new('<<')
        elif carte['valeur'] == 10:
            return rang_new('^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'O':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('<')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('>')
        elif carte['valeur'] in (7, 8, 9):
            return rang_new('^')
        elif carte['valeur'] in (10, ):
            return rang_new('^^')
        elif carte['valeur'] == 11:
            return rang_new('*')
        elif carte['valeur'] == 12:
            return rang_new('x')
        elif carte['valeur'] == 13:
            return rang_new('xx')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'HE':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5):
            return rang_new('<')
        elif carte['valeur'] in (6, 7):
            return rang_new('^')
        elif carte['valeur'] in (8, ):
            return rang_new('<<')
        elif carte['valeur'] == 9:
            return rang_new('^^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] in (11, 12):
            return rang_new('*')
        elif carte['valeur'] in(13, 14):
            return rang_new('**')

    elif arm == 'B':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5):
            return rang_new('<')
        elif carte['valeur'] in (6, 7):
            return rang_new('^')
        elif carte['valeur'] in (8, ):
            return rang_new('<<')
        elif carte['valeur'] == 9:
            return rang_new('^^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] in (11, 12):
            return rang_new('*')
        elif carte['valeur'] in (13, 14):
            return rang_new('**')

    elif arm == 'N':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<')
        elif carte['valeur'] in (7, 8, 9):
            return rang_new('^')
        elif carte['valeur'] in (10, ):
            return rang_new('^^^')
        elif carte['valeur'] == 11:
            return rang_new('x')
        elif carte['valeur'] == 12:
            return rang_new('*')
        elif carte['valeur'] == 13:
            return rang_new('xx')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'ES':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('<')
        elif carte['valeur'] in (4, 5):
            return rang_new('^')
        elif carte['valeur'] in (6, 7):
            return rang_new('<<')
        elif carte['valeur'] in (8, 9):
            return rang_new('^^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

    elif arm == 'S':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('^')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<<')
        elif carte['valeur'] in (7, 8):
            return rang_new('^^')
        elif carte['valeur'] in (9, 10):
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('*')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('**')
        elif carte['valeur'] == 14:
            return rang_new('xx')

    elif arm == 'EN':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('^')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<<')
        elif carte['valeur'] in (7, 8, 9):
            return rang_new('^^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] in (11, 12):
            return rang_new('*')
        elif carte['valeur'] == 13:
            return rang_new('**')
        elif carte['valeur'] == 14:
            return rang_new('x')

    elif arm == 'CV':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<')
        elif carte['valeur'] in (7, 8, 9):
            return rang_new('^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] in (11, ):
            return rang_new('*')
        elif carte['valeur'] == 12:
            return rang_new('x')
        elif carte['valeur'] == 13:
            return rang_new('**')
        elif carte['valeur'] == 14:
            return rang_new('xx')

    elif arm == 'HL':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('>')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('<')
        elif carte['valeur'] in (7, 8, 9):
            return rang_new('^')
        elif carte['valeur'] == 10:
            return rang_new('^^^')
        elif carte['valeur'] in (11, ):
            return rang_new('*')
        elif carte['valeur'] == 12:
            return rang_new('x')
        elif carte['valeur'] == 13:
            return rang_new('**')
        elif carte['valeur'] == 14:
            return rang_new('xx')

    elif arm == 'HB':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('<')
        elif carte['valeur'] in (4, 5, 6):
            return rang_new('^')
        elif carte['valeur'] in (7, 8):
            return rang_new('^^')
        elif carte['valeur'] == 9:
            return rang_new('<<<')
        elif carte['valeur'] in (10, ):
            return rang_new('^^^')
        elif carte['valeur'] in (11, 12):
            return rang_new('*')
        elif carte['valeur'] == 13:
            return rang_new('**')
        elif carte['valeur'] == 14:
            return rang_new('xx')

    elif arm == 'OG':
        if carte['valeur'] in (1, 2, 3):
            return rang_new('<')
        elif carte['valeur'] in (4, 5):
            return rang_new('^')
        elif carte['valeur'] in (6, 7):
            return rang_new('^^')
        elif carte['valeur'] in (8, 9):
            return rang_new('<<<')
        elif carte['valeur'] in (10, ):
            return rang_new('^^^')
        elif carte['valeur'] == 12 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'r'):
            return rang_new('x')
        elif carte['valeur'] == 13 or \
             (carte['valeur'] == 11 and carte['r_n'] == 'n'):
            return rang_new('*')
        elif carte['valeur'] == 14:
            return rang_new('**')

