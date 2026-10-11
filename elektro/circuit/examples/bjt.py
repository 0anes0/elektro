"""Bipolar transistör devreleri."""


from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("bjt", T("Transistors (BJT)", "Transistörler (BJT)", "Transistoren (BJT)", "Транзисторы (БТ)"))


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _late(values, frac=0.5):
    return values[int(len(values) * frac):]


def _supply(s: Sheet, x: int, y: int, value: str = "12", name: str = "VCC"):
    """Etiketli besleme: kaynak + ucu `name`, − ucu toprak."""
    s.v(x, y, value, ref="V" + name if name != "VCC" else "VCC")
    s.lab(x, y, name)
    s.gnd(x, y + 2)


@example("led_driver", "bjt",
         T("NPN switch (LED driver)", "NPN anahtar (LED sürücü)", "NPN-Schalter (LED-Treiber)", "Ключ на NPN (драйвер светодиода)"),
         T("A 3.3 V logic pulse drives the base through 4.7 kΩ; the saturated transistor switches 13 mA through the LED (Vce ≈ 50 mV).",
           "3.3 V'luk lojik darbe tabanı 4.7 kΩ üzerinden sürer; doyuma giren transistör LED'den 13 mA geçirir (Vce ≈ 50 mV).",
           "Ein 3,3-V-Logikimpuls steuert die Basis über 4,7 kΩ; der gesättigte Transistor schaltet 13 mA durch die LED (Uce ≈ 50 mV).",
           "Логический импульс 3,3 В управляет базой через 4,7 кОм; насыщенный транзистор пропускает 13 мА через светодиод (Uкэ ≈ 50 мВ)."),
         check=lambda c: _between(max(c.t["I(D1)"]), 12e-3, 15e-3))
def _led_driver():
    s = Sheet()
    _supply(s, 1, 1, "5")
    s.lab(8, 1, "VCC")
    s.r(8, 1, "220", d="v")
    s.d(8, 3, "LED", way="v")
    s.q(8, 6)
    s.v(1, 6, "PULSE(0 3.3 1m 1u 1u 2m 4m)", ref="VIN")
    s.r(1, 6, "4k7")
    s.w((4, 6), (7, 6))
    s.gnd(1, 8)
    s.gnd(8, 7)
    s.lab(1, 6, "IN", side="l")
    return s.done(["V(IN)", "I(D1)", "I(Q1.B)"], ".tran 8m")


@example("pnp_switch", "bjt",
         T("PNP high-side switch", "PNP üst taraf anahtar", "PNP-High-Side-Schalter", "Ключ на PNP в плюсовой цепи"),
         T("The PNP sits between the supply and the load. Pulling its base LOW turns it on; a high base turns it off.",
           "PNP besleme ile yük arasındadır. Taban ALÇAK çekilince iletir, yüksekte kesimdedir.",
           "Der PNP liegt zwischen Versorgung und Last. Basis LOW schaltet ein, Basis HIGH aus.",
           "PNP стоит между питанием и нагрузкой. Низкий уровень на базе открывает его, высокий — закрывает."),
         check=lambda c: (_between(max(c.t["V(LOAD)"]), 11.5, 12.0), _between(min(c.t["V(LOAD)"]), -0.01, 0.1)))
def _pnp_switch():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(8, 2, "VCC", side="u")
    s.q(8, 3, "2N3906", rot=180)                       # rot 180: C altta, B sağda, E üstte
    s.r(8, 4, "1k", d="v", ref="RL")
    s.gnd(8, 6)
    s.lab(8, 4, "LOAD", side="l")
    s.r(9, 3, "4k7", ref="RB")
    s.v(12, 3, "PULSE(12 0 1m 1u 1u 2m 4m)", ref="VIN")
    s.gnd(12, 5)
    s.lab(12, 3, "IN")
    return s.done(["V(IN)", "V(LOAD)"], ".tran 8m")


@example("emitter_follower", "bjt",
         T("Emitter follower", "Emetör izleyici", "Emitterfolger", "Эмиттерный повторитель"),
         T("The emitter follows the base about 0.65 V lower: voltage gain ≈ 1, but the input current is β times smaller (buffer).",
           "Emetör tabanı yaklaşık 0.65 V aşağıdan izler: gerilim kazancı ≈ 1 ama giriş akımı β kat küçüktür (tampon).",
           "Der Emitter folgt der Basis etwa 0,65 V tiefer: Spannungsverstärkung ≈ 1, aber β-fach kleinerer Eingangsstrom (Puffer).",
           "Эмиттер повторяет базу на 0,65 В ниже: усиление ≈ 1, но входной ток в β раз меньше (буфер)."),
         check=lambda c: _between((max(_late(c.t["V(OUT)"])) - min(_late(c.t["V(OUT)"]))) / 2, 0.95, 1.0))
