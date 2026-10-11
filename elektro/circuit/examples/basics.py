"""Temel devreler: Ohm ve Kirchhoff yasaları, kondansatör ve bobin."""

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("basics", T("Basics", "Temel", "Grundlagen", "Основы"))
folder("basics/ohm", T("Ohm's and Kirchhoff's laws", "Ohm ve Kirchhoff yasaları",
                       "Ohmsches Gesetz und Kirchhoff", "Законы Ома и Кирхгофа"))
folder("basics/lc", T("Capacitors and inductors", "Kondansatör ve bobin", "Kondensatoren und Spulen",
                      "Конденсаторы и катушки"))


def _near(value, target, rel=0.01):
    assert abs(value - target) <= abs(target) * rel + 1e-12, f"{value:.6g} ≠ {target:.6g}"


# --- Ohm ve Kirchhoff ---------------------------------------------------------------------------

@example("ohms_law", "basics/ohm",
         T("Ohm's law (I–V line)", "Ohm yasası (I–V doğrusu)", "Ohmsches Gesetz (I-U-Gerade)", "Закон Ома (прямая I–U)"),
         T("The source voltage is swept from 0 to 10 V; the current through the 1 kΩ resistor rises in a straight line: I = V/R.",
           "Kaynak gerilimi 0'dan 10 V'a taranır; 1 kΩ'luk dirençten geçen akım doğru boyunca artar: I = V/R.",
           "Die Quellspannung wird von 0 bis 10 V durchlaufen; der Strom durch 1 kΩ steigt linear: I = U/R.",
           "Напряжение источника меняется от 0 до 10 В; ток через 1 кОм растёт линейно: I = U/R."),
         check=lambda c: _near(c.t["I(R1)"][-1], 10e-3))
def _ohms_law():
    s = Sheet()
    s.v(1, 1, "5")
    s.r(1, 1, "1k", d="h")
    s.w((4, 1), (4, 3), (1, 3))
    s.gnd(1, 3)
    return s.done(["I(R1)"], ".dc V1 0 10 0.5")


@example("series_resistors", "basics/ohm",
         T("Resistors in series", "Seri dirençler", "Reihenschaltung", "Последовательное соединение"),
         T("The same current flows through every resistor; the voltages add up to the source voltage (KVL).",
           "Her dirençten aynı akım geçer; dirençlerdeki gerilimlerin toplamı kaynak gerilimine eşittir (KGY).",
           "Durch alle Widerstände fließt derselbe Strom; die Teilspannungen ergeben die Quellspannung (Maschenregel).",
           "Через все резисторы течёт один ток; сумма напряжений равна напряжению источника (2-й закон Кирхгофа)."),
         check=lambda c: (_near(c.r["I(R1)"], 2e-3), _near(c.r["V(A,B)"], 4)))
def _series():
    s = Sheet()
    s.v(1, 1, "12")
    s.r(1, 1, "1k")
    s.r(4, 1, "2k")
    s.r(7, 1, "3k", d="v")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "A", side="u")
    s.lab(7, 1, "B")
    return s.done(["I(R1)", "V(A)", "V(A,B)", "V(B)"])


@example("parallel_resistors", "basics/ohm",
         T("Resistors in parallel", "Paralel dirençler", "Parallelschaltung", "Параллельное соединение"),
         T("Every resistor sees the full voltage; the branch currents add up to the source current (KCL).",
           "Her direnç kaynağın tam gerilimini görür; kol akımlarının toplamı kaynak akımına eşittir (KAY).",
           "Jeder Widerstand liegt an der vollen Spannung; die Zweigströme ergeben den Gesamtstrom (Knotenregel).",
           "Каждый резистор под полным напряжением; сумма токов ветвей равна току источника (1-й закон Кирхгофа)."),
         check=lambda c: _near(-c.r["I(V1)"], 12e-3 + 6e-3 + 4e-3))
def _parallel():
    s = Sheet()
    s.v(1, 1, "12")
    s.w((1, 1), (10, 1))
    for x, val in ((4, "1k"), (7, "2k"), (10, "3k")):
        s.r(x, 1, val, d="v")
    s.w((1, 3), (10, 3))
    s.gnd(1, 3)
    return s.done(["I(R1)", "I(R2)", "I(R3)", "I(V1)"])


