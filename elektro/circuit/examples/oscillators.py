"""Osilatörler: gevşemeli, fonksiyon üreteci, Wien köprüsü, faz kaydırmalı."""


from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("oscillators", T("Oscillators", "Osilatörler", "Oszillatoren", "Генераторы"))


def _between(value, lo, hi):
    assert lo <= value <= hi, f"{value:.4g} ∉ [{lo:g}, {hi:g}]"


def _late(values, frac=0.5):
    return values[int(len(values) * frac):]


def _period(c, expr, frac=0.5):
    """Son kısımdaki yükselen sıfır geçişlerinden ortalama periyot."""
    xs, ys = c.sweep.x, c.t[expr]
    mid = (max(_late(ys, frac)) + min(_late(ys, frac))) / 2
    start = int(len(xs) * frac)
    cross = [xs[i] for i in range(max(start, 1), len(xs)) if ys[i - 1] < mid <= ys[i]]
    assert len(cross) >= 3, f"{expr}: salınım yok ({len(cross)} geçiş)"
    return (cross[-1] - cross[0]) / (len(cross) - 1)


@example("relaxation", "oscillators",
         T("Op-amp relaxation oscillator", "Op-amp'lı gevşemeli osilatör", "Relaxationsoszillator mit OPV", "Релаксационный генератор на ОУ"),
         T("A Schmitt trigger that charges its own capacitor: the output flips each time the capacitor reaches ±6 V. T = 2RC·ln 3 ≈ 2.2 ms.",
           "Kendi kondansatörünü dolduran bir Schmitt tetikleyici: kondansatör ±6 V'a her ulaştığında çıkış döner. T = 2RC·ln 3 ≈ 2.2 ms.",
           "Ein Schmitt-Trigger, der seinen eigenen Kondensator lädt: der Ausgang kippt bei ±6 V am Kondensator. T = 2RC·ln 3 ≈ 2,2 ms.",
           "Триггер Шмитта, заряжающий свой конденсатор: выход переключается при ±6 В на конденсаторе. T = 2RC·ln 3 ≈ 2,2 мс."),
         check=lambda c: _between(_period(c, "V(OUT)"), 2.0e-3, 2.4e-3))
def _relaxation():
    s = Sheet()
    s.u(5, 3, "TL072 ±12")             # + (4,2), − (4,4), çıkış (7,3)
    s.r(4, 4, "10k", ref="RT")
    s.w((7, 3), (7, 4))
    s.cap(4, 4, "100n", d="v", ref="CT")
    s.gnd(4, 6)
    s.w((4, 2), (4, 1))
    s.r(4, 1, "10k", ref="R2")
    s.w((7, 1), (7, 3))
    s.r(1, 1, "10k", ref="R1")
    s.gnd(1, 1)
    s.lab(4, 4, "CAP", side="l")
    s.lab(7, 3, "OUT")
    return s.done(["V(OUT)", "V(CAP)"], ".tran 20m")


@example("function_generator", "oscillators",
         T("Function generator (square + triangle)", "Fonksiyon üreteci (kare + üçgen)", "Funktionsgenerator (Rechteck + Dreieck)",
           "Функциональный генератор (меандр + треугольник)"),
         T("An integrator turns the square wave into a triangle; a Schmitt trigger turns the triangle back into a square. f = R2/(4·R1·R·C) = 500 Hz.",
           "Entegratör kare dalgayı üçgene çevirir; Schmitt tetikleyici üçgeni yeniden kareye çevirir. f = R2/(4·R1·R·C) = 500 Hz.",
           "Ein Integrator macht aus dem Rechteck ein Dreieck, ein Schmitt-Trigger daraus wieder ein Rechteck. f = R2/(4·R1·R·C) = 500 Hz.",
           "Интегратор превращает меандр в треугольник, триггер Шмитта — треугольник обратно в меандр. f = R2/(4·R1·R·C) = 500 Гц."),
         check=lambda c: (_between(_period(c, "V(SQ)"), 1.8e-3, 2.2e-3), _between(max(_late(c.t["V(TRI)"])), 5.4, 6.6)))
