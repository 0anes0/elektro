"""Güç elektroniği: anahtarlamalı dönüştürücüler, doğrusal regülatörler, şarj pompası."""

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("power", T("Power supplies", "Güç kaynakları", "Stromversorgung", "Источники питания"))


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _mean_late(values, frac=0.75):
    late = values[int(len(values) * frac):]
    return sum(late) / len(late)


def _ripple(values, frac=0.75):
    late = values[int(len(values) * frac):]
    return max(late) - min(late)


def _supply(s: Sheet, x, y, value, name="VIN"):
    s.v(x, y, value, ref=name)
    s.lab(x, y, name)
    s.gnd(x, y + 2)


@example("buck", "power",
         T("Buck converter (step-down)", "Buck dönüştürücü (düşürücü)", "Tiefsetzsteller (Buck)", "Понижающий преобразователь"),
         T("A switch chops 12 V at 100 kHz; the LC filter averages it. Vout ≈ D·Vin = 6 V at 50 % duty — with almost no heat, unlike a resistor divider. At start-up the LC filter overshoots and rings down.",
           "Anahtar 12 V'u 100 kHz'de doğrar; LC süzgeç ortalamasını alır. %50 doluluk oranında Vout ≈ D·Vin = 6 V — direnç bölücünün aksine neredeyse ısı yok. Açılışta LC süzgeç aşım yapar ve salınarak oturur.",
           "Ein Schalter zerhackt 12 V mit 100 kHz, das LC-Filter mittelt. Uaus ≈ D·Uein = 6 V bei 50 % Tastgrad — fast ohne Wärme, anders als ein Teiler. Beim Einschalten schwingt das LC-Filter über und klingt ab.",
           "Ключ нарезает 12 В с частотой 100 кГц, LC-фильтр усредняет. Uвых ≈ D·Uвх = 6 В при 50 % — почти без нагрева, в отличие от делителя. При включении LC-фильтр даёт выброс и затухающие колебания."),
         check=lambda c: (_between(_mean_late(c.t["V(OUT)"]), 5.3, 6.1), _between(_ripple(c.t["V(OUT)"], 0.9), 0, 0.3)))
def _buck():
    s = Sheet()
    _supply(s, 1, 1, "12")
    s.lab(8, 2, "VIN", side="u")
    s.m(8, 3, "IRF9540", rot=180)      # S (8,2), G (9,3), D (8,4)
    s.lab(9, 3, "G")
    s.d(8, 4, "1N5819", way="^")       # anot toprakta, katot SW'de
    s.gnd(8, 6)
    s.lab(8, 4, "SW", side="l")
    s.w((8, 4), (10, 4))
    s.ind(10, 4, "100u", d="h")
    s.cap(13, 4, "22u", d="v")
    s.gnd(13, 6)
    s.w((13, 4), (16, 4))
    s.r(16, 4, "10", d="v", ref="RL")
    s.gnd(16, 6)
    s.lab(16, 4, "OUT")
    s.v(1, 5, "PULSE(12 0 0 50n 50n 5u 10u)", ref="VG")
    s.gnd(1, 7)
    s.lab(1, 5, "G")
    return s.done(["V(SW)", "V(OUT)", "I(L1)"], ".tran 0.2u 1m")


@example("boost", "power",
         T("Boost converter (step-up)", "Boost dönüştürücü (yükseltici)", "Hochsetzsteller (Boost)", "Повышающий преобразователь"),
         T("While the switch is on the coil stores energy; when it opens, the coil adds its voltage to the input. Vout ≈ Vin/(1 − D) ≈ 10 V from 5 V.",
           "Anahtar kapalıyken bobin enerji depolar; açılınca gerilimini girişe ekler. Vout ≈ Vin/(1 − D): 5 V'tan ≈ 10 V.",
           "Bei geschlossenem Schalter speichert die Spule Energie, beim Öffnen addiert sie ihre Spannung zum Eingang. Uaus ≈ Uein/(1 − D) ≈ 10 V aus 5 V.",
           "Пока ключ замкнут, катушка накапливает энергию; при размыкании добавляет своё напряжение ко входу. Uвых ≈ Uвх/(1 − D) ≈ 10 В из 5 В."),
         check=lambda c: _between(_mean_late(c.t["V(OUT)"]), 8.5, 10.2))
