#primjeri za predaju
from ip_dz2 import *

def f(izraz, okolina):
    P.tokeniziraj(izraz)
    ast = P(izraz)
    prikaz(ast)
    ast.izvršiNaOkolini(okolina)

if __name__ == "__main__":

    primjeri = list()

    #DFS primjer
    primjeri.append(
        ('''
            otvoreno€ = [koordinate];
            zatvoreno€ = [];
            prolasci = 0;
            while(duljina(otvoreno€) <> 0){
                pozicija€ = izbaci(otvoreno€);

                if(Covjek){
                    Alarm;
                    break;
                }
                
                y = izbaci(pozicija€);
                x = izbaci(pozicija€);
                
                postaviKoordinate(x, y);

                ubaci(zatvoreno€, [x, y]);
                potencijalni€ = [];
                if (not prepreka desno){
                    xNov = x + 0;
                    yNov = y + 1;
                    ubaci(potencijalni€, [xNov, yNov]);
                }
                
                if (not prepreka lijevo) {
                    xNov = x + 0;
                    yNov = y - 1;
                    ubaci(potencijalni€, [xNov, yNov]);
                }
                
                if (not prepreka gore){
                    xNov = x - 1;
                    yNov = y + 0;
                    ubaci(potencijalni€, [xNov, yNov]);
                }
                
                if (not prepreka dolje) {
                    xNov = x + 1;
                    yNov = y + 0;
                    ubaci(potencijalni€, [xNov, yNov]);
                }

                while(duljina(potencijalni€) <> 0){
                    pot€ = izbaci(potencijalni€);
                    yNov = izbaci(pot€);
                    xNov = izbaci(pot€);
                    zatvCopy€ = zatvoreno€;
                    proden$ = Laz;
                    while(duljina(zatvCopy€) <> 0){
                        mogucaPoz€ = izbaci(zatvCopy€);
                        potY = izbaci(mogucaPoz€);
                        potX = izbaci(mogucaPoz€);
                        if (potX == xNov and potY == yNov){
                            proden$ = Istina;
                            break;
                        }
                    }
                    if (not proden$)
                        ubaci(otvoreno€, [xNov, yNov]);
                }
            }
        ''',
        {   
            'vidljiva_okolina': [
                list('...?C?...'),
                list('....#....'),
                list('.........'),
            ],
            'okolina' : [
                list('...#C....'),
                list('....#....'),
                list('.........'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )

        
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

