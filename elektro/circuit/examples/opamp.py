"""Op-amp devreleri: yükselteçler, doğrusal olmayan devreler, aktif filtreler.

Op-amp'ların besleme uçları yok; çıkış sınırları değerdeki raydan gelir ("TL072 ±15").
Standart yerleşim: op-amp (5, 3) → + (4, 2), − (4, 4), çıkış (7, 3).
"""

import math

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("opamp", T("Op-amps", "Op-amp'lar", "Operationsverstärker", "Операционные усилители"))
folder("opamp/amps", T("Amplifiers", "Yükselteçler", "Verstärker", "Усилители"))
folder("opamp/nonlinear", T("Comparators & nonlinear", "Karşılaştırıcılar ve doğrusal olmayan", "Komparatoren & nichtlinear",
                            "Компараторы и нелинейные схемы"))
folder("opamp/filters", T("Active filters", "Aktif filtreler", "Aktive Filter", "Активные фильтры"))


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _late(values, frac=0.5):
    return values[int(len(values) * frac):]


def _amp(values):
    late = _late(values)
    return (max(late) - min(late)) / 2


def _at(c, expr, x):
    k = min(range(len(c.sweep.x)), key=lambda i: abs(c.sweep.x[i] - x))
    return c.t[expr][k]


def _db(c, expr, f):
    return 20 * math.log10(abs(_at(c, expr, f)))


def _src(s: Sheet, x, y, value, name="IN", ref=None):
    """Toprağa bağlı dikey kaynak; üst ucu etiketli."""
    s.v(x, y, value, ref=ref)
    s.gnd(x, y + 2)
    s.lab(x, y, name, side="l")


# --- yükselteçler ------------------------------------------------------------------------------

@example("inverting", "opamp/amps",
         T("Inverting amplifier", "Eviren yükselteç", "Invertierender Verstärker", "Инвертирующий усилитель"),
         T("The − input is a virtual ground, so the gain is −Rf/Rin = −10: a 0.5 V sine becomes a 5 V sine in antiphase.",
           "− giriş sanal topraktır; kazanç −Rf/Rin = −10: 0.5 V'luk sinüs ters fazlı 5 V'luk sinüs olur.",
           "Der −-Eingang ist virtuelle Masse, die Verstärkung −Rf/Rin = −10: aus 0,5 V Sinus wird ein gegenphasiger 5-V-Sinus.",
           "Вход − — виртуальная земля, усиление −Rf/Rin = −10: синус 0,5 В превращается в противофазный синус 5 В."),
         check=lambda c: _between(_amp(c.t["V(OUT)"]), 4.9, 5.05))
def _inverting():
    s = Sheet()
    _src(s, 1, 4, "SINE(0 0.5 1k) AC 1")
    s.r(1, 4, "10k", ref="RIN")
    s.u(5, 3)
    s.r(4, 4, "100k", ref="RF")
    s.w((7, 3), (7, 4))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("non_inverting", "opamp/amps",
         T("Non-inverting amplifier", "Evirmeyen yükselteç", "Nichtinvertierender Verstärker", "Неинвертирующий усилитель"),
         T("The input goes to +; the divider feeds back a part of the output. Gain = 1 + Rf/Rg = 11, in phase with the input.",
           "Giriş + uca gider; bölücü çıkışın bir kısmını geri besler. Kazanç = 1 + Rf/Rg = 11, girişle aynı fazda.",
           "Das Signal liegt am +-Eingang; der Teiler koppelt einen Teil des Ausgangs zurück. Verstärkung 1 + Rf/Rg = 11, gleichphasig.",
           "Сигнал подан на вход +; делитель возвращает часть выхода. Усиление 1 + Rf/Rg = 11, в фазе со входом."),
         check=lambda c: _between(_amp(c.t["V(OUT)"]), 5.4, 5.55))
