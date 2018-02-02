# Webprogrammeren Informatiekunde

### Werkgroep IK21
Winston Lam,
Raphaël Koning,
Ruben Klarenaar

"ratemypet.nl"

# LET OP!!
> Om RateMyPet goed te laten werken zijn voor "upload" en de "giphy api" twee extra installaties nodig in de CS50 IDE omgeving. Om deze modules te installeren moeten in de terminal de volgende commands uitgevoerd worden:

$ pip install Flask-Uploads

$ pip install requests giphypop

## Productvideo
[Youtube](https://youtu.be/gUJM_SqKcvE)

## Samenvatting
> Het project bestaat uit een website / social-media waarop mensen foto’s van hun huisdier kunnen plaatsen en foto’s van anderen kunnen raten. Het is ook mogelijk om comments plaatsen, in deze comments kunnen gif’s worden gebruikt met de Giphy API.
Ook is er een ranking met “Hot”, een pagina waarop de hoogst ge-rated posts staan. De site is gebaseerd op tinder, er staat steeds maar 1 post op de pagina. Wanneer je de foto rate gaat hij weg en komt er een nieuwe voor in de plaats.
De ranking is op een schaal van één tot vijf. Eveneens komt er bij elke foto een report-button waarmee foto’s die ongepast of irrelevant zijn kunnen worden gereport, nadat vijf maal op deze reportbutton is geklikt door verschilllende gebruikers zal de foto verwijderd worden. Als van een gebruiker drie foto's zijn verwijderd, zal zijn account ook worden verwijderd.

## Screenshots
<img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Login_zpseaqi5rmf.png" alt="Login" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Register_zpsky6psxcu.png" alt="Register" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Feed_zpss6lapqhd.png" alt="Feed" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Userpage_zpsthwwf1no.png" alt="Userpage" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20My%20Userpage_zps4xhuktvi.png" alt="My Userpage" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Profile%20Pic%20Upload_zpslkto7rt6.png" alt="Upload Profile Picture" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Change%20Password_zps6oq1fctg.png" alt="Change Password" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Hotpage_zpst8tsbvpj.png" alt="Hotpage" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Search_zpsurut55d4.png" alt="Search" width="300px"> <img src="http://i1371.photobucket.com/albums/ag319/ruben_mhk/Screen%20Shot%20Upload_zpstdv4rl6e.png" alt="Upload" width="300px">

## Opbouw / Githubindeling
In het "Doc" directory zijn alle bestanden te vinden de uitleg of toelichting geven over het gebolwerkte project.
In het "static" directory hebben we twee subdirectories, "uploads" en "profile_pic" de inhoud spreekt hopelijk, voor zich. Daarnaast hebben we "dinkleberg.png" voor de apology pagina en "logo.png" voor het logo in de navbar. Eveneens hebben we het "stylesheet.css" bestand, verantwoordelijk voor alle styling de website.
In het "templates" directory staan alle .html bestanden voor het renderen van de pagina's.
In application.py en helpers.py, in het hoofd directory, zijn alle python/flask codes te vinden.
In database.db, in het hoofd directory

## Features
> Gebruikers kunnen publieke foto’s uploaden met een caption.
Gebruikers kunnen posts van anderen beoordelen waardoor de gemiddelde score van de post veranderd.
Gebruikers kunnen andere mensen volgen. Het aantal volgers is ook voor anderen te zien op je profielpagina.
Posts kunnen gereport worden.
Gebruikers kunnen comments plaatsen onder posts van andere gebruikers.
Gebruikers kunnen gif’s plaatsen als comment.
Gebruikers kunnen hun eigen profiel aanpassen(profielfoto, wachtwoord).
Gebruikers kunnen andere gebruikers zoeken met behulp van een zoekfunctie.
Gebruikers kunnen een hotpage bekijken met de hoogst ge-rate posts.

## Minimum viable product
> Gebruikers kunnen publieke foto’s posten met of zonder begeleidende tekst.
Gebruikers kunnen posts van andere beoordelen waardoor de gemiddelde score van de post veranderd.
Gebruikers kunnen andere mensen volgen.
Gebruikers kunnen comments plaatsen onder posts van andere gebruikers.
Gebruikers kunnen gif’s plaatsen als comment.
Gebruikers kunnen hun eigen profiel aanpassen(profielfoto, naam)

## Taakverdeling

Winston en Raphaël hebben zich met name op het Python/Flask gedeelte gefocussed. Ruben met name op het HTML/CSS/Jinja gedeelte. Echter is het zo dat iedereen zich met elke aspect van het project wel een aantal keer bezig heeft gehouden.

#### Afhankelijkheden Databronnen
1. Giphy API - https://developers.giphy.com/ / http://api.giphy.com/

#### Externe componenten
1. Github - http://www.github.com/
2. Mprog - https://webik.mprog.nl/

#### Concurrerende bestaande websites
1. Instagram - http://www.instagram.com/
2. Hot or Not - http://www.hotornot.nl/

## Moeilijkste delen
> Het opslaan van posts en zorgen dat deze op juiste manier worden weergegeven op de website.
Het managen en opslaan van de verschillende gebruikersaccounts.
Het ratingsysteem.

## Sanity Check
We maken een project bouwend op de Photo Sharing opdracht.
> Gebruikers kunnen publiekelijk foto’s posten met of zonder begeleidende tekst. Alle gebruikers kunnen elkaar “volgen” en zo de foto’s bekijken en 💕. Gebruikers kunnen in plaats van een eigen foto ook een gif zoeken uit een online API zoals die van http://api.giphy.com.

We zijn ervan overtuigd dat we met de omschrijving zoals wij die hebben gegeven en zoals we deze in gedachte voor ons zien, overeenkomt met de beschrijving zoals deze is gegeven in de studiewijzer.
