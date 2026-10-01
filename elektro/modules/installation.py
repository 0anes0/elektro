"""Alçak gerilim tesisatı: kablo kesiti, koruma (MCB/sigorta), kısa devre akımı.

Akım taşıma kapasiteleri IEC 60364-5-52 tablolarından (PVC, bakır, 30 °C hava / 20 °C toprak)
alınmıştır; XLPE ve alüminyum için yaklaşık çarpanlar kullanılır.
"""

from __future__ import annotations

import math
from typing import Optional

import typer
from rich.table import Table

from elektro.i18n import pct, t
from elektro.modules.wiring import parse_length
from elektro.ui import cli_parser, console, eng, fail, json_mode, result_panel, theory, warn
from elektro.units import format_si

SECTIONS = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]

# IEC 60364-5-52 Tablo B.52.2 (2 yüklü iletken) ve B.52.4 (3 yüklü iletken), PVC/bakır, A
AMPACITY = {
    ("A1", 2): [14.5, 19.5, 26, 34, 46, 61, 80, 99, 119, 151, 182, 210, 240, 273, 321, 367],
    ("A1", 3): [13.5, 18, 24, 31, 42, 56, 73, 89, 108, 136, 164, 188, 216, 245, 286, 328],
    ("B1", 2): [17.5, 24, 32, 41, 57, 76, 101, 125, 151, 192, 232, 269, 300, 341, 400, 458],
    ("B1", 3): [15.5, 21, 28, 36, 50, 68, 89, 110, 134, 171, 207, 239, 262, 296, 346, 394],
    ("C", 2): [19.5, 27, 36, 46, 63, 85, 112, 138, 168, 213, 258, 299, 344, 392, 461, 530],
    ("C", 3): [17.5, 24, 32, 41, 57, 76, 96, 119, 144, 184, 223, 259, 299, 341, 403, 464],
    ("D", 2): [22, 29, 38, 47, 63, 81, 104, 125, 148, 183, 216, 246, 278, 312, 361, 408],
    ("D", 3): [18, 24, 31, 39, 52, 67, 86, 103, 122, 151, 179, 203, 230, 258, 297, 336],
}
METHODS = ("A1", "B1", "C", "D")

# Bir arada döşenmiş devre sayısına göre azaltma katsayısı (IEC 60364-5-52 B.52.17)
GROUPING = {1: 1.0, 2: 0.80, 3: 0.70, 4: 0.65, 5: 0.60, 6: 0.57, 7: 0.54, 8: 0.52, 9: 0.50,
            12: 0.45, 16: 0.41, 20: 0.38}

MATERIALS = {
    # özdirenç 20 °C (Ω·mm²/m), sıcaklık katsayısı, akım kapasitesi çarpanı (bakıra göre)
    "cu": (0.017241, 0.00393, 1.0),
    "al": (0.028264, 0.00403, 0.78),
}
INSULATION = {
    # en yüksek iletken sıcaklığı (°C), kapasite çarpanı (havada, toprakta), kısa devre k (Cu, Al)
    "pvc": (70, 1.0, 1.0, 115, 76),
    "xlpe": (90, 1.24, 1.15, 143, 94),
}
X_PER_M = 0.08e-3          # Ω/m, AG kablolar için tipik reaktans

MCB_RATINGS = [6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125]
FUSE_RATINGS = [2, 4, 6, 10, 16, 20, 25, 32, 35, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400,
                500, 630, 800, 1000, 1250]
CURVES = {"B": (3, 5), "C": (5, 10), "D": (10, 20)}
BREAKING_KA = [6, 10, 15, 25, 36, 50, 70, 100, 150]


def _choice(value: str, options, key: str) -> str:
    v = value.strip()
    match = [o for o in options if o.lower() == v.lower()]
    if not match:
        fail(t(key, value=value, options=", ".join(options)))
    return match[0]


def _check(ok: bool) -> str:
    return "[green]✓[/]" if ok else "[red]✗[/]"


def grouping_factor(circuits: int) -> float:
    if circuits < 1:
        raise ValueError(t("common.positive"))
    for n in sorted(GROUPING):
        if n >= circuits:
            return GROUPING[n]
    return GROUPING[20]