def _function_generator():
    s = Sheet()
    # entegratör
    s.lab(1, 4, "SQ", side="l")
    s.r(1, 4, "10k", ref="R")
    s.u(5, 3, "TL072 ±12", ref="U1")
    s.cap(4, 4, "100n", ref="C", d="h")
    s.w((7, 3), (7, 4))
    s.w((4, 2), (3, 2))
    s.gnd(3, 2)
    s.lab(7, 3, "TRI")
    # evirmeyen Schmitt tetikleyici
    s.lab(10, 2, "TRI", side="l")
    s.r(10, 2, "10k", ref="R1")
    s.u(14, 3, "TL072 ±12", ref="U2")  # + (13,2), − (13,4), çıkış (16,3)
    s.w((13, 2), (13, 1))
    s.r(13, 1, "20k", ref="R2")
    s.w((16, 1), (16, 3))
    s.w((13, 4), (12, 4))
    s.gnd(12, 4)
    s.lab(16, 3, "SQ")
    return s.done(["V(SQ)", "V(TRI)"], ".tran 2u 16m")


@example("wien_bridge", "oscillators",
         T("Wien bridge oscillator", "Wien köprüsü osilatörü", "Wien-Brücken-Oszillator", "Генератор с мостом Вина"),
         T("The RC bridge passes f = 1/(2πRC) ≈ 1.6 kHz with 1/3 gain and 0° phase. The amplifier gain is a bit over 3; the diodes lower it as the amplitude grows, giving a clean sine.",
           "RC köprüsü f = 1/(2πRC) ≈ 1.6 kHz'i 1/3 kazanç ve 0° fazla geçirir. Yükselteç kazancı 3'ün biraz üstündedir; genlik büyüdükçe diyotlar kazancı düşürür, temiz bir sinüs çıkar.",
           "Die RC-Brücke lässt f = 1/(2πRC) ≈ 1,6 kHz mit 1/3 und 0° durch. Die Verstärkung liegt knapp über 3; die Dioden senken sie bei wachsender Amplitude: sauberer Sinus.",
           "RC-мост пропускает f = 1/(2πRC) ≈ 1,6 кГц с ослаблением 1/3 и фазой 0°. Усиление чуть больше 3; диоды снижают его с ростом амплитуды — получается чистый синус."),
         check=lambda c: (_between(1 / _period(c, "V(OUT)", 0.7), 1450, 1700), _between(max(_late(c.t["V(OUT)"], 0.7)), 0.5, 11.5)))
def _wien_bridge():
    s = Sheet()
    s.u(9, 5)                          # + (8,4), − (8,6), çıkış (11,5)
    s.lab(11, 5, "OUT")
    # seri RC (çıkıştan + girişe) ve paralel RC (+ girişten toprağa)
    s.w((11, 5), (11, 1))
    s.cap(8, 1, "10n", ref="CS", d="h")
    s.r(5, 1, "10k", ref="RS")
    s.w((5, 1), (5, 4), (8, 4))
    s.r(5, 4, "10k", d="v", ref="RP")
    s.gnd(5, 6)
    s.w((5, 4), (2, 4))
    s.cap(2, 4, "10n", d="v", ref="CP")
    s.gnd(2, 6)
    s.lab(8, 4, "P", side="u")
    # kazanç: Rf = 18k + (4k7 ∥ diyotlar), Rg = 10k
    s.lab(8, 6, "N", side="l")
    s.lab(2, 9, "N", side="l")
    s.r(2, 9, "18k", ref="RF1")
    s.r(5, 9, "4k7", ref="RF2")
    s.lab(8, 9, "OUT")
    s.w((5, 9), (5, 13))
    s.w((8, 9), (8, 13))
    s.d(5, 11, way=">")
    s.d(5, 13, way="<")
    s.lab(13, 9, "N", side="l")
    s.r(13, 9, "10k", d="v", ref="RG")
    s.gnd(13, 11)
    return s.done(["V(OUT)", "V(P)"], ".tran 30m")


