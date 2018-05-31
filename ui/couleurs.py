from PyQt4 import QtGui, QtCore

rouge  = QtGui.QColor(255, 0, 0)
vert  = QtGui.QColor(0, 255, 0)
orange  = QtGui.QColor(255, 127, 0)
jaune  = QtGui.QColor(238, 201, 0)
indian_red  = QtGui.QColor(205, 92, 92)
noir  = QtGui.QColor(0, 0, 0)
bleu = QtGui.QColor(0, 0, 255)
gris = QtGui.QColor(217, 217, 217)
blanc = QtGui.QColor(255, 255, 255)

couleurs_equipes = dict(AL = QtGui.QColor(51, 255, 51),
                        AL2 = QtGui.QColor(204, 102, 0),
                        ALT = QtGui.QColor(0, 0, 204),
                        ALT2 = QtGui.QColor(255, 0, 0),
                        APA = QtGui.QColor(0, 255, 128),
                        APA2 = QtGui.QColor(224, 224, 224),
                        BRB = QtGui.QColor(255, 128, 0),
                        BRB2 = QtGui.QColor(255, 0, 0),
                        BSK = QtGui.QColor(102, 21, 0),
                        BSK2 = QtGui.QColor(255, 255, 0),
                        CAT = QtGui.QColor(204, 0, 102),
                        CAT2 = QtGui.QColor(0, 128, 255),
                        DKF = QtGui.QColor(160, 160, 160),
                        DKF2 = QtGui.QColor(255, 102, 102),
                        DKW = QtGui.QColor(102, 102, 0),
                        DKW2 = QtGui.QColor(51, 0, 0),
                        ED = QtGui.QColor(0, 0, 102),
                        ED2 = QtGui.QColor(255, 255, 255),
                        ERE = QtGui.QColor(255, 0, 0),
                        ERE2 = QtGui.QColor(255, 255, 0),
                        FS = QtGui.QColor(0, 102, 0),
                        FS2 = QtGui.QColor(102, 0, 0),
                        GP = QtGui.QColor(0, 102, 102),
                        GP2  = QtGui.QColor(0, 102, 51),
                        HTH = QtGui.QColor(51, 255, 255),
                        HTH2 = QtGui.QColor(153, 255, 51),
                        KAK = QtGui.QColor(102, 21, 0),
                        KAK2 = QtGui.QColor(204, 204, 0),
                        KH = QtGui.QColor(255, 255, 102),
                        KH2 = QtGui.QColor(224, 224, 224),
                        KHR = QtGui.QColor(0, 0, 0),
                        KHR2 = QtGui.QColor(255, 0, 0),
                        KIS = QtGui.QColor(153, 0, 0),
                        KIS2 = QtGui.QColor(0, 0, 0),
                        MDL = QtGui.QColor(255, 0, 0),
                        MDL2 = QtGui.QColor(255, 255, 255),
                        MRB = QtGui.QColor(255, 153, 204),
                        MRB2 = QtGui.QColor(51, 153, 255),
                        MSL = QtGui.QColor(255, 255, 0),
                        MSL2 = QtGui.QColor(0, 0, 0),
                        PRG = QtGui.QColor(0, 0, 0),
                        PRG2 = QtGui.QColor(255, 255, 255),
                        QNL = QtGui.QColor(255, 255, 255),
                        QNL2 = QtGui.QColor(0, 102, 204),
                        SN = QtGui.QColor(102, 0, 102),
                        SN2 = QtGui.QColor(0, 102, 51),
                        TA = QtGui.QColor(255, 128, 0),
                        TA2 = QtGui.QColor(0, 0, 0),
                        TLB = QtGui.QColor(204, 0, 0),
                        TLB2 = QtGui.QColor(255, 255, 255),
                        TO = QtGui.QColor(255, 255, 0),
                        TO2 = QtGui.QColor(0, 153, 76),
                        Vide = QtGui.QColor(0, 0, 0),
                        Vide2 = QtGui.QColor(255, 255, 255),
                        vide = QtGui.QColor(0, 0, 0),
                        vide2 = QtGui.QColor(255, 255, 255),
                        AES = QtGui.QColor(204, 0, 0),
                        FST = QtGui.QColor(244, 100, 102),
                        KKR = QtGui.QColor(255, 0, 0),
                        MDH = QtGui.QColor(0, 102, 255),
                        AHK = QtGui.QColor(255, 255, 0),
                        CPH = QtGui.QColor(162, 190, 136),
                        MRT = QtGui.QColor(254, 72, 255),
                        MAG = QtGui.QColor(35, 57, 67),
                        BIL = QtGui.QColor(10, 157, 15),
                        EKR = QtGui.QColor(64, 217, 146),
                        AES2 = QtGui.QColor(0, 0, 0),
                        FST2 = QtGui.QColor(233, 214, 190),
                        KKR2 = QtGui.QColor(200, 91, 80),
                        MDH2 = QtGui.QColor(255, 255, 255),
                        AHK2 = QtGui.QColor(255, 0, 0),
                        CPH2 = QtGui.QColor(126, 42, 233),
                        MRT2 = QtGui.QColor(188, 146, 137),
                        MAG2 = QtGui.QColor(188, 206, 190),
                        BIL2 = QtGui.QColor(156, 227, 61),
                        EKR2 = QtGui.QColor(9, 42, 184),

                        ARA = QtGui.QColor(255, 239, 0),
                        B = QtGui.QColor(0, 102, 204),
                        CHS = QtGui.QColor(0, 0, 0),
                        CV = QtGui.QColor(204, 0, 0),
                        EMP = QtGui.QColor(0, 0, 204),
                        EN = QtGui.QColor(153, 0, 76),
                        ES = QtGui.QColor(0, 204, 0),
                        EST = QtGui.QColor(255, 255, 153),
                        HB = QtGui.QColor(51, 102, 0),
                        HE = QtGui.QColor(204, 255, 255),
                        HL = QtGui.QColor(0, 153, 153),
                        K = QtGui.QColor(220, 225, 255),
                        N = QtGui.QColor(255, 255, 0),
                        O = QtGui.QColor(102, 204, 0),
                        OG = QtGui.QColor(255, 0, 0),
                        S = QtGui.QColor(153, 153, 0),

                        ARA2 = QtGui.QColor( 224 , 129 , 217 ),
                        B2 = QtGui.QColor( 147 , 68 , 156 ),
                        CHS2 = QtGui.QColor( 20 , 233 , 254 ),
                        CV2 = QtGui.QColor( 78 , 224 , 160 ),
                        EMP2 = QtGui.QColor( 132 , 4 , 220 ),
                        EN2 = QtGui.QColor( 80 , 5 , 229 ),
                        ES2 = QtGui.QColor( 17 , 120 , 73 ),
                        EST2 = QtGui.QColor( 191 , 193 , 166 ),
                        HB2 = QtGui.QColor( 192 , 140 , 203 ),
                        HE2 = QtGui.QColor( 119 , 181 , 15 ),
                        HL2 = QtGui.QColor( 55 , 22 , 106 ),
                        K2 = QtGui.QColor( 160 , 213 , 6 ),
                        N2 = QtGui.QColor( 206 , 13 , 168 ),
                        O2 = QtGui.QColor( 53 , 152 , 240 ),
                        OG2 = QtGui.QColor( 98 , 172 , 204 ),
                        S2 = QtGui.QColor( 13 , 74 , 10 ),

                        ULT = QtGui.QColor(255, 0, 0),
                        ULTB = QtGui.QColor(0, 255, 0))