@example("divider", "basics/ohm",
         T("Voltage divider", "Gerilim bölücü", "Spannungsteiler", "Делитель напряжения"),
         T("Vout = Vin·R2/(R1+R2) = 12·4.7/14.7 ≈ 3.84 V. R(OUT,GND) is the source resistance seen by a load.",
           "Vçıkış = Vgiriş·R2/(R1+R2) = 12·4.7/14.7 ≈ 3.84 V. R(OUT,GND) bir yükün gördüğü iç dirençtir.",
           "Uaus = Uein·R2/(R1+R2) = 12·4,7/14,7 ≈ 3,84 V. R(OUT,GND) ist der Innenwiderstand für eine Last.",
           "Uвых = Uвх·R2/(R1+R2) = 12·4,7/14,7 ≈ 3,84 В. R(OUT,GND) — внутреннее сопротивление для нагрузки."),
         check=lambda c: (_near(c.r["V(OUT)"], 12 * 4.7 / 14.7), _near(c.r["R(OUT,GND)"], 1 / (1 / 10e3 + 1 / 4.7e3))))
def _divider():
    s = Sheet()
    s.v(1, 1, "12")
    s.r(1, 1, "10k")
    s.r(4, 1, "4k7", d="v")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "OUT")
    return s.done(["V(OUT)", "I(R1)", "R(OUT,GND)"])


@example("current_divider", "basics/ohm",
         T("Current divider", "Akım bölücü", "Stromteiler", "Делитель тока"),
         T("A 10 mA current source feeds two parallel resistors; the smaller resistor takes the larger share: I1 = I·R2/(R1+R2).",
           "10 mA'lik akım kaynağı iki paralel direnci besler; küçük direnç akımın büyük kısmını alır: I1 = I·R2/(R1+R2).",
           "Eine 10-mA-Stromquelle speist zwei parallele Widerstände; der kleinere nimmt mehr Strom: I1 = I·R2/(R1+R2).",
           "Источник тока 10 мА питает два параллельных резистора; меньший берёт больше тока: I1 = I·R2/(R1+R2)."),
         check=lambda c: (_near(c.r["I(R1)"], 10e-3 * 2 / 3), _near(c.r["I(R2)"], 10e-3 / 3)))
def _current_divider():
    s = Sheet()
    s.i(1, 1, "10m", flip=True)                       # akım üst düğüme verilir
    s.w((1, 1), (7, 1))
    s.r(4, 1, "1k", d="v")
    s.r(7, 1, "2k", d="v")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    return s.done(["I(R1)", "I(R2)", "V(B2)"])


@example("bridge", "basics/ohm",
         T("Wheatstone bridge", "Wheatstone köprüsü", "Wheatstone-Brücke", "Мост Уитстона"),
         T("A balanced bridge (1k/1k = 2k/2k): no current flows through the 5 kΩ middle resistor, so it does not change R(A,B).",
           "Dengeli köprü (1k/1k = 2k/2k): ortadaki 5 kΩ'dan akım geçmez, bu yüzden R(A,B)'yi değiştirmez.",
           "Abgeglichene Brücke (1k/1k = 2k/2k): durch den mittleren 5-kΩ-Widerstand fließt kein Strom; R(A,B) bleibt gleich.",
           "Сбалансированный мост (1k/1k = 2k/2k): через средний резистор 5 кОм ток не идёт, R(A,B) не меняется."),
         check=lambda c: _near(c.r["R(A,B)"], 4000 / 3))
def _bridge():
    s = Sheet()
    s.r(1, 1, "1k")
    s.r(4, 1, "1k")
    s.w((1, 1), (1, 3))
    s.r(1, 3, "2k")
    s.r(4, 3, "2k")
    s.w((7, 1), (7, 3))
    s.r(4, 1, "5k", d="v")
    s.lab(1, 2, "A", side="l")
    s.lab(7, 2, "B")
    return s.done(["R(A,B)"])


