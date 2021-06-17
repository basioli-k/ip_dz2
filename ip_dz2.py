from vepar import *
import fractions

class T(TipoviTokena):
    PLUS, MINUS, PUTA, KROZ, NA = '+-*/^'
    OOTVR, OZTVR, UOTVR, UZTVR, VOTVR, VZTVR = '()[]{}'
    MANJE, VECE, JEDNAKO = '<>=' # Napravljeno kao u 21_BASIC.
    TOCKAZ, ZAREZ = ';,'
    FOR, IF, TO, AND, OR, NOT = 'for', 'if', 'to', 'and', 'or', 'not'
    UBROJ, UIZRAZ = 'broj', 'izraz'
    POMAKNI, PREPREKA, COVJEK, ALARM = 'pomakni', 'prepreka', 'covjek', 'alarm'

    class GORE(Token):
        literal = 'gore'
        def vrijednost(self, mem): return (0, -1)
    class DOLJE(Token):
        literal = 'dolje'
        def vrijednost(self, mem): return (0, 1)
    class LIJEVO(Token):
        literal = 'lijevo'
        def vrijednost(self, mem): return (-1, 0)
    class DESNO(Token):
        literal = 'desno'
        def vrijednost(self, mem): return (1, 0)
    class ISTINA(Token):
        literal = 'istina'
        def vrijednost(self, mem): return True
    class LAZ(Token):
        literal = 'laz'
        def vrijednost(self, mem): return False
    class NEODLUCNO(Token):
        literal = 'neodlucno'
        def vrijednost(self, mem): return nenavedeno
    class BREAK(Token):
        literal = 'break'
        def izvrši(self, mem): raise Prekid
    class BROJ(Token):
        def vrijednost(self, mem): return fractions.Fraction(self.sadržaj)
    class BVAR(Token):
        def vrijednost(self, mem): return mem[self]
    class LVAR(Token):
        def vrijednost(self, mem): return mem[self]
    class AVAR(Token):
        def vrijednost(self, mem): return mem[self]


def rikose(lex):
    for znak in lex:
        if znak.isspace(): lex.zanemari()
        elif znak == '#': 
            lex.pročitaj_do('\n')
            lex.zanemari()
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
        elif znak.isalpha():
            lex.zvijezda(str.isalnum)
            tipVarijable = T.BVAR
            if lex >= '$':
               tipVarijable = T.LVAR
            if lex >= '€':
               tipVarijable = T.AVAR
            yield lex.literal(tipVarijable, case=False)
        else:
            yield lex.literal(T)

### BKG
# start = naredbe -> naredba*
# naredba -> pridruzivanje TOCKAZ  | petlja | grananje | akcija | ocitavanje | BREAK TOCKAZ 
# ocitavanje -> PREPREKA smjer TOCKAZ  | COVJEK TOCKAZ 
# akcija -> POMAKNI smjer TOCKAZ  | ALARM TOCKAZ 
# smjer -> GORE | DOLJE | LIJEVO | DESNO
# petlja -> FOR OOTVR BVAR JEDNAKO broj TO broj OZTVR blok
# grananje -> IF izraz blok
# blok -> naredba | VOTVR naredbe VZTVR
# pridruzivanje -> BVAR JEDNAKO broj | LVAR JEDNAKO izraz | AVAR JEDNAKO lista

# izraz -> disjunkt | izraz OR dijsunkt
# disjunkt -> konjunkt | disjunkt AND konjunkt
# konjunkt -> NOT konjunkt | konjunkt | broj usporedba+ broj | log JEDNAKO log
# log -> LVAR | ISTINA | LAZ | NEODLUCNO | UIZRAZ OOTVR broj OZTVR | OOTVR izraz OZTVR

# broj -> clan | broj (PLUS | MINUS) clan
# clan -> faktor | clan (PUTA | KROZ) faktor
# faktor -> baza | baza NA faktor | MINUS faktor
# baza -> BROJ | OOTVR broj OZTVR | BVAR | UBROJ OOTVR izraz OZTVR

# lista -> UOTVR (elementi | '') UZTVR
# elementi -> element | element ZAREZ elementi
# element -> broj | ISTINA | LAZ | NEODLUCNO | lista