def _non_inverting():
    s = Sheet()
    _src(s, 1, 2, "SINE(0 0.5 1k) AC 1")
    s.w((1, 2), (4, 2))
    s.u(5, 3)
    s.r(4, 4, "1k", d="v", ref="RG")
    s.gnd(4, 6)
    s.r(4, 4, "10k", ref="RF")
    s.w((7, 3), (7, 4))
    s.lab(7, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("follower", "opamp/amps",
         T("Voltage follower (buffer)", "Gerilim izleyici (tampon)", "Spannungsfolger (Puffer)", "Повторитель напряжения"),
         T("Output tied to −: gain is exactly 1. A 100 kΩ source drives a 100 Ω load without sagging, because the + input draws no current.",
           "Çıkış − uca bağlı: kazanç tam 1. + giriş akım çekmediği için 100 kΩ'luk kaynak 100 Ω'luk yükü çökmeden sürer.",
           "Ausgang an −: Verstärkung genau 1. Eine 100-kΩ-Quelle treibt 100 Ω ohne Einbruch, da der +-Eingang keinen Strom zieht.",
           "Выход соединён с −: усиление ровно 1. Источник 100 кОм питает нагрузку 100 Ом без просадки — вход + не потребляет ток."),
         check=lambda c: _between(c.r["V(OUT)"], 2.99, 3.01))
def _follower():
    s = Sheet()
    _src(s, 1, 2, "3")
    s.r(1, 2, "100k", ref="RS")
    s.u(5, 3)
    s.w((4, 4), (4, 5), (7, 5), (7, 3))
    s.w((7, 3), (10, 3))
    s.r(10, 3, "100", d="v", ref="RL")
    s.gnd(10, 5)
    s.lab(10, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)", "I(RL)"])


@example("summing", "opamp/amps",
         T("Summing amplifier (audio mixer)", "Toplayıcı yükselteç (ses mikseri)", "Summierverstärker (Mischpult)", "Сумматор (микшер)"),
         T("Each input sends a current Vi/R into the virtual ground; the feedback resistor turns their sum into −(V1 + V2).",
           "Her giriş sanal toprağa Vi/R akımı gönderir; geri besleme direnci bunların toplamını −(V1 + V2) gerilimine çevirir.",
           "Jeder Eingang schickt Vi/R in die virtuelle Masse; der Rückkopplungswiderstand macht daraus −(V1 + V2).",
           "Каждый вход подаёт ток Vi/R в виртуальную землю; резистор обратной связи превращает их сумму в −(V1 + V2)."),
         check=lambda c: (_between(max(_late(c.t["V(OUT)"])), -1.05, -0.95), _between(min(_late(c.t["V(OUT)"])), -3.05, -2.95)))
def _summing():
    s = Sheet()
    _src(s, 1, 4, "SINE(0 1 1k)", "A", ref="VA")
    _src(s, 1, 8, "2", "B", ref="VB")
    s.r(1, 4, "10k", ref="RA")
    s.r(1, 8, "10k", ref="RB")
    s.w((4, 8), (4, 4))
    s.u(5, 3)
    s.r(4, 4, "10k", ref="RF")
    s.w((7, 3), (7, 4))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "OUT")
    return s.done(["V(A)", "V(B)", "V(OUT)"], ".tran 3m")


@example("difference", "opamp/amps",
         T("Difference amplifier", "Fark yükselteci", "Differenzverstärker", "Дифференциальный усилитель"),
         T("With four equal resistors the output is V(+side) − V(−side): here 2 V − sine. Common voltages on both inputs cancel.",
           "Dört eşit dirençle çıkış V(+ taraf) − V(− taraf) olur: burada 2 V − sinüs. İki girişteki ortak gerilim birbirini götürür.",
           "Mit vier gleichen Widerständen ist der Ausgang U(+Seite) − U(−Seite): hier 2 V − Sinus. Gleichtaktanteile heben sich auf.",
           "При четырёх равных резисторах выход = U(+сторона) − U(−сторона): здесь 2 В − синус. Синфазная составляющая гасится."),
         check=lambda c: (_between(max(_late(c.t["V(OUT)"])), 2.95, 3.05), _between(min(_late(c.t["V(OUT)"])), 0.95, 1.05)))
