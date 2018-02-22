import selection as s

class EquipeMatch():
    def __init__(self, nom, comp, match=None, c_ou_s='c'):
        self.nom = nom
        self.comp = comp
        self.match = match
        self.c_ou_s = c_ou_s
        self.equipe = s.charger(nom, self.c_ou_s)
        if self.c_ou_s == 's':
            self.points_championat = self.equipe.points_championat
        self.bonus_def = False

        #la compo avec seulement les 15 joueurs sur le terrain
        #amenée à évoluer avec les remplacements
        self.comp_XV = s.compo()
        for nn in range(1, 16):
            key = 'n' + str(nn)
            self.comp_XV.joueurs[key] = self.comp.joueurs[key]
        for rol in self.comp_XV.roles.keys():
            self.comp_XV.roles[rol] = self.comp.roles[rol]
        s.set_caracs_old_compo(self.comp_XV, self.equipe, fatigue=True)
        self.comp_XV.calc_totaux_old()

        #Les points sont notes sous forme de liste de dict (k=nom, v=nombre)
        self.dict_essais = dict()
        self.dict_transformations = dict()
        self.dict_transformation_ratees = dict()
        self.dict_drops = dict()
        self.dict_drop_rates = dict()
        self.dict_penalites = dict()
        self.dict_penalite_ratees = dict()
        self.dict_rouges = dict()
        self.dict_jaunes = dict()
        self.dict_blessures = dict()

        #Pour les stats
        self.occase_essai = 0
        self.occase_penalite = 0
        self.occase_melee = 0
        self.occase_touche = 0

    @property
    def autre_equipe(self):
        return self.match.eq1 if self.match.eq2==self else self.match.eq2

    @property
    def essais(self):
        res = 0
        for n in self.dict_essais.values():#nombres:
            res += n
        return res
    
    @property
    def transformations(self):
        res = 0
        for n in self.dict_transformations.values():#nombres:
            res += n
        return res
    
    @property
    def drops(self):
        res = 0
        for n in self.dict_drops.values():#nombres:
            res += n
        return res
    
    @property
    def penalites(self):
        res = 0
        for n in self.dict_penalites.values():#nombres:
            res += n
        return res

    @property
    def bonus_off(self):
        return True if self.essais >= 4 else False
    
    @property
    def score(self):
        return 5*self.essais + 2*self.transformations + 3*(self.drops + self.penalites)

    def set_dict_score(self, option, separateur=', '):
        if not option in ["essais", "transformations", "drops", "penalites"]:
            raise ValueError("Wrong option ! Got " + option)
        attribut = self.dict_essais if option=="essais" \
                   else self.dict_transformations if option=="transformations" \
                   else self.dict_drops if option=="drops" \
                   else self.dict_penalites

        l = raw_input("Lister les joueurs aillant marque des " \
                      + option \
                      + " pendant le match " \
                      + " pour " \
                      + self.nom \
                      + " ")
        for nom in l.split(separateur):
            if nom in attribut.keys():
                attribut[nom] += 1
            else:
                attribut[nom] = 1

    def changement(self, key_sortant, key_entrant, forcer_mauvais_poste=False):
        print self.comp_XV.joueurs[key_sortant].nom, "sort", \
              self.comp.joueurs[key_entrant].nom, "entre"
        jj_entrant = self.comp.joueurs[key_entrant]
        poste = s.corres_num_poste[key_sortant]
        #Comme le sortant a un num <= 15, poste est un seul poste
        #Pour nes n16 à n22 poste est par exemple "TL N8"
        if s.ne_joue_pas([poste], jj_entrant):
            raise ValueError(jj_entrant.nom + " ne joue pas " + poste + " !")
        self.comp_XV.joueurs[key_sortant] = jj_entrant
        s.set_caracs_old_compo(self.comp_XV, self.equipe, fatigue=True)
        self.comp_XV.calc_totaux_old()
        
