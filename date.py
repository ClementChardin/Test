def lire_date():
    with open("date.txt", "r") as ff:
        st = ff.readline()
        date = int(st.split(" = ")[1])
    return date

date = lire_date()

def incrementer_date():
    date = lire_date()
    with open("date.txt", "w") as ff:
        ff.write("date = " + str(date + 1))
