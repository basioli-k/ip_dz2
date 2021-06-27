# Robot za spašavanje ljudi iz potresa
Nakon strašnih događaja koji su u proteklih dvije godine zahvatili Hrvatsku u obliku potresa u Petrinji i Zagrebu, naša firma ABĐ (Avirović, Basioli, Đurić) odlučila je izgraditi robota koji traži ljude u ruševinama. Za fizičku implementaciju robota unajmili smo vanjske suradnike dok smo mi razvili jezik koji omogućuje programiranje ovog robota.
Minimalistički i intuitivni programski jezik koji u nekim aspektima izgleda kao dijete C-a i Pythona jednostavan je za naučiti te njime svako može zadati robotu niz instrukcija kojima možda može spasiti život.  

Robot je sposoban uočiti čovjeka kada mu se nalazi dovoljno blizu te oglasiti alarm po potrebi. Međutim kako se dogodio potres robot može naići na prepreke. Neke od ovih prepreka robot može vidjeti, ali zbog grešaka pri dizajnu senzora (vanjski suradnici nažalost nisu išli na PMF) robot ponekad nije siguran što vidi. U tom slučaju robot nasumično odabire hoće li izvršiti neki niz naredbi.  
Ukoliko robot dođe do prepreke nažalost će umrijeti.

## Implementacija i rad sa programom
Primjere programiranja robota možete vidjeti u datoteci *pokazni_primjeri.py*, a za one znatiželjne o tijeku razvoja programa pogledajte i datoteku *testovi.py*.

Za znatiželjne u datoteci nazvanoj kodnim imenom *ip_dz2.py* moguće je pronaći lekser, parser te AST-ove za programski jezik.

Rad robota izvršava se na nekoj okolini. Simulacija toga je jasno vidljiva u primjerima. 
Da bi sve radilo kako je očekivano potrebno je predati polja stringova "vidljiva_okolina" i "okolina" te koordinate robota "posX" i "posY".  

Elementi polja "okolina" sastavljeni su od znakova:
* "." - prazno polje
* "C" - čovjek na polju
* "#" - prepreka
Elementi polja "vidljiva_okolina" sastavljeni su od istih znakova uz dodatni znak "?" koji simbolizira da robot ne zna što se tamo nalazi. Na istoj poziciji na polju "okolina" može stajati bilo koji od prije navedena tri znaka.