@example("wheatstone_unbalanced", "basics/ohm",
         T("Unbalanced Wheatstone bridge", "Dengesiz Wheatstone köprüsü", "Unabgeglichene Wheatstone-Brücke",
           "Несбалансированный мост Уитстона"),
         T("One arm is 1.2 kΩ instead of 1 kΩ: a voltage appears between the bridge midpoints. This is how strain gauges are read.",
           "Bir kol 1 kΩ yerine 1.2 kΩ: köprünün orta noktaları arasında gerilim oluşur. Gerinim ölçerler böyle okunur.",
           "Ein Zweig hat 1,2 kΩ statt 1 kΩ: zwischen den Brückenmitten entsteht eine Spannung (so liest man DMS aus).",
           "Одно плечо 1,2 кОм вместо 1 кОм: между серединами моста появляется напряжение (так читают тензодатчики)."),
         check=lambda c: _near(c.r["V(L,R)"], 10 * (0.5 - 1.2 / 2.2)))
def _wheatstone_unbalanced():
    s = Sheet()
    s.v(1, 1, "10")
    s.w((1, 1), (8, 1))
    s.r(5, 1, "1k", d="v")
    s.r(5, 3, "1k", d="v")
    s.r(8, 1, "1k", d="v")
    s.r(8, 3, "1k2", d="v")
    s.w((1, 3), (1, 5), (8, 5))
    s.gnd(1, 5)
    s.lab(5, 3, "L", side="l")
    s.lab(8, 3, "R")
    return s.done(["V(L)", "V(R)", "V(L,R)"])


@example("thevenin", "basics/ohm",
         T("Thévenin's theorem", "Thevenin teoremi", "Satz von Thévenin", "Теорема Тевенина"),
         T("Left: the original circuit with a 2.2 kΩ load. Right: its Thévenin equivalent (Vth = 8.16 V, Rth = 3.2 kΩ) gives the same load voltage.",
           "Solda yüklü (2.2 kΩ) asıl devre, sağda Thevenin eşdeğeri (Vth = 8.16 V, Rth = 3.2 kΩ): yük gerilimi aynıdır.",
           "Links die Originalschaltung mit 2,2 kΩ Last, rechts ihr Thévenin-Ersatz (Uth = 8,16 V, Rth = 3,2 kΩ): gleiche Lastspannung.",
           "Слева исходная схема с нагрузкой 2,2 кОм, справа эквивалент Тевенина (Uт = 8,16 В, Rт = 3,2 кОм): напряжение на нагрузке то же."),
         check=lambda c: _near(c.r["V(OUT1)"], c.r["V(OUT2)"], rel=0.002))
def _thevenin():
    s = Sheet()
    s.v(1, 1, "12")
    s.r(1, 1, "4k7")
    s.r(4, 1, "10k", d="v", ref="R2")
    s.w((4, 1), (7, 1))
    s.r(7, 1, "2k2", d="v", ref="RL1")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(7, 1, "OUT1")
    s.v(11, 1, "8.163", ref="VTH")
    s.r(11, 1, "3.197k", ref="RTH")
    s.r(14, 1, "2k2", d="v", ref="RL2")
    s.w((11, 3), (14, 3))
    s.gnd(11, 3)
    s.lab(14, 1, "OUT2")
    return s.done(["V(OUT1)", "V(OUT2)"])


@example("norton", "basics/ohm",
         T("Norton's theorem", "Norton teoremi", "Satz von Norton", "Теорема Нортона"),
         T("The same divider replaced by a current source (In = Vth/Rth = 2.55 mA) in parallel with Rth: the load sees the same voltage.",
           "Aynı bölücünün Norton eşdeğeri: Rth'ye paralel akım kaynağı (In = Vth/Rth = 2.55 mA). Yük aynı gerilimi görür.",
           "Derselbe Teiler als Norton-Ersatz: Stromquelle (In = Uth/Rth = 2,55 mA) parallel zu Rth. Die Last sieht dieselbe Spannung.",
           "Тот же делитель как эквивалент Нортона: источник тока (Iн = Uт/Rт = 2,55 мА) параллельно Rт. Напряжение на нагрузке то же."),
         check=lambda c: _near(c.r["V(OUT)"], 12 * (1 / (1 / 10e3 + 1 / 2.2e3)) / (4.7e3 + 1 / (1 / 10e3 + 1 / 2.2e3)), rel=0.002))
