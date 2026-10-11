"""Alternatif akım devreleri: faz, rezonans, güç faktörü."""

import cmath
import math

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("ac", T("AC circuits", "AC devreleri", "Wechselstromkreise", "Цепи переменного тока"))


def _near(value, target, rel=0.02):
    assert abs(value - target) <= abs(target) * rel + 1e-12, f"{value:.6g} ≠ {target:.6g}"


def _phase(v) -> float:
    return math.degrees(cmath.phase(v))


def _at(c, f):
    return min(range(len(c.sweep.x)), key=lambda i: abs(c.sweep.x[i] - f))


@example("cap_ac", "ac",
         T("Capacitor on AC: current leads", "AC'de kondansatör: akım öndedir", "Kondensator an Wechselspannung: Strom eilt vor",
           "Конденсатор на переменном токе: ток опережает"),
         T("The capacitor current leads its voltage by 90°. Its reactance Xc = 1/(2πfC) ≈ 1.6 kΩ at 1 kHz.",
           "Kondansatör akımı geriliminden 90° öndedir. 1 kHz'de reaktans Xc = 1/(2πfC) ≈ 1.6 kΩ.",
           "Der Kondensatorstrom eilt der Spannung um 90° voraus. Blindwiderstand Xc = 1/(2πfC) ≈ 1,6 kΩ bei 1 kHz.",
           "Ток конденсатора опережает напряжение на 90°. Реактивное сопротивление Xc = 1/(2πfC) ≈ 1,6 кОм при 1 кГц."),
         check=lambda c: _near(max(c.t["I(C1)"][500:]), 1 / (1 / (2 * math.pi * 1e3 * 100e-9))))
def _cap_ac():
    s = Sheet()
    s.v(1, 1, "SINE(0 1 1k)")
    s.w((1, 1), (4, 1))
    s.cap(4, 1, "100n")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "V")
    return s.done(["V(V)", "I(C1)"], ".tran 3m")


@example("ind_ac", "ac",
         T("Inductor on AC: current lags", "AC'de bobin: akım geridedir", "Spule an Wechselspannung: Strom eilt nach",
           "Катушка на переменном токе: ток отстаёт"),
         T("The inductor current lags its voltage by 90°. Its reactance XL = 2πfL ≈ 63 Ω at 1 kHz; a small resistor sets the DC level.",
           "Bobin akımı geriliminden 90° geridedir. 1 kHz'de XL = 2πfL ≈ 63 Ω; küçük direnç DC seviyesini belirler.",
           "Der Spulenstrom eilt der Spannung um 90° nach. XL = 2πfL ≈ 63 Ω bei 1 kHz; ein kleiner Widerstand legt den Gleichanteil fest.",
           "Ток катушки отстаёт от напряжения на 90°. XL = 2πfL ≈ 63 Ом при 1 кГц; малый резистор задаёт постоянную составляющую."),
         check=lambda c: _near((max(c.t["I(L1)"][700:]) - min(c.t["I(L1)"][700:])) / 2,
                               1 / math.hypot(5, 2 * math.pi * 1e3 * 10e-3), rel=0.03))
def _ind_ac():
    s = Sheet()
    s.v(1, 1, "SINE(0 1 1k)")
    s.r(1, 1, "5")
    s.ind(4, 1, "10m", d="v")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(4, 1, "V")
    return s.done(["V(V)", "I(L1)"], ".tran 10m")


@example("rc_phase", "ac",
         T("RC phase shift (phasors)", "RC faz kayması (fazörler)", "RC-Phasenverschiebung (Zeiger)", "Фазовый сдвиг RC (векторы)"),
         T("AC analysis: at f = 1/(2πRC) ≈ 1 kHz the capacitor voltage is 0.707 of the input and 45° behind it.",
           "AC analiz: f = 1/(2πRC) ≈ 1 kHz'de kondansatör gerilimi girişin 0.707 katıdır ve 45° geridedir.",
           "AC-Analyse: bei f = 1/(2πRC) ≈ 1 kHz ist die Kondensatorspannung 0,707 der Eingangsspannung und 45° nacheilend.",
           "AC-анализ: при f = 1/(2πRC) ≈ 1 кГц напряжение на конденсаторе 0,707 от входного и отстаёт на 45°."),
         check=lambda c: _near(_phase(c.t["V(VC)"][_at(c, 1e3)]), -45, rel=0.03))
def _rc_phase():
    s = Sheet()
    s.v(1, 1, "AC 1")
    s.r(1, 1, "1k")
    s.cap(4, 1, "159n")
    s.w((1, 3), (4, 3))
    s.gnd(1, 3)
    s.lab(1, 1, "IN", side="l")
    s.lab(4, 1, "VC")
    return s.done(["V(IN)", "V(VC)", "V(IN,VC)", "I(R1)"], ".ac dec 50 10 100k")


