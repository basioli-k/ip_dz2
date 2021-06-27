from typing import Literal
from vepar import *
import fractions
import copy
import random

class SmrtRobota(Greška):
    pass

class T(TipoviTokena):
    PLUS, MINUS, PUTA, KROZ, NA = '+-*/^'
    OOTVR, OZTVR, UOTVR, UZTVR, VOTVR, VZTVR = '()[]{}'
    MANJE, VECE, JEDNAKO = '<>=' # Napravljeno kao u 21_BASIC.
    TOCKAZ, ZAREZ = ';,'
    FOR, IF, TO, AND, OR, NOT, WHILE = 'for', 'if', 'to', 'and', 'or', 'not', "while"
    ISPIS, UBROJ, UIZRAZ = 'ispis', 'broj', 'izraz'
    POMAKNI, PREPREKA, COVJEK, ALARM, KOORDINATE = 'pomakni', 'prepreka', 'covjek', 'alarm', 'koordinate'
    POSTAVIKOORDINATE = 'postavikoordinate'
    UBACI, IZBACI, DULJINA = 'ubaci', 'izbaci', 'duljina'

    class GORE(Token):
        literal = 'gore'
        def vrijednost(self, mem): return (-1, 0)
    class DOLJE(Token):
        literal = 'dolje'
        def vrijednost(self, mem): return (1, 0)
    class LIJEVO(Token):
        literal = 'lijevo'
        def vrijednost(self, mem): return (0, -1)
    class DESNO(Token):
        literal = 'desno'
        def vrijednost(self, mem): return (0, 1)

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

    # ispisivanje okoline bi se trebalo koristiti u potrebe testiranja
    class OKOLINA(Token):
        literal = 'okolina'
        def vrijednost(self, mem): 
            okolina = copy.deepcopy(mem['okolina'])
            okolina[int(mem['posX'])][int(mem['posY'])] = 'R'
            ret = ""
            for element in okolina:
                ret += ''.join(element) + '\n'
            return ret


    class BROJ(Token):
        def vrijednost(self, mem): return fractions.Fraction(self.sadržaj)
    class BVAR(Token):
        def vrijednost(self, mem): return mem[self]
    class LVAR(Token):
        def vrijednost(self, mem): return mem[self]
    class AVAR(Token):
        def vrijednost(self, mem): return mem[self]

alias = { 'up' : T.GORE, 'down' : T.DOLJE, 'left' : T.LIJEVO, 'right' : T.DESNO,
          'false' : T.LAZ, 'true' : T.ISTINA, 'unknown' : T.NEODLUCNO,
          'print' : T.ISPIS, "dok" : T.WHILE}

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
            s = lex.sadržaj.casefold()
            if s in alias: yield lex.token(alias[s])
            else: yield lex.literal(tipVarijable, case=False)
        else:
            yield lex.literal(T)

### BKG
# start = naredbe -> naredba*
# naredba -> pridruzivanje TOCKAZ  | petlja | grananje | akcija | BREAK TOCKAZ | ubaci TOCKAZ | izbaci TOCKAZ | ispis

# ubaci -> UBACI OOTVR AVAR ZAREZ lista OZTVR | UBACI OOTVR AVAR ZAREZ broj OZTVR
# izbaci -> IZBACI OOTVR AVAR OZTVR
# duljina -> DULJINA OOTVR lista OZTVR

# pridruzivanje -> BVAR JEDNAKO broj | LVAR JEDNAKO izraz | AVAR JEDNAKO lista | BVAR JEDNAKO izbaci | AVAR JEDNAKO izbaci | LVAR JEDNAKO izbaci
# petlja -> FOR OOTVR BVAR JEDNAKO broj TO broj OZTVR blok | WHILE OOTVR izraz OZTVR blok
# grananje -> IF OOTVR izraz OZTVR blok
# blok -> naredba | VOTVR naredbe VZTVR
# akcija -> POMAKNI smjer TOCKAZ  | ALARM TOCKAZ 
# ocitavanje -> PREPREKA smjer | COVJEK 
# smjer -> GORE | DOLJE | LIJEVO | DESNO
# ispis -> ISPIS OOTVR broj OZTVR TOCKAZ | ISPIS OOTVR lista OZTVR TOCKAZ | ISPIS OOTVR OKOLINA OZTVR TOCKAZ

