"""MOSFET devreleri: anahtarlar, yükselteçler, akım aynası, CMOS evirici."""

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("mosfet", T("MOSFETs", "MOSFET'ler", "MOSFETs", "МОП-транзисторы"))


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _late(values, frac=0.5):
    return values[int(len(values) * frac):]


def _supply(s: Sheet, x: int, y: int, value: str = "12", name: str = "VDD"):
    s.v(x, y, value, ref=name)
    s.lab(x, y, name)
    s.gnd(x, y + 2)


@example("nmos_switch", "mosfet",
         T("NMOS low-side switch", "NMOS alt taraf anahtar", "NMOS-Low-Side-Schalter", "Ключ на N-МОП в минусовой цепи"),
         T("The gate takes no DC current: 0 V turns the MOSFET off, 5 V turns it fully on and the 100 Ω load gets almost the whole 12 V.",
           "Kapı DC akım çekmez: 0 V MOSFET'i keser, 5 V tam iletime sokar ve 100 Ω'luk yük 12 V'un neredeyse tamamını alır.",
           "Das Gate nimmt keinen Gleichstrom auf: 0 V sperrt den MOSFET, 5 V schaltet ihn voll durch; die 100-Ω-Last bekommt fast 12 V.",
           "Затвор не потребляет постоянного тока: 0 В закрывает транзистор, 5 В открывает полностью, нагрузка 100 Ом получает почти 12 В."),
         check=lambda c: (_between(min(c.t["V(D)"]), 0, 1.5), _between(max(c.t["V(D)"]), 11.9, 12.01)))
def _nmos_switch():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(8, 1, "VDD", side="u")
    s.r(8, 1, "100", d="v", ref="RL")
    s.m(8, 4)                          # D (8,3), G (7,4), S (8,5)
    s.gnd(8, 5)
    s.lab(8, 3, "D")
    s.v(4, 4, "PULSE(0 5 1m 1u 1u 2m 4m)", ref="VG")
    s.w((4, 4), (7, 4))
    s.gnd(4, 6)
    s.lab(4, 4, "G", side="u")
    return s.done(["V(G)", "V(D)", "I(RL)"], ".tran 8m")


@example("pmos_switch", "mosfet",
         T("PMOS high-side switch", "PMOS üst taraf anahtar", "PMOS-High-Side-Schalter", "Ключ на P-МОП в плюсовой цепи"),
         T("The PMOS source sits at +12 V. It conducts when the gate is pulled well below the source (Vgs < −2.5 V).",
           "PMOS'un kaynağı +12 V'tadır. Kapı kaynağın yeterince altına çekilince (Vgs < −2.5 V) iletir.",
           "Die Source des PMOS liegt an +12 V. Er leitet, wenn das Gate deutlich unter die Source gezogen wird (Ugs < −2,5 V).",
           "Исток P-МОП подключён к +12 В. Транзистор открыт, когда затвор заметно ниже истока (Uзи < −2,5 В)."),
         check=lambda c: (_between(max(c.t["V(LOAD)"]), 11.0, 12.0), _between(min(c.t["V(LOAD)"]), -0.01, 0.1)))
def _pmos_switch():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(8, 2, "VDD", side="u")
    s.m(8, 3, "BS250", rot=180)        # S (8,2), G (9,3), D (8,4)
    s.r(8, 4, "1k", d="v", ref="RL")
    s.gnd(8, 6)
    s.lab(8, 4, "LOAD", side="l")
    s.w((9, 3), (12, 3))
    s.v(12, 3, "PULSE(12 0 1m 1u 1u 2m 4m)", ref="VG")
    s.gnd(12, 5)
    s.lab(12, 3, "G")
    return s.done(["V(G)", "V(LOAD)"], ".tran 8m")


@example("mosfet_switch", "mosfet",
         T("PWM motor/lamp drive", "PWM motor/lamba sürme", "PWM-Ansteuerung (Motor/Lampe)", "ШИМ-управление нагрузкой"),
         T("A 1 kHz PWM signal switches a power MOSFET. The average load voltage follows the duty cycle (here 30 % → ≈ 3.6 V).",
           "1 kHz'lik PWM işareti güç MOSFET'ini anahtarlar. Ortalama yük gerilimi doluluk oranını izler (burada %30 → ≈ 3.6 V).",
           "Ein 1-kHz-PWM-Signal schaltet einen Leistungs-MOSFET. Die mittlere Lastspannung folgt dem Tastgrad (30 % → ≈ 3,6 V).",
           "ШИМ 1 кГц переключает силовой МОП-транзистор. Среднее напряжение на нагрузке следует скважности (30 % → ≈ 3,6 В)."),
         check=lambda c: _between(sum(c.t["V(VDD,D)"]) / len(c.t["V(VDD,D)"]), 2.5, 4.5))