alpha  = 255
values_rouge = "{r}, {g}, {b}, {a}".format(r = rouge.red(),
                                     g = rouge.green(),
                                     b = rouge.blue(),
                                     a = alpha
                                     )

values_vert = "{r}, {g}, {b}, {a}".format(r = vert.red(),
                                     g = vert.green(),
                                     b = vert.blue(),
                                     a = alpha
                                     )

values_orange = "{r}, {g}, {b}, {a}".format(r = orange.red(),
                                     g = orange.green(),
                                     b = orange.blue(),
                                     a = alpha
                                     )
values_jaune = "{r}, {g}, {b}, {a}".format(r = jaune.red(),
                                           g = jaune.green(),
                                           b = jaune.blue(),
                                           a = alpha
                                           )
values_indian_red = "{r}, {g}, {b}, {a}".format(r = indian_red.red(),
                                           g = indian_red.green(),
                                           b = indian_red.blue(),
                                           a = alpha
                                           )

def get_colors(nom):
    coul = couleurs_equipes[nom].getRgb()
    tu1 = (coul[0]/255., coul[1]/255., coul[2]/255., coul[3]/255.)
    coul2 = couleurs_equipes[nom+'2'].getRgb()
    tu2 = (coul2[0]/255., coul2[1]/255., coul2[2]/255., coul2[3]/255.)
    figure()
    bar([0], [1], color=tu1, label=nom, width=1)
    bar([1], [1], color=tu2, label=nom+' 2', width=1)

def colorer_qlabel(lab, qcolor):
    pal = lab.palette()
    pal.setColor(lab.foregroundRole(), qcolor)
    lab.setPalette(pal)

