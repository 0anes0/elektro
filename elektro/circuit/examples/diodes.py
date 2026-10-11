"""Diyot devreleri: karakteristik, doğrultucular, kırpıcı/kenetleyici, çoklayıcılar, zener, diyot lojiği."""

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("diodes", T("Diodes", "Diyotlar", "Dioden", "Диоды"))


def _src(s: Sheet, value: str, label: str = "IN"):
    """Kaynak solda, kabloyla (1, 1)–(1, 3) hattına bağlı: uzun kaynak etiketi yandaki dikey
    elemanın etiketine değmesin."""
    s.v(-2, 1, value)
    s.w((-2, 1), (1, 1))
    s.w((-2, 3), (1, 3))
    s.gnd(-2, 3)
    s.lab(-2, 1, label, side="l")


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _late(values, frac=0.5):
    return values[int(len(values) * frac):]


@example("diode_iv", "diodes",
         T("Diode I–V curve", "Diyot I–V eğrisi", "Dioden-Kennlinie", "ВАХ диода"),
         T("The source is swept from −1 V to 1 V. Almost no current flows until about 0.6 V, then it rises exponentially.",
           "Kaynak −1 V'tan 1 V'a taranır. Yaklaşık 0.6 V'a kadar neredeyse akım akmaz, sonra üstel olarak artar.",
           "Die Quelle läuft von −1 V bis 1 V. Bis etwa 0,6 V fließt kaum Strom, danach steigt er exponentiell.",
           "Источник меняется от −1 В до 1 В. Почти до 0,6 В тока нет, затем он растёт экспоненциально."),
         check=lambda c: (_between(c.t["I(D1)"][0], -1e-6, 0), _between(c.t["I(D1)"][-1], 10e-3, 50e-3)))
def _diode_iv():
    s = Sheet()
    s.v(1, 1, "0")
    s.r(1, 1, "10")
    s.d(4, 1, "1N4148", way="v")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    return s.done(["I(D1)", "V(E2)"], ".dc V1 -1 1 0.01")


@example("led_colors", "diodes",
         T("LED colours and forward voltage", "LED renkleri ve iletim gerilimi", "LED-Farben und Flussspannung",
           "Цвета светодиодов и прямое напряжение"),
         T("Red, green and blue LEDs with the same 330 Ω resistor: blue needs the most voltage, so it gets the least current.",
           "Aynı 330 Ω dirençle kırmızı, yeşil ve mavi LED: mavi en yüksek gerilimi ister, bu yüzden en az akımı alır.",
           "Rote, grüne und blaue LED mit gleichem 330-Ω-Widerstand: Blau braucht die höchste Spannung und bekommt den kleinsten Strom.",
           "Красный, зелёный и синий светодиоды с одинаковым резистором 330 Ом: синему нужно больше всего напряжения, его ток меньше."),
         check=lambda c: (c.r["I(D1)"] > c.r["I(D2)"] > c.r["I(D3)"]) or _between(0, 1, 2))
def _led_colors():
    s = Sheet()
    s.v(1, 1, "5")
    s.w((1, 1), (13, 1))
    for x, model in ((5, "LED"), (9, "LED-GREEN"), (13, "LED-BLUE")):
        s.r(x, 1, "330", d="v")
        s.d(x, 3, model, way="v")
    s.w((1, 3), (1, 5), (13, 5))
    s.gnd(1, 5)
    return s.done(["I(D1)", "I(D2)", "I(D3)"])


@example("half_wave", "diodes",
         T("Half-wave rectifier", "Yarım dalga doğrultucu", "Einweggleichrichter", "Однополупериодный выпрямитель"),
         T("The diode passes only the positive half-waves; the capacitor holds the peak (≈ 11.3 V) between them, leaving a small ripple.",
           "Diyot yalnız pozitif yarım dalgaları geçirir; kondansatör aralarda tepe değerini (≈ 11.3 V) tutar, küçük bir dalgalanma kalır.",
           "Die Diode lässt nur positive Halbwellen durch; der Kondensator hält dazwischen den Spitzenwert (≈ 11,3 V).",
           "Диод пропускает только положительные полуволны; конденсатор держит пиковое значение (≈ 11,3 В) между ними."),
         check=lambda c: _between(max(_late(c.t["V(OUT)"])), 11.0, 11.5))
