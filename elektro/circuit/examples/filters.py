"""Pasif filtreler (AC analiz ile Bode eğrileri)."""

import math

from elektro.circuit.examples import T, example, folder
from elektro.circuit.examples._sheet import Sheet

folder("filters", T("Passive filters", "Pasif filtreler", "Passive Filter", "Пассивные фильтры"))


def _gain_db(c, expr, f):
    k = min(range(len(c.sweep.x)), key=lambda i: abs(c.sweep.x[i] - f))
    return 20 * math.log10(abs(c.t[expr][k]))


def _expect_db(c, expr, f, db, tol=0.4):
    got = _gain_db(c, expr, f)
    assert abs(got - db) <= tol, f"{expr} @ {f:g} Hz: {got:.2f} dB ≠ {db:.2f} dB"


def _ladder(s: Sheet, parts, source="AC 1", out="OUT"):
    """Soldan sağa merdiven: ('s', tür, değer) üst hatta seri, ('p', tür, değer) toprağa paralel.

    Art arda iki paralel eleman (ya da kaynağın hemen yanındaki paralel eleman) aynı yere
    düşmesin diye araya kısa bir kablo konur. Alt hat, paralel elemanların alt uçlarından geçer.
    """
    s.v(1, 1, source)
    s.lab(1, 1, "IN", side="l")
    x, last_parallel = 1, None
    for role, kind, value in parts:
        if role == "s":
            getattr(s, kind)(x, 1, value, d="h")
            x += 3
        else:
            if last_parallel == x or x == 1:
                s.w((x, 1), (x + 3, 1))
                x += 3
            getattr(s, kind)(x, 1, value, d="v")
            last_parallel = x
    s.w((1, 3), (x, 3))
    s.gnd(1, 3)
    s.lab(x, 1, out)
    return x


@example("rc_lowpass", "filters",
         T("RC low-pass", "RC alçak geçiren", "RC-Tiefpass", "RC фильтр нижних частот"),
         T("Low frequencies pass, high ones are attenuated by 20 dB per decade. Cutoff fc = 1/(2πRC) ≈ 1 kHz (−3 dB, −45°).",
           "Düşük frekanslar geçer, yüksekler dekad başına 20 dB zayıflar. Kesim fc = 1/(2πRC) ≈ 1 kHz (−3 dB, −45°).",
           "Tiefe Frequenzen passieren, hohe werden mit 20 dB/Dekade gedämpft. Grenzfrequenz fc = 1/(2πRC) ≈ 1 kHz (−3 dB, −45°).",
           "Низкие частоты проходят, высокие ослабляются на 20 дБ/дек. Частота среза fc = 1/(2πRC) ≈ 1 кГц (−3 дБ, −45°)."),
         check=lambda c: (_expect_db(c, "V(OUT)", 1001, -3.01), _expect_db(c, "V(OUT)", 100e3, -40, tol=0.5)))
def _rc_lowpass():
    s = Sheet()
    _ladder(s, [("s", "r", "1k"), ("p", "cap", "159n")])
    return s.done(["V(IN)", "V(OUT)"], ".ac dec 50 10 100k")


@example("rc_highpass", "filters",
         T("RC high-pass", "RC yüksek geçiren", "RC-Hochpass", "RC фильтр верхних частот"),
         T("The capacitor blocks DC and low frequencies; above fc ≈ 1 kHz the signal passes almost unchanged.",
           "Kondansatör DC'yi ve düşük frekansları tutar; fc ≈ 1 kHz'in üstünde işaret neredeyse olduğu gibi geçer.",
           "Der Kondensator sperrt Gleichspannung und tiefe Frequenzen; oberhalb fc ≈ 1 kHz passiert das Signal fast unverändert.",
           "Конденсатор не пропускает постоянный ток и низкие частоты; выше fc ≈ 1 кГц сигнал проходит почти без изменений."),
         check=lambda c: (_expect_db(c, "V(OUT)", 1001, -3.01), _expect_db(c, "V(OUT)", 10, -40, tol=0.5)))
