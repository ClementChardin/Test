def recuperer_donnes(source, nouveau):
    """
    Recupere les attributs de source et les donne a nouveau
    nouveau est un objet nouvellement cree

    Ne retourne rien !

    Stocke les listes des attributs non recuperes car pas meme type ou
    AttributeError dans nouveau.pas_meme_type et nouveau.attribute_error
    
    Sert lorsqu'on ajoute un attribut a la definition de la classe
    """
    dd = nouveau.__dict__
    pas_meme_type = []
    attribute_error = []
    for attr, val in dd.items():
        if not callable(val):
            try:
                if type(getattr(nouveau, attr)) == type(getattr(source, attr)):
                    setattr(nouveau, attr, getattr(source, attr))
                else:
                    print attr, "n'a pas ete recupere car pas le meme type."
                    pas_meme_type.append(attr)
            except AttributeError:
                print attr, "AttributeError"
                attribute_error.append(attr)
    nouveau.pas_meme_type = pas_meme_type
    nouveau.attribute_error = attribute_error