# izraz -> disjunkt | izraz OR dijsunkt
# disjunkt -> konjunkt | disjunkt AND konjunkt
# konjunkt -> NOT konjunkt | log | broj usporedba+ broj | log JEDNAKO log 
# log -> LVAR | ISTINA | LAZ | NEODLUCNO | ocitavanje | UIZRAZ OOTVR broj OZTVR | OOTVR izraz OZTVR
# usporedba -> MANJE | VECE | JEDNAKO

# broj -> clan | broj (PLUS | MINUS) clan
# clan -> faktor | clan (PUTA | KROZ) faktor
# faktor -> baza | baza NA faktor | MINUS faktor
# baza -> BROJ | OOTVR broj OZTVR | BVAR | UBROJ OOTVR izraz OZTVR | DULJINA lista

# lista -> UOTVR (elementi | '') UZTVR | AVAR | KOORDINATE
# elementi -> element | element ZAREZ elementi
# element -> broj | ISTINA | LAZ | NEODLUCNO | lista

class P(Parser):
    def naredbe(self):
        naredbe = []
        while not self > KRAJ: naredbe.append(self.naredba())
        return Program(naredbe)

    def naredba(self):
        if self > {T.BVAR, T.LVAR, T.AVAR}: return self.pridruzivanje()
        elif self > {T.FOR, T.WHILE}: return self.petlja()
        elif self > T.IF: return self.grananje()
        elif self > {T.POMAKNI, T.ALARM}: return self.akcija()
        elif self > T.ISPIS: return self.ispis()
        elif self > T.UBACI: return self.ubaci()
        elif self > T.IZBACI: return self.izbaci()
        elif self >= T.POSTAVIKOORDINATE: return self.postavi_koordinate()
        elif br := self >> T.BREAK:
            self >> T.TOCKAZ
            return br
    
    def ispis(self):
        self >> T.ISPIS
        self >> T.OOTVR
        if self > T.OKOLINA: ispisant = self >> T.OKOLINA
        elif self > {T.AVAR, T.UOTVR}: ispisant = self.lista()
        else: ispisant = self.broj()
        #TODO ne znam bili ovo odradio sa else if i onda else pa raiseao neki exception, zvuci bolje
        self >> T.OZTVR
        self >> T.TOCKAZ
        return Ispis(ispisant)

    def ubaci(self):
        self >> T.UBACI
        self >> T.OOTVR
        lista = self >> T.AVAR
        self >> T.ZAREZ

        if self > {T.AVAR, T.UOTVR, T.KOORDINATE}: ubacenik = self.lista()
        else: ubacenik = self.broj()
        #TODO ne znam bili ovo odradio sa else if i onda else pa raiseao neki exception, zvuci bolje
        self >> T.OZTVR
        self >> T.TOCKAZ
        return Ubaci(lista, ubacenik)

    def izbaci(self, pozvana = False):
        self >> T.IZBACI
        self >> T.OOTVR
        lista = self >> T.AVAR
        self >> T.OZTVR
        if not pozvana:
            self >> T.TOCKAZ
        return Izbaci(lista)
    
    def duljina(self): #smije se koristiti samo tako da se pridruzi nekoj varijabli
        self >> T.DULJINA
        self >> T.OOTVR
        lista = self >> T.AVAR
        self >> T.OZTVR

        return Duljina(lista)

    def akcija(self):
        if self >= T.POMAKNI:
            pomak = self >> {T.GORE, T.DOLJE, T.LIJEVO, T.DESNO}
            self >> T.TOCKAZ
            return Pomakni(pomak)
        elif self >> T.ALARM:
            self >> T.TOCKAZ
            return Alarm()

    def ocitavanje(self):
        if self >= T.PREPREKA:
            pomak = self >> {T.GORE, T.DOLJE, T.LIJEVO, T.DESNO}
            return Prepreka(pomak)
        elif self >> T.COVJEK:
            return Covjek()

    def pridruzivanje(self):
        varijabla = self >> {T.BVAR, T.LVAR, T.AVAR}
        self >> T.JEDNAKO
        if self > T.IZBACI:
            pridruzeno = self.izbaci(True)
        elif varijabla ^ T.BVAR: pridruzeno =  self.broj()
        elif varijabla ^ T.LVAR: pridruzeno =  self.izraz()
        elif varijabla ^ T.AVAR: pridruzeno = self.lista()
        self >> T.TOCKAZ
        return Pridruzivanje(varijabla, pridruzeno)
    
    def petlja(self):
        if self >= T.WHILE:
            self >>T.OOTVR
            izraz = self.izraz()
            self >>T.OZTVR
            naredbe = self.blok()
            return WhilePetlja(izraz, naredbe)

        elif self >> T.FOR:
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
        self >> T.OOTVR
        uvjet = self.izraz()
        self >> T.OZTVR
        naredbe = self.blok()
        return Grananje(uvjet, naredbe)
        
    def blok(self):
        if self >= T.VOTVR:
            blok = []
            while not self >= T.VZTVR:
                blok.append(self.naredba())
        else: blok = [self.naredba()]
        return blok

    def postavi_koordinate(self):
        self >> T.OOTVR
        x = self.broj()
        self >> T.ZAREZ
        y = self.broj() 
        self >> T.OZTVR
        self >> T.TOCKAZ
        return PostaviKoordinate(x, y)
        
    def lista(self):
        if avar := self >= T.AVAR: return Lista(avar, [])
        if avar := self >= T.KOORDINATE: return Koordinate() 
        else:
            self >> T.UOTVR
            if self >= T.UZTVR:
                return Lista(nenavedeno, []) 
            popis = self.elementi()
            self >> T.UZTVR
            return Lista(nenavedeno, popis)
    
    def elementi(self):
        lista = [self.element()]
        while self >= T.ZAREZ: lista.append(self.element())
        return lista

    def element(self):
        if self > {T.ISTINA, T.LAZ, T.NEODLUCNO, T.LVAR}: return self.izraz()
        if val := self >= T.AVAR: return val
        elif self > {T.UOTVR, T.KOORDINATE}: return self.lista()
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
        elif self > {T.ISTINA, T.LAZ, T.NEODLUCNO, T.LVAR, T.UIZRAZ, T.OOTVR, T.COVJEK, T.PREPREKA}:
            first_log = self.log()
            if op := self >= T.JEDNAKO:
                return Usporedba(first_log, self.log(), nenavedeno, nenavedeno, op)
            return first_log
        elif broj := self.broj():
            usporedba = {T.MANJE, T.VECE, T.JEDNAKO}
            manje = vece = jednako = nenavedeno
            if self > usporedba:
                while u:= self >= usporedba:
                    if u ^ T.MANJE: manje = u
                    elif u ^ T.VECE: vece = u
                    elif u ^ T.JEDNAKO: jednako = u
                return Usporedba(broj, self.broj(), manje, vece, jednako)
            else: raise SintaksnaGreška('Neispravan izraz')

    def log(self):
        if self > {T.COVJEK, T.PREPREKA}:
            return self.ocitavanje()
        elif self >= T.UIZRAZ:
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
        elif self > T.DULJINA:
            return self.duljina()
        elif self >= T.OOTVR:
            u_zagradi = self.broj()
            self >> T.OZTVR
            return u_zagradi
        elif self >> T.UBROJ:
            self >> T.OOTVR
            log_izraz = self.izraz()
            self >= T.OZTVR
            return LogUBroj(log_izraz)

    start = naredbe
    lexer = rikose