def _boost():
    s = Sheet()
    _supply(s, 1, 1, "5")
    s.lab(5, 2, "VIN", side="l")
    s.ind(5, 2, "47u", d="h")
    s.m(8, 4, "IRFZ44N")               # D (8,3), G (7,4), S (8,5)
    s.w((8, 2), (8, 3))
    s.gnd(8, 5)
    s.lab(7, 4, "G", side="l")
    s.d(8, 2, "1N5819", way=">")
    s.w((11, 2), (14, 2))
    s.cap(14, 2, "22u", d="v")
    s.gnd(14, 4)
    s.w((14, 2), (17, 2))
    s.r(17, 2, "10", d="v", ref="RL")
    s.gnd(17, 4)
    s.lab(17, 2, "OUT")
    s.lab(8, 2, "SW", side="u")
    s.v(1, 5, "PULSE(0 10 0 50n 50n 5u 10u)", ref="VG")
    s.gnd(1, 7)
    s.lab(1, 5, "G")
    return s.done(["V(SW)", "V(OUT)", "I(L1)"], ".tran 0.4u 1m")


@example("buck_boost", "power",
         T("Inverting buck-boost converter", "Eviren buck-boost dönüştürücü", "Invertierender Buck-Boost-Wandler",
           "Инвертирующий понижающе-повышающий преобразователь"),
         T("The coil is charged from the input, then dumps its energy into the output through the diode: the output is negative, Vout ≈ −D/(1 − D)·Vin.",
           "Bobin girişten dolar, sonra enerjisini diyot üzerinden çıkışa boşaltır: çıkış negatiftir, Vout ≈ −D/(1 − D)·Vin.",
           "Die Spule wird aus dem Eingang geladen und gibt ihre Energie über die Diode an den Ausgang ab: Ausgang negativ, Uaus ≈ −D/(1 − D)·Uein.",
           "Катушка заряжается от входа, затем отдаёт энергию на выход через диод: выход отрицательный, Uвых ≈ −D/(1 − D)·Uвх."),
         check=lambda c: _between(_mean_late(c.t["V(OUT)"]), -12.2, -9.5))
def _buck_boost():
    s = Sheet()
    _supply(s, 1, 1, "12")
    s.lab(8, 2, "VIN", side="u")
    s.m(8, 3, "IRF9540", rot=180)
    s.lab(9, 3, "G")
    s.ind(8, 4, "47u", d="v")
    s.gnd(8, 6)
    s.lab(8, 4, "SW", side="l")
    s.d(8, 4, "1N5819", way="<")       # anot OUT'ta (11,4), katot SW'de
    s.cap(11, 4, "22u", d="v")
    s.gnd(11, 6)
    s.w((11, 4), (14, 4))
    s.r(14, 4, "10", d="v", ref="RL")
    s.gnd(14, 6)
    s.lab(14, 4, "OUT")
    s.v(1, 5, "PULSE(12 0 0 50n 50n 5u 10u)", ref="VG")
    s.gnd(1, 7)
    s.lab(1, 5, "G")
    return s.done(["V(SW)", "V(OUT)", "I(L1)"], ".tran 0.4u 1m")


@example("series_regulator", "power",
         T("Zener + transistor regulator", "Zener + transistörlü regülatör", "Längsregler mit Z-Diode und Transistor",
           "Стабилизатор на стабилитроне и транзисторе"),
         T("The zener sets the base at 5.1 V; the emitter follower supplies the load current. A 2 V ripple on the input almost vanishes at the output (≈ 4.4 V).",
           "Zener tabanı 5.1 V'ta tutar; emetör izleyici yük akımını sağlar. Girişteki 2 V'luk dalgalanma çıkışta (≈ 4.4 V) neredeyse yok olur.",
           "Die Z-Diode legt die Basis auf 5,1 V, der Emitterfolger liefert den Laststrom. 2 V Welligkeit am Eingang verschwinden am Ausgang (≈ 4,4 V) fast.",
           "Стабилитрон задаёт на базе 5,1 В, эмиттерный повторитель питает нагрузку. Пульсации 2 В на входе почти исчезают на выходе (≈ 4,4 В)."),
         check=lambda c: (_between(_mean_late(c.t["V(OUT)"], 0.5), 4.1, 4.7), _between(_ripple(c.t["V(OUT)"], 0.5), 0, 0.1)))
def _series_regulator():
    s = Sheet()
    _supply(s, 1, 1, "SINE(12 1 100)")
    s.lab(5, 1, "VIN", side="u")
    s.r(5, 1, "1k", d="v", ref="RZ")
    s.d(5, 3, "BZX5V1", way="^")
    s.gnd(5, 5)
    s.w((5, 3), (9, 3))
    s.lab(10, 2, "VIN", side="u")
    s.q(10, 3)                         # C (10,2), B (9,3), E (10,4)
    s.r(10, 4, "100", d="v", ref="RL")
    s.gnd(10, 6)
    s.lab(10, 4, "OUT")
    return s.done(["V(VIN)", "V(OUT)"], ".tran 40m")


