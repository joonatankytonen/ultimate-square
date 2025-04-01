# ultimate-square

SeAMK:n ohjelmistoprojekti kurssin ryhmätyö, jossa tehtiin pythonin pygame frameworkilla videopeli, nimeltään Ultimate Square.

Voidaksesi pelata peliä, voit joko ladata Releases kohdasta zippi tiedoston, joka sisältää windowsin .exe tiedoston ja muut pelin tarvitsemat assetit ja ajaa vain .exe tiedoston pelataksesi peliä tai voit ajaa pelin manuaalisesti alla olevilla ohjeilla.

---

## Ohjeet ultimate-squaren manuaalisen ajamiseen.

Voidaksesi pelata peliä manuaalisesti on sinun ensin kloonattava tämä repo tai asentaa tiedostot zippinä. Kun tämä on tehty, mene ultimate-square hakemiston sisään terminaalissa. Suosittelemme tekemään ultimate-square hakemiston sisälle virtual environmentin. Virtual environment asennetaan pythonilla, jos sinulla ei ole pythonia asennettuna, asenna se. Tämän jälkeen voit käyttää komentoa `python -m venv venv` tai `py -m venv venv` tehdäksesi virtual environmentin. Tämän komennon viimeinen venv ei ole pakko olla nimeltään venv, tämä vain on virtual environment hakemiston nimi, joten se voi olla mikä tahansa.

Nyt kun virtual environment on luotu, voit terminaallisa aktivoida sen:

### Linux/Mac

`source venv/bin/activate` (tässä on venv, mutta se voi olla sinulla joku toinen, riippuen annoitko venv hakemistolle erilaisen nimen.)

### Windows

`\venv\Scripts\Activate.ps1` (tässä on venv, mutta se voi olla sinulla joku toinen, riippuen annoitko venv hakemistolle erilaisen nimen.)

---

Nyt kun venv on aktivoitu, niin asennamme tänne pygame frameworkin. Pygame asennetaan pip paketinhallinta järjestelmällä. voit tarkistaa onko sinulla pip asennettuna, komennolla `python -m pip --version`, jos ei ole, niin asennea se komennolla `py -m ensurepip --upgrade` tai `python -m ensurepip --upgrade`.

Tämän jälkeen voit asentaa pygamen alle olevalla komennolla:

`pip install pygame`

Nyt pygame on asennettu virtual environmentin sisälle, voit nyt käynnistää ultimate-square videopelin ajammalla main.py tieodoston joko vscoden kautta tai terminaalista komennolla `py main.py` tai `python main.py`.