class Program(AST('naredbe')):
    def izvršiNaOkolini(self, okolina):
        if "okolina" in okolina and "vidljiva_okolina" in okolina:
            razlicite_dimenzije_redaka = len( set([len(redak) for redak in okolina["okolina"]]) |  set([len(redak) for redak in okolina["vidljiva_okolina"]]))

            if len(okolina["okolina"]) !=  len(okolina["vidljiva_okolina"]) or razlicite_dimenzije_redaka != 1: 
                assert False, "Dimenzije okoline i vidljive okoline se ne podudaraju."  
        
        self.izvrši(Memorija(okolina))

    def izvrši(self, mem):
        try:  # break izvan petlje je zapravo sintaksna greška - kompliciranije
            for naredba in self.naredbe: naredba.izvrši(mem)
        except Prekid: raise SemantičkaGreška('Nedozvoljen break izvan petlje')

class Ispis(AST('ispisant')):
    def izvrši(self, mem):
        print(self.ispisant.vrijednost(mem))

#akcije
class Pomakni(AST('pomak')): 
    def izvrši(self, mem):
        novi_x = mem['posX'] + self.pomak.vrijednost(mem)[0]
        novi_y = mem['posY'] + self.pomak.vrijednost(mem)[1]

        if not (0 <= novi_x and novi_x < len(mem['okolina']) and 0 <= novi_y and novi_y < len(mem['okolina'][0])):
            raise SmrtRobota("Robot je izletio iz polja i umro :'(")
        elif mem['okolina'][novi_x][novi_y] == '#':
            raise SmrtRobota("Robot je došao na prepreku i umro :'(")
        else:   
            mem['posX'] = novi_x
            mem['posY'] = novi_y