def temperature_factor(ta: float, insulation: str, ground: bool) -> float:
    tmax = INSULATION[insulation][0]
    ref = 20 if ground else 30
    if ta >= tmax:
        raise ValueError(t("cable.too_hot", tmax=tmax))
    return math.sqrt((tmax - ta) / (tmax - ref))


def ampacity(section: float, method: str, phases: int, material: str = "cu", insulation: str = "pvc",
             ta: Optional[float] = None, circuits: int = 1) -> float:
    """Düzeltilmiş akım taşıma kapasitesi Iz (A)."""
    ground = method == "D"
    base = AMPACITY[(method, 3 if phases == 3 else 2)][SECTIONS.index(section)]
    ins = INSULATION[insulation]
    k_ins = ins[2] if ground else ins[1]
    ta = (20 if ground else 30) if ta is None else ta
    return base * MATERIALS[material][2] * k_ins * temperature_factor(ta, insulation, ground) \
        * grouping_factor(circuits)


def resistance_per_m(section: float, material: str, temp: float) -> float:
    rho, alpha, _ = MATERIALS[material]
    return rho * (1 + alpha * (temp - 20)) / section


def voltage_drop(section: float, current: float, length: float, phases: int, pf: float,
                 material: str, temp: float) -> float:
    """Gerilim düşümü (V). 1 faz: gidiş-dönüş; 3 faz: hat gerilimine göre."""
    r = resistance_per_m(section, material, temp)
    sin = math.sqrt(max(0.0, 1 - pf * pf))
    k = math.sqrt(3) if phases == 3 else 2
    return k * length * current * (r * pf + X_PER_M * sin)


def conductor_temp(current: float, iz: float, ta: float, insulation: str) -> float:
    """Yüke göre tahmini iletken sıcaklığı: Ta + (Tmax − Ta)·(Ib/Iz)²."""
    tmax = INSULATION[insulation][0]
    return ta + (tmax - ta) * min(1.0, (current / iz) ** 2)


def design_current(v: float, phases: int, pf: float, current: Optional[float], power: Optional[float]) -> float:
    if current is not None:
        return current
    if power is None:
        raise ValueError(t("cable.need"))
    return power / ((math.sqrt(3) if phases == 3 else 1) * v * pf)


def select_cable(current: float, length: Optional[float], v: float, phases: int, pf: float,
                 drop_pct: float, method: str, material: str, insulation: str, ta: Optional[float],
                 circuits: int) -> list:
    """Her kesit için kapasite ve gerilim düşümü; seçilen satırda 'ok' True."""
    ground = method == "D"
    ta_eff = (20 if ground else 30) if ta is None else ta
    rows = []
    for s in SECTIONS:
        if material == "al" and s < 16:
            continue
        iz = ampacity(s, method, phases, material, insulation, ta, circuits)
        row = {"mm2": s, "iz_a": iz, "ampacity_ok": iz >= current}
        if length is not None:
            temp = conductor_temp(current, iz, ta_eff, insulation)
            du = voltage_drop(s, current, length, phases, pf, material, temp)
            r = resistance_per_m(s, material, temp)
            row.update(drop_v=du, drop_pct=du / v * 100, drop_ok=du / v * 100 <= drop_pct,
                       loss_w=(3 if phases == 3 else 2) * current ** 2 * r * length, temp_c=temp)
        else:
            row["drop_ok"] = True
        row["ok"] = row["ampacity_ok"] and row["drop_ok"]
        rows.append(row)
    return rows


def next_rating(value: float, ratings) -> Optional[float]:
    return next((r for r in ratings if r >= value - 1e-9), None)