class P(Parser):
    def naredbe(self):
        naredbe = []
        while not self > KRAJ: naredbe.append(self.naredba())
        return Program(naredbe)

    def naredba(self):
        if self > {T.BVAR, T.LVAR, T.AVAR}: return self.pridruzivanje()
        elif self > T.FOR: return self.petlja()
        elif self > T.IF: return self.grananje()
        elif self > {T.POMAKNI, T.ALARM}: self.akcija()
        elif self > {T.PREPREKA, T.COVJEK}: self.ocitavanje()
        elif br := self >> T.BREAK:
            self >> T.TOCKAZ
            return br

    def akcija(self):
        if self >= T.POMAKNI:
            pomak = self >> {T.GORE, T.DOLJE, T.LIJEVO, T.DESNO}
            self >> T.TOCKAZ
            return Pomakni(pomak)
        elif self >> T.ALARM:
            self >> T.TOCKAZ
            return Akcija()

    def ocitavanje(self):
        if self >= T.PREPREKA:
            pomak = self >> {T.GORE, T.DOLJE, T.LIJEVO, T.DESNO}
            self >> T.TOCKAZ
            return Prepreka(pomak)
        elif self >> T.COVJEK:
            self >> T.TOCKAZ
            return Covjek()

    def pridruzivanje(self):
        varijabla = self >> {T.BVAR, T.LVAR, T.AVAR}
        self >> T.JEDNAKO
        if varijabla ^ T.BVAR: pridruzeno =  self.broj()
        elif varijabla ^ T.LVAR: pridruzeno =  self.izraz()
        elif varijabla ^ T.AVAR: pridruzeno = self.lista()
        self >> T.TOCKAZ
        return Pridruzivanje(varijabla, pridruzeno)
    
    def petlja(self):
        self >> T.FOR
        self >> T.OOTVR
        varijabla = self >> T.BVAR
        self >> T.JEDNAKO
        pocetak = self.broj()
        self >> T.TO
        kraj = self.broj()
        self >> T.OZTVR
        naredbe = self.blok()
        return Petlja(varijabla, pocetak, kraj, naredbe)
    
    def grananje(self):
        self >> T.IF
        uvjet = self.izraz()
        naredbe = self.blok()
        return Grananje(uvjet, naredbe)
        
    def blok(self):
        if self >= T.VOTVR:
            blok = []
            while not self >= T.VOTVR:
                blok.append(self.naredba())
        else: blok = [self.naredba()]
        return blok
        
    def lista(self):
        self >> T.UOTVR
        if self >= T.UZTVR:
            return Lista([])
        lista = self.elementi()
        self >> T.UZTVR
        return Lista(lista)
    
    def elementi(self):
        lista = [self.element()]
        while self >= T.ZAREZ: lista. append(self.element())
        return lista

    def element(self):
        if op := self >= {T.ISTINA, T.LAZ, T.NEODLUCNO}: return op
        elif self > T.UOTVR: return self.lista()
        else: return self.broj()

    def izraz(self):
        disjunkti = [self.disjunkt()]
        while self >= T.OR: disjunkti.append(self.disjunkt())
        return Disjunkcija.ili_samo(disjunkti)
        
    def disjunkt(self):
        konjunkti = [self.konjunkt()]
        while self >= T.AND: konjunkti.append(self.konjunkt())
        return Konjunkcija.ili_samo(konjunkti)
        
    def konjunkt(self):
        if self >= T.NOT:
            return Negacija(self.konjunkt())
            #izgledna greška
        elif self > {T.ISTINA, T.LAZ, T.NEODLUCNO, T.LVAR, T.UIZRAZ, T.OOTVR}:
            first_log = self.log()
            if op := self >= T.JEDNAKO:
                return Usporedba(first_log, self.log(), nenavedeno, nenavedeno, op)
            return first_log
        elif broj := self.broj():
            usporedba = {T.MANJE, T.VECE, T.JEDNAKO}
            manje = vece = jednako = nenavedeno
            try:
                if self > usporedba:
                    while u:= self >= usporedba:
                        if u ^ T.MANJE: manje = u
                        elif u ^ T.VECE: vece = u
                        elif u ^ T.JEDNAKO: jednako = u
                    return Usporedba(broj, self.broj(), manje, vece, jednako)
                else:
                    assert False, f'potreban operator uspoređivanja'
            except AssertionError as ae:
                pass
                #TODO smisli bolji error za hvatat        

    def log(self):
        if self >= T.UIZRAZ:
            self >> T.OOTVR
            broj = self.broj()
            self >> T.OZTVR
            return BrojULog(broj)
        elif self >= T.OOTVR:
            izraz = self.izraz()
            self >> T.OZTVR
            return izraz
            
        return self >> {T.ISTINA, T.LAZ, T.NEODLUCNO, T.LVAR}

    def broj(self):
        t = self.član()
        while op := self >= {T.PLUS, T.MINUS}: t = Op(op, t, self.član())
        return t

    def član(self):
        trenutni = self.faktor()
        while operator := self >= {T.PUTA, T.KROZ}:
            trenutni = Op(operator, trenutni, self.faktor())
        return trenutni

    def faktor(self):
        if op := self >= T.MINUS: return Op(op, nenavedeno, self.faktor())
        baza = self.baza()
        if op := self >= T.NA: return Op(op, baza, self.faktor())
        else: return baza

    def baza(self):
        if broj := self >= T.BROJ: return broj
        elif varijabla := self >= T.BVAR:
            return varijabla
        elif self >= T.OOTVR:
            u_zagradi = self.broj()
            self >> T.OZTVR
            return u_zagradi
        elif self >> T.UBROJ:
            self >> T.OOTVR
            log_izraz = self.izraz()
            self >= T.OZTVR
            return LogUBroj(log_izraz)

    start = broj
    lexer = rikose