class Alarm(AST('')): 
    def izvrši(self, mem): 
        print("ALARM!!!")
        #mozda neki inkrement za broj pronađenih ljudi

#očitavanja
class Prepreka(AST('pomak')):
    def vrijednost(self, mem): 
        #ovo sam pri dfsu skuzio slucajno
        #cini mi se da se desilo jer funkcija postavikoordinate postavi
        #fractione
        novi_x = int(mem['posX'] + self.pomak.vrijednost(mem)[0])
        novi_y = int(mem['posY'] + self.pomak.vrijednost(mem)[1])
        
        if not(0 <= novi_x and novi_x < len(mem['vidljiva_okolina']) and 0 <= novi_y and novi_y < len(mem['vidljiva_okolina'][0])):
            return True
        elif mem['vidljiva_okolina'][novi_x][novi_y] == '#':
            return True
        elif mem['vidljiva_okolina'][novi_x][novi_y] == '?':
            return nenavedeno
        return False

class Covjek(AST('')): 
    def vrijednost(self, mem): 
        if mem['okolina'][int(mem['posX'])][int(mem['posY'])] == 'C':
            return True
        return False

class Pridruzivanje(AST('varijabla pridruzeno')):
    def izvrši(self, mem): 
        #kolko sam se napatio zbog ovog Ivane ...
        mem[self.varijabla] = copy.deepcopy(self.pridruzeno.vrijednost(mem))

class Petlja(AST('varijabla pocetak kraj naredbe')):
    def izvrši(self, mem): 
        kv = self.varijabla
        p, k = self.pocetak.vrijednost(mem), self.kraj.vrijednost(mem)
        korak = 1 if p <= k else -1
        mem[kv] = p
        while (mem[kv] - k) * korak <= 0:
            try: 
                for naredba in self.naredbe: naredba.izvrši(mem)
            except Prekid: break
            mem[kv] += korak

class WhilePetlja(AST('izraz naredbe')):
    def izvrši(self, mem):
        while (random.choice([True, False]) if self.izraz.vrijednost(mem) == nenavedeno else self.izraz.vrijednost(mem)):
            try: 
                for naredba in self.naredbe: naredba.izvrši(mem)
            except Prekid: break

