from ip_dz2 import *

if __name__ == "__main__":
    program = '''
    for i = 0 to 4 cigo$ = istina;

    if cigo$ {
        for i = 0 to 3 {
            alarm;
            coVjek;
        }
        a3KvaR$ = iStiNa
        
        if a3KvaR$ <> neodlucno and a3KvaR$ <> laz    
            nekaLista€ = [3, 7, [True, False, 69], 5]
        
        for i = 3 to 4
            pomakni dolje;
        
        prepreka;
    }

    '''
    izrazi = []
    #zakomentirani primjeri nerade ali su poprilicno nebitni, vjv bi radili da stavimo neka_var = taj izraz
    # izrazi.append('''
    # Istina and Laz
    # ''')


    def f(izraz, okolina):
        P.tokeniziraj(izraz)
        ast = P(izraz)
        prikaz(ast)
        ast.izvršiNaOkolini(okolina)

    # izrazi.append('''
    # Istina and Laz or Istina
    # ''')

    # izrazi.append('''
    # 2<3
    # ''')

    # izrazi.append('''
    # not Istina
    # ''')

    # izrazi.append('''
    # Istina = Istina
    # ''')

    # izrazi.append('''
    # 2>3 and Laz or 4<5 
    # ''')

    # izrazi.append('''
    # (3<4) = Istina 
    # ''')

    # izrazi.append('''
    # not not 2>3
    # ''')

    # izrazi.append('''
    # Istina = Laz
    # ''')

    # izrazi.append('''
    # 3 + 5
    # ''')

    # izrazi.append('''
    # 3 * 5 * 2 + 4
    # ''')

    # izrazi.append('''
    #  3 / 5
    # ''')

    # izrazi.append('''
    # 3 * broj(laz) 
    # ''')

    # izrazi.append('''
    # 3 * broj(laz) + broj(istina)
    # ''')

    # izrazi.append('''
    # 2+-3
    # ''')

    # izrazi.append('''
    # (2 * (3 + 4 ^ 2) - 2)
    # ''')

    izrazi.append('''
    a = 5;
    b = 3;
    c = a + b * 2;
    ''')

    izrazi.append('''
    lista€ = [2 , istina, [], [3, 5, []]];
    ''')

    izrazi.append('''
    izraz$ = True or lAZ and not False;
    ''')

    izrazi.append('''
    a = 5 * 10;
    ispis a;
    ''')

    izrazi.append('''
    a = 3;
    l€ = [2, istina, faLSE, [a, 5 * 3 - 2 / 1]];
    ispis l€;
    ''')

    izrazi.append('''
    a = 3;
    b = 4;
    c = a + b;
    ispis c;
    '''
    )

    izrazi.append('''
    a = 0;
    for (i = 3 to 36) {
        a = a + i;
    }
    ispis a;
    '''
    )

    izrazi.append('''
    x=2;
    b$ = Istina and (3 <= x + 1);
    ispis broj(b$);
    ''')

    izrazi.append('''
    x = 2;
    b$ = Istina and (3 <= x + 1);
    a€ = [3, 4, b$];
    ispis a€;
    ispis broj(b$);
    ''')

    izrazi.append('''
    x = 2;
    b$ = Istina and (3 <= x + 1);
    ''')


    izrazi.append('''
    l€ = [1, 2];
    for (x = 1 to 4){
        y$ = istina and ( x <= 2 );
        lista€ = [y$, x, l€, [Istina and Laz, 3 + 4^2]];
        ispis lista€;
    }
    ''')

    #TODO ubaci(l€, 3+4) iz nekog razloga ispis PLUS'+' BROJ'3' BROJ'4' 
    izrazi.append('''
    l€ = [];
    ubaci(l€, 1);
    ispis l€;
    izbaci(l€);
    ispis l€;
    ubaci(l€, 3+4);
    ispis l€;
    ubaci(l€, [1,2,3]);
    ispis l€;
    ispis l€;
    '''
    )

    #slicno kao gornja stvar samo s varijablama
    izrazi.append('''
    l€ = [];
    x = 3*5/4;
    y$ = (x + 3 >= 3) or ( Laz and Istina);
    lista€ = [3, 2];

    ubaci(l€, x);
    ubaci(l€, lista€);

    ispis l€;
    ''')

    izrazi.append('''
    l€ = [1,2,3];
    n = duljina(l€);
    ispis n;
    ''')


    izrazi.append('''
    l€ = [1,2,3];

    n = duljina(l€);
    for (i = 1 to n){
        k = izbaci(l€);
        ispis k;
    }
    ''')


    izrazi.append('''
    l€ = [1,2,3];

    for (i = 1 to duljina(l€)){
        k = izbaci(l€);
        ispis k;
    }
    ''')

    #testiranje trovaljane logike
    izrazi.append('''
    c$ = neodlucno;
    b$ = Istina and neodlucno and c$;
    ''')

    #f(izrazi[-1], {})
    for izraz in izrazi:
        try:
            f(izraz, {})
        except SintaksnaGreška as sg:
            print("greška")
            print(sg)
            print(izraz)
            break
    
    primjeriSOkolinom = []

    primjeriSOkolinom.append(
        ('''
        alarm;
        ''',
        {
            'okolina' : [
                list('...'),
                list('...'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )

    primjeriSOkolinom.append(
        ('''
        ispis okolina;
        if (not prepreka dolje ) {
            pomakni down;
        }
        ispis okolina;
        ''',
        {
            'okolina' : [
                list('.##'),
                list('...'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )

    primjeriSOkolinom.append(
        ('''
        for( i = 1 to 10) {
            if (Covjek) {
                alarm;
                break;
            }
            pomakni desno;
        }
        ''',
        {
            'okolina' : [
                list('.....C....'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )

    primjeriSOkolinom.append(
        ('''
            pomakni lijevo;
        ''',
        {
            'okolina' : [
                list('.....C....'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )

    primjeriSOkolinom.append(
        ('''
            a = 3;
            b = 4;
            ispis a;
        ''',
        {
            'okolina' : [
                list('.?C....'),
            ],
            'posX' : 0,
            'posY' : 0
        }
        )
    )
    # k, o = primjeriSOkolinom[-1]
    # f(k, o)
    
    for kod, okolina in primjeriSOkolinom:
        try:
            f(kod, okolina)
        except SintaksnaGreška as sg:
            print("greška")
            print(kod)
            break