def cable(
    current: Optional[float] = typer.Option(None, "--current", "-i", **eng(t("cable.opt.current"))),
    power: Optional[float] = typer.Option(None, "--power", "-p", **eng(t("cable.opt.power"))),
    v: Optional[float] = typer.Option(None, "--v", **eng(t("cable.opt.v"))),
    phases: int = typer.Option(1, "--phases", help=t("ac.opt.phases")),
    pf: float = typer.Option(1.0, "--pf", help=t("ac.opt.pf")),
    length: Optional[float] = typer.Option(None, "--length", "-l", parser=cli_parser(parse_length),
                                           metavar=t("wire.metavar.length"), help=t("cable.opt.length")),
    drop: float = typer.Option(3.0, "--drop", help=t("cable.opt.drop")),
    method: str = typer.Option("B1", "--method", help=t("cable.opt.method")),
    material: str = typer.Option("cu", "--material", help=t("cable.opt.material")),
    insulation: str = typer.Option("pvc", "--insulation", help=t("cable.opt.insulation")),
    ta: Optional[float] = typer.Option(None, "--ta", help=t("cable.opt.ta")),
    group: int = typer.Option(1, "--group", help=t("cable.opt.group")),
    mm2: Optional[float] = typer.Option(None, "--mm2", help=t("cable.opt.mm2")),
):
    if phases not in (1, 3):
        fail(t("ac.bad_phases"))
    if not 0 < pf <= 1:
        fail(t("ac.bad_pf"))
    method = _choice(method, METHODS, "cable.bad_choice")
    material = _choice(material, MATERIALS, "cable.bad_choice")
    insulation = _choice(insulation, INSULATION, "cable.bad_choice")
    v = v or (400.0 if phases == 3 else 230.0)
    try:
        ib = design_current(v, phases, pf, current, power)
        if ib <= 0 or drop <= 0 or (length is not None and length <= 0):
            raise ValueError(t("common.positive_all"))
        rows = select_cable(ib, length, v, phases, pf, drop, method, material, insulation, ta, group)
    except ValueError as e:
        fail(str(e))
    if mm2 is not None:
        chosen = next((r for r in rows if abs(r["mm2"] - mm2) < 1e-9), None)
        if chosen is None:
            fail(t("cable.bad_section", options=", ".join(f"{s:g}" for s in SECTIONS)))
    else:
        chosen = next((r for r in rows if r["ok"]), None)
        if chosen is None:
            fail(t("cable.none"))

    by_amp = next((r for r in rows if r["ampacity_ok"]), None)
    mcb = next((r for r in MCB_RATINGS if ib <= r <= chosen["iz_a"]), None)
    res = {
        t("cable.system"): f"{t('ac.three') if phases == 3 else t('ac.single')}, {format_si(v, 'V')}",
        t("cable.ib"): format_si(ib, "A"),
        t("cable.section"): f"{chosen['mm2']:g} mm² {material.capitalize()} ({insulation.upper()}, {method})",
        t("cable.iz"): f"{chosen['iz_a']:.1f} A  {_check(chosen['ampacity_ok'])}",
    }
    if "drop_v" in chosen:
        drop_txt = pct(f"{chosen['drop_pct']:.2f}")
        res[t("cable.drop")] = f"{format_si(chosen['drop_v'], 'V')} ({drop_txt})  {_check(chosen['drop_ok'])}"
        res[t("cable.loss")] = format_si(chosen["loss_w"], "W")
        res[t("cable.temp")] = f"≈ {chosen['temp_c']:.0f} °C"
    if mm2 is None and by_amp is not None and by_amp is not chosen:
        res[t("cable.by_ampacity")] = f"{by_amp['mm2']:g} mm²"
    res[t("cable.mcb")] = f"{mcb} A" if mcb else t("cable.no_mcb")
    data = {"current_a": ib, "v": v, "phases": phases, "pf": pf, "method": method, "material": material,
            "insulation": insulation, "length_m": length, "allowed_drop_pct": drop, "selected": chosen,
            "mcb_a": mcb, "candidates": rows}
    result_panel(t("cable.title"), res, data=data)

    if not json_mode():
        i = rows.index(chosen)
        tbl = Table(box=None, header_style="bold")
        tbl.add_column("mm²", justify="right")
        tbl.add_column("Iz", justify="right")
        if length is not None:
            tbl.add_column("ΔU", justify="right")
        tbl.add_column("")
        for r in rows[max(0, i - 3): i + 2]:
            style = "bold green" if r is chosen else "" if r["ok"] else "dim"
            cells = [f"{r['mm2']:g}", f"{r['iz_a']:.1f} A"]
            if length is not None:
                cells.append(pct(f"{r['drop_pct']:.2f}"))
            cells.append(_check(r["ok"]))
            tbl.add_row(*cells, style=style)
        console.print(tbl)
    if mm2 is not None and not chosen["ok"]:
        warn(t("cable.not_ok"))
    theory(t("cable.note1"), t("cable.note2"))


