class compo:
    def __init__(self):
        self.piliers = ["", ""]
        self.talon = [""]
        self.deuxiemes_lignes = ["", ""]
        self.troisiemes_lignes = ["", ""]
        self.numero_8 = [""]
        self.demi_melee = [""]
        self.demi_ouverture = [""]
        self.centre_1 = [""]
        self.centre_2 = [""]
        self.ailiers = [""]
        self.arriere = [""]
        
        self.seize = [""]
        self.dix_sept = [""]
        self.dix_huit = [""]
        self.dix_neuf = [""]
        self.vingt = [""]
        self.vingt_un = [""]
        self.vingt_deux = [""]

def creer_compo():
    c = compo()
    c.piliers = [raw_input('pilier1'), raw_input('pilier2')]
    c.talon = [raw_input('talon')]
    c.deuxiemes_lignes = [raw_input('deuxieme ligne 1'),  raw_input('deuxieme ligne 2')]
    c.troisiemes_lignes = [raw_input('troisieme ligne 1'), raw_input('troisieme ligne 2')]
    c.numero_8 = [raw_input('numero 8')]
    c.demi_melee = [raw_input('demi de melee')]
    c.demi_ouverture = [raw_input('demi d\'ouverture')]
    c.centre_1 = [raw_input('premier centre')]
    c.centre_2 = [raw_input('deuxieme centre')]
    c.ailiers = [raw_input('ailier 1'), raw_input('ailier 2')]
    c.arriere = [raw_input('arriere')]
    
    c.seize = [raw_input('16')]
    c.dix_sept = [raw_input('17')]
    c.dix_huit = [raw_input('18')]
    c.dix_neuf = [raw_input('19')]
    c.vingt = [raw_input('20')]
    c.vingt_un = [raw_input('21')]
    c.vingt_deux = [raw_input('22')]

    return c
    