def _mosfet_switch():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(9, 1, "VDD", side="u")
    s.r(9, 1, "10", d="v", ref="RL")
    s.d(12, 3, "1N5819", way="^")
    s.w((9, 1), (12, 1), (12, 3))
    s.w((9, 3), (9, 5), (12, 5))
    s.m(9, 6, "IRFZ44N")               # D (9,5), G (8,6), S (9,7)
    s.gnd(9, 7)
    s.lab(9, 5, "D", side="l")
    s.v(5, 6, "PULSE(0 10 0 1u 1u 0.3m 1m)", ref="VPWM")
    s.w((5, 6), (8, 6))
    s.gnd(5, 8)
    s.lab(5, 6, "PWM", side="u")
    return s.done(["V(PWM)", "V(VDD,D)"], ".tran 5m")


@example("common_source", "mosfet",
         T("Common-source amplifier", "Ortak kaynaklı yükselteç", "Sourceschaltung", "Усилитель с общим истоком"),
         T("The MOSFET version of the common-emitter stage: a divider biases the gate, the drain output is inverted and amplified.",
           "Ortak emetörün MOSFET karşılığı: bölücü kapıyı kutuplar, savak çıkışı ters dönmüş ve yükseltilmiştir.",
           "Die MOSFET-Variante der Emitterschaltung: ein Teiler stellt das Gate ein, der Drain-Ausgang ist invertiert und verstärkt.",
           "МОП-аналог каскада с общим эмиттером: делитель смещает затвор, выход со стока инвертирован и усилен."),
         check=lambda c: _between((max(_late(c.t["V(OUT)"])) - min(_late(c.t["V(OUT)"]))) / 0.2, 2.0, 8.0))
def _common_source():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(5, 1, "VDD", side="u")
    s.r(5, 1, "1meg", d="v")
    s.r(5, 3, "330k", d="v")
    s.gnd(5, 5)
    s.lab(9, 1, "VDD", side="u")
    s.r(9, 1, "4k7", d="v", ref="RD")
    s.m(9, 4)                          # D (9,3), G (8,4), S (9,5)
    s.w((5, 3), (8, 3), (8, 4))
    s.r(9, 5, "1k", d="v", ref="RS")
    s.gnd(9, 7)
    s.lab(9, 3, "OUT")
    s.v(1, 5, "SINE(0 0.1 1k)", ref="VIN")
    s.gnd(1, 7)
    s.cap(1, 5, "1u", d="h")
    s.w((4, 5), (4, 3), (5, 3))
    s.lab(1, 5, "IN", side="l")
    return s.done(["V(IN)", "V(OUT)"], ".tran 5m")


@example("source_follower", "mosfet",
         T("Source follower", "Kaynak izleyici", "Sourcefolger", "Истоковый повторитель"),
         T("The source follows the gate a threshold voltage lower. Gain is a bit below 1, but the output can drive much lower loads.",
           "Kaynak, kapıyı bir eşik gerilimi aşağıdan izler. Kazanç 1'in biraz altındadır ama çıkış çok daha küçük yükleri sürebilir.",
           "Die Source folgt dem Gate um die Schwellspannung tiefer. Verstärkung knapp unter 1, aber viel kleinere Lasten sind treibbar.",
           "Исток повторяет затвор на пороговое напряжение ниже. Усиление чуть меньше 1, зато выход держит гораздо меньшую нагрузку."),
         check=lambda c: _between((max(_late(c.t["V(OUT)"])) - min(_late(c.t["V(OUT)"]))) / 2, 0.8, 1.0))
