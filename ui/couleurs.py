from PyQt4 import QtGui, QtCore

rouge  = QtGui.QColor(255, 0, 0)
vert  = QtGui.QColor(0, 255, 0)
orange  = QtGui.QColor(255, 127, 0)
jaune  = QtGui.QColor(238, 201, 0)
indian_red  = QtGui.QColor(205, 92, 92)
noir  = QtGui.QColor(0, 0, 0)
bleu = QtGui.QColor(0, 0, 255)

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
                        ERE = QtGui.QColor(220, 30, 186),
                        ERE2 = QtGui.QColor(30, 186, 220),
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
                        KIS = QtGui.QColor(255, 255, 255),
                        KIS2 = QtGui.QColor(255, 10, 20),
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
                        TO = QtGui.QColor(255, 255, 0),
                        TO2 = QtGui.QColor(0, 153, 76),
                        Vide = QtGui.QColor(0, 0, 0),
                        Vide2 = QtGui.QColor(255, 255, 255),
                        vide = QtGui.QColor(0, 0, 0),
                        vide2 = QtGui.QColor(255, 255, 255),
                        AES = QtGui.QColor(255, 255, 255),
                        FST = QtGui.QColor(255, 255, 255),
                        KKR = QtGui.QColor(255, 255, 255),
                        MDH = QtGui.QColor(255, 255, 255),
                        AHK = QtGui.QColor(255, 255, 255),
                        CPH = QtGui.QColor(255, 255, 255),
                        MRT = QtGui.QColor(255, 255, 255),
                        MAG = QtGui.QColor(255, 255, 255),
                        BIL = QtGui.QColor(255, 255, 255),
                        EKR = QtGui.QColor(255, 255, 255),
                        AES2 = QtGui.QColor(0, 0, 0),
                        FST2 = QtGui.QColor(0, 0, 0),
                        KKR2 = QtGui.QColor(0, 0, 0),
                        MDH2 = QtGui.QColor(0, 0, 0),
                        AHK2 = QtGui.QColor(0, 0, 0),
                        CPH2 = QtGui.QColor(0, 0, 0),
                        MRT2 = QtGui.QColor(0, 0, 0),
                        MAG2 = QtGui.QColor(0, 0, 0),
                        BIL2 = QtGui.QColor(0, 0, 0),
                        EKR2 = QtGui.QColor(0, 0, 0),

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
