# Primjeri za predaju. Za laksu uporabu mozda je bolje zakomentirati primjeri.append(...) za sve primjere osim jednog, te samo pokrenuti program.
from ip_dz2 import *

def f(izraz, okolina):
    P.tokeniziraj(izraz)
    ast = P(izraz)
    prikaz(ast)
    ast.izvršiNaOkolini(okolina)

if __name__ == "__main__":

    primjeri = list()

    # Primjer koji prikazuje osnove nasem programskog jezika.
    primjeri.append(
        ('''
            a = 0;
            b = 3 + 5;
            ispis(a);
            ispis(b); 
            ispis(4 + 6 / 2 * 3 - 2^2); # OVO JE KOMENTAR. ispis ovog retka bi trebao biti 9.

            # logicke varijable imaju '$' na kraju.
            logickaVarijabla$ = True and False or True;

            if (logickaVarijabla$) {
                for (i = 1 to 10)  ispis(i);
            }

            for (i = 10 to 5) {
                j = i * i;
                ispis(j);
            }

            # primjer s breakom.
            forever$ = not laz or ( not IsTiNa and izraz(a + 5 * 3));
            k = 5;
            while( forever$ ) {
                if (k <= 9) ispis(k);
                if (k > 9) break;
                k = k + 1;
            }


            lista€ = [0 * 3 + 1 + 3^2, [True, laz], [[[[0]]]]];
            izbaci(lista€);
            ubaci(lista€, 4 /2 +1);

            for (l = 0 to duljina(lista€)) {
                ispis(lista€);
            }
        ''',
        # Ovom primjeru nije potreba okolina, pa je zato sljedeci dictionary prazan.
        {

        }
        )
    )


    # Primjer gdje robot za spasavnje u potresu pretrazuje neku okolinu pomocu DFS-a.
    # Radi bolje vizualizacije kretnje robota u kodu koristimo mogucnost ispisa cijele okoline.
    # Robot naravno nema mogucnost da vidi cijelu okolinu, on zna samo one informacije koje je zatrazio i na temelju njih se krece.
    # Svakako je bitno primjetiti da robot nekad dobije "neodlucnu" informaciju. Npr. u "vidljivoj okolini" (na dnu ovog primjera),
    # u prvom retku matrice u zadnjem stupcu je upitnik, dok u "okolini" na tom mjestu je prepreka tj '#'. Robot ce u nekom trenutku 
    # pitati da li je na tom polju prepreka i dobit ce odgovor "neodlucno" tj. nezna da li je na tom polju prepreka ili nije. Posto
    # na tom polju moze biti covjek kojeg treba spasiti, nas robot ce nekad riskirati i otici na to polje, ako je na tom polju prepreka
    # onda se robot zabusi na prepreku i umre :(, ako nije prepreka onda se uspjesno pomaknu na to polje i dalje nastavlja normalno.
    # Posto je cijela nasa logika s "neodlucom" vrijednoscu slozena tako da u 50% slucajeva bude izvrsen pomak. Nas robot ce u 50% slucajeva 
    # umrijeti u ovom primjeru, a u 50% slucajeva ce naci covjeka.
    """
    primjeri.append(
        ('''
            put€ = [koordinate];
            posjeceni€ = [];
            korak = 0;

            while(duljina(put€) <> 0){
                if(Covjek){
                    Alarm;
                    break;
                }
                
                # gledanje trenutacne pozicije
                pozicija€ = izbaci(put€);
                y = izbaci(pozicija€);
                x = izbaci(pozicija€);
                ubaci(put€, [x, y]);
                
                # ispis okoline
                ispis(korak);
                ispis(okolina);
                korak = korak + 1;

                ubaci(posjeceni€, [x, y]);
                nasaoDijete$ = laz;

                # provjera da li se smijem kretati desno.
                if (not prepreka desno and not nasaoDijete$){
                    xNov = x + 0;
                    yNov = y + 1;

                    posjeceniCopy€ = posjeceni€;
                    posjecen$ = Laz;
                    while(duljina(posjeceniCopy€) <> 0){
                        mogucaPoz€ = izbaci(posjeceniCopy€);
                        potY = izbaci(mogucaPoz€);
                        potX = izbaci(mogucaPoz€);
                        if (potX == xNov and potY == yNov){
                            posjecen$ = Istina;
                            break;
                        }
                    }
                    if (not posjecen$) {
                        pomakni desno;
                        ubaci(put€, [xNov, yNov]);
                        nasaoDijete$ = istina;
                    }
                }
                
                # provjera da li se smijem kretati lijevo.
                if (not prepreka lijevo and not nasaoDijete$) {
                    xNov = x + 0;
                    yNov = y - 1;

                    posjeceniCopy€ = posjeceni€;
                    posjecen$ = Laz;
                    while(duljina(posjeceniCopy€) <> 0){
                        mogucaPoz€ = izbaci(posjeceniCopy€);
                        potY = izbaci(mogucaPoz€);
                        potX = izbaci(mogucaPoz€);
                        if (potX == xNov and potY == yNov){
                            posjecen$ = Istina;
                            break;
                        }
                    }
                    if (not posjecen$) {
                        pomakni lijevo;
                        ubaci(put€, [xNov, yNov]);
                        nasaoDijete$ = istina;
                    }
                }

                # provjera da li se smijem kretati gore.
                if (not prepreka gore and not nasaoDijete$){
                    xNov = x - 1;
                    yNov = y + 0;

                    posjeceniCopy€ = posjeceni€;
                    posjecen$ = Laz;
                    while(duljina(posjeceniCopy€) <> 0){
                        mogucaPoz€ = izbaci(posjeceniCopy€);
                        potY = izbaci(mogucaPoz€);
                        potX = izbaci(mogucaPoz€);
                        if (potX == xNov and potY == yNov){
                            posjecen$ = Istina;
                            break;
                        }
                    }
                    if (not posjecen$) {
                        pomakni gore;
                        ubaci(put€, [xNov, yNov]);
                        nasaoDijete$ = istina;
                    }
                }
                
                # provjera da li se smijem kretati dolje.
                if (not prepreka dolje and not nasaoDijete$) {
                    xNov = x + 1;
                    yNov = y + 0;


                    posjeceniCopy€ = posjeceni€;
                    posjecen$ = Laz;
                    while(duljina(posjeceniCopy€) >< 0){
                        mogucaPoz€ = izbaci(posjeceniCopy€);
                        potY = izbaci(mogucaPoz€);
                        potX = izbaci(mogucaPoz€);
                        if (potX == xNov and potY == yNov){
                            posjecen$ = Istina;
                            break;
                        }
                    }
                    if (not posjecen$) {
                        pomakni dolje;
                        ubaci(put€, [xNov, yNov]);
                        nasaoDijete$ = istina;
                    }
                }

                # zavrsen sam sa ovim cvorom i svom njegovom djecom, izbaci ga iz puta i pokamni se na cvor s kojeg si dosao na njega.
                if (not nasaoDijete$) {
                    if (duljina(put€) <= 1) 
                        break;
                    tmpPoz€ = izbaci(put€);
                    tmpY = izbaci(tmpPoz€);
                    tmpX = izbaci(tmpPoz€);

                    oldPoz€ = izbaci(put€);
                    oldY = izbaci(oldPoz€);
                    oldX = izbaci(oldPoz€);
                    ubaci(put€, [oldX, oldY]);

                    # obrnuti pomaci, tj vracanje na novi prvi cvor u putu.
                    if (tmpX - oldX = 0 and tmpY - oldY = 1) {
                        pomakni lijevo;
                    }
                    if (tmpX - oldX = 0 and tmpY - oldY = -1) {
                        pomakni desno;
                    }
                    if (tmpX - oldX = 1 and tmpY - oldY = 0) {
                        pomakni gore;
                    }
                    if (tmpX - oldX = -1 and tmpY - oldY = 0) {
                        pomakni dolje;
                    }
                }
            }
        ''',
        {   
            'vidljiva_okolina': [
                list('.....####....#?'),
                list('.##.#..........'),
                list('.##.##.#.###.##'),
                list('......##.#...##'),
                list('.##.##.#.#.#..#'),
                list('.........#.#C.#'),
            ],
            'okolina' : [
                list('.....####....##'),
                list('.##.#..........'),
                list('.##.##.#.###.##'),
                list('......##.#...##'),
                list('.##.##.#.#.#..#'),
                list('.........#.#C.#'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )
    """

    for kod, okolina in primjeri:
        try:
            f(kod, okolina)
        except SintaksnaGreška as sg:
            print("greška")
            print(sg)
            # print(kod)
            break
        except SmrtRobota as sr:
            print(sr)