# --- Koruma: MCB / sigorta ---------------------------------------------------------------------

def fuse_i2_factor(rating: float) -> float:
    """gG sigortanın anma çalışma akımı katsayısı (IEC 60269-2)."""
    if rating <= 4:
        return 2.1
    if rating < 16:
        return 1.9
    return 1.6


def breaker_calc(ib: float, iz: Optional[float], kind: str, curve: str) -> dict:
    ratings = MCB_RATINGS if kind == "mcb" else FUSE_RATINGS
    rating = next_rating(ib, ratings)
    if rating is None:
        raise ValueError(t("brk.too_big"))
    i2 = rating * (1.45 if kind == "mcb" else fuse_i2_factor(rating))
    out = {"in_a": rating, "i2_a": i2}
    if kind == "mcb":
        lo, hi = CURVES[curve]
        out.update(trip_min_a=lo * rating, trip_max_a=hi * rating, ia_a=hi * rating)
    if iz is not None:
        out.update(iz_a=iz, in_ok=rating <= iz, i2_ok=i2 <= 1.45 * iz)
        # Iz'yi aşmayan en büyük anma akımı
        out["max_in_a"] = max((r for r in ratings
                               if r <= iz and r * (1.45 if kind == "mcb" else fuse_i2_factor(r)) <= 1.45 * iz),
                              default=None)
    return out


def breaker(
    current: float = typer.Option(..., "--current", "-i", **eng(t("brk.opt.current"))),
    iz: Optional[float] = typer.Option(None, "--iz", **eng(t("brk.opt.iz"))),
    kind: str = typer.Option("mcb", "--type", help=t("brk.opt.type")),
    curve: str = typer.Option("C", "--curve", help=t("brk.opt.curve")),
    zs: Optional[float] = typer.Option(None, "--zs", **eng(t("brk.opt.zs"))),
    mm2: Optional[float] = typer.Option(None, "--mm2", help=t("brk.opt.mm2")),
    length: Optional[float] = typer.Option(None, "--length", "-l", parser=cli_parser(parse_length),
                                           metavar=t("wire.metavar.length"), help=t("brk.opt.length")),
    material: str = typer.Option("cu", "--material", help=t("cable.opt.material")),
    ze: float = typer.Option(0.35, "--ze", help=t("brk.opt.ze")),
    u0: float = typer.Option(230, "--u0", help=t("brk.opt.u0")),
):
    kind = _choice(kind, ("mcb", "fuse"), "cable.bad_choice")
    curve = _choice(curve, CURVES, "cable.bad_choice")
    material = _choice(material, MATERIALS, "cable.bad_choice")
    if current <= 0 or (iz is not None and iz <= 0) or u0 <= 0:
        fail(t("common.positive_all"))
    try:
        r = breaker_calc(current, iz, kind, curve)
    except ValueError as e:
        fail(str(e))

    rows = {
        t("brk.device"): (f"MCB {curve}{r['in_a']:g}" if kind == "mcb" else f"gG {r['in_a']:g} A"),
        "Ib ≤ In": f"{format_si(current, 'A')} ≤ {r['in_a']:g} A",
        "I2": format_si(r["i2_a"], "A"),
    }
    if iz is not None:
        rows["In ≤ Iz"] = f"{r['in_a']:g} ≤ {iz:g} A  {_check(r['in_ok'])}"
        rows["I2 ≤ 1.45·Iz"] = f"{r['i2_a']:.1f} ≤ {1.45 * iz:.1f} A  {_check(r['i2_ok'])}"
    if kind == "mcb":
        rows[t("brk.magnetic")] = f"{r['trip_min_a']:g} … {r['trip_max_a']:g} A"
        zs_max = u0 / r["ia_a"]
        rows[t("brk.zs_max")] = format_si(zs_max, "Ω")
        r["zs_max_ohm"] = zs_max
        if zs is None and mm2 is not None and length is not None:
            if mm2 <= 0 or length <= 0:
                fail(t("common.positive_all"))
            # faz + koruma iletkeni (aynı kesit), arıza anında ~70 °C
            zs = ze + 2 * length * resistance_per_m(mm2, material, 70)
            rows[t("brk.zs_calc")] = format_si(zs, "Ω")
        if zs is not None:
            ok = zs <= zs_max
            rows["Zs ≤ Zs,max"] = f"{format_si(zs, 'Ω')}  {_check(ok)}"
            rows[t("brk.ik_min")] = format_si(u0 / zs, "A")
            r.update(zs_ohm=zs, zs_ok=ok, fault_current_a=u0 / zs)
        if mm2 is not None and mm2 > 0 and zs_max > ze:
            lmax = (zs_max - ze) / (2 * resistance_per_m(mm2, material, 70))
            rows[t("brk.lmax", mm2=f"{mm2:g}")] = f"{lmax:.0f} m"
            r["max_length_m"] = lmax
    if iz is not None and r.get("max_in_a") and not (r["in_ok"] and r["i2_ok"]):
        warn(t("brk.not_ok", max=f"{r['max_in_a']:g}"))
    elif iz is not None and not r.get("max_in_a"):
        warn(t("brk.no_device"))
    r.update(type=kind, curve=curve if kind == "mcb" else None, ib_a=current)
    result_panel(t("brk.title"), rows, data=r)
    if kind == "mcb":
        theory(t("brk.note.curve"), t("brk.note.zs", ze=f"{ze:g}"))
    else:
        theory(t("brk.note.fuse"))


# --- Kısa devre akımı ----------------------------------------------------------------------

def transformer_impedance(kva: float, uk: float, v: float, ur: float) -> complex:
    zt = uk / 100 * v * v / (kva * 1e3)
    rt = ur / 100 * v * v / (kva * 1e3)
    return complex(rt, math.sqrt(max(zt * zt - rt * rt, 0)))


def network_impedance(sk_mva: float, v: float, c: float = 1.1) -> complex:
    """Üst şebeke (IEC 60909): Xq = 0.995·Zq, Rq = 0.1·Xq."""
    zq = c * v * v / (sk_mva * 1e6)
    xq = 0.995 * zq
    return complex(0.1 * xq, xq)


def short_circuit(kva: float, uk: float, v: float, ur: float, sk_mva: Optional[float],
                  mm2: Optional[float], length: Optional[float], material: str, parallel: int) -> dict:
    zt = transformer_impedance(kva, uk, v, ur)
    zq = network_impedance(sk_mva, v) if sk_mva else 0j
    zc = 0j
    if mm2 and length:
        r20 = resistance_per_m(mm2, material, 20) * length / parallel
        zc = complex(r20, X_PER_M * length / parallel)
    z = zt + zq + zc
    ik3 = 1.05 * v / (math.sqrt(3) * abs(z))
    kappa = 1.02 + 0.98 * math.exp(-3 * z.real / z.imag) if z.imag > 0 else 1.0
    # Faz-nötr: çevrim empedansı (nötr kesiti faz kesitine eşit), iletken ~80 °C, cmin = 0.95
    loop = zt + zq + 2 * complex(zc.real * 1.24, zc.imag)
    ik1 = 0.95 * v / math.sqrt(3) / abs(loop)
    return {"zt": zt, "zq": zq, "zc": zc, "z": z, "ik3_a": ik3, "ip_a": kappa * math.sqrt(2) * ik3,
            "kappa": kappa, "ik1_a": ik1, "in_a": kva * 1e3 / (math.sqrt(3) * v)}


def _z(z: complex) -> str:
    return f"{format_si(abs(z), 'Ω')}  ({format_si(z.real, 'Ω', 3)} + j{format_si(z.imag, 'Ω', 3)})"


def shortcircuit(
    kva: float = typer.Option(..., "--kva", help=t("sc.opt.kva")),
    uk: Optional[float] = typer.Option(None, "--uk", help=t("sc.opt.uk")),
    v: float = typer.Option(400, "--v", **eng(t("sc.opt.v"))),
    pk: Optional[float] = typer.Option(None, "--pk", **eng(t("sc.opt.pk"))),
    sk: Optional[float] = typer.Option(500, "--sk", help=t("sc.opt.sk")),
    mm2: Optional[float] = typer.Option(None, "--mm2", help=t("sc.opt.mm2")),
    length: Optional[float] = typer.Option(None, "--length", "-l", parser=cli_parser(parse_length),
                                           metavar=t("wire.metavar.length"), help=t("sc.opt.length")),
    material: str = typer.Option("cu", "--material", help=t("cable.opt.material")),
    parallel: int = typer.Option(1, "--parallel", help=t("sc.opt.parallel")),
    time: Optional[float] = typer.Option(None, "--time", "-t", **eng(t("sc.opt.time"))),
    insulation: str = typer.Option("pvc", "--insulation", help=t("cable.opt.insulation")),
):
    material = _choice(material, MATERIALS, "cable.bad_choice")
    insulation = _choice(insulation, INSULATION, "cable.bad_choice")
    uk = uk if uk is not None else (4.0 if kva <= 630 else 6.0)
    if kva <= 0 or uk <= 0 or v <= 0 or parallel < 1 or (sk is not None and sk <= 0):
        fail(t("common.positive_all"))
    if (mm2 is None) != (length is None):
        fail(t("sc.need_cable"))
    if mm2 is not None and (mm2 <= 0 or length <= 0):
        fail(t("common.positive_all"))
    ur = pk / (kva * 1e3) * 100 if pk is not None else 1.0
    if ur >= uk:
        fail(t("sc.bad_pk"))
    r = short_circuit(kva, uk, v, ur, sk, mm2, length, material, parallel)
    rows = {
        t("sc.trafo"): f"{kva:g} kVA, uk = {pct(f'{uk:g}')}, {format_si(v, 'V')}",
        t("sc.in"): format_si(r["in_a"], "A"),
        "Zt": _z(r["zt"]),
    }
    if sk:
        rows[t("sc.zq", sk=f"{sk:g}")] = _z(r["zq"])
    if mm2:
        rows[t("sc.zc", cable=f"{parallel}×{mm2:g} mm², {length:g} m")] = _z(r["zc"])
    rows["Σ Z"] = _z(r["z"])
    rows["Ik3 (max)"] = format_si(r["ik3_a"], "A")
    rows[f"ip (κ = {r['kappa']:.2f})"] = format_si(r["ip_a"], "A")
    rows["Ik1 (min)"] = format_si(r["ik1_a"], "A")
    icu = next((x for x in BREAKING_KA if x * 1e3 >= r["ik3_a"]), None)
    rows[t("sc.icu")] = f"≥ {icu} kA" if icu else f"> {BREAKING_KA[-1]} kA"
    data = {"kva": kva, "uk_pct": uk, "ur_pct": ur, "v": v, "sk_mva": sk, "in_a": r["in_a"],
            "z_ohm": abs(r["z"]), "r_ohm": r["z"].real, "x_ohm": r["z"].imag, "ik3_a": r["ik3_a"],
            "ip_a": r["ip_a"], "kappa": r["kappa"], "ik1_a": r["ik1_a"], "breaking_capacity_ka": icu}
    if time is not None:
        if time <= 0:
            fail(t("common.positive"))
        k = INSULATION[insulation][3 if material == "cu" else 4]
        s_min = r["ik3_a"] * math.sqrt(time) / k
        rows[t("sc.smin", t=format_si(time, "s"), k=k)] = f"{s_min:.1f} mm²" + (
            f"  {_check(mm2 * parallel >= s_min)}" if mm2 else "")
        data.update(time_s=time, k=k, min_section_mm2=s_min)
    result_panel(t("sc.title"), rows, data=data)
    theory(t("sc.note1"), t("sc.note2"))
