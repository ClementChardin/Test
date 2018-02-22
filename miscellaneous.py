from numpy import random

def d6():
	return random.random_integers(6)

def d3():
	return random.random_integers(3)

def d4():
	return random.random_integers(4)

def tirer_carte():
	"""
	renvoie un dict {valeur, couleur, r_n}
	avec :
	valeur = numero carte (11=valet, 12=dame, 13=roi et 14=jocker)
	couleur : 1=pique, 2=coeur, 3=trefle, 4=carreau
	r_n : 'r'=rouge, 'n'=noir
	"""
	carte = random.random_integers(54)
	if carte in (53, 54):
		return dict(valeur=14,
                            couleur=None,
                            r_n='r' if carte == 53 else 'n')
	else:
                val = 13 if carte % 13 == 0 else carte % 13
                coul = carte / 13 if carte % 13 == 0 else carte / 13 + 1
                r_n_ = 'r' if coul % 2 == 0 else 'n'
		return dict(valeur=val, couleur=coul, r_n=r_n_)

				
def d3_plus(carte=None):
	if carte is None:
                carte = tirer_carte()
	if carte["valeur"] == 14 :
		return 5
	elif carte["valeur"] == 13:
		return 4
	elif carte["valeur"] == 1:
		return 0
	else:
		return carte["valeur"]/4 if carte["valeur"] % 4 == 0 else carte["valeur"]/4 +1

def d2_plus(carte=None):
	if carte is None:
                carte = tirer_carte()
	if carte["valeur"] == 14:
		return 4
	elif carte["valeur"] == 13:
		return 3
	elif carte["valeur"] == 1:
		return 0
	elif carte["valeur"] < 7:
		return 1
	else:
		return 2

def d1_plus(carte=None):
	if carte is None:
                carte = tirer_carte()
	if carte["valeur"] in (14, 13) :
		return 3
	elif carte["valeur"] == 12:
		return 2
	elif carte["valeur"] < 7:
		return 0
	else:
		return 1

def d0_plus(carte=None):
	if carte is None:
                carte = tirer_carte()
	if carte["valeur"] in (14, 13) :
		return 2
	elif carte["valeur"] in (12, 11):
		return 1
	elif carte["valeur"] == 1:
		return -1
	else:
		return 0
def d6_plus(carte=None):
	if carte is None:
                carte = tirer_carte()
	if carte["valeur"] == 14:
		return 8
	elif carte["valeur"] == 13:
                return 7
	elif carte["valeur"] == 1:
		return 0
	else:
		return (carte["valeur"]+1)/2

def lettre():
        carte = tirer_carte()
        if carte["valeur"] == 14:
                return "Jocker !"
        else:
                k = 1 if carte["r_n"] == "r" else 2
                return chr(96 + k*carte["valeur"])