def _half_wave():
    s = Sheet()
    s.v(1, 1, "SINE(0 12 50)")
    s.d(1, 1, "1N4007", way=">")
    s.cap(4, 1, "470u")
    s.w((4, 1), (7, 1))
    s.r(7, 1, "470", d="v")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(1, 1, "IN", side="l")
    s.lab(7, 1, "OUT")
    return s.done(["V(IN)", "V(OUT)", "I(D1)"], ".tran 100m")


@example("full_wave_ct", "diodes",
         T("Full-wave rectifier (centre tap)", "Tam dalga doğrultucu (orta uçlu)", "Mittelpunkt-Gleichrichter",
           "Двухполупериодный выпрямитель со средней точкой"),
         T("Two sources in antiphase stand for a centre-tapped transformer: each diode conducts on one half, so the ripple is at 100 Hz.",
           "Ters fazlı iki kaynak orta uçlu trafoyu temsil eder: her diyot bir yarımda iletir, dalgalanma 100 Hz olur.",
           "Zwei gegenphasige Quellen ersetzen einen Trafo mit Mittelanzapfung: jede Diode leitet eine Halbwelle, Brummen bei 100 Hz.",
           "Два источника в противофазе изображают трансформатор со средней точкой: каждый диод проводит полуволну, пульсации 100 Гц."),
         check=lambda c: _between(min(_late(c.t["V(OUT)"])), 9.5, 11.3))
def _full_wave_ct():
    s = Sheet()
    s.v(1, 1, "SINE(0 12 50)")
    s.v(1, 4, "SINE(0 12 50 0 0 180)")
    s.gnd(1, 3)
    s.gnd(1, 6)
    s.lab(1, 1, "A", side="l")
    s.lab(1, 4, "B", side="l")
    s.lab(4, 1, "A", side="l")
    s.d(4, 1, "1N4007", way=">")
    s.lab(4, 4, "B", side="l")
    s.d(4, 4, "1N4007", way=">")
    s.w((7, 1), (7, 4))
    s.w((7, 1), (10, 1))
    s.cap(10, 1, "470u")
    s.w((10, 1), (13, 1))
    s.r(13, 1, "470", d="v")
    s.w((10, 3), (13, 3))
    s.gnd(10, 3)
    s.lab(13, 1, "OUT")
    return s.done(["V(A)", "V(B)", "V(OUT)"], ".tran 60m")


@example("bridge_rectifier", "diodes",
         T("Bridge rectifier", "Köprü doğrultucu", "Brückengleichrichter", "Мостовой выпрямитель"),
         T("Four diodes steer both half-waves to the same output polarity. Two diodes are always in the path, so the output loses ≈ 1.4 V.",
           "Dört diyot iki yarım dalgayı da aynı çıkış yönüne yönlendirir. Yolda hep iki diyot vardır; çıkış ≈ 1.4 V kaybeder.",
           "Vier Dioden leiten beide Halbwellen zur gleichen Ausgangspolarität. Es liegen immer zwei Dioden im Pfad (≈ 1,4 V Verlust).",
           "Четыре диода направляют обе полуволны в одну полярность. В цепи всегда два диода, поэтому теряется ≈ 1,4 В."),
         check=lambda c: _between(max(_late(c.t["V(OUT)"])), 10.2, 10.8))
