
''' 
SCHEMAT ZAKUPOWY

NORMALIZACJA

# user: 1, maciek12, Maciek, maciek@wp.pl, 2137
# user: 2, karol12, Karol, karol@wp.pl, 21372

# product: 1, karma, 12, whiskas, 213123
# product: 2, gowno, 121, dupa, 12312314


    #Maciek 12 zmienia nick:

    # 1. Jest tak ustawione zeby zmiana nicku integrowala baze danych i wszystkie Maciek12 zmienia sie na nowy nick
    # 2. Baza danych zostaje niezmieniona i wszystkie zakupy Maciek12 zostaja tak jak są nieruszone
    # 3. Jezeli pojawi sie nowy Maciek12 to i tak bedzie mial inny primary_key
    # 
    # 4. Czy można ustawić db zakupy żeby brały tylko primary key innych tabel ?
    # 4. Odpowiedź : ForeginKey do ustawiania rekordu (rzędu) w innej tabeli. "Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)"
    # Co jeśli maciek12 kupi więcej niż jeden produkt
    # n-n relation
    #  inne relacje (1-1 np. | 1-n jeden-do-wielu | n-n wiele do wielu | )

# zamówienie: id (pk), id_user (fk), data, kwota
# zamówienie: 1, 1, 13.01.1212, 11
# zamówienie: 2, 2, 13.12.2137, 20

# zamówienie_detal: id_zamówienie_detal (pk), zamówienie_id (fk), id_produkt (fk), ilosc
# zamówienie_detal: 1, 1, 1, 2
# zamówienie_detal: 2, 1, 2, 7
# zamówienie_detal: 3, 1, 3, 2
# zamówienie_detal: 4, 2, 1, 2
# zamówienie_detal: 5, 2, 2, 1

Robisz jakiś endpoint np /add-to-cart przyjmujący POST
Na stronie robisz JavaScript który wykonuje asynchroniczny request (tj. taki który nie przeładowuje strony) 
tzn. AJAX endpoint /add-to-cart dostaje sesje usera (czy to możliwe?), produkt oraz ilość i dodaje mu te dane 
do jego słownika sesji endpoint zwraca JSON z aktualnym koszykiem usera






Jeśli chce wiedzieć więcej to zobaczę

teoria
- normalizacja 
    - https://devszczepaniak.pl/postaci-normalne/
    - https://pl.wikipedia.org/wiki/Posta%C4%87_normalna_(bazy_danych)
- ACID - atomicity, consistency, isolation, durability
    - https://pl.wikipedia.org/wiki/ACID
- CAP theroem
    - https://en.wikipedia.org/wiki/CAP_theorem

praktyka
- sharding - rozłożenie baz danych na kilka pomniejszych
- indexy - do optymalizacji wyszukiwania w tabeli
- transakcje - Poznanie koncepcji transakcji i transakcyjności w bazach danych.
- WHERE i JOIN. + optymalizacja zapytań
'''

'''
Docker zadanie domowe

1. Skonteneryzować aplikacje sklep zoo
2. Napisać docker-compose.yml który odpali !skonfigurowaną! baze danych mysql i sklep zoo

Rezultat:
Będę w stanie wziąć twoje repozytorium, ściągnąć je za pomocą git clone, odpalić docker compose up --build i otrzymać twoją aplikacje
'''

    #TODO LIST

    # Idempotency with HTTP Methods,  https://restfulapi.net/idempotent-rest-apis/ tabelka 2, https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/

    # czemu w panelu admina przy dodawaniu produktu nie ma dodawania do category id 

    # dodac search
       
    # Entity schema (nazwy encji powinny byc w pojedynczej), ERD online(zapytac Adama w czym robił)
    
    # ogarnąc żeby przy logowaniu nie było widac hasła gołym okiem w zbadaj źródło, payload (zoabczyc HTTPS co i jak, self certyfiakt 509)

    # dodać maxlength do inputow, ktore dotycza kolumn z ogranizczona liczba znakow

    # dodac walidacje danych otrzymywanych z frontu, zeby np. jako ilosc nie móc podać "aaaeee"

