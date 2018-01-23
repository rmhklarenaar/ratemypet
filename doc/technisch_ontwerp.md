>Inlogpagina     Hier logt de user in (GET, POST)

>Registerpagina  Hier maakt de user een account aan (GET, POST)

>redircted naar index direct na register of inlog pagina
en te bereiken vanuit account_pagina, HOT, NOT
>index           Dit is de feed van de user (POST)

    ### deze pagina's kunnen bereikt worden vanuit de index pagina en elkaar
    account_pagina   Dit is de pagina van het account van de user, hier kan men ook andere opzoeken (GET, POST)
    HOT              Dit is de pagina waar de hoogst gerate foto's staan (GET, POST)
    NOT              Dit is de pagina waar de laagst gerate foto's staan (GET, POST)


    ### alleen bereikbaar via de account_pagina
    andere_mensen    Dit is de pagina van het account van andere personen (GET, POST)
    aanpas_pagina    Dit is de pagina waar users hun account kunnen aanpassen (POST)
    upload_pagina    Dit is de pagina waar users hun foto's kunnen uploaden (POST)
    Volgers_pagina   Dit is de pagina waar users hun volges kunnen bekijken (POST)
    Volgend_pagina   Dit is de pagina waar users kunnen zien wij zij volgen (POST)