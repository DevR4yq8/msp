# Kompletny Bot Discord by DevR4yq

Witaj, szefie! To jest kompletna dokumentacja i instrukcja obsługi twojego nowego, wszechpotężnego bota. Wszystko, co musisz wiedzieć, jest tutaj.

---

## 🚀 1. Instalacja i Konfiguracja (krok po kroku)

### a) Wymagania
- Python 3.8+
- Konto Discord

### b) Konfiguracja Plików
1.  Upewnij się, że masz taką strukturę plików:
    ```
    bot/
    ├── main.py
    ├── database.py
    ├── cogs/
    │   ├── moderation.py
    │   ├── tickets.py
    │   ├── giveaway.py
    │   ├── automod.py
    │   ├── events.py
    │   ├── selfroles.py
    │   └── logging.py
    ├── .env
    └── requirements.txt
    ```
2.  W pliku `.env` wklej swój token i ID serwera:
    ```.env
    DISCORD_TOKEN=TUTAJ_WKLEJ_SWÓJ_TOKEN
    GUILD_ID=TUTAJ_WKLEJ_ID_TWOJEGO_SERWERA
    ```
    *(Aby uzyskać ID serwera, włącz Tryb Dewelopera w Discordzie, kliknij PPM na ikonę serwera i "Kopiuj ID serwera")*

### d) Uruchomienie
1.  Otwórz terminal/konsolę w folderze `bot/`.
2.  Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`
3.  Uruchom bota: `python main.py`
4.  Bot powinien być online!

### e) Konfiguracja Uprawnień Bota na Serwerze
1.  Zaproś bota na serwer używając linku wysłanego przez DevR4yq
2.  Na swoim serwerze wejdź w `Ustawienia serwera` -> `Role`.
3.  Znajdź rolę z nazwą swojego bota i **przeciągnij ją na samą górę listy ról**. To jest MEGA ważne, żeby bot miał władzę nad innymi rolami.

---

## 📚 2. Książka Komend

Oto lista wszystkich zabawek, które stworzyliśmy.

### Moderacja
| Komenda | Opis | Przykład Użycia | Wymagane Uprawnienia |
| :--- | :--- | :--- |:--- |
| `/kick` | Wyrzuca użytkownika z serwera. | `/kick @Użytkownik powód: Byłeś niegrzeczny` | `Wyrzucanie członków` |
| `/ban` | Banuje użytkownika na serwerze. | `/ban @Użytkownik powód: Złamanie regulaminu` | `Banowanie członków` |
| `/mute` | Wycisza użytkownika na określony czas. | `/mute @Użytkownik minutes:10 powód: Spam` | `Wyciszanie członków` |
| `/clear` | Usuwa określoną liczbę wiadomości (1-100).| `/clear amount:50` | `Zarządzanie wiadomościami`|
| `/warn` | Daje użytkownikowi ostrzeżenie (zapis w bazie). | `/warn @Użytkownik powód: Obrażanie innych` | `Wyrzucanie członków` |
| `/warnings`| Sprawdza listę ostrzeżeń danego usera. | `/warnings @Użytkownik` | `Wyrzucanie członków` |

### Giveawaye
| Komenda | Opis | Przykład Użycia | Wymagane Uprawnienia |
| :--- | :--- | :--- |:--- |
| `/giveaway`| Tworzy nowy konkurs. | `/giveaway minutes:60 prize:Nitro winners:2`| `Zarządzanie serwerem`|
| `/reroll` | Losuje nowego zwycięzcę. | `/reroll message_id:123456789012345678` | `Zarządzanie serwerem`|

### Role
| Komenda | Opis | Przykład Użycia | Wymagane Uprawnienia |
| :--- | :--- | :--- |:--- |
| `/panel-rol` | Tworzy panel z przyciskami do samo-roli. | `/panel-rol` (na wybranym kanale) | `Zarządzanie rolami` |

### Tickety
| Komenda | Opis | Przykład Użycia | Wymagane Uprawnienia |
| :--- | :--- | :--- |:--- |
| `/panel-ticketow` | Tworzy panel do otwierania ticketów. | `/panel-ticketow` (na wybranym kanale) | `Zarządzanie serwerem` |

---
**Pamiętaj, słodziaku: z wielką mocą wiąże się wielka zabawa! ;)**