def _rc_highpass():
    s = Sheet()
    _ladder(s, [("s", "cap", "159n"), ("p", "r", "1k")])
    return s.done(["V(IN)", "V(OUT)"], ".ac dec 50 10 100k")


@example("rl_lowpass", "filters",
         T("RL low-pass", "RL alçak geçiren", "RL-Tiefpass", "RL фильтр нижних частот"),
         T("A series inductor passes DC but its reactance grows with frequency. fc = R/(2πL) ≈ 1.6 kHz.",
           "Seri bobin DC'yi geçirir ama reaktansı frekansla büyür. fc = R/(2πL) ≈ 1.6 kHz.",
           "Eine Längsspule lässt Gleichstrom durch, ihr Blindwiderstand wächst mit der Frequenz. fc = R/(2πL) ≈ 1,6 kHz.",
           "Последовательная катушка пропускает постоянный ток, но её сопротивление растёт с частотой. fc = R/(2πL) ≈ 1,6 кГц."),
         check=lambda c: _expect_db(c, "V(OUT)", 1e3 / (2 * math.pi * 0.1), -3.01))
def _rl_lowpass():
    s = Sheet()
    _ladder(s, [("s", "ind", "100m"), ("p", "r", "1k")])
    return s.done(["V(IN)", "V(OUT)"], ".ac dec 50 10 100k")


@example("rl_highpass", "filters",
         T("RL high-pass", "RL yüksek geçiren", "RL-Hochpass", "RL фильтр верхних частот"),
         T("A parallel inductor shorts low frequencies to ground; above fc = R/(2πL) ≈ 1.6 kHz they pass.",
           "Paralel bobin düşük frekansları toprağa kısa devre eder; fc = R/(2πL) ≈ 1.6 kHz'in üstü geçer.",
           "Eine Querspule schließt tiefe Frequenzen kurz; oberhalb fc = R/(2πL) ≈ 1,6 kHz passieren sie.",
           "Параллельная катушка замыкает низкие частоты на землю; выше fc = R/(2πL) ≈ 1,6 кГц они проходят."),
         check=lambda c: _expect_db(c, "V(OUT)", 1e3 / (2 * math.pi * 0.1), -3.01))
def _rl_highpass():
    s = Sheet()
    _ladder(s, [("s", "r", "1k"), ("p", "ind", "100m")])
    return s.done(["V(IN)", "V(OUT)"], ".ac dec 50 10 100k")


@example("rlc_bandpass", "filters",
         T("RLC band-pass", "RLC bant geçiren", "RLC-Bandpass", "Полосовой RLC фильтр"),
         T("Series L and C pass only frequencies near f0 = 1/(2π√LC) ≈ 1.6 kHz; the bandwidth is R/(2πL) ≈ 160 Hz.",
           "Seri L ve C yalnız f0 = 1/(2π√LC) ≈ 1.6 kHz civarını geçirir; bant genişliği R/(2πL) ≈ 160 Hz.",
           "Reihen-L und -C lassen nur Frequenzen um f0 = 1/(2π√LC) ≈ 1,6 kHz durch; Bandbreite R/(2πL) ≈ 160 Hz.",
           "Последовательные L и C пропускают только частоты около f0 = 1/(2π√LC) ≈ 1,6 кГц; полоса R/(2πL) ≈ 160 Гц."),
         check=lambda c: _expect_db(c, "V(OUT)", 1 / (2 * math.pi * math.sqrt(10e-3 * 1e-6)), 0, tol=0.2))
def _rlc_bandpass():
    s = Sheet()
    _ladder(s, [("s", "ind", "10m"), ("s", "cap", "1u"), ("p", "r", "10")])
    return s.done(["V(OUT)"], ".ac dec 100 100 10k")


