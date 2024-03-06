class Osoba():
    def __init__(self, imie, nazwisko) -> None:
        self.imie = imie
        self.nazwisko = nazwisko

    def __eq__(self, __value: object) -> bool:
        if self.imie == __value.imie and self.nazwisko == __value.nazwisko:
            return True
        return False

karol = Osoba("Karol", "Wojtyła")

print("== ", Osoba("Karol", "Wojtyła") == Osoba("Karol", "Wojtyła"))
print("== ", Osoba("Karol", "Wojtyła") == Osoba("Karol", "Nowak"))
print("is ", Osoba("Karol", "Wojtyła") is Osoba("Karol", "Wojtyła"))
print("is ", Osoba("Karol", "Wojtyła") is Osoba("Karol", "Nowak"))


if Osoba("Karol", "Wojtyła") == Osoba("Karol", "Wojtyła") and not Osoba("Karol", "Wojtyła") == Osoba("Karol", "Nowak"):
    print("xd")

print("id ", id(karol), " ", id(Osoba("Karol", "Wojtyła")))

print("int ", 1231232131231 is 1231232131231)