def _emitter_follower():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(8, 3, "VCC", side="u")
    s.q(8, 4)
    s.r(8, 5, "1k", d="v", ref="RE")
    s.gnd(8, 7)
    s.lab(8, 5, "OUT")
    s.v(4, 4, "SINE(6 1 1k)", ref="VIN")
    s.w((4, 4), (7, 4))
    s.gnd(4, 6)
    s.lab(4, 4, "IN", side="u")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("common_emitter", "bjt",
         T("Common-emitter amplifier", "Ortak emetörlü yükselteç", "Emitterschaltung", "Усилитель с общим эмиттером"),
         T("Voltage-divider bias with emitter degeneration. Gain ≈ −Rc/Re = −4.7; the output is inverted (180°).",
           "Bölücüyle kutuplama ve emetör direnci. Kazanç ≈ −Rc/Re = −4.7; çıkış terstir (180°).",
           "Spannungsteiler-Arbeitspunkt mit Emitterwiderstand. Verstärkung ≈ −Rc/Re = −4,7; der Ausgang ist invertiert (180°).",
           "Смещение делителем и эмиттерная обратная связь. Усиление ≈ −Rк/Rэ = −4,7; выход инвертирован (180°)."),
         check=lambda c: _between((max(_late(c.t["V(OUT)"])) - min(_late(c.t["V(OUT)"]))) / 2 / 0.01, 4.3, 4.8))