@example("rlc_notch", "filters",
         T("LC notch (band-stop)", "LC çentik (bant durduran)", "LC-Bandsperre", "Режекторный LC фильтр"),
         T("A series LC to ground shorts out f0 ≈ 1.6 kHz: that frequency almost disappears at the output (hum filters use this).",
           "Toprağa giden seri LC, f0 ≈ 1.6 kHz'i kısa devre eder: bu frekans çıkışta neredeyse yok olur (uğultu süzgeçleri böyledir).",
           "Ein Reihen-LC gegen Masse schließt f0 ≈ 1,6 kHz kurz: diese Frequenz verschwindet am Ausgang fast (Brummfilter).",
           "Последовательный LC на землю закорачивает f0 ≈ 1,6 кГц: на выходе эта частота почти исчезает (фильтр фона)."),
         check=lambda c: _gain_db(c, "V(OUT)", 1 / (2 * math.pi * math.sqrt(10e-3 * 1e-6))) < -30 or _expect_db(c, "V(OUT)", 1, -99))
def _rlc_notch():
    s = Sheet()
    s.v(1, 1, "AC 1")
    s.lab(1, 1, "IN", side="l")
    s.r(1, 1, "1k")
    s.ind(4, 1, "10m", d="v")
    s.cap(4, 3, "1u")
    s.w((1, 3), (1, 5), (4, 5))
    s.gnd(1, 5)
    s.lab(4, 1, "OUT")
    return s.done(["V(OUT)"], ".ac dec 100 100 10k")


@example("rc_lowpass_2", "filters",
         T("Two-stage RC low-pass", "İki katlı RC alçak geçiren", "Zweistufiger RC-Tiefpass", "Двухзвенный RC фильтр"),
         T("Two RC stages fall by 40 dB per decade. The second stage loads the first, so the corner is softer than a true 2nd-order filter.",
           "İki RC katı dekad başına 40 dB düşer. İkinci kat birinciyi yükler; köşe gerçek 2. dereceden filtreden daha yumuşaktır.",
           "Zwei RC-Glieder fallen mit 40 dB/Dekade. Die zweite Stufe belastet die erste, der Knick ist weicher als bei echter 2. Ordnung.",
           "Два RC-звена дают спад 40 дБ/дек. Второе звено нагружает первое, поэтому излом мягче, чем у настоящего фильтра 2-го порядка."),
         check=lambda c: (_gain_db(c, "V(OUT)", 10e3) - _gain_db(c, "V(OUT)", 100e3) > 38) or _expect_db(c, "V(OUT)", 1, -99))
def _rc_lowpass_2():
    s = Sheet()
    _ladder(s, [("s", "r", "1k"), ("p", "cap", "159n"), ("s", "r", "1k"), ("p", "cap", "159n")])
    s.lab(4, 1, "MID", side="u")
    return s.done(["V(MID)", "V(OUT)"], ".ac dec 50 10 100k")


@example("lc_butterworth", "filters",
         T("3rd-order LC Butterworth low-pass", "3. derece LC Butterworth alçak geçiren", "LC-Butterworth-Tiefpass 3. Ordnung",
           "LC фильтр Баттерворта 3-го порядка"),
         T("Between 50 Ω terminations the passband is flat up to 1 kHz, then falls by 60 dB per decade (−6 dB at 1 kHz from the source divider).",
           "50 Ω sonlandırmalar arasında geçiş bandı 1 kHz'e kadar düzdür, sonra dekad başına 60 dB düşer (1 kHz'de kaynak bölücüsüyle −6 dB'nin 3 dB altı).",
           "Zwischen 50-Ω-Abschlüssen ist der Durchlass bis 1 kHz flach und fällt dann mit 60 dB/Dekade.",
           "Между нагрузками 50 Ом полоса пропускания ровная до 1 кГц, затем спад 60 дБ/дек."),
         check=lambda c: (_expect_db(c, "V(OUT)", 100, -6.02, tol=0.1), _expect_db(c, "V(OUT)", 1e3, -9.03, tol=0.4)))
def _lc_butterworth():
    s = Sheet()
    _ladder(s, [("s", "r", "50"), ("p", "cap", "3.183u"), ("s", "ind", "15.92m"), ("p", "cap", "3.183u"),
                ("p", "r", "50")])
    return s.done(["V(OUT)"], ".ac dec 50 10 100k")


