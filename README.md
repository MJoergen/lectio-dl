# Installation
Lige nu findes programmet til Windows kun. Du kan hente programmet her (vælg den version, der passer til dit styresystem):
* [Windows 10 (64-bit)](http://mjoergen.eu/lectio-dl.zip)
* [Windows 7 (64-bit)](http://mjoergen.eu/lectio-dl-win7-64bit.zip)

Så skal du pakke zip-filen ud og lægge den i roden af din harddisk (C:\lectio-dl)

Så skal du dobbelt-klikke på filen **lectio-dl.exe**

Du vil nu blive bedt om at indtaste din skoles navn, og derefter dit brugernavn og kodeord til lectio.

# Ofte stillede spørsgsmål (FAQ)
## Hvad er lectio-dl?
Det er et lille program til at hente alle dine dokumenter på lectio til din computer!
## Hvilke filer bliver hentet?
Alle filer, som ligger under 'Dokumenter' på lectio, bliver hentet ned til din computer.
## Hvorfor er dette program lavet?
Fordi alle skoler skal stoppe brugen af lectio, se her: [Brev om dispensation fra STIL](http://www.stil.dk/-/media/STIL/Filer/PDF16/160526-Brev-om-dispensation-til-DG-og-DEL,-d-,docx.ashx)
## Er det sikkert?
Dette program gør kun som beskrevet. Men hvis sikkerhed betyder meget, så bør man sørge for at ændre sit lectio-kodeord før og efter at have brugt dette program.
## Hvor lang tid tager det?
Det kan godt tage over en time at hente alle sine dokumenter ned, afhængig af antal og størrelse.
## Virker programmet som lovet?
Ja, bortset fra, at filer som ligger under "Opgaver", eller som er vedhæftet "Beskeder", bliver ikke taget med.

# For udviklere
Programmet kan også køres direkte fra Python, hvis man har [Python 2.7](https://www.python.org/) er installeret. Følgende moduler skal så også installeres:
* requests
* python-dateutil