def _bridge_rectifier():
    s = Sheet()
    s.v(1, 1, "SINE(0 12 50)")
    s.lab(1, 1, "AC1", side="l")
    s.lab(1, 3, "AC2", side="l")
    for k, (anode, cathode) in enumerate((("AC1", "OUT"), ("AC2", "OUT"), ("GND", "AC1"), ("GND", "AC2"))):
        y = 1 + 2 * k
        s.d(5, y, "1N4007", way=">")
        if anode == "GND":
            s.gnd(5, y)
        else:
            s.lab(5, y, anode, side="l")
        s.lab(8, y, cathode)
    s.cap(12, 1, "470u")
    s.r(15, 1, "1k", d="v")
    s.w((12, 1), (15, 1))
    s.w((12, 3), (15, 3))
    s.lab(12, 1, "OUT", side="l")
    s.gnd(12, 3)
    return s.done(["V(AC1,AC2)", "V(OUT)"], ".tran 60m")


@example("clipper", "diodes",
         T("Diode clipper", "Diyotlu kırpıcı", "Diodenbegrenzer", "Диодный ограничитель"),
         T("A diode to ground limits the positive half to about 0.65 V; the negative half passes unchanged.",
           "Toprağa bağlı diyot pozitif yarımı yaklaşık 0.65 V'ta keser; negatif yarım olduğu gibi geçer.",
           "Eine Diode gegen Masse begrenzt die positive Halbwelle auf etwa 0,65 V; die negative bleibt unverändert.",
           "Диод на землю ограничивает положительную полуволну примерно 0,65 В; отрицательная проходит без изменений."),
         check=lambda c: (_between(max(c.t["V(OUT)"]), 0.55, 0.8), _between(min(c.t["V(OUT)"]), -5.0, -4.9)))
def _clipper():
    s = Sheet()
    _src(s, "SINE(0 5 1k)")
    s.r(1, 1, "1k")
    s.d(4, 1, "1N4148", way="v")
    s.w((1, 3), (4, 3))
    s.lab(4, 1, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("double_clipper", "diodes",
         T("Double clipper (antiparallel diodes)", "Çift kırpıcı (ters paralel diyot)", "Doppelbegrenzer (antiparallele Dioden)",
           "Двусторонний ограничитель"),
         T("Two diodes in opposite directions clip both halves at ±0.65 V — a simple input protection.",
           "Ters yönlü iki diyot iki yarımı da ±0.65 V'ta keser — basit bir giriş koruması.",
           "Zwei gegensinnige Dioden begrenzen beide Halbwellen auf ±0,65 V — ein einfacher Eingangsschutz.",
           "Два встречных диода ограничивают обе полуволны на ±0,65 В — простая защита входа."),
         check=lambda c: (_between(max(c.t["V(OUT)"]), 0.55, 0.8), _between(min(c.t["V(OUT)"]), -0.8, -0.55)))
def _double_clipper():
    s = Sheet()
    _src(s, "SINE(0 5 1k)")
    s.r(1, 1, "1k")
    s.w((4, 1), (7, 1))
    s.d(4, 1, "1N4148", way="v")
    s.d(7, 1, "1N4148", way="^")
    s.w((1, 3), (7, 3))
    s.lab(7, 1, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 3m")


@example("clamper", "diodes",
         T("Clamper (DC restorer)", "Kenetleyici (DC düzey kaydırıcı)", "Klemmschaltung", "Фиксатор уровня"),
         T("The capacitor charges to the negative peak through the diode: the whole wave is shifted up, from ≈ −0.6 V to ≈ +9.4 V.",
           "Kondansatör diyot üzerinden negatif tepeye dolar: tüm dalga yukarı kayar, ≈ −0.6 V ile ≈ +9.4 V arasında salınır.",
           "Der Kondensator lädt sich über die Diode auf die negative Spitze: die Welle wird nach oben verschoben (≈ −0,6 … +9,4 V).",
           "Конденсатор заряжается через диод до отрицательного пика: волна сдвигается вверх (≈ −0,6 … +9,4 В)."),
         check=lambda c: (_between(max(_late(c.t["V(OUT)"])), 9.0, 9.7), _between(min(_late(c.t["V(OUT)"])), -0.8, -0.3)))
def _clamper():
    s = Sheet()
    _src(s, "SINE(0 5 1k)")
    s.cap(1, 1, "10u", d="h")
    s.w((4, 1), (7, 1))
    s.d(4, 1, "1N4148", way="^")
    s.r(7, 1, "100k", d="v")
    s.w((1, 3), (7, 3))
    s.lab(7, 1, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 10m")


@example("voltage_doubler", "diodes",
         T("Voltage doubler (Greinacher)", "Gerilim katlayıcı (Greinacher)", "Spannungsverdoppler (Greinacher)", "Удвоитель напряжения"),
         T("A clamper followed by a peak detector: the output charges up to about twice the input peak (≈ 18.7 V from 10 V).",
           "Kenetleyiciyi tepe dedektörü izler: çıkış giriş tepesinin yaklaşık iki katına dolar (10 V'tan ≈ 18.7 V).",
           "Eine Klemmschaltung mit nachfolgendem Spitzengleichrichter: der Ausgang lädt sich auf etwa die doppelte Spitze (≈ 18,7 V).",
           "Фиксатор уровня и пиковый детектор: выход заряжается почти до удвоенной амплитуды (≈ 18,7 В из 10 В)."),
         check=lambda c: _between(max(c.t["V(OUT)"]), 17.5, 19.5))
def _voltage_doubler():
    s = Sheet()
    _src(s, "SINE(0 10 1k)")
    s.cap(1, 1, "10u", d="h")
    s.d(4, 1, "1N4148", way="^")
    s.d(4, 1, "1N4148", way=">")
    s.cap(7, 1, "10u")
    s.w((7, 1), (10, 1))
    s.r(10, 1, "100k", d="v")
    s.w((1, 3), (10, 3))
    s.lab(4, 1, "MID", side="u")
    s.lab(10, 1, "OUT")
    return s.done(["V(MID)", "V(OUT)"], ".tran 30m")


@example("voltage_quadrupler", "diodes",
         T("Voltage quadrupler (Cockcroft–Walton)", "Gerilim dörtleyici (Cockcroft–Walton)", "Spannungsvervierfacher (Cockcroft-Walton)",
           "Учетверитель напряжения (Кокрофт–Уолтон)"),
         T("Two doubler stages stacked: each stage adds about two input peaks. Used in high-voltage supplies (CRT, ion generators).",
           "Üst üste iki katlayıcı: her kat yaklaşık iki giriş tepesi ekler. Yüksek gerilim kaynaklarında kullanılır.",
           "Zwei gestapelte Verdopplerstufen: jede Stufe addiert etwa zwei Eingangsspitzen. Für Hochspannungsquellen.",
           "Две ступени удвоителя друг над другом: каждая добавляет около двух амплитуд входа. Применяется в источниках высокого напряжения."),
         check=lambda c: _between(max(c.t["V(OUT)"]), 30, 40))
def _voltage_quadrupler():
    """C1: IN–A1, D1: GND→A1, D2: A1→B1, C2: GND–B1, C3: A1–A2, D3: B1→A2, D4: A2→OUT, C4: B1–OUT."""
    s = Sheet()
    s.v(1, 1, "SINE(0 10 1k)")
    s.gnd(1, 3)
    s.lab(1, 1, "IN", side="l")
    s.lab(4, 1, "IN", side="l")
    s.cap(4, 1, "10u", d="h")
    s.lab(7, 1, "A1")
    s.lab(10, 1, "A1", side="l")
    s.d(10, 1, way=">")
    s.lab(13, 1, "B1")
    s.lab(16, 1, "A1", side="l")
    s.cap(16, 1, "10u", d="h")
    s.lab(19, 1, "A2")
    s.gnd(4, 4)
    s.d(4, 4, way=">")
    s.lab(7, 4, "A1")
    s.gnd(10, 4)
    s.cap(10, 4, "10u", d="h")
    s.lab(13, 4, "B1")
    s.lab(16, 4, "B1", side="l")
    s.d(16, 4, way=">")
    s.lab(19, 4, "A2")
    s.lab(4, 7, "A2", side="l")
    s.d(4, 7, way=">")
    s.lab(7, 7, "OUT")
    s.lab(10, 7, "B1", side="l")
    s.cap(10, 7, "10u", d="h")
    s.lab(13, 7, "OUT")
    s.lab(16, 7, "OUT", side="l")
    s.r(16, 7, "1meg", d="h")
    s.gnd(19, 7)
    return s.done(["V(B1)", "V(OUT)"], ".tran 60m")


@example("zener", "diodes",
         T("Zener regulator", "Zener regülatör", "Z-Dioden-Regler", "Стабилизатор на стабилитроне"),
         T("The input is swept 0–15 V: above ≈ 5.1 V the zener conducts in reverse and holds the output almost constant.",
           "Giriş 0–15 V taranır: ≈ 5.1 V'un üstünde zener ters yönde iletir ve çıkışı neredeyse sabit tutar.",
           "Der Eingang läuft von 0 bis 15 V: oberhalb ≈ 5,1 V leitet die Z-Diode in Sperrrichtung und hält den Ausgang fast konstant.",
           "Вход меняется 0–15 В: выше ≈ 5,1 В стабилитрон пробивается и держит выход почти постоянным."),
         check=lambda c: (_between(c.t["V(OUT)"][-1], 5.0, 5.4), _between(c.t["V(OUT)"][-1] - c.t["V(OUT)"][100], 0, 0.3)))
def _zener():
    s = Sheet()
    s.v(1, 1, "12")
    s.r(1, 1, "470")
    s.d(4, 1, "BZX5V1", way="^")
    s.w((4, 1), (7, 1))
    s.r(7, 1, "1k", d="v")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(7, 1, "OUT")
    return s.done(["V(OUT)", "I(D1.K)"], ".dc V1 0 15 0.1")


@example("zener_iv", "diodes",
         T("Zener I–V curve", "Zener I–V eğrisi", "Kennlinie der Z-Diode", "ВАХ стабилитрона"),
         T("Forward: like a normal diode (≈ 0.7 V). Reverse: almost no current until the breakdown voltage −5.1 V, then a steep rise.",
           "İleri yönde normal diyot gibi (≈ 0.7 V). Ters yönde −5.1 V kırılma gerilimine kadar neredeyse akım yok, sonra dik artış.",
           "Durchlass: wie eine normale Diode (≈ 0,7 V). Sperrrichtung: kaum Strom bis −5,1 V, dann steiler Anstieg.",
           "Прямое направление: как обычный диод (≈ 0,7 В). Обратное: почти нет тока до −5,1 В, затем резкий рост."),
         check=lambda c: (_between(c.t["I(D1)"][0], -60e-3, -5e-3), _between(c.t["I(D1)"][len(c.t["I(D1)"]) // 2], -1e-6, 1e-6)))
def _zener_iv():
    s = Sheet()
    s.v(1, 1, "0")
    s.r(1, 1, "100")
    s.d(4, 1, "BZX5V1", way="v")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    return s.done(["I(D1)"], ".dc V1 -8 1 0.02")


@example("peak_detector", "diodes",
         T("Peak detector", "Tepe dedektörü", "Spitzenwertgleichrichter", "Пиковый детектор"),
         T("The capacitor charges to the highest input value and keeps it; the large resistor discharges it slowly (AM radio detectors).",
           "Kondansatör girişin en yüksek değerine dolar ve onu tutar; büyük direnç yavaşça boşaltır (AM radyo dedektörü).",
           "Der Kondensator lädt sich auf den höchsten Eingangswert und hält ihn; der große Widerstand entlädt langsam (AM-Demodulator).",
           "Конденсатор заряжается до максимального входного значения и держит его; большой резистор медленно разряжает (АМ-детектор)."),
         check=lambda c: _between(min(_late(c.t["V(OUT)"])), 3.5, 4.5))
def _peak_detector():
    s = Sheet()
    s.v(1, 1, "SINE(0 5 1k)")
    s.d(1, 1, "1N4148", way=">")
    s.cap(4, 1, "1u")
    s.w((4, 1), (7, 1))
    s.r(7, 1, "100k", d="v")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(1, 1, "IN", side="l")
    s.lab(7, 1, "OUT")
    return s.done(["V(IN)", "V(OUT)"], ".tran 10m")


def _logic_inputs(s: Sheet):
    s.v(1, 1, "PULSE(0 5 1m 1u 1u 1m 2m)", ref="VA")
    s.v(1, 5, "PULSE(0 5 2m 1u 1u 2m 4m)", ref="VB")
    s.gnd(1, 3)
    s.gnd(1, 7)
    s.lab(1, 1, "A", side="l")
    s.lab(1, 5, "B", side="l")


@example("diode_or", "diodes",
         T("Diode OR gate", "Diyotlu VEYA kapısı", "Dioden-ODER-Gatter", "Диодный элемент ИЛИ"),
         T("The output is high when input A OR input B is high (minus one diode drop). The resistor pulls it low otherwise.",
           "A VEYA B girişi yüksekken çıkış yüksektir (bir diyot düşümü eksik). Aksi halde direnç çıkışı aşağı çeker.",
           "Der Ausgang ist high, wenn A ODER B high ist (minus eine Diodenspannung). Sonst zieht der Widerstand nach unten.",
           "Выход в 1, если A ИЛИ B в 1 (минус падение на диоде). Иначе резистор тянет его вниз."),
         check=lambda c: (_between(c.t["V(OUT)"][50], -0.1, 0.5),          # t = 0.4 ms: A = B = 0
                          _between(max(c.t["V(OUT)"]), 4.0, 4.6)))
def _diode_or():
    s = Sheet()
    _logic_inputs(s)
    s.lab(5, 2, "A", side="l")
    s.d(5, 2, way=">")
    s.lab(5, 5, "B", side="l")
    s.d(5, 5, way=">")
    s.w((8, 2), (8, 5))
    s.w((8, 2), (11, 2))
    s.r(11, 2, "10k", d="v")
    s.gnd(11, 4)
    s.lab(8, 4, "OUT", side="l")
    return s.done(["V(A)", "V(B)", "V(OUT)"], ".tran 8m")


@example("diode_and", "diodes",
         T("Diode AND gate", "Diyotlu VE kapısı", "Dioden-UND-Gatter", "Диодный элемент И"),
         T("A pull-up resistor tries to lift the output; any low input pulls it down through its diode. High only when A AND B are high.",
           "Yukarı çekme direnci çıkışı kaldırmaya çalışır; alçak olan her giriş kendi diyotuyla onu aşağı çeker. Yalnız A VE B yüksekken yüksek.",
           "Ein Pull-up hebt den Ausgang an; jeder Low-Eingang zieht ihn über seine Diode herunter. High nur, wenn A UND B high sind.",
           "Подтягивающий резистор поднимает выход; любой вход в 0 тянет его вниз через диод. 1 только при A И B в 1."),
         check=lambda c: (_between(min(c.t["V(OUT)"]), 0.4, 0.8), _between(max(c.t["V(OUT)"]), 4.9, 5.1)))
def _diode_and():
    s = Sheet()
    _logic_inputs(s)
    s.v(14, 1, "5", ref="VCC")
    s.gnd(14, 3)
    s.lab(14, 1, "VCC")
    s.lab(11, 0, "VCC", side="u")
    s.r(11, 0, "10k", d="v")
    s.w((11, 2), (11, 5))
    s.lab(5, 2, "A", side="l")
    s.d(5, 2, way="<")
    s.lab(5, 5, "B", side="l")
    s.d(5, 5, way="<")
    s.w((8, 2), (11, 2))
    s.w((8, 5), (11, 5))
    s.lab(11, 4, "OUT")
    return s.done(["V(A)", "V(B)", "V(OUT)"], ".tran 8m")
