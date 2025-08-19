# Aplikacja Movie Database - projekt na wcześniejsze zaliczenie
Projekt został przygotowany przy pomocy biblioteki django oraz z wykorzystaniem HTML i CSS. Wszystkie użyte biblioteki zostały spisane w pliku requirements.txt.<br>
Składa się z 3 modeli: Movie, Rating i Bookmark. Pierwszy model zawiera infomacje o filmie, kolejne 2 infomację o ocenie oraz zakładce dla filmów.
## Strona główna
<img title="main-page" alt="Main page" src="screens/main_page.png">
Strona główna składa się z navbara, na którym znajdują się odnośniki do poszczególnych podstron. Żeby mieć do nich dostęp użytkownik musi być zalogowany. W przeciwnym przypadku przyciski nie wyświetlą się i będzie jedynie dostęp do strony logowania lub rejestracji. <br>
Dodatkowo znajduje się panel z filmami na czasie. Są one wyświetlane na podstawie tabeli z ocenami użytkowników dla poszczególnych filmów. Klikając w tytuł filmu zostaniemy przeniesieni do strony z infomacjami na jego temat.

## Lista filmów
<img title="movielist-page" alt="Movie list page" src="screens/movie_list_page.png">
Po kliknięciu w przycisk movies zostaniemy przeniesieni na stronę z listą filmów. Zawiera one wszystkie filmy dodane do bazy danych. Jeżeli lista będzie zbyt długa, tabela zostanie podzielona na strony w celu łatwiejszego przeglądania. Filmy mogą być filtrowane przy pomocy dostępnego formularza. Każdy film może zostać dodany do zakładek użytkownika. Zakładki są przechowywane w specjalnej do tego tabeli.
Dla osób z rangą MovieEditor dostępny jest przycisk "Add movie", który przeniesie nas do strony z formularzem dodawania filmu.
<img title="add-movie-page" alt="Add movie page" src="screens/add_movie_page.png">

## Profil użytkownika
<img title="profile_page" alt="Profile page" src="screens/profile_page.png">
Strona ta zawiera wszystkie informacje przechowywane na temat użytkownika. Tabela poniżej jest połączeniem tabel z zakładkami i ocenami. Przedstawia wystawione oceny i zakładki użytkownika. 

## Informacje o filmie
<img title="movie_page" alt="movie page" src="screens/movie_page.png">
Strona z informacjami o filmie. Można dodać zakładkę i ocenę. Liczba zakładek się dynamicznie zmienia. Tabela ocen użytkowników.

## Logowanie, rejestracja i reset hasła
<img title="login_page" alt="login page" src="screens/login_page.png">
<img title="register_page" alt="register page" src="screens/register_page.png">
<img title="reset_password_page" alt="reset_password page" src="screens/reset_password.png">

Po zalogowaniu/wylogowaniu przenosiemy się na stronę główną. <br>
Po wpisaniu maila w konsoli zostanie wypisana treść maila wzraz z linkiem do resetu hasła (jeśli mail był w bazie danych).