'''
Po zrobieniu api zrobić autoryzacje i token lata po froncie
'/auth -> [email, password] => token
token (id, roles: [ ] ) 
FE -> Authorization.header = Berearer <token>
'POST -> includes <token> -> decode -> roles.includes('admin)


'''

'''  


Folder "constants" (stałe) w aplikacji Flask może być używany do przechowywania stałych, które są używane w różnych częściach aplikacji. Jest to dobre praktyka, ponieważ pozwala to na scentralizowane zarządzanie stałymi i ułatwia zmiany w razie potrzeby.

W takim folderze możesz przechowywać różne rodzaje stałych, takie jak:

Stałe związane z konfiguracją aplikacji, takie jak nazwy baz danych, klucze API, adresy URL innych usług, itp.
Stałe związane z wiadomościami wyświetlanymi w interfejsie użytkownika, takie jak komunikaty o błędach, wiadomości sukcesu, teksty na przyciskach, itp.
Stałe związane z logiką biznesową, takie jak maksymalne długości pól formularza, wartości stałe wykorzystywane w obliczeniach, itp.
Przykładowa struktura folderu "constants" w aplikacji Flask mogłaby wyglądać tak:

arduino
Copy code
my_flask_app/
    app/
        constants/
            __init__.py
            config.py
            messages.py
            business_logic.py
        routes.py
        models.py
        templates/
        static/
    tests/
    config.py
    run.py
W pliku __init__.py w folderze "constants" możesz zdefiniować moduł jako pakiet, a następnie w poszczególnych plikach, takich jak config.py, messages.py, business_logic.py, przechowywać odpowiednie stałe w formie zmiennych lub klas.

Na przykład w pliku config.py możesz mieć:

python
Copy code
DEBUG = True
DATABASE_URI = 'sqlite:///mydatabase.db'
SECRET_KEY = 'super_secret_key'
W pliku messages.py możesz mieć:

python
Copy code
ERROR_MESSAGES = {
    'not_found': 'Nie znaleziono zasobu.',
    'unauthorized': 'Brak autoryzacji.'
}
W pliku business_logic.py możesz mieć:

python
Copy code
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 100
Następnie możesz importować te stałe w innych częściach swojej aplikacji, takich jak pliki routingu, modele, itp., co pozwoli uniknąć duplikacji kodu i ułatwi zmiany w stałych, gdy zajdzie taka potrzeba.









'''


# DO BYKA
# Ngin X docker i jak przesylac dockera do kogos ? i jak zrobic zeby kazdy mogl o danej porze sobie wejsc na strone 
# dodac do gitignore notes.py i usunac z poprzednich commitow

# DO STAJKIEGO
# Idempotency with HTTP Methods,  https://restfulapi.net/idempotent-rest-apis/ tabelka 2, czy flasgger np w add product to cart powinien zawsze zwracac to smao czy np dodawac do siebie nowe produkty

# zawsze liczba mnoga w linkach w route a potem single rzecz po id /api/products     api/products/1
# JWT TOKENY
# mcertyfikat SSL zeby po https lecialo
# content pod seo  jak powinien wygladac


# DO CAVIORA/ADAMA
# Idempotency with HTTP Methods,  https://restfulapi.net/idempotent-rest-apis/ tabelka 2, czy flasgger np w add product to cart powinien zawsze zwracac to smao czy np dodawac do siebie nowe produkty
# jak to jest z usuwaniem np kategori, jezeli chce usunac kategorie a nie moge bo baza danych wymaga zeby to bylo przez fk
"""

/api/product/ [ GET (localhost:5000/api/product?price_low=10&price_high=50) | POST | DELETE ] / filtrowanie produktów ?
- GET = pokaż produkty, możliwe filtrowanie
- POST = dodaj produkt
- DELETE = usuń produkty

"""