def _norton():
    s = Sheet()
    s.i(1, 1, "2.5532m", flip=True, ref="IN")
    s.w((1, 1), (7, 1))
    s.r(4, 1, "3.197k", d="v", ref="RN")
    s.r(7, 1, "2k2", d="v", ref="RL")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(7, 1, "OUT")
    return s.done(["V(OUT)", "I(RL)"])


@example("superposition", "basics/ohm",
         T("Two sources (superposition)", "İki kaynak (süperpozisyon)", "Zwei Quellen (Überlagerung)", "Два источника (наложение)"),
         T("Two batteries feed a common resistor. The middle voltage equals the sum of the effects of each source alone.",
           "İki kaynak ortak bir direnci besler. Orta noktanın gerilimi, kaynakların tek tek etkilerinin toplamıdır.",
           "Zwei Quellen speisen einen gemeinsamen Widerstand. Die Mittenspannung ist die Summe der Einzelwirkungen.",
           "Два источника питают общий резистор. Напряжение в середине равно сумме действий каждого источника."),
         check=lambda c: _near(c.r["V(MID)"], (12 / 1e3 + 5 / 2e3) / (1 / 1e3 + 1 / 2e3 + 1 / 3e3)))
def _superposition():
    s = Sheet()
    s.v(1, 1, "12")
    s.r(1, 1, "1k")
    s.r(4, 1, "3k", d="v")
    s.r(4, 1, "2k")
    s.v(7, 1, "5", ref="V2")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "MID", side="u")
    return s.done(["V(MID)", "I(R1)", "I(R2)", "I(R3)"])


# --- kondansatör ve bobin ------------------------------------------------------------------------

def _tau_check(c, key, final, start=0.0, at=1.0):
    import math
    w = c.sweep
    k = min(range(len(w.x)), key=lambda i: abs(w.x[i] - (0.5e-3 + at * 1e-3)))
    expected = final + (start - final) * math.exp(-at)
    _near(c.t[key][k], expected, rel=0.02)


@example("rc_charge", "basics/lc",
         T("RC charging", "RC dolma", "RC-Ladung", "Заряд RC-цепи"),
         T("After the 5 V step the capacitor charges with τ = RC = 1 ms: 63 % after one τ, practically full after 5τ.",
           "5 V basamaktan sonra kondansatör τ = RC = 1 ms ile dolar: bir τ'da %63, 5τ'da neredeyse tam dolu.",
           "Nach dem 5-V-Sprung lädt der Kondensator mit τ = RC = 1 ms: 63 % nach einem τ, nach 5τ praktisch voll.",
           "После скачка 5 В конденсатор заряжается с τ = RC = 1 мс: 63 % за τ, почти полностью за 5τ."),
         check=lambda c: _tau_check(c, "V(OUT)", 5.0))
def _rc_charge():
    s = Sheet()
    s.v(1, 1, "PULSE(0 5 0.5m 1u 1u 10m 20m)")
    s.r(1, 1, "1k")
    s.cap(4, 1, "1u")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "OUT")
    return s.done(["V(OUT)", "I(C1)"], ".tran 6m")


@example("rc_discharge", "basics/lc",
         T("RC discharging", "RC boşalma", "RC-Entladung", "Разряд RC-цепи"),
         T("The source drops from 5 V to 0: the capacitor discharges through the resistor, the current flows backwards.",
           "Kaynak 5 V'tan 0'a iner: kondansatör direnç üzerinden boşalır, akım ters yönde akar.",
           "Die Quelle fällt von 5 V auf 0: der Kondensator entlädt sich über den Widerstand, der Strom fließt rückwärts.",
           "Источник падает с 5 В до 0: конденсатор разряжается через резистор, ток течёт в обратную сторону."),
         check=lambda c: _tau_check(c, "V(OUT)", 0.0, start=5.0))
def _rc_discharge():
    s = Sheet()
    s.v(1, 1, "PULSE(5 0 0.5m 1u 1u 10m 20m)")
    s.r(1, 1, "1k")
    s.cap(4, 1, "1u")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "OUT")
    return s.done(["V(OUT)", "I(C1)"], ".tran 6m")


