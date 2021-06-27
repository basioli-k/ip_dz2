from ip_dz2 import *

if __name__ == "__main__":
    izrazi = []

    def f(izraz, okolina):
        P.tokeniziraj(izraz)
        ast = P(izraz)
        prikaz(ast)
        ast.izvršiNaOkolini(okolina)

    # izrazi.append('''
    # a = 5;
    # b = 3;
    # c = a + b * 2;
    # ''')

    # izrazi.append('''
    # lista€ = [2 , istina, [], [3, 5, []]];
    # ''')

    # izrazi.append('''
    # izraz$ = True or lAZ and not False;
    # ''')

    # izrazi.append('''
    # a = 5 * 10;
    # ispis(a);
    # ''')

    # izrazi.append('''
    # a = 3;
    # l€ = [2, istina, faLSE, [a, 5 * 3 - 2 / 1]];
    # ispis(l€);
    # ''')

    # izrazi.append('''
    # a = 3;
    # b = 4;
    # c = a + b;
    # ispis(c);
    # '''
    # )

    # izrazi.append('''
    # a = 0;
    # for (i = 3 to 36) {
    #     a = a + i;
    # }
    # ispis(a);
    # '''
    # )

    # izrazi.append('''
    # x=2;
    # b$ = Istina and (3 <= x + 1);
    # ispis(broj(b$));
    # ''')

    # izrazi.append('''
    # x = 2;
    # b$ = Istina and (3 <= x + 1);
    # a€ = [3, 4, b$];
    # ispis(a€);
    # ispis(broj(b$));
    # ''')

    # izrazi.append('''
    # x = 2;
    # b$ = Istina and (3 <= x + 1);
    # ''')


    # izrazi.append('''
    # l€ = [1, 2];
    # for (x = 1 to 4){
    #     y$ = istina and ( x <= 2 );
    #     lista€ = [y$, x, l€, [Istina and Laz, 3 + 4^2]];
    #     ispis(lista€);
    # }
    # ''')

    # #TODO ubaci(l€, 3+4) iz nekog razloga ispis PLUS'+' BROJ'3' BROJ'4' 
    # izrazi.append('''
    # l€ = [];
    # ubaci(l€, 1);
    # ispis(l€);
    # izbaci(l€);
    # ispis(l€);
    # ubaci(l€, 3+4);
    # ispis(l€);
    # ubaci(l€, [1,2,3]);
    # ispis(l€);
    # ispis(l€);
    # '''
    # )

    # #slicno kao gornja stvar samo s varijablama
    izrazi.append('''
    l€ = [];
    x = 3*5/4;
    y$ = (x + 3 >= 3) or ( Laz and Istina);
    lista€ = [3, 2];

    ubaci(l€, x);
    ubaci(l€, lista€);

    ispis(l€);
    ''')

    izrazi.append('''
        l€ = [1,2];
        x = 0;
        for( x = 1 to 12 )
        {
            if( x < 7 ){
                ubaci( l€ , x );
            }
        }
        ispis( l€ );
    ''')

    izrazi.append('''
        x = 3;
        y$ = (x > 2);
        
        if( y$ )
        {
            ispis(57);
        }
        ispis(1);
    
    ''')

    # izrazi.append('''
    # l€ = [1,2,3];
    # n = duljina(l€);
    # ispis(n);
    # ''')


    # izrazi.append('''
    # l€ = [1,2,3];

    # n = duljina(l€);
    # for (i = 1 to n){
    #     k = izbaci(l€);
    #     ispis(k);
    # }
    # ''')


    # izrazi.append('''
    # l€ = [1,2,3];

    # for (i = 1 to duljina(l€)){
    #     k = izbaci(l€);
    #     ispis(k);
    # }
    # ''')

    # #testiranje trovaljane logike
    # izrazi.append('''
    # c$ = neodlucno;
    # b$ = Istina and neodlucno and c$;
    # ''')

    # izrazi.append('''
    #     l€ = [1,2,3,4,5,6];
    #     dok (duljina(l€) <> 0){
    #         a = izbaci(l€);
    #         ispis(a);
    #     } 
    # ''')

    # izrazi.append('''
    #     #kad je neodlucno robot nasumicno bira hoce li proci ili ne
    #     #ocekivano ispis je nista ili samo dio liste
    #     l€ = [1,2,3,4,5,6];
    #     dok (neodlucno and duljina(l€) <> 0){
    #         a = izbaci(l€);
    #         ispis(a);
    #     } 
    # ''')

    #f(izrazi[-1], {})
    for izraz in izrazi:
        try:
            f(izraz, {})
        except SintaksnaGreška as sg:
            print("greška")
            print(sg)
            print(izraz)
            exit() #da ne bi slucajno nastavio na daljnje primjer ako dode do greske

    # primjeriSOkolinom = []

    # primjeriSOkolinom.append(
    #     ('''
    #     alarm;
    #     ''',
    #     {
    #         'vidljiva_okolina' : [
    #             list('...'),
    #             list('...'),
    #         ],
    #         'okolina' : [
    #             list('...'),
    #             list('...'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )

    # primjeriSOkolinom.append(
    #     ('''
    #     ispis(okolina);
    #     if (not prepreka dolje ) {
    #         pomakni down;
    #     }
    #     ispis(okolina);
    #     ''',
    #     {
    #         'vidljiva_okolina' : [
    #             list('.##'),
    #             list('...'),
    #         ],
    #         'okolina' : [
    #             list('.##'),
    #             list('...'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )

    # primjeriSOkolinom.append(
    #     ('''
    #     for( i = 1 to 10) {
    #         if (Covjek) {
    #             alarm;
    #             break;
    #         }
    #         pomakni desno;
    #     }
    #     ''',
    #     {
    #         'vidljiva_okolina' : [
    #             list('.....C....'),
    #         ],
    #         'okolina' : [
    #             list('.....C....'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )

    # primjeriSOkolinom.append(
    #     ('''
    #         pomakni desno;
    #     ''',
    #     {
    #         'vidljiva_okolina' : [
    #             list('.#..C....'),
    #         ],
    #         'okolina' : [
    #             list('.#..C....'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )
    

    # primjeriSOkolinom.append(
    #     ('''
    #         #ako više puta pokrenete ovaj program viditi ćete da će robot 
    #         #nekada odabrati prelazak na upitnik a nekad nece
    #         #kada se odluči za prelazak umrijeti će inače će preživjeti

    #         if (prepreka desno)
    #             pomakni desno;
    #     ''',
    #     {   #unatoč sjajno isprogramiranom robota, FER-ovci koji su napravili stroj zeznuli su senzore
    #         #tako da robot ne zna uvijek razliku između čovjeka, praznog polja i sigurne smrti

    #         'vidljiva_okolina': [
    #             list('.?..C....'),
    #         ],
    #         'okolina' : [
    #             list('.#..C....'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )

    # primjeriSOkolinom.append(
    #     ('''
    #         lista€ = [1, 2, koordinate];
    #         ubaci(lista€, koordinate);
    #         ispis(lista€);
    #     ''',
    #     {   #unatoč sjajno isprogramiranom robota, FER-ovci koji su napravili stroj zeznuli su senzore
    #         #tako da robot ne zna uvijek razliku između čovjeka, praznog polja i sigurne smrti
    #         #kad robot nije siguran s vjerojatnošću 50 posto bira napraviti blok naredbi
    #         'vidljiva_okolina': [
    #             list('...?C?...'),
    #             list('....?....'),
    #             list('.........'),
    #         ],
    #         'okolina' : [
    #             list('...#C#...'),
    #             list('....#....'),
    #             list('.........'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # )

    # #DFS dok ne nade covjeka
    # primjeriSOkolinom.append(
    #     ('''
    #         otvoreno€ = [koordinate];
    #         zatvoreno€ = [];
    #         prolasci = 0;
    #         while(duljina(otvoreno€) <> 0){
    #             pozicija€ = izbaci(otvoreno€);

    #             if(Covjek){
    #                 Alarm;
    #                 break;
    #             }
                
    #             y = izbaci(pozicija€);
    #             x = izbaci(pozicija€);
                
    #             postaviKoordinate(x, y);

    #             ubaci(zatvoreno€, [x, y]);
    #             potencijalni€ = [];
    #             if (not prepreka desno){
    #                 xNov = x + 0;
    #                 yNov = y + 1;
    #                 ubaci(potencijalni€, [xNov, yNov]);
    #             }
                
    #             if (not prepreka lijevo) {
    #                 xNov = x + 0;
    #                 yNov = y - 1;
    #                 ubaci(potencijalni€, [xNov, yNov]);
    #             }
                
    #             if (not prepreka gore){
    #                 xNov = x - 1;
    #                 yNov = y + 0;
    #                 ubaci(potencijalni€, [xNov, yNov]);
    #             }
                
    #             if (not prepreka dolje) {
    #                 xNov = x + 1;
    #                 yNov = y + 0;
    #                 ubaci(potencijalni€, [xNov, yNov]);
    #             }

    #             while(duljina(potencijalni€) <> 0){
    #                 pot€ = izbaci(potencijalni€);
    #                 yNov = izbaci(pot€);
    #                 xNov = izbaci(pot€);
    #                 zatvCopy€ = zatvoreno€;
    #                 proden$ = Laz;
    #                 while(duljina(zatvCopy€) <> 0){
    #                     mogucaPoz€ = izbaci(zatvCopy€);
    #                     potY = izbaci(mogucaPoz€);
    #                     potX = izbaci(mogucaPoz€);
    #                     if (potX == xNov and potY == yNov){
    #                         proden$ = Istina;
    #                         break;
    #                     }
    #                 }
    #                 if (not proden$)
    #                     ubaci(otvoreno€, [xNov, yNov]);
    #             }
    #         }
    #     ''',
    #     {   
    #         'vidljiva_okolina': [
    #             list('...?C?...'),
    #             list('....#....'),
    #             list('.........'),
    #         ],
    #         'okolina' : [
    #             list('...#C....'),
    #             list('....#....'),
    #             list('.........'),
    #         ],
    #         'posX' : 0,
    #         'posY' : 0
    #     }
    #     )
    # ) # sa ovom okolinom moze se dogoditi da robot ne nade nista, 
    #   # da robot umre i da robot nade covjeka
    #   # robot ce preziviti / ne naci covjeka jako rijetko
    #   # da bi se to dogodilo robot mora sa svih polja oko upitnika pogledati na upitnik
    #   # i reci da nece ici tamo (50 posto je sansa da ce robot otici na upitnik)

    # # k, o = primjeriSOkolinom[-1]
    # # f(k, o)
    
    # for kod, okolina in primjeriSOkolinom:
    #     try:
    #         f(kod, okolina)
    #     except SintaksnaGreška as sg:
    #         print("greška")
    #         print(sg)
    #         # print(kod)
    #         break
    #     except SmrtRobota as sr:
    #         print(sr)
    #         #tu ne treba break robot je umro (ovo je poruka koju bi saznali da nam robot stvarno umre)