@example("series_resonance", "ac",
         T("Series resonance", "Seri rezonans", "Reihenschwingkreis", "Последовательный резонанс"),
         T("At f0 = 1/(2π√LC) ≈ 1.6 kHz the reactances of L and C cancel: the current is maximum, limited only by R.",
           "f0 = 1/(2π√LC) ≈ 1.6 kHz'de L ve C reaktansları birbirini götürür: akım en büyüktür, yalnız R sınırlar.",
           "Bei f0 = 1/(2π√LC) ≈ 1,6 kHz heben sich die Blindwiderstände auf: der Strom ist maximal, nur R begrenzt ihn.",
           "На f0 = 1/(2π√LC) ≈ 1,6 кГц реактивные сопротивления компенсируются: ток максимален, его ограничивает только R."),
         check=lambda c: _near(c.sweep.x[max(range(len(c.sweep.x)), key=lambda i: abs(c.t["I(R1)"][i]))],
                               1 / (2 * math.pi * math.sqrt(10e-3 * 1e-6)), rel=0.03))
def _series_resonance():
    s = Sheet()
    s.v(1, 1, "AC 1")
    s.r(1, 1, "10")
    s.ind(4, 1, "10m")
    s.cap(7, 1, "1u")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    return s.done(["I(R1)", "V(H2)"], ".ac dec 100 100 10k")


@example("parallel_resonance", "ac",
         T("Parallel resonance (tank)", "Paralel rezonans (tank)", "Parallelschwingkreis", "Параллельный резонанс (контур)"),
         T("A parallel LC has its highest impedance at resonance: the voltage across the tank peaks at f0 ≈ 1.6 kHz.",
           "Paralel LC'nin empedansı rezonansta en büyüktür: tank gerilimi f0 ≈ 1.6 kHz'de tepe yapar.",
           "Ein Parallel-LC hat bei Resonanz die größte Impedanz: die Spannung am Kreis ist bei f0 ≈ 1,6 kHz maximal.",
           "Параллельный LC имеет наибольшее сопротивление на резонансе: напряжение на контуре максимально при f0 ≈ 1,6 кГц."),
         check=lambda c: _near(c.sweep.x[max(range(len(c.sweep.x)), key=lambda i: abs(c.t["V(TANK)"][i]))],
                               1 / (2 * math.pi * math.sqrt(10e-3 * 1e-6)), rel=0.03))
def _parallel_resonance():
    s = Sheet()
    s.v(1, 1, "AC 1")
    s.r(1, 1, "10k")
    s.w((4, 1), (7, 1))
    s.ind(4, 1, "10m", d="v")
    s.cap(7, 1, "1u")
    s.w((1, 3), (7, 3))
    s.gnd(1, 3)
    s.lab(7, 1, "TANK")
    return s.done(["V(TANK)", "I(L1)", "I(C1)"], ".ac dec 100 100 10k")


@example("power_factor", "ac",
         T("Power factor correction", "Güç faktörü düzeltme", "Blindleistungskompensation", "Компенсация реактивной мощности"),
         T("Two identical 230 V / 50 Hz inductive loads (R + L, cos φ = 0.6). The right one has a 47 µF capacitor: its source current drops from 4.6 A to 2.8 A peak.",
           "İki aynı 230 V / 50 Hz endüktif yük (R + L, cos φ = 0.6). Sağdakinde 47 µF kondansatör var: kaynak akımı 4.6 A'den 2.8 A tepeye düşer.",
           "Zwei gleiche induktive Lasten an 230 V / 50 Hz (R + L, cos φ = 0,6). Rechts mit 47 µF: der Quellstrom sinkt von 4,6 A auf 2,8 A Spitze.",
           "Две одинаковые индуктивные нагрузки 230 В / 50 Гц (R + L, cos φ = 0,6). Справа конденсатор 47 мкФ: ток источника падает с 4,6 до 2,8 А (амплитуда)."),
         check=lambda c: _near(max(c.t["I(V1)"][600:]) / max(c.t["I(V2)"][600:]), 1 / 0.6, rel=0.05))
def _power_factor():
    s = Sheet()
    for k, cap in enumerate((None, "47u")):
        x = 1 + 9 * k
        s.v(x, 1, "SINE(0 325 50)")
        s.w((x, 1), (x + 3, 1))
        s.r(x + 3, 1, "30", d="v")
        s.ind(x + 3, 3, "127m", d="v")
        s.w((x, 3), (x, 5), (x + 3, 5))
        s.gnd(x, 5)
        if cap:
            s.w((x + 3, 1), (x + 6, 1))
            s.cap(x + 6, 1, cap)
            s.w((x + 6, 3), (x + 6, 5), (x + 3, 5))
    return s.done(["I(V1)", "I(V2)"], ".tran 60m")
