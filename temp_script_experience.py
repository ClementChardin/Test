import selection as s

def age(jj, dat):
    return dat - jj.C

def bonus_atteints(jj, dat, atteint_precedant, xp_sais, res_xp):
    seuil = atteint_precedant + age(jj, dat) 
    xp = xp_sais + res_xp
    res_xp = xp
    atteint = atteint_precedant
    bonus = 0
    while res_xp >= seuil:
        bonus += 1
        atteint += 1
        res_xp -= seuil
        seuil += atteint
    return atteint, bonus, res_xp

def club_formateur(jj):
    if jj.anciens_clubs == '':
        return jj.club
    else:
        return jj.anciens_clubs.split(';')[0].split(' ')[0]

dd_xp_tot = {}
dd_xp_saison = {}
dd_bonus_atteints = {}
dd_residu_experience = {}
#dd_num_dernier_bonus = {}

for dat in (11, 12, 13, 14):
    key = 's_'+str(dat)
    key_prec = 's_'+str(dat-1)
    dd_xp_tot[key] = {}
    dd_xp_saison[key] = {}
    dd_bonus_atteints[key] = {}
    dd_residu_experience[key] = {}
    #dd_num_dernier_bonus[key] = {}
    print '\n', dat
    for nom in s.noms_clubs(dat):
        cc = s.charger(nom, 'c', dat)
        for jj in cc.get_all_joueurs():
            for dada in range(11, dat):
                if dada >= jj.C:
                    keke = 's_'+str(dada)
                    kjj = 's'+str(dada)
                    if jj.nom in dd_xp_saison[keke].keys():
                        jj.jj_passe[kjj].experience_saison = dd_xp_saison[keke][jj.nom]
                        jj.jj_passe[kjj].experience_total = dd_xp_tot[keke][jj.nom]
                        jj.jj_passe[kjj].num_dernier_bonus = dd_bonus_atteints[keke][jj.nom]
                        jj.jj_passe[kjj].residu_experience = dd_residu_experience[keke][jj.nom]
                    else:
                        print jj.nom, keke, 'not found'
                        jj.jj_passe[kjj].experience_saison = 0
                        jj.jj_passe[kjj].experience_total = 0
                        jj.jj_passe[kjj].num_dernier_bonus = 0
                        jj.jj_passe[kjj].residu_experience = 0

            if dat < 14:
                jj.nouveau_bonus_evolution = (jj.C >= 11)
                jj.bonus = 0
                jj.carte_evolution = {'valeur':0, 'couleur':1, 'r_nr':'n'}
                jj.evolution = 0

                xp_sais = jj.MJ1['CT'] + jj.MJ1['ST'] + .5*(jj.MJ1['CR'] + jj.MJ1['SR']) +\
                          jj.MJ2['CT'] + jj.MJ2['ST'] + .5*(jj.MJ2['CR'] + jj.MJ2['SR']) +\
                          jj.MJ3['CT'] + jj.MJ3['ST'] + .5*(jj.MJ3['CR'] + jj.MJ3['SR'])



                if dat == 11 or jj.C == dat or jj.ARM in ('K', 'EST', 'ARA') or club_formateur(jj) in s.noms_clubs_nord+s.noms_clubs_sud:
                    atteint_precedant = 0
                    res_xp = 0
                else:
                    atteint_precedant = dd_bonus_atteints[key_prec][jj.nom]
                    res_xp = dd_residu_experience[key_prec][jj.nom]

                atteint, bonus, res_xp = bonus_atteints(jj,
                                                        dat,
                                                        atteint_precedant,
                                                        xp_sais,
                                                        res_xp)

                if dat == 11 or jj.C == dat or jj.ARM in ('K', 'EST', 'ARA') or club_formateur(jj) in s.noms_clubs_nord+s.noms_clubs_sud:
                    xp_tot = xp_sais
                else:
                    cp_tot = dd_xp_tot[key_prec][jj.nom] + xp_sais

                dd_xp_saison[key][jj.nom] = xp_sais
                dd_xp_tot[key][jj.nom] = xp_tot
                dd_bonus_atteints[key][jj.nom] = atteint
                dd_residu_experience[key][jj.nom] = res_xp

                jj.experience_saison = xp_sais
                jj.experience_total = xp_tot
                jj.num_dernier_bonus = atteint
                jj.residu_experience = res_xp

            else:
                if not jj.C == 14:
                    jj.experience_saison = 0
                    jj.experience_total = dd_xp_saison['s_13'][jj.nom]
                    jj.num_dernier_bonus = dd_bonus_atteints['s_13'][jj.nom]
                    jj.residu_experience = dd_residu_experience['s_13'][jj.nom]

        cc.sauvegarder(dat)
            