@example("phase_shift", "oscillators",
         T("RC phase-shift oscillator", "RC faz kaydırmalı osilatör", "RC-Phasenschieber-Oszillator", "Генератор с фазосдвигающей RC-цепью"),
         T("Three RC sections shift the phase by 180° at f = 1/(2πRC√6) ≈ 650 Hz; the inverting amplifier adds another 180°. It needs a gain of at least 29.",
           "Üç RC katı f = 1/(2πRC√6) ≈ 650 Hz'de fazı 180° kaydırır; eviren yükselteç 180° daha ekler. En az 29 kazanç gerekir.",
           "Drei RC-Glieder drehen die Phase bei f = 1/(2πRC√6) ≈ 650 Hz um 180°, der invertierende Verstärker um weitere 180°. Nötig ist Verstärkung ≥ 29.",
           "Три RC-звена сдвигают фазу на 180° при f = 1/(2πRC√6) ≈ 650 Гц; инвертирующий усилитель добавляет ещё 180°. Нужно усиление не менее 29."),
         check=lambda c: _between(1 / _period(c, "V(OUT)", 0.6), 520, 720))
def _phase_shift():
    s = Sheet()
    s.lab(1, 4, "OUT", side="l")
    s.cap(1, 4, "10n", ref="C1", d="h")
    s.r(4, 4, "10k", d="v", ref="R1")
    s.gnd(4, 6)
    s.cap(4, 4, "10n", ref="C2", d="h")
    s.r(7, 4, "10k", d="v", ref="R2")
    s.gnd(7, 6)
    s.cap(7, 4, "10n", ref="C3", d="h")
    s.r(10, 4, "10k", ref="R3")
    s.u(14, 3)                         # + (13,2), − (13,4), çıkış (16,3)
    s.r(13, 4, "330k", ref="RF")
    s.w((16, 3), (16, 4))
    s.w((13, 2), (12, 2))
    s.gnd(12, 2)
    s.lab(16, 3, "OUT")
    return s.done(["V(OUT)"], ".tran 40m")


@example("ring_oscillator", "oscillators",
         T("Ring oscillator (3 inverters)", "Halka osilatör (3 evirici)", "Ringoszillator (3 Inverter)", "Кольцевой генератор (3 инвертора)"),
         T("An odd number of inverters in a loop can never settle: each RC delay passes the change on, so the ring keeps toggling.",
           "Halka halinde tek sayıda evirici asla dengeye gelemez: her RC gecikmesi değişimi bir sonrakine aktarır, halka sürekli döner.",
           "Eine ungerade Zahl von Invertern im Ring kommt nie zur Ruhe: jede RC-Verzögerung reicht die Änderung weiter.",
           "Нечётное число инверторов в кольце не может прийти к равновесию: каждая RC-задержка передаёт изменение дальше."),
         check=lambda c: _between(1 / _period(c, "V(O1)"), 5e3, 500e3))
def _ring_oscillator():
    """Evirici k: giriş Ik (iki kapı da etiketle), çıkış Ok; Ok —R— I(k+1), I(k+1) —C— toprak."""
    s = Sheet()
    s.v(1, 1, "5", ref="VDD")
    s.lab(1, 1, "VDD")
    s.gnd(1, 3)
    for k in range(3):
        x = 7 + 7 * k
        s.lab(x, 1, "VDD", side="u")
        s.m(x, 2, "BS250", rot=180)    # S (x,1), G (x+1,2), D (x,3)
        s.m(x, 4)                      # D (x,3), G (x−1,4), S (x,5)
        s.gnd(x, 5)
        s.lab(x + 1, 2, f"I{k + 1}")
        s.lab(x - 1, 4, f"I{k + 1}", side="l")
        s.lab(x, 3, f"O{k + 1}")
        s.lab(x - 3, 8, f"O{k + 1}", side="l")
        s.r(x - 3, 8, "10k", ref=f"RD{k + 1}")
        s.cap(x, 8, "1n", d="v", ref=f"CD{k + 1}")
        s.gnd(x, 10)
        s.lab(x, 8, f"I{k % 3 + 2 if k < 2 else 1}")
    return s.done(["V(O1)", "V(O2)", "V(O3)"], ".tran 0.2u 200u")