def _common_emitter():
    s = Sheet()
    s.v(12, 2, "12")
    s.lab(12, 2, "VCC")
    s.gnd(12, 4)
    s.r(5, 1, "100k", d="v")
    s.lab(5, 1, "VCC")
    s.r(9, 1, "4k7", d="v")
    s.lab(9, 1, "VCC")
    s.q(9, 5)
    s.w((9, 3), (9, 4))
    s.w((5, 3), (5, 5))
    s.w((5, 5), (8, 5))
    s.r(5, 5, "22k", d="v")
    s.r(9, 6, "1k", d="v")
    s.cap(2, 5, "10u", d="h")
    s.w((5, 7), (5, 8))
    s.w((5, 8), (9, 8))
    s.gnd(5, 8)
    s.v(2, 5, "SINE(0 10m 1k) AC 1")
    s.gnd(2, 7)
    s.lab(2, 5, "IN", side="l")
    s.lab(9, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("darlington", "bjt",
         T("Darlington pair", "Darlington çifti", "Darlington-Schaltung", "Пара Дарлингтона"),
         T("Two transistors in cascade multiply their gains (β ≈ 250 × 250): a 1 MΩ base resistor is enough to drive 100 mA.",
           "Ardışık iki transistör kazançlarını çarpar (β ≈ 250 × 250): 100 mA sürmek için 1 MΩ taban direnci yeter.",
           "Zwei Transistoren in Kaskade multiplizieren ihre Verstärkung (β ≈ 250 × 250): 1 MΩ Basiswiderstand reicht für 100 mA.",
           "Два транзистора каскадом перемножают усиление (β ≈ 250 × 250): резистора 1 МОм в базе хватает для 100 мА."),
         check=lambda c: _between(c.r["I(RL)"], 0.09, 0.12))
def _darlington():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(11, 1, "VCC")
    s.r(11, 1, "100", d="v", ref="RL")
    s.w((11, 3), (11, 4))
    s.w((8, 4), (11, 4))
    s.q(8, 5)                          # Q1: C (8,4), B (7,5), E (8,6)
    s.q(11, 7)                         # Q2: C (11,6), B (10,7), E (11,8)
    s.w((11, 4), (11, 6))
    s.w((8, 6), (8, 7), (10, 7))
    s.gnd(11, 8)
    s.lab(4, 5, "VCC", side="l")
    s.r(4, 5, "1meg", ref="RB")
    return s.done(["I(RL)", "I(Q1.B)", "I(Q2.B)"])


@example("push_pull", "bjt",
         T("Push-pull output stage", "İt-çek çıkış katı", "Gegentakt-Endstufe", "Двухтактный выходной каскад"),
         T("NPN pushes the positive half, PNP pulls the negative half into the 100 Ω load. Near zero both are off: crossover distortion.",
           "NPN pozitif yarımı iter, PNP negatif yarımı çeker (yük 100 Ω). Sıfır civarında ikisi de kesimde: geçiş bozulması.",
           "Der NPN liefert die positive, der PNP die negative Halbwelle an 100 Ω. Um null sind beide aus: Übernahmeverzerrung.",
           "NPN отдаёт положительную полуволну, PNP — отрицательную в нагрузку 100 Ом. Около нуля оба закрыты: искажения типа «ступенька»."),
         check=lambda c: (_between(max(c.t["V(OUT)"]), 4.0, 4.5), _between(min(c.t["V(OUT)"]), -4.5, -4.0)))
def _push_pull():
    s = Sheet()
    _supply(s, 1, 1, "12", "VP")
    s.v(1, 5, "-12", ref="VNEG")
    s.lab(1, 5, "VN")
    s.gnd(1, 7)
    s.lab(9, 2, "VP", side="u")
    s.q(9, 3)                          # NPN: C (9,2), B (8,3), E (9,4)
    s.q(9, 6, "2N3906", rot=180)       # PNP: C (9,7), B (10,6)?  rot 180: B sağda
    s.w((9, 4), (9, 5))
    s.lab(9, 7, "VN", side="d")
    s.w((9, 4), (12, 4))
    s.r(12, 4, "100", d="v", ref="RL")
    s.gnd(12, 6)
    s.lab(12, 4, "OUT")
    s.v(5, 3, "SINE(0 5 1k)", ref="VIN")
    s.w((5, 3), (8, 3))
    s.gnd(5, 5)
    s.lab(5, 3, "IN", side="u")
    s.w((8, 3), (8, 1), (11, 1), (11, 6), (10, 6))
    return s.done(["V(IN)", "V(OUT)"], ".tran 2m")


@example("current_source", "bjt",
         T("Transistor current source", "Transistörlü akım kaynağı", "Transistor-Stromquelle", "Транзисторный источник тока"),
         T("The base is held at 2.7 V by a divider, so the emitter current is (2.7 − 0.65)/1 kΩ ≈ 2 mA whatever the load supply is.",
           "Taban bölücüyle 2.7 V'ta tutulur; emetör akımı yük beslemesi ne olursa olsun (2.7 − 0.65)/1 kΩ ≈ 2 mA'dir.",
           "Die Basis liegt über einen Teiler auf 2,7 V; der Emitterstrom ist unabhängig von der Lastspannung ≈ 2 mA.",
           "База удерживается делителем на 2,7 В, поэтому ток эмиттера ≈ 2 мА независимо от напряжения нагрузки."),
         check=lambda c: _between(c.t["I(Q1)"][-1] / c.t["I(Q1)"][len(c.t["I(Q1)"]) // 2], 0.97, 1.05))
def _current_source():
    s = Sheet()
    s.v(1, 1, "12", ref="VLOAD")
    s.lab(1, 1, "VL")
    s.gnd(1, 3)
    s.v(1, 5, "12", ref="VCC")
    s.lab(1, 5, "VCC")
    s.gnd(1, 7)
    s.lab(8, 1, "VL", side="u")
    s.r(8, 1, "1k", d="v", ref="RL")
    s.q(8, 4)
    s.r(8, 5, "1k", d="v", ref="RE")
    s.gnd(8, 7)
    s.lab(8, 5, "E")
    s.lab(5, 2, "VCC", side="u")
    s.r(5, 2, "33k", d="v")
    s.w((5, 4), (7, 4))
    s.r(5, 4, "10k", d="v")
    s.gnd(5, 6)
    return s.done(["I(Q1)", "V(E)"], ".dc VLOAD 0.5 12 0.1")


@example("current_mirror", "bjt",
         T("Current mirror", "Akım aynası", "Stromspiegel", "Токовое зеркало"),
         T("Q1 is diode-connected and sets Vbe for the reference current (≈ 1.1 mA); Q2 copies it into the load whatever its voltage.",
           "Q1 diyot bağlıdır ve referans akımı (≈ 1.1 mA) için Vbe'yi ayarlar; Q2 bu akımı yük gerilimi ne olursa olsun kopyalar.",
           "Q1 ist als Diode geschaltet und stellt Ube für den Referenzstrom (≈ 1,1 mA) ein; Q2 kopiert ihn in die Last.",
           "Q1 включён диодом и задаёт Uбэ для опорного тока (≈ 1,1 мА); Q2 копирует этот ток в нагрузку."),
         check=lambda c: _between(c.t["I(Q2)"][len(c.t["I(Q2)"]) // 2] / c.r["I(RREF)"], 0.95, 1.15))
def _current_mirror():
    s = Sheet()
    _supply(s, 1, 1)
    s.v(1, 5, "6", ref="VOUT")
    s.lab(1, 5, "VO")
    s.gnd(1, 7)
    s.lab(6, 1, "VCC", side="u")
    s.r(6, 1, "10k", d="v", ref="RREF")
    s.q(6, 4)                          # Q1: C (6,3), B (5,4), E (6,5) — diyot bağlı
    s.w((6, 3), (5, 3), (5, 4))
    s.gnd(6, 5)
    s.lab(5, 4, "BASE", side="l")
    s.q(14, 4)                         # Q2: C (14,3), B (13,4), E (14,5)
    s.lab(13, 4, "BASE", side="l")
    s.lab(14, 3, "VO", side="u")
    s.gnd(14, 5)
    return s.done(["I(RREF)", "I(Q2)"], ".dc VOUT 0.2 12 0.1")


@example("diff_pair", "bjt",
         T("Differential pair", "Fark yükselteci (diferansiyel çift)", "Differenzverstärker", "Дифференциальный каскад"),
         T("Two transistors share a tail current. Sweeping the input difference steers the current from one side to the other (tanh curve).",
           "İki transistör ortak bir kuyruk akımını paylaşır. Giriş farkı taranınca akım bir koldan diğerine geçer (tanh eğrisi).",
           "Zwei Transistoren teilen sich einen Fußpunktstrom. Die Eingangsdifferenz verschiebt den Strom von einer Seite zur anderen (tanh).",
           "Два транзистора делят общий ток «хвоста». Разность входов перераспределяет ток между плечами (кривая tanh)."),
         check=lambda c: (_between(c.t["I(Q1)"][0], 0, 1e-4), _between(c.t["I(Q1)"][-1], 0.9e-3, 1.2e-3)))
def _diff_pair():
    s = Sheet()
    _supply(s, 1, 1)
    s.v(1, 5, "-12", ref="VEE")
    s.lab(1, 5, "VEE")
    s.gnd(1, 7)
    s.lab(7, 1, "VCC", side="u")
    s.r(7, 1, "4k7", d="v", ref="RC1")
    s.lab(14, 1, "VCC", side="u")
    s.r(14, 1, "4k7", d="v", ref="RC2")
    s.q(7, 4)                          # Q1: C (7,3), B (6,4), E (7,5)
    s.q(14, 4)                         # Q2: C (14,3), B (13,4), E (14,5)
    s.w((7, 5), (7, 6), (14, 6), (14, 5))
    s.r(10, 6, "11k", d="v", ref="RTAIL")
    s.lab(10, 8, "VEE", side="d")
    s.v(4, 4, "0", ref="VDIFF")
    s.w((4, 4), (6, 4))
    s.gnd(4, 6)
    s.gnd(13, 4)
    s.lab(7, 3, "OUT1", side="l")
    s.lab(14, 3, "OUT2")
    return s.done(["I(Q1)", "I(Q2)", "V(OUT1,OUT2)"], ".dc VDIFF -0.2 0.2 0.005")


@example("astable", "bjt",
         T("Astable multivibrator", "Kararsız (astable) multivibratör", "Astabiler Multivibrator", "Мультивибратор"),
         T("Two transistors switch each other off through the capacitors: a square wave with T ≈ 2·0.69·RC ≈ 0.65 s (blinking LED circuit).",
           "İki transistör kondansatörler üzerinden birbirini keser: T ≈ 2·0.69·RC ≈ 0.65 s'lik kare dalga (yanıp sönen LED devresi).",
           "Zwei Transistoren schalten sich über die Kondensatoren gegenseitig ab: Rechteck mit T ≈ 2·0,69·RC ≈ 0,65 s (Blinker).",
           "Два транзистора поочерёдно запирают друг друга через конденсаторы: меандр с T ≈ 2·0,69·RC ≈ 0,65 с (мигалка)."),
         check=lambda c: _between(sum(1 for a, b in zip(c.t["V(C1)"], c.t["V(C1)"][1:]) if a < 4.5 <= b), 3, 6))
def _astable():
    s = Sheet()
    _supply(s, 1, 1, "9")
    for k, xq in enumerate((6, 14)):
        s.lab(xq, 1, "VCC", side="u")
        s.r(xq, 1, "1k", d="v", ref=f"RC{k + 1}")
        s.q(xq, 5)
        s.w((xq, 3), (xq, 4))
        s.gnd(xq, 6)
        s.lab(xq, 3, f"C{k + 1}")
        s.lab(xq - 3, 1, "VCC", side="u")
        s.r(xq - 3, 1, "47k", d="v", ref=f"RB{k + 1}")
        s.w((xq - 3, 3), (xq - 3, 5), (xq - 1, 5))
        s.lab(xq - 3, 4, f"B{k + 1}", side="l")
    s.lab(18, 2, "C1", side="l")
    s.cap(18, 2, "10u", d="h")
    s.lab(21, 2, "B2")
    s.lab(18, 5, "C2", side="l")
    s.cap(18, 5, "10u", d="h")
    s.lab(21, 5, "B1")
    return s.done(["V(C1)", "V(C2)"], ".tran 3")


@example("bistable", "bjt",
         T("Bistable latch (flip-flop)", "Çift kararlı tutucu (flip-flop)", "Bistabile Kippstufe (Flipflop)", "Триггер на транзисторах"),
         T("Cross-coupled transistors keep one of two states. A SET pulse turns Q1 off (Q goes high); a RESET pulse switches it back.",
           "Çapraz bağlı transistörler iki durumdan birini korur. SET darbesi Q1'i keser (Q yükselir); RESET darbesi geri çevirir.",
           "Kreuzgekoppelte Transistoren halten einen von zwei Zuständen. SET schaltet Q1 ab (Q wird high); RESET schaltet zurück.",
           "Перекрёстно связанные транзисторы хранят одно из двух состояний. Импульс SET закрывает Q1 (Q = 1), RESET возвращает."),
         check=lambda c: _between(c.t["V(Q)"][int(0.4 * len(c.sweep.x))] - c.t["V(Q)"][int(0.9 * len(c.sweep.x))], 3, 6))
def _bistable():
    s = Sheet()
    _supply(s, 1, 1, "5")
    for k, xq in enumerate((6, 14)):
        s.lab(xq, 1, "VCC", side="u")
        s.r(xq, 1, "1k", d="v", ref=f"RC{k + 1}")
        s.q(xq, 5)
        s.w((xq, 3), (xq, 4))
        s.gnd(xq, 6)
    s.lab(6, 3, "Q", side="l")
    s.lab(14, 3, "QN")
    s.lab(18, 1, "Q", side="l")
    s.r(18, 1, "10k", d="h", ref="RX1")
    s.lab(21, 1, "B2")
    s.lab(18, 3, "QN", side="l")
    s.r(18, 3, "10k", d="h", ref="RX2")
    s.lab(21, 3, "B1")
    s.lab(5, 5, "B1", side="l")
    s.lab(13, 5, "B2", side="l")
    s.v(18, 6, "PULSE(0 5 1m 1u 1u 0.2m 10)", ref="VSET")
    s.gnd(18, 8)
    s.d(18, 6, "1N4148", way=">")
    s.lab(21, 6, "B2")
    s.v(1, 5, "PULSE(0 5 3m 1u 1u 0.2m 10)", ref="VRST")
    s.gnd(1, 7)
    s.d(1, 5, "1N4148", way=">")
    s.w((4, 5), (5, 5))
    return s.done(["V(Q)", "V(QN)"], ".tran 5m")


@example("inductive_kick", "bjt",
         T("Relay coil with flyback diode", "Röle bobini ve serbest geçiş diyotu", "Relaisspule mit Freilaufdiode",
           "Катушка реле с защитным диодом"),
         T("When the transistor turns off, the coil wants to keep its current; the diode gives it a path and limits the voltage to ≈ 12.7 V.",
           "Transistör kesime girince bobin akımını sürdürmek ister; diyot ona yol verir ve gerilimi ≈ 12.7 V ile sınırlar.",
           "Beim Abschalten will die Spule ihren Strom halten; die Diode gibt ihm einen Weg und begrenzt die Spannung auf ≈ 12,7 V.",
           "При выключении катушка стремится сохранить ток; диод даёт ему путь и ограничивает напряжение ≈ 12,7 В."),
         check=lambda c: _between(max(c.t["V(COIL)"]), 12.4, 13.2))
def _inductive_kick():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(9, 1, "VCC", side="u")
    s.w((9, 1), (12, 1), (12, 3))
    s.r(9, 1, "120", d="v", ref="RCOIL")
    s.ind(9, 3, "50m", d="v")
    s.d(12, 3, "1N4007", way="^")      # katot VCC'de, anot bobinin alt ucunda
    s.w((9, 5), (12, 5))
    s.q(9, 7)                          # C (9,6), B (8,7), E (9,8)
    s.w((9, 5), (9, 6))
    s.gnd(9, 8)
    s.lab(9, 5, "COIL", side="l")
    s.v(4, 7, "PULSE(0 5 1m 1u 1u 5m 20m)", ref="VIN")
    s.r(4, 7, "1k", ref="RB")
    s.w((7, 7), (8, 7))
    s.gnd(4, 9)
    return s.done(["V(COIL)", "I(L1)"], ".tran 10m")
