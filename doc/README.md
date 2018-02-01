# Webprogrammeren Informatiekunde

### Werkgroep IK21

Winston Lam,
Raphaël Koning,
Ruben Klarenaar

"ratemypet.nl"

# LET OP!!
> Om RateMyPet goed te laten werken zijn voor "upload" en de "giphy api" twee extra installaties nodig in de CS50 IDE omgeving. Om deze modules te installeren moeten in de terminal de volgende commands uitgevoerd worden:
$
$ pip install Flask-Uploads
$ pip install requests giphypop
$

## Samenvatting
> Het project zal bestaan uit een website / social-media waarop mensen foto’s van hun huisdier kunnen plaatsen en foto’s van anderen kunnen raten. Het is ook mogelijk om comments plaatsen, in deze comments kunnen gif’s worden gebruikt met de Giphy API.
Ook komt er een ranking met “Hottest of the week” en “Nottest of the week”, een pagina waarop de hoogst ge-rated post naast de laagst ge-rated post van de week staan. De site krijgt is gebaseerd op tinder, er staat steeds maar 1 post op de pagina. Wanneer je de foto rate gaat hij weg en komt er een nieuwe voor in de plaats.
De ranking is op een schaal van één tot vijf, deze . Eveneens komt er bij elke foto een report-button waarmee foto’s die ongepast of irrelevant zijn kunnen worden gereport.

## Schetsen
> Zie slack of GitHub

## Features

> Gebruikers kunnen publieke foto’s posten met of zonder begeleidende tekst.
Gebruikers kunnen posts van andere beoordelen waardoor de gemiddelde score van de post veranderd.
Gebruikers kunnen andere mensen volgen. Het aantal volgers is ook voor anderen te zien op je profielpagina.
Posts van gebruikers die je volgt komen bovenaan in je feed te staan.
Volgorde van de posts kunnen veranderd worden(van laag naar hoog, hoog naar laag of meest recent).
Posts kunnen gereport worden(bij niet relevante foto’s, nudity of je bent er door iemand op gezet en wil er af).
Gebruikers kunnen een status krijgen(door meedere keren een hoge of een lage score te krijgen bij posts enz..).
Gebruikers kunnen comments plaatsen onder posts van andere gebruikers.
Gebruikers kunnen gif’s plaatsen als comment. Het zal er zo uitzien als bij facebook,
Gebruikers kunnen anoniem foto’s posten
Gebruikers kunnen hun eigen profiel aanpassen(profielfoto, naam)
gebruikers kunnen hun volgers op een aparte pagina zien en die van anderen.
gebruikers kunnen zien wie zei volgen op een aparte pagina en van anderen.
Gebruikers kunnen andere gebruikers zoeken met behulp van een zoekfunctie

## Minimum viable product

> Gebruikers kunnen publieke foto’s posten met of zonder begeleidende tekst.
Gebruikers kunnen posts van andere beoordelen waardoor de gemiddelde score van de post veranderd.
Gebruikers kunnen andere mensen volgen.
Gebruikers kunnen comments plaatsen onder posts van andere gebruikers.
Gebruikers kunnen gif’s plaatsen als comment.
Gebruikers kunnen hun eigen profiel aanpassen(profielfoto, naam)


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
Sanity Check
We maken een project bouwend op de Photo sharing opdracht.
Gebruikers kunnen publiekelijk foto’s posten met of zonder begeleidende tekst. Alle gebruikers kunnen elkaar “volgen” en zo de foto’s bekijken en 💕. Gebruikers kunnen in plaats van een eigen foto ook een gif zoeken uit een online API zoals die van http://api.giphy.com.

> We zijn ervan overtuigd dat we met de omschrijving zoals wij die hebben gegeven en zoals we deze in gedachte voor ons zien, overeenkomt met de beschrijving zoals deze is gegeven in de studiewijzer.