class Grananje(AST('uvjet naredbe')):
    def izvrši(self, mem): 
        b = self.uvjet.vrijednost(mem)
        if b == True:
            for naredba in self.naredbe: naredba.izvrši(mem)
        elif b == nenavedeno and random.randint(0, 1) == 1: #robot nasumično bira hoće li ili neće riskirati
            for naredba in self.naredbe: naredba.izvrši(mem)
    
class Lista(AST('var lista')):
    def vrijednost(self, mem): 
        if self.var ^ T.AVAR: return self.var.vrijednost(mem)
        else: return [element.vrijednost(mem) for element in self.lista]

class Koordinate(AST('')):
    def vrijednost(self, mem):
        if "posX" in mem and "posY" in mem:
            return [mem["posX"], mem["posY"]]
        return []

class PostaviKoordinate(AST('x y')):
    def izvrši(self, mem):
        if "posX" in mem and "posY" in mem:
            mem["posX"] = self.x.vrijednost(mem)
            mem["posY"] = self.y.vrijednost(mem)
            if mem['okolina'][int(mem["posX"])][int(mem["posY"])] == '#':
                raise SmrtRobota("Robot je došao na prepreku i umro :'(")

class Ubaci(AST('lista element')):
    def izvrši(self, mem):
        self.lista.vrijednost(mem).append(self.element.vrijednost(mem))
        return True

class Izbaci(AST('lista')):
    def izvrši(self, mem):
        self.lista.vrijednost(mem).pop()
    def vrijednost(self,mem):
        return self.lista.vrijednost(mem).pop()

class Duljina(AST('lista')):
    def vrijednost(self, mem):
        return len(self.lista.vrijednost(mem)) 

class LogUBroj(AST('izraz')):
    def vrijednost(self, mem):
        if self.izraz.vrijednost(mem) == True: return 2
        elif self.izraz.vrijednost(mem) == False: return 0
        else: return 1

class BrojULog(AST('broj')):
    def vrijednost(self, mem):
        if self.broj.vrijednost(mem) == 0: return False
        elif self.broj.vrijednost(mem) == 1: return nenavedeno
        else: return True

class Disjunkcija(AST('disjunkti')):
    def vrijednost(self, mem):
        neodlucno = False
        for disj in self.disjunkti:
            if disj.vrijednost(mem) == nenavedeno:
                neodlucno = True

        if any([disj.vrijednost(mem) for disj in self.disjunkti]):
            return True
        elif neodlucno:
            return nenavedeno
        return False

class Konjunkcija(AST('konjunkti')):
    def vrijednost(self, mem):
        neodlucno = False
        for konj in self.konjunkti:
            if konj.vrijednost(mem) == nenavedeno:
                neodlucno = True

        if not all([konj.vrijednost(mem) for konj in self.konjunkti if konj.vrijednost(mem) != nenavedeno]):
            return False
        elif neodlucno:
            return nenavedeno
        return True
        
class Negacija(AST('log_vrijednost')):
    def vrijednost(self, mem):
        if self.log_vrijednost.vrijednost(mem) == nenavedeno:
            return nenavedeno

        return not self.log_vrijednost.vrijednost(mem)

class Usporedba(AST('lijevo desno manje veće jednako')):
    def vrijednost(self, mem):
        l, d = self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        return bool((self.manje and l < d) or (self.jednako and l == d) \
                   or (self.veće and l > d) or False)

class Op(AST('operator lijevo desno')):
    def vrijednost(self, mem):
        o = self.operator
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
            if  self.desno.vrijednost(mem) == 0:
                raise SemantičkaGreška("Ne smijete dijeliti s nulom.")
            return self.lijevo.vrijednost(mem) / self.desno.vrijednost(mem)


class Prekid(NelokalnaKontrolaToka): pass


if __name__ == "__main__":
    pass