@example("twin_t_notch", "filters",
         T("Twin-T notch", "Çift-T çentik", "Doppel-T-Sperre", "Двойной Т-образный режекторный"),
         T("Two T networks (R-2C-R and C-R/2-C) cancel each other at f0 = 1/(2πRC) ≈ 1 kHz — a deep notch without coils.",
           "İki T ağı (R-2C-R ve C-R/2-C) f0 = 1/(2πRC) ≈ 1 kHz'de birbirini götürür: bobinsiz derin bir çentik.",
           "Zwei T-Glieder (R-2C-R und C-R/2-C) heben sich bei f0 = 1/(2πRC) ≈ 1 kHz auf: tiefe Kerbe ohne Spulen.",
           "Два Т-звена (R-2C-R и C-R/2-C) взаимно гасятся на f0 = 1/(2πRC) ≈ 1 кГц: глубокий провал без катушек."),
         check=lambda c: _gain_db(c, "V(OUT)", 1 / (2 * math.pi * 10e3 * 15.9e-9)) < -25 or _expect_db(c, "V(OUT)", 1, -99))
def _twin_t():
    s = Sheet()
    s.v(1, 3, "AC 1")
    s.lab(1, 3, "IN", side="l")
    s.gnd(1, 5)
    s.lab(4, 3, "IN", side="l")
    s.w((4, 1), (4, 6))
    # üst T: R – 2C – R
    s.r(4, 1, "10k")
    s.r(7, 1, "10k")
    s.cap(7, 1, "31.8n")
    s.gnd(7, 3)
    # alt T: C – R/2 – C
    s.cap(4, 6, "15.9n", d="h")
    s.cap(7, 6, "15.9n", d="h")
    s.r(7, 6, "5k", d="v")
    s.gnd(7, 8)
    s.w((10, 1), (10, 6))
    s.r(10, 1, "100k", ref="RL")
    s.w((13, 1), (13, 3))
    s.gnd(13, 3)
    s.lab(10, 3, "OUT", side="l")
    return s.done(["V(OUT)"], ".ac dec 100 100 10k")


@example("crossover", "filters",
         T("Loudspeaker crossover", "Hoparlör ayırıcı (crossover)", "Lautsprecherweiche", "Разделительный фильтр"),
         T("A 2nd-order low-pass feeds the woofer (8 Ω) and a high-pass feeds the tweeter (8 Ω); both are −3 dB near 2.5 kHz.",
           "2. derece alçak geçiren bas hoparlörü (8 Ω), yüksek geçiren tiz hoparlörü (8 Ω) besler; ikisi de 2.5 kHz civarında −3 dB.",
           "Ein Tiefpass 2. Ordnung speist den Tieftöner (8 Ω), ein Hochpass den Hochtöner (8 Ω); beide −3 dB bei etwa 2,5 kHz.",
           "ФНЧ 2-го порядка питает низкочастотный динамик (8 Ом), ФВЧ — высокочастотный (8 Ом); оба −3 дБ около 2,5 кГц."),
         check=lambda c: abs(_gain_db(c, "V(WOOFER)", 2.5e3) - _gain_db(c, "V(TWEETER)", 2.5e3)) < 1.5 or _expect_db(c, "V(WOOFER)", 1, -99))
def _crossover():
    s = Sheet()
    s.v(1, 1, "AC 1")
    s.gnd(1, 3)
    s.lab(1, 1, "IN", side="u")
    s.w((1, 1), (1, 0), (4, 0))
    s.ind(4, 0, "720u")
    s.cap(7, 0, "5.6u", d="v")
    s.gnd(7, 2)
    s.w((7, 0), (10, 0))
    s.r(10, 0, "8", d="v", ref="RW")
    s.gnd(10, 2)
    s.lab(10, 0, "WOOFER")
    s.lab(4, 5, "IN", side="l")
    s.cap(4, 5, "5.6u", d="h")
    s.ind(7, 5, "720u", d="v")
    s.gnd(7, 7)
    s.w((7, 5), (10, 5))
    s.r(10, 5, "8", d="v", ref="RT")
    s.gnd(10, 7)
    s.lab(10, 5, "TWEETER")
    return s.done(["V(WOOFER)", "V(TWEETER)"], ".ac dec 50 100 100k")