@example("opamp_regulator", "power",
         T("Regulator with feedback (op-amp)", "Geri beslemeli regülatör (op-amp)", "Spannungsregler mit Rückkopplung (OPV)",
           "Стабилизатор с обратной связью (ОУ)"),
         T("The op-amp compares a divided output with the 5.1 V zener reference and drives the pass transistor: Vout = Vref·(1 + R1/R2) ≈ 10.2 V once Vin is high enough.",
           "Op-amp bölünmüş çıkışı 5.1 V'luk zener referansıyla karşılaştırır ve geçiş transistörünü sürer: Vin yeterince yüksekse Vout = Vref·(1 + R1/R2) ≈ 10.2 V.",
           "Der OPV vergleicht den geteilten Ausgang mit der 5,1-V-Referenz und steuert den Längstransistor: Uaus = Uref·(1 + R1/R2) ≈ 10,2 V, sobald Uein reicht.",
           "ОУ сравнивает часть выходного напряжения с опорными 5,1 В и управляет проходным транзистором: Uвых = Uоп·(1 + R1/R2) ≈ 10,2 В при достаточном Uвх."),
         check=lambda c: (_between(c.t["V(OUT)"][-1], 9.9, 10.6), _between(c.t["V(OUT)"][-1] - c.t["V(OUT)"][len(c.t["V(OUT)"]) * 3 // 4], 0, 0.1)))
def _opamp_regulator():
    s = Sheet()
    _supply(s, 1, 1, "15")
    s.lab(5, 1, "VIN", side="u")
    s.r(5, 1, "2k2", d="v", ref="RZ")
    s.d(5, 3, "BZX5V1", way="^")
    s.gnd(5, 5)
    s.lab(5, 3, "REF", side="l")
    s.u(9, 5, "LM358 0..20")           # + (8,4), − (8,6), çıkış (11,5)
    s.lab(8, 4, "REF", side="l")
    s.lab(8, 6, "FB", side="l")
    s.r(11, 5, "1k", ref="RB")
    s.q(15, 5)                         # C (15,4), B (14,5), E (15,6)
    s.lab(15, 4, "VIN", side="u")
    s.r(15, 6, "10k", d="v", ref="R1")
    s.r(15, 8, "10k", d="v", ref="R2")
    s.gnd(15, 10)
    s.lab(15, 8, "FB")
    s.w((15, 6), (18, 6))
    s.r(18, 6, "100", d="v", ref="RL")
    s.gnd(18, 8)
    s.lab(18, 6, "OUT")
    return s.done(["V(VIN)", "V(OUT)"], ".dc VIN 0 20 0.1")


@example("charge_pump", "power",
         T("Inverting charge pump", "Eviren şarj pompası", "Invertierende Ladungspumpe", "Инвертирующий накачивающий преобразователь"),
         T("A square wave pushes charge through C1 and two diodes into C2: a negative supply (≈ −8.5 V) made from a 0–10 V signal, without a coil.",
           "Kare dalga, C1 ve iki diyot üzerinden C2'ye yük pompalar: 0–10 V'luk işaretten bobinsiz negatif besleme (≈ −8.5 V).",
           "Ein Rechteck pumpt über C1 und zwei Dioden Ladung in C2: eine negative Spannung (≈ −8,5 V) aus 0–10 V, ohne Spule.",
           "Меандр перекачивает заряд через C1 и два диода в C2: отрицательное питание (≈ −8,5 В) из сигнала 0–10 В без катушки."),
         check=lambda c: _between(_mean_late(c.t["V(OUT)"]), -9.4, -7.5))
def _charge_pump():
    s = Sheet()
    s.v(-2, 1, "PULSE(0 10 0 1u 1u 50u 100u)", ref="VCLK")
    s.lab(-2, 1, "CLK", side="l")
    s.gnd(-2, 3)
    s.w((-2, 1), (1, 1))
    s.cap(1, 1, "10u", d="h", ref="C1")
    s.d(4, 1, "1N4148", way="v")       # anot A'da, katot toprakta
    s.gnd(4, 3)
    s.d(4, 1, "1N4148", way="<")       # anot OUT'ta, katot A'da
    s.cap(7, 1, "10u", d="v", ref="C2")
    s.gnd(7, 3)
    s.w((7, 1), (10, 1))
    s.r(10, 1, "1k", d="v", ref="RL")
    s.gnd(10, 3)
    s.lab(4, 1, "A", side="u")
    s.lab(10, 1, "OUT")
    return s.done(["V(CLK)", "V(A)", "V(OUT)"], ".tran 2u 20m")