class Disjunkcija(AST('disjunkti')):
    def vrijednost(self, mem):
        return any([disj.vrijednost(mem) for disj in self.disjunkti])

class Konjunkcija(AST('konjunkti')):
    def vrijednost(self, mem):
        return all([konj.vrijednost(mem) for konj in self.konjunkti])
        
class Negacija(AST('log_vrijednost')):
    def vrijednost(self, mem):
        return not self.log_vrijednost.vrijednost(mem)

class Usporedba(AST('lijevo desno manje veće jednako')):
    def vrijednost(self, mem):
        l, d = self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        return bool((self.manje and l < d) or (self.jednako and l == d) \
                   or (self.veće and l > d) or False)

class Op(AST('operator lijevo desno')):
    def izvrši(self, mem):
        o = self.operator
        print(o, self.lijevo, self.desno)
        if o ^ T.MINUS:
            if self.lijevo == nenavedeno:
                return -self.desno.vrijednost(mem)
            else:
                return self.lijevo.vrijednost(mem) - self.desno.vrijednost(mem)

        elif o ^ T.NA:
             return self.lijevo.vrijednost(mem) ** self.desno.vrijednost(mem)
        
        elif o ^ T.PLUS: 
            return self.lijevo.vrijednost(mem) + self.desno.vrijednost(mem)
    
        elif o ^ T.PUTA:
            return self.lijevo.vrijednost(mem) * self.desno.vrijednost(mem)
        
        elif o ^ T.KROZ: 
            try:
                return self.lijevo.vrijednost(mem) * self.desno.vrijednost(mem)
            except ZeroDivisionError as zde:
                print(zde)


        else:
            assert False, 'ne podržavamo ovaj operator'

class Prekid(NelokalnaKontrolaToka): pass

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
izrazi.append('''
Istina and Laz
''')


def f(izraz):
    P.tokeniziraj(izraz)
    ast = P(izraz)
    mem = Memorija()
    print(ast.izvrši(mem))

    prikaz(ast)

izrazi.append('''
Istina and Laz or Istina
''')

izrazi.append('''
2<3
''')

izrazi.append('''
not Istina
''')

izrazi.append('''
Istina = Istina
''')

izrazi.append('''
2>3 and Laz or 4<5 
''')

izrazi.append('''
(3<4) = Istina 
''')

izrazi.append('''
not not 2>3
''')

izrazi.append('''
Istina = Laz
''')

izrazi.append('''
3 + 5
''')

izrazi.append('''
3 * 5 * 2 + 4
''')

# izrazi.append('''
# 3 / 5
# ''')

f(izrazi[-1])
# for izraz in izrazi:
#     try:
#         f(izraz)
#     except SintaksnaGreška as sg:
#         print("greška")
#         print(izraz)
#         break