@example("rl_rise", "basics/lc",
         T("RL current rise", "RL akım yükselişi", "RL-Stromanstieg", "Нарастание тока в RL-цепи"),
         T("An inductor resists changes of current: after the step the current rises with τ = L/R = 1 ms to 10 mA.",
           "Bobin akım değişimine karşı koyar: basamaktan sonra akım τ = L/R = 1 ms ile 10 mA'e yükselir.",
           "Eine Spule bremst Stromänderungen: nach dem Sprung steigt der Strom mit τ = L/R = 1 ms auf 10 mA.",
           "Катушка препятствует изменению тока: после скачка ток растёт с τ = L/R = 1 мс до 10 мА."),
         check=lambda c: _tau_check(c, "I(L1)", 10e-3))
def _rl_rise():
    s = Sheet()
    s.v(1, 1, "PULSE(0 1 0.5m 1u 1u 10m 20m)")
    s.r(1, 1, "100")
    s.ind(4, 1, "100m", d="v")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    return s.done(["I(L1)", "V(E2)"], ".tran 6m")


@example("lc_ringing", "basics/lc",
         T("LC ringing (RLC step response)", "LC salınımı (RLC basamak yanıtı)", "LC-Schwingung (RLC-Sprungantwort)",
           "Колебания LC (переходная характеристика RLC)"),
         T("Energy swings between the coil and the capacitor at f = 1/(2π√LC) ≈ 1.6 kHz; the resistor slowly damps it.",
           "Enerji bobin ile kondansatör arasında f = 1/(2π√LC) ≈ 1.6 kHz'de gidip gelir; direnç salınımı yavaşça söndürür.",
           "Die Energie pendelt mit f = 1/(2π√LC) ≈ 1,6 kHz zwischen Spule und Kondensator; der Widerstand dämpft langsam.",
           "Энергия колеблется между катушкой и конденсатором с f = 1/(2π√LC) ≈ 1,6 кГц; резистор медленно гасит колебания."),
         check=lambda c: (_near(max(c.t["V(OUT)"]), 1.85, rel=0.05)))
def _lc_ringing():
    s = Sheet()
    s.v(1, 1, "PULSE(0 1 0.2m 1u 1u 10m 20m)")
    s.r(1, 1, "10")
    s.ind(4, 1, "10m")
    s.cap(7, 1, "1u")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(7, 1, "OUT")
    return s.done(["V(OUT)", "I(L1)"], ".tran 5m")


@example("rlc_damping", "basics/lc",
         T("Under-, critically and over-damped RLC", "Az, kritik ve aşırı sönümlü RLC", "Unter-, kritisch und überdämpftes RLC",
           "Недо-, критически и передемпфированная RLC"),
         T("The same LC with R = 20 Ω (rings), R = 2√(L/C) = 200 Ω (fastest without overshoot) and R = 1 kΩ (slow).",
           "Aynı LC üç farklı dirençle: 20 Ω (salınır), 2√(L/C) = 200 Ω (aşmadan en hızlı), 1 kΩ (yavaş).",
           "Dasselbe LC mit R = 20 Ω (schwingt), R = 2√(L/C) = 200 Ω (am schnellsten ohne Überschwingen) und 1 kΩ (träge).",
           "Тот же LC с R = 20 Ом (колеблется), R = 2√(L/C) = 200 Ом (быстрее всего без выброса) и 1 кОм (медленно)."),
         check=lambda c: (max(c.t["V(UNDER)"]) > 1.5 and max(c.t["V(CRIT)"]) < 1.02
                          and max(c.t["V(OVER)"]) < 1.0) or _near(0, 1))
def _rlc_damping():
    s = Sheet()
    s.v(1, 3, "PULSE(0 1 0.2m 1u 1u 10m 20m)")
    s.lab(1, 3, "IN", side="l")
    s.gnd(1, 5)
    for row, (r, name) in enumerate((("20", "UNDER"), ("200", "CRIT"), ("1k", "OVER"))):
        y = 1 + 4 * row
        s.lab(5, y, "IN", side="l")
        s.r(5, y, r)
        s.ind(8, y, "10m")
        s.cap(11, y, "1u")
        s.gnd(11, y + 2)
        s.lab(11, y, name)
    return s.done(["V(UNDER)", "V(CRIT)", "V(OVER)"], ".tran 4m")
