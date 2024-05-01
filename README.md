# tsoha-Topway

Topway on sovellus, jossa voit lähettää viestejä eri käyttäjille. Ensin luot tilisi ja kirjoitat muistiin tietoja itsestäsi.
Kun olet luonut tilisi, voit lisätä ystäviä firends-sivun kautta. Siellä näet myös jo lisätyt ystävät ja ihmiset, jotka ovat lähettäneet sinulle kaveripyynnön. Viestisivulla näet kaikki sinulle tai sinulta lähetetyt viestit. Sieltä voit myös lähettää omia viestejäsi.

# Sovelluksen nykyinen tilanne

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen
- Sovellus ilmoittaa käyttäjälle virheellisistä syötteistä
- Käyttäjä voi kirjoittaa lisätä tietoa itsestään
- Käyttäjä voi lähettää kaveripyyntöjä.
- Käyttäjä voi hyväksyä tai hylkää kaveri pyynnön, sekä poistaa lisätyn kaverin.
- Käyttäjä voi nähdä kaverin profiilin.
- Käyttäjä voi lähettää kaikille viestejä sekä vastaanottaa niitä.

# Käynnistysohjeet (lokaalisesti)

Taustavaatimukset:

- python3 ladattuna
- Pip (Python package manager)
- PostgreSQL ladattuna ja serveri on auki, ohjeita tietokannan käynnistykseen täältä --> https://github.com/hy-tsoha/local-pg

Kloonaa repositorio omalle koneellesi

`git clone https://github.com/acpeltol/Topway`

Siirry oikeaan hakemistoon, johon repositorio kloonattiin

Luo .env ympäristö tiedosto seuraavilla muuttujilla:

`DATABASE_URL=<tietokannan-paikallinen-osoite>`  
`SECRET_KEY=<salainen-avain>`  

Käynnistä virtuaaliympäristö

`python3 -m venv venv`  
`source venv/bin/activate`

Asenna Flask koneellesi

`pip install flask`

Jos PostreSQL-tietokanta asennettuna onnistuneesti koneelle serveri avataan ennen sovelluksen käynnistystä

`start-pg.sh`

Sovellus käyttää PostgreSQL-tietokantaa. Tietokannan skeema määritellään seuraavalla komennolla

`psql < schema.sql`

Käynnistä sovellus

`flask run`