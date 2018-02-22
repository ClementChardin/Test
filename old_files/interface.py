# -*- coding: cp1252 -*-
from Tkinter import *
import selection as s
import pickle

class Interface(Frame):
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        
        self.pack1 = PanedWindow(self, orient=HORIZONTAL)        
        self.pack1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        self.pack11 = PanedWindow(self.pack1, orient=VERTICAL)        
        self.pack11.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)
        
        self.pack1.add(self.pack11)

        """
        Liste des noms de clubs
        """
        self.frame110 = Frame(self.pack11)
        self.pack11.add(self.frame110)

        """
        Barre de défilement de la liste des noms de club
        """
        self.vsb = Scrollbar(self.frame110, orient=VERTICAL)
        self.vsb.grid(row=0, column=0, sticky=N+S)
        self.c = Canvas(self.frame110,yscrollcommand=self.vsb.set)
        self.c.grid(row=0, column=1, sticky="news")
        self.vsb.config(command=self.c.yview)
        self.frame110.grid_rowconfigure(0, weight=1)

        """
        Ajout des choix possibles
        """
        self.frame11 = Frame(self.c)
        self.var_choix = StringVar()
        for nom in sorted(s.noms_clubs):
            choix = Radiobutton(self.frame11, text=nom, variable=self.var_choix, value=nom, command=self.commande_radio)
            choix.pack()

        self.c.create_window(0, 0,  window=self.frame11)
        self.frame11.update_idletasks()
        self.c.config(scrollregion=self.c.bbox("all"))

        """
        Caracs de la compo en cours
        """
        self.caracs = Label(self.pack11, text=afficher_car(self.charger_equipe().compo_defaut.caracs_old), background='white', anchor="w", justify=LEFT)
        self.pack11.add(self.caracs)

        """
        Totaux de la compo en cours
        """
        self.totaux = Label(self.pack11, text=afficher_tot(self.charger_equipe().compo_defaut.totaux_old), background='white', anchor="w", justify=LEFT)
        self.pack11.add(self.totaux)

        """
        Compo en cours
        """
        self.pack12 = PanedWindow(self.pack1, orient=VERTICAL)        
        self.pack12.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)
        
        self.pack1.add(self.pack12)

        self.compo = Label(self.pack12, text=afficher_comp(self.charger_equipe().compo_defaut.joueurs), background='white', anchor="w", justify=LEFT)
        self.pack12.add(self.compo)

        """
        Roles compo en cours
        """
        self.roles = Label(self.pack12, text=afficher_roles(self.charger_equipe().compo_defaut.roles), background='white', anchor="w", justify=LEFT)
        self.pack12.add(self.roles)

        """
        Liste des postes
        """
        self.pack13 = PanedWindow(self.pack1, orient=VERTICAL)        
        self.pack13.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)
        self.pack1.add(self.pack13)

        self.frame13 = Frame(self.pack13)
        self.liste_postes = Listbox(self.frame13)
        for k in self.charger_equipe().joueurs.keys():
            self.liste_postes.insert(END, k)
        self.liste_postes.pack()
        self.pack13.add(self.frame13)
        self.liste_postes.bind('<Button-1>', self.clic)

        """
        Liste des joueurs qui jouent au(x) poste(s) selectionne(s)
        """
#        self.joueurs_a_montrer = Label(self.pack12, text=self.clic('<Button-1>'), background='white', anchor="w", justify=LEFT)
#        self.pack13.add(self.joueurs_a_montrer)        
        """
        dernière ligne du code
        """
        self.pack1.pack()
        
    def charger_equipe(self):
        nom = self.var_choix.get()
        if nom != '':
            return s.charger(nom, 'c')
        else:
            return s.club(nom='')
        
    def commande_radio(self):
        commande_radio = self.caracs.configure(text=afficher_car(self.charger_equipe().compo_defaut.caracs_old), background='white', anchor="w", justify=LEFT)
        commande_radio = self.totaux.configure(text=afficher_tot(self.charger_equipe().compo_defaut.totaux_old), background='white', anchor="w", justify=LEFT)
        commande_radio = self.compo.configure(text=afficher_comp(self.charger_equipe().compo_defaut.joueurs), background='white', anchor="w", justify=LEFT)
        commande_radio = self.roles.configure(text=afficher_roles(self.charger_equipe().compo_defaut.roles), background='white', anchor="w", justify=LEFT)

    def clic(self,evt):
        index = self.liste_postes.curselection()
        if index == '':
            return ''
        else:
            return self.liste_postes.get(index)

def afficher_dict(d):
    st = ''
    for k, v in d.items():
        if st == '':
            st += k + ' : ' + str(v)
        else:
            st += '\n' + k + ' : ' + str(v)
    return st

def afficher_car(caracs):
    st = ''
    for k, v in sorted(caracs.items(), key = lambda (k,v): s.ordres_caracs_compo[k]):
        if st == '':
            st += k + ' : ' + str(v)
        else:
            st += '\n' + k + ' : ' + str(v)
    return st

def afficher_tot(totaux):
    st = ''
    for k, v in sorted(totaux.items(), key = lambda (k,v): k.split('T')[1]):
        if st == '':
            st += k + ' : ' + str(v)
        else:
            st += '\n' + k + ' : ' + str(v)
    return st

def afficher_comp(d):
    st = ''
    for k, v in sorted(d.items(), key = lambda (k,v): int(k.split('n')[1])):
        if st != '':
            st += '\n'
        st += k + ' - ' + v.nom + ' : '
        poste = v.postes['poste1']
        i = 1
        while poste != '':
            if poste in ['C1', 'CE']:
                st += ' C1 ' + str('%0.2f' % s.calc_EV(v, 'C1')) + ' C2 ' + str('%0.2f' % s.calc_EV(v, 'C2'))
            elif poste == 'C2':
                st += ' C2 ' + str('%0.2f' % s.calc_EV(v, 'C2')) + ' C1 ' + str('%0.2f' % s.calc_EV(v, 'C1'))
            else:
                st += ' ' + poste + ' ' + str('%0.2f' % s.calc_EV(v, poste))
            i += 1
            if i < 3:
                poste = v.postes['poste'+str(i)]
            else:
                poste = ''
    return st

def afficher_roles(roles):
    st = ''
    for k, v in sorted(roles.items(), key = lambda (k,v): s.ordre_roles[k]):
        if st != '':
            st += '\n'
        st += k + ' : ' + v.nom + ' - ' + s.carac_roles[k] + ' : ' + str(v.caracs[s.carac_roles[k]])
    return st

def afficher_joueurs(joueurs):
    st = ''
    for k, v in sorted(joueurs.items(), key = lambda (k,v): s.ordre_postes[k]):
        if st != '':
            st += '\n'
        st += k
        for jj in v:
            st += '\n' + jj.nom
            poste = jj.postes['poste1']
            i = 1
            while poste != '':
                if poste in ['C1', 'CE']:
                    st += ' C1 ' + str('%0.2f' % s.calc_EV(jj, 'C1')) + ' C2 ' + str('%0.2f' % s.calc_EV(jj, 'C2'))
                elif poste == 'C2':
                    st += ' C2 ' + str('%0.2f' % s.calc_EV(jj, 'C2')) + ' C1 ' + str('%0.2f' % s.calc_EV(jj, 'C1'))
                else:
                    st += ' ' + poste + ' ' + str('%0.2f' % s.calc_EV(jj, poste))
                i += 1
                if i < 3:
                    poste = jj.postes['poste'+str(i)]
                else:
                    poste = ''
    return st