def _difference():
    s = Sheet()
    _src(s, 1, 4, "SINE(0 1 1k)", "A", ref="VA")
    _src(s, 1, 8, "2", "B", ref="VB")
    s.r(1, 4, "10k", ref="R1")
    s.u(5, 3)
    s.r(4, 4, "10k", ref="R2")
    s.w((7, 3), (7, 4))
    s.lab(1, 1, "B", side="l")
    s.r(1, 1, "10k", ref="R3")
    s.w((4, 1), (4, 2))
    s.w((4, 1), (10, 1))
    s.r(10, 1, "10k", d="v", ref="R4")
    s.gnd(10, 3)
    s.lab(7, 3, "OUT")
    return s.done(["V(A)", "V(B)", "V(OUT)"], ".tran 3m")


@example("instrumentation", "opamp/amps",
         T("Instrumentation amplifier", "Enstrümantasyon yükselteci", "Instrumentenverstärker", "Инструментальный усилитель"),
         T("Two buffers with gain 1 + 2R/Rg ≈ 10 and a difference stage: a 0.1 V differential signal on 2 V common mode becomes ≈ 1 V.",
           "Kazancı 1 + 2R/Rg ≈ 10 olan iki tampon ve bir fark katı: 2 V ortak gerilim üstündeki 0.1 V'luk fark işareti ≈ 1 V olur.",
           "Zwei Puffer mit Verstärkung 1 + 2R/Rg ≈ 10 und eine Differenzstufe: 0,1 V Differenz auf 2 V Gleichtakt werden ≈ 1 V.",
           "Два буфера с усилением 1 + 2R/Rg ≈ 10 и дифференциальный каскад: 0,1 В разностного сигнала на фоне 2 В дают ≈ 1 В."),
         check=lambda c: (_between(_amp(c.t["V(OUT)"]), 0.95, 1.06), _between(abs(sum(c.t["V(OUT)"]) / len(c.t["V(OUT)"])), 0, 0.05)))
def _instrumentation():
    s = Sheet()
    _src(s, 1, 2, "SINE(2 50m 1k)", "INP", ref="VP")
    _src(s, 1, 7, "SINE(2 50m 1k 0 0 180)", "INN", ref="VN")
    # giriş tamponları
    s.w((1, 2), (4, 2))
    s.u(5, 3, ref="U1")
    s.r(4, 4, "10k", ref="R1")
    s.w((7, 3), (7, 4))
    s.lab(7, 3, "O1")
    s.w((1, 7), (4, 7))
    s.u(5, 8, ref="U2")
    s.r(4, 9, "10k", ref="R2")
    s.w((7, 8), (7, 9))
    s.lab(7, 8, "O2")
    s.lab(4, 4, "A", side="d")
    s.lab(4, 9, "B", side="d")
    s.lab(1, 12, "A", side="l")
    s.r(1, 12, "2k2", ref="RG")
    s.lab(4, 12, "B")
    # fark katı
    s.lab(11, 6, "O2", side="l")
    s.r(11, 6, "10k", ref="R3")
    s.u(15, 5, ref="U3")
    s.r(14, 6, "10k", ref="R4")
    s.w((17, 5), (17, 6))
    s.lab(11, 4, "O1", side="l")
    s.r(11, 4, "10k", ref="R5")
    s.w((14, 4), (14, 2))
    s.r(14, 2, "10k", ref="R6")
    s.gnd(17, 2)
    s.lab(17, 5, "OUT")
    return s.done(["V(INP,INN)", "V(OUT)"], ".tran 3m")


@example("transimpedance", "opamp/amps",
         T("Transimpedance amplifier (photodiode)", "Transempedans yükselteci (fotodiyot)", "Transimpedanzverstärker (Fotodiode)",
           "Трансимпедансный усилитель (фотодиод)"),
         T("A photodiode is a current source. The op-amp turns its 10 µA into −Rf·I = −1 V while holding the diode at 0 V.",
           "Fotodiyot bir akım kaynağıdır. Op-amp onun 10 µA'ini −Rf·I = −1 V'a çevirir ve diyotu 0 V'ta tutar.",
           "Eine Fotodiode ist eine Stromquelle. Der OPV macht aus 10 µA die Spannung −Rf·I = −1 V und hält die Diode auf 0 V.",
           "Фотодиод — источник тока. ОУ превращает 10 мкА в −Rf·I = −1 В и удерживает диод при 0 В."),
         check=lambda c: _between(min(c.t["V(OUT)"]), -1.02, -0.98))