def _source_follower():
    s = Sheet()
    _supply(s, 1, 1)
    s.lab(8, 3, "VDD", side="u")
    s.m(8, 4)
    s.r(8, 5, "1k", d="v", ref="RS")
    s.gnd(8, 7)
    s.lab(8, 5, "OUT")
    s.v(4, 4, "SINE(7 1 1k)", ref="VIN")
    s.w((4, 4), (7, 4))
    s.gnd(4, 6)
    s.lab(4, 4, "IN", side="u")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("mos_current_mirror", "mosfet",
         T("MOSFET current mirror", "MOSFET akım aynası", "MOSFET-Stromspiegel", "Токовое зеркало на МОП"),
         T("M1 is diode-connected (gate = drain) and carries the reference current; M2 has the same Vgs and copies that current to the load.",
           "M1 diyot bağlıdır (kapı = savak) ve referans akımı taşır; M2 aynı Vgs'ye sahiptir ve bu akımı yüke kopyalar.",
           "M1 ist als Diode geschaltet (Gate = Drain) und führt den Referenzstrom; M2 hat dieselbe Ugs und kopiert den Strom.",
           "M1 включён диодом (затвор = сток) и несёт опорный ток; у M2 то же Uзи, и он копирует этот ток в нагрузку."),
         check=lambda c: _between(c.t["I(M2)"][len(c.t["I(M2)"]) // 2] / c.r["I(RREF)"], 0.95, 1.1))
def _mos_current_mirror():
    s = Sheet()
    _supply(s, 1, 1)
    s.v(1, 5, "6", ref="VOUT")
    s.lab(1, 5, "VO")
    s.gnd(1, 7)
    s.lab(6, 1, "VDD", side="u")
    s.r(6, 1, "10k", d="v", ref="RREF")
    s.m(6, 4)                          # D (6,3), G (5,4), S (6,5)
    s.w((6, 3), (5, 3), (5, 4))
    s.gnd(6, 5)
    s.lab(5, 4, "GATE", side="l")
    s.m(14, 4)
    s.lab(13, 4, "GATE", side="l")
    s.lab(14, 3, "VO", side="u")
    s.gnd(14, 5)
    return s.done(["I(RREF)", "I(M2)"], ".dc VOUT 0.2 12 0.1")


def _cmos(s: Sheet):
    """VDD, P üstte (S yukarıda), N altta; girişler birleşik, çıkış ortada."""
    s.lab(8, 1, "VDD", side="u")
    s.m(8, 2, "BS250", rot=180)        # S (8,1), G (9,2), D (8,3)
    s.m(8, 4)                          # D (8,3), G (7,4), S (8,5)
    s.gnd(8, 5)
    s.w((9, 2), (10, 2), (10, 6), (7, 6), (7, 4))
    s.w((8, 3), (4, 3))
    s.lab(4, 3, "OUT", side="l")
    s.lab(6, 7, "IN", side="l")
    s.w((7, 6), (7, 7), (6, 7))


@example("cmos_inverter_dc", "mosfet",
         T("CMOS inverter — transfer curve", "CMOS evirici — aktarım eğrisi", "CMOS-Inverter — Übertragungskennlinie",
           "КМОП-инвертор — передаточная характеристика"),
         T("One PMOS and one NMOS in series. Sweeping the input shows the sharp switch from 5 V to 0 V around the middle.",
           "Seri bir PMOS ve bir NMOS. Giriş taranınca çıkışın ortalarda 5 V'tan 0 V'a keskin geçişi görülür.",
           "Ein PMOS und ein NMOS in Reihe. Der Eingangsdurchlauf zeigt den steilen Wechsel von 5 V auf 0 V etwa in der Mitte.",
           "PMOS и NMOS последовательно. При развёртке входа видно резкое переключение выхода с 5 В на 0 В около середины."),
         check=lambda c: (_between(c.t["V(OUT)"][0], 4.95, 5.01), _between(c.t["V(OUT)"][-1], -0.01, 0.05)))
def _cmos_inverter_dc():
    s = Sheet()
    _supply(s, 1, 1, "5")
    _cmos(s)
    s.v(6, 7, "0", ref="VIN")
    s.gnd(6, 9)
    return s.done(["V(OUT)", "I(M1)"], ".dc VIN 0 5 0.02")


@example("cmos_inverter", "mosfet",
         T("CMOS inverter — square wave", "CMOS evirici — kare dalga", "CMOS-Inverter — Rechteck", "КМОП-инвертор — меандр"),
         T("The logic NOT gate in action: the output is the inverse of the input. Only during switching does current flow from VDD.",
           "Lojik DEĞİL kapısı iş başında: çıkış girişin tersidir. Yalnız geçiş sırasında VDD'den akım akar.",
           "Das logische NICHT-Gatter: der Ausgang ist das Inverse des Eingangs. Nur beim Umschalten fließt Strom aus VDD.",
           "Логический элемент НЕ: выход — инверсия входа. Ток от VDD течёт только во время переключения."),
         check=lambda c: _between(max(c.t["V(OUT)"]) - min(c.t["V(OUT)"]), 4.9, 5.3))
def _cmos_inverter():
    s = Sheet()
    _supply(s, 1, 1, "5")
    _cmos(s)
    s.v(6, 7, "PULSE(0 5 0.2m 50u 50u 0.4m 1m)", ref="VIN")
    s.gnd(6, 9)
    s.cap(4, 3, "1n", d="v", ref="CL")
    s.gnd(4, 5)
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")
