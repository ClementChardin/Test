# -*- coding: cp1252 -*-
"""
Liste des scripts / fichiers à exécuter :

1 : Pour créer les fichiers de la saison suivante
1_preparer_nouvelle_saison.py
1_script_mise_a_jour_budget.py
1_script_prestige.py

2 : Choisir qui part
2_departs.py

3 : Définir les besoins
3_script_definir_besoins_recrutements_clubs.py
%run script_master.py (les départs sont surlignés)

4 : Création des joueurs légendaires
scrip_creation_legendaires.py

5 : dans la console
> from ui.propositions_widget import *
> %matplotlib qt4
> TW = PropositionsWidget()
  TW.showMaximized()

6 : Recrutements
%run Partir/script_recrutement_widget.py

7 : évolution joueurs

8 : créations joueurs

7 : Choix des expoirs qui passent pro / restent / partent
from ui.espoirs_widget import *
%gui qt
ll = []
for nom in s.noms_clubs():
    ll.append(s.charger(nom, 'c'))
EW = EspoirsWidget(clubs=ll)
EW.showMaximized()


script_evolution_joueurs.py
script_evolution_tab.py
script_reinitialiser_clubs.py


"""