def _transimpedance():
    s = Sheet()
    s.i(4, 4, "PULSE(0 10u 0.5m 10u 10u 1m 2m)", flip=True, ref="IPD")
    s.gnd(4, 6)
    s.u(5, 3)
    s.r(4, 4, "100k", ref="RF")
    s.w((7, 3), (7, 4))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "OUT")
    return s.done(["I(IPD)", "V(OUT)"], ".tran 4m")


# --- doğrusal olmayan ----------------------------------------------------------------------------

@example("comparator", "opamp/nonlinear",
         T("Comparator", "Karşılaştırıcı", "Komparator", "Компаратор"),
         T("Without feedback the huge gain drives the output to a rail: 5 V when the input is above the 2.5 V reference, 0 V below.",
           "Geri besleme yokken dev kazanç çıkışı bir raya sürer: giriş 2.5 V referansın üstündeyken 5 V, altındayken 0 V.",
           "Ohne Rückkopplung treibt die riesige Verstärkung den Ausgang an eine Grenze: 5 V über der 2,5-V-Referenz, 0 V darunter.",
           "Без обратной связи огромное усиление выводит выход на шину: 5 В выше опорных 2,5 В, 0 В ниже."),
         check=lambda c: (_between(max(c.t["V(OUT)"]), 4.95, 5.01), _between(min(c.t["V(OUT)"]), -0.01, 0.05)))
def _comparator():
    s = Sheet()
    _src(s, 1, 2, "SINE(2.5 2 1k)")
    s.w((1, 2), (4, 2))
    s.u(5, 3, "LM358 0..5")
    s.lab(4, 4, "REF", side="d")
    s.v(10, 1, "5", ref="VCC")
    s.gnd(10, 3)
    s.w((10, 1), (13, 1))
    s.r(13, 1, "10k", d="v")
    s.r(13, 3, "10k", d="v")
    s.gnd(13, 5)
    s.lab(13, 3, "REF")
    s.lab(7, 3, "OUT", side="d")
    return s.done(["V(IN)", "V(REF)", "V(OUT)"], ".tran 3m")


def _first_switch(c):
    out, vin = c.t["V(OUT)"], c.t["V(IN)"]
    for a, b, v in zip(out, out[1:], vin[1:]):
        if a > 0 > b:
            return v
    raise AssertionError("çıkış hiç düşmedi")


@example("schmitt", "opamp/nonlinear",
         T("Schmitt trigger", "Schmitt tetikleyici", "Schmitt-Trigger", "Триггер Шмитта"),
         T("Positive feedback creates two thresholds (±6 V). Noise near one threshold can no longer make the output chatter: hysteresis.",
           "Pozitif geri besleme iki eşik oluşturur (±6 V). Bir eşik civarındaki gürültü artık çıkışı titretemez: histerezis.",
           "Mitkopplung erzeugt zwei Schwellen (±6 V). Rauschen nahe einer Schwelle lässt den Ausgang nicht mehr flattern: Hysterese.",
           "Положительная обратная связь создаёт два порога (±6 В). Шум возле порога больше не вызывает дребезг выхода: гистерезис."),
         check=lambda c: _between(_first_switch(c), 5.6, 6.4))
