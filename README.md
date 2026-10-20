# LUNAB Entreprenad & Transport – webbplats

Ny webbplats för LUNAB Entreprenad & Transport (Ekås 180, 442 98 Kode). Designen blandar de tre AMT Bygg-sajterna
(mörk filmisk hero, numrerade rubrikhuvuden, faktarad och svepande streck under heron) med S-Byggs knappar
(piller-knappar, runda Ring-knappar). Loggans orange (#e5651f) och grafit bär färgerna.

## Sidor

Allt ligger i `docs/` – öppna `docs/index.html` i en webbläsare.

- `index.html` – hero, faktarad, om oss, sex tjänstekort, varför LUNAB, bildgalleri, kontakt med karta
- `tjanster.html` – alla sex tjänster med ”Begär offert” som förväljer tjänsten i formuläret
- `om-oss.html`, `kontakt.html` (kontaktuppgifter, karta, offertformulär), `404.html`, `sitemap.xml`, `robots.txt`

Sidorna genereras av `scripts/build.py` (all text, tjänster och kontaktuppgifter). Ändra där och kör
`python3 scripts/build.py`. CSS och JS ligger i `docs/assets/`.

## Logga och bilder

- Loggan är LUNAB:s egen, hämtad från lunab.eu (`assets-src/`). `docs/img/lunab-logo-ljus.png` är samma logga med
  den grå texten gjord vit för mörk bakgrund; favicon är cirkelsymbolen.
- Alla foton är LUNAB:s egna: `grav-villa` och `gator` från lunab.eu, `hero-maskin`, `hjullastare-kvall`,
  `traktor-natt` och `markarbete-grus` från företagets Google Maps-profil. Profilen har 8 foton, men bara 4 gick att
  hämta automatiskt – resterande kan läggas till i `docs/img/` (både `namn.jpg` ca 1920 px och `namn-s.jpg` ca 820 px).
- Transport och Personaluthyrning saknar passande foto och visas därför som grafiska kort i loggans orange.

## Fakta – gå igenom före lansering

Endast verifierade uppgifter används: namn, adress, telefon, e-post, öppettid (”öppet till kl. 18” enligt Google
Maps) och de sex verksamhetsområdena. Inga årtal, certifieringar, maskinmodeller, kundprojekt, omdömen eller
garantier anges. Tjänstetexterna är neutrala förslag som LUNAB bör läsa igenom.

## Offertformuläret

Formuläret skickas via [FormSubmit](https://formsubmit.co) och visar tackmeddelandet först när servern bekräftat
att det gått fram – annars ett felmeddelande med telefon och e-post. Under förhandsvisningen går förfrågningarna
till Elevate Studio; byt `FORM_EMAIL` i `scripts/build.py` till `nicklas@lunab.eu` vid lansering (första förfrågan
till en ny adress skickar ett aktiveringsmejl).

## Publicera

`.github/workflows/deploy-pages.yml` publicerar `docs/` på GitHub Pages vid push. Byt `SITE_URL` i
`scripts/build.py` när sidan flyttas till lunab.eu.