def _schmitt():
    s = Sheet()
    _src(s, 1, 4, "SINE(0 10 1k)")
    s.w((1, 4), (4, 4))
    s.u(5, 3, "TL072 ±12")
    s.w((4, 2), (4, 1))
    s.r(4, 1, "10k", ref="RF")
    s.w((7, 1), (7, 3))
    s.r(1, 1, "10k", ref="R1")
    s.gnd(1, 1)
    s.lab(4, 1, "P", side="u")
    s.lab(7, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("precision_rectifier", "opamp/nonlinear",
         T("Precision rectifier (super diode)", "Hassas doğrultucu (süper diyot)", "Präzisionsgleichrichter (Superdiode)",
           "Прецизионный выпрямитель (супердиод)"),
         T("The diode sits inside the feedback loop, so its 0.6 V drop is divided by the op-amp gain: even a 0.3 V signal is rectified.",
           "Diyot geri besleme döngüsünün içindedir; 0.6 V düşümü op-amp kazancına bölünür: 0.3 V'luk işaret bile doğrultulur.",
           "Die Diode liegt in der Rückkopplungsschleife, ihr Spannungsabfall wird durch die Verstärkung geteilt: selbst 0,3 V werden gleichgerichtet.",
           "Диод внутри петли обратной связи, его падение делится на усиление ОУ: выпрямляется даже сигнал 0,3 В."),
         check=lambda c: (_between(max(c.t["V(OUT)"]), 0.28, 0.301), _between(min(c.t["V(OUT)"]), -0.01, 0.01)))
def _precision_rectifier():
    s = Sheet()
    _src(s, 1, 2, "SINE(0 0.3 1k)")
    s.w((1, 2), (4, 2))
    s.u(5, 3)
    s.d(7, 3, "1N4148", way=">")
    s.w((10, 3), (10, 5), (4, 5), (4, 4))
    s.w((10, 3), (13, 3))
    s.r(13, 3, "10k", d="v", ref="RL")
    s.gnd(13, 5)
    s.lab(13, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("log_amp", "opamp/nonlinear",
         T("Logarithmic amplifier", "Logaritmik yükselteç", "Logarithmierer", "Логарифмический усилитель"),
         T("A diode in the feedback path: the output follows −n·VT·ln(Vin/(R·Is)), so every ×10 at the input adds the same step at the output.",
           "Geri beslemede bir diyot: çıkış −n·VT·ln(Vin/(R·Is)) izler; girişteki her ×10 çıkışa aynı adımı ekler.",
           "Eine Diode in der Rückkopplung: der Ausgang folgt −n·UT·ln(Ue/(R·Is)); jedes ×10 am Eingang ergibt den gleichen Schritt.",
           "Диод в обратной связи: выход следует −n·UT·ln(Uвх/(R·Is)); каждое ×10 на входе даёт одинаковый шаг на выходе."),
         check=lambda c: (_between(_at(c, "V(OUT)", 1) - _at(c, "V(OUT)", 0.1), -0.16, -0.04),
                          _between(abs((_at(c, "V(OUT)", 1) - _at(c, "V(OUT)", 0.1))
                                       - (_at(c, "V(OUT)", 10) - _at(c, "V(OUT)", 1))), 0, 0.03)))
def _log_amp():
    s = Sheet()
    _src(s, 1, 4, "1")
    s.r(1, 4, "10k", ref="RIN")
    s.u(5, 3)
    s.d(4, 4, "1N4148", way=">")
    s.w((7, 3), (7, 4))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "OUT")
    return s.done(["V(OUT)"], ".dc V1 0.1 10 0.1")


# --- aktif filtreler ----------------------------------------------------------------------------

@example("integrator", "opamp/filters",
         T("Integrator", "Entegratör (integral alıcı)", "Integrator", "Интегратор"),
         T("A capacitor in the feedback path integrates the input: a square wave becomes a triangle. The large resistor stops DC drift.",
           "Geri beslemedeki kondansatör girişin integralini alır: kare dalga üçgen olur. Büyük direnç DC kaymasını önler.",
           "Ein Kondensator in der Rückkopplung integriert den Eingang: aus Rechteck wird Dreieck. Der große Widerstand verhindert Drift.",
           "Конденсатор в обратной связи интегрирует вход: меандр превращается в треугольник. Большой резистор предотвращает дрейф."),
         check=lambda c: _between(_amp(c.t["V(OUT)"]) * 2, 4.0, 5.2))
def _integrator():
    s = Sheet()
    _src(s, 1, 4, "PULSE(-1 1 0 1u 1u 0.5m 1m)")
    s.r(1, 4, "10k", ref="RIN")
    s.u(5, 3)
    s.cap(4, 4, "10n", d="h")
    s.w((4, 4), (4, 6))
    s.r(4, 6, "100k", ref="RF")
    s.w((7, 6), (7, 3))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 20m")


@example("differentiator", "opamp/filters",
         T("Differentiator", "Türev alıcı", "Differenzierer", "Дифференциатор"),
         T("Swap R and C of the integrator: the output is −RC·dVin/dt. A triangle (±4 V/ms slope) becomes a ±0.4 V square wave.",
           "Entegratörün R ve C'si yer değiştirir: çıkış −RC·dVin/dt olur. Üçgen (±4 V/ms eğim) ±0.4 V'luk kare dalgaya dönüşür.",
           "R und C des Integrators getauscht: Ausgang −RC·dUe/dt. Ein Dreieck (±4 V/ms) wird ein Rechteck mit ±0,4 V.",
           "R и C интегратора меняются местами: выход −RC·dUвх/dt. Треугольник (±4 В/мс) превращается в меандр ±0,4 В."),
         check=lambda c: _between(_amp(c.t["V(OUT)"]), 0.36, 0.42))
def _differentiator():
    s = Sheet()
    _src(s, 1, 4, "PULSE(-1 1 0 0.5m 0.5m 0 1m)")
    s.r(1, 4, "1k", ref="RS")
    s.cap(4, 4, "10n", d="h")
    s.u(8, 3)                          # + (7,2), − (7,4), çıkış (10,3)
    s.w((7, 4), (7, 5))
    s.r(7, 5, "10k", ref="RF")
    s.w((10, 5), (10, 3))
    s.w((7, 2), (6, 2))
    s.gnd(6, 2)
    s.lab(10, 3, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 4m")


@example("sallen_key_lp", "opamp/filters",
         T("Sallen–Key low-pass (2nd order)", "Sallen–Key alçak geçiren (2. derece)", "Sallen-Key-Tiefpass (2. Ordnung)",
           "ФНЧ Саллена–Ки 2-го порядка"),
         T("A unity-gain follower with RC feedback gives a Butterworth response: flat, −3 dB at 1.1 kHz, then −40 dB per decade.",
           "Kazancı 1 olan izleyici ve RC geri besleme Butterworth yanıtı verir: düz, 1.1 kHz'de −3 dB, sonra dekad başına −40 dB.",
           "Ein Spannungsfolger mit RC-Rückkopplung ergibt Butterworth-Verhalten: flach, −3 dB bei 1,1 kHz, dann −40 dB/Dekade.",
           "Повторитель с RC-обратной связью даёт характеристику Баттерворта: ровно, −3 дБ на 1,1 кГц, далее −40 дБ/дек."),
         check=lambda c: (_between(_db(c, "V(OUT)", 100), -0.1, 0.1),
                          _between(_db(c, "V(OUT)", 1 / (2 * math.pi * 10e3 * math.sqrt(20e-9 * 10e-9))), -3.4, -2.6)))
def _sallen_key_lp():
    s = Sheet()
    _src(s, 1, 3, "AC 1")
    s.r(1, 3, "10k", ref="R1")
    s.r(4, 3, "10k", ref="R2")
    s.w((7, 3), (10, 3))
    s.cap(7, 3, "10n", d="v", ref="C2")
    s.gnd(7, 5)
    s.w((4, 3), (4, 1))
    s.cap(4, 1, "20n", d="h", ref="C1")
    s.w((7, 1), (13, 1), (13, 4))
    s.u(11, 4)                         # + (10,3), − (10,5), çıkış (13,4)
    s.w((10, 5), (10, 6), (13, 6), (13, 4))
    s.lab(13, 4, "OUT")
    return s.done(["V(OUT)"], ".ac dec 50 10 100k")


@example("sallen_key_hp", "opamp/filters",
         T("Sallen–Key high-pass (2nd order)", "Sallen–Key yüksek geçiren (2. derece)", "Sallen-Key-Hochpass (2. Ordnung)",
           "ФВЧ Саллена–Ки 2-го порядка"),
         T("Same structure with R and C swapped: frequencies below ≈ 1 kHz are attenuated by 40 dB per decade.",
           "Aynı yapıda R ve C yer değiştirir: ≈ 1 kHz'in altındaki frekanslar dekad başına 40 dB zayıflar.",
           "Gleiche Struktur mit vertauschten R und C: Frequenzen unter ≈ 1 kHz werden mit 40 dB/Dekade gedämpft.",
           "Та же схема с переставленными R и C: частоты ниже ≈ 1 кГц ослабляются на 40 дБ/дек."),
         check=lambda c: (_between(_db(c, "V(OUT)", 50e3), -0.1, 0.1),
                          _between(_db(c, "V(OUT)", 1 / (2 * math.pi * 10e-9 * math.sqrt(11e3 * 22e3))), -3.4, -2.6)))
def _sallen_key_hp():
    s = Sheet()
    _src(s, 1, 3, "AC 1")
    s.cap(1, 3, "10n", d="h", ref="C1")
    s.cap(4, 3, "10n", d="h", ref="C2")
    s.w((7, 3), (10, 3))
    s.r(7, 3, "22k", d="v", ref="R2")
    s.gnd(7, 5)
    s.w((4, 3), (4, 1))
    s.r(4, 1, "11k", ref="R1")
    s.w((7, 1), (13, 1), (13, 4))
    s.u(11, 4)
    s.w((10, 5), (10, 6), (13, 6), (13, 4))
    s.lab(13, 4, "OUT")
    return s.done(["V(OUT)"], ".ac dec 50 10 100k")


def _peak(c, expr):
    k = max(range(len(c.sweep.x)), key=lambda i: abs(c.t[expr][i]))
    return c.sweep.x[k], 20 * math.log10(abs(c.t[expr][k]))


@example("mfb_bandpass", "opamp/filters",
         T("Multiple-feedback band-pass", "Çoklu geri beslemeli bant geçiren", "Bandpass mit Mehrfachgegenkopplung",
           "Полосовой фильтр с многопетлевой ОС"),
         T("Two capacitors and three resistors around one op-amp: a narrow peak (Q ≈ 5) at 1.67 kHz with gain −R2/(2R1) = −5 (14 dB).",
           "Bir op-amp çevresinde iki kondansatör ve üç direnç: 1.67 kHz'de dar bir tepe (Q ≈ 5), kazanç −R2/(2R1) = −5 (14 dB).",
           "Zwei Kondensatoren und drei Widerstände um einen OPV: schmale Spitze (Q ≈ 5) bei 1,67 kHz, Verstärkung −R2/(2R1) = −5 (14 dB).",
           "Два конденсатора и три резистора вокруг ОУ: узкий пик (Q ≈ 5) на 1,67 кГц с усилением −R2/(2R1) = −5 (14 дБ)."),
         check=lambda c: (_between(_peak(c, "V(OUT)")[0], 1580, 1760), _between(_peak(c, "V(OUT)")[1], 13.5, 14.3)))
def _mfb_bandpass():
    s = Sheet()
    _src(s, 1, 3, "AC 1")
    s.r(1, 3, "10k", ref="R1")
    s.r(4, 3, "1k", d="v", ref="R3")
    s.gnd(4, 5)
    s.cap(4, 3, "10n", d="h", ref="C1")
    s.w((7, 3), (10, 3))
    s.u(11, 4, flip=True)              # − (10,3), + (10,5), çıkış (13,4)
    s.gnd(10, 5)
    s.w((4, 3), (4, 0))
    s.cap(4, 0, "10n", d="h", ref="C2")
    s.w((7, 0), (13, 0), (13, 2))
    s.w((10, 3), (10, 2))
    s.r(10, 2, "100k", ref="R2")
    s.w((13, 2), (13, 4))
    s.lab(13, 4, "OUT")
    return s.done(["V(OUT)"], ".ac dec 100 100 10k")
