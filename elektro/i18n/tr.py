"""Türkçe."""

MESSAGES = {
    # --- genel -------------------------------------------------------------------
    "fmt.pct": "%{v}",
    "ui.error": "Hata",
    "ui.warning": "Uyarı",
    "ui.metavar.value": "DEĞER",
    "ui.metavar.values": "DEĞERLER...",
    "common.positive": "değer pozitif olmalı",
    "common.positive_all": "değerler pozitif olmalı",
    "units.empty": "boş değer",
    "units.invalid": "'{text}' anlaşılamadı (örnek: 1k, 4k7, 100n, 2.2u, 1e-3)",
    "units.unknown_series": "bilinmeyen seri '{name}' (seçenekler: {options})",

    # --- Typer / Click -------------------------------------------------------------
    "typer.options": "Seçenekler",
    "typer.arguments": "Argümanlar",
    "typer.commands": "Komutlar",
    "typer.error": "Hata",
    "typer.aborted": "İptal edildi.",
    "typer.required": "[zorunlu]",
    "typer.default": "[varsayılan: {}]",
    "typer.try_help": "Yardım için [blue]'{command_path} {help_option}'[/] yazın.",
    "typer.help_option": "Bu mesajı göster ve çık.",

    # --- ana CLI ---------------------------------------------------------------------
    "cli.help": "Terminal tabanlı Elektrik-Elektronik Mühendisliği aracı.",
    "cli.help_long": (
        "⚡ Elektrik-Elektronik Mühendisliği hesaplamaları için terminal aracı.\n\n"
        "Değerler mühendislik gösterimiyle yazılabilir: 4k7, 100n, 2.2u, 10M, 1meg"
    ),
    "cli.opt.version": "Sürümü göster",
    "cli.opt.lang": "Bu çalıştırma için arayüz dili (en, tr, de, ru)",
    "panel.basic": "Temel",
    "panel.passive": "Pasif elemanlar",
    "panel.signal": "Sinyal & RF",
    "panel.tools": "Araçlar",
    "menu.ohm": "Ohm kanunu ve güç",
    "menu.resistor": "Renk kodu, SMD kodu",
    "menu.555": "NE555 zamanlayıcı",
    "menu.logic": "Tabanlar, kapılar, ifadeler",
    "menu.combine": "Seri/paralel eşdeğer",
    "menu.divider": "Gerilim bölücü",
    "menu.led": "LED ön direnci",
    "menu.eseries": "Standart değerler",
    "menu.cap": "Kondansatör kodu",
    "menu.filter": "RC/RL/LC/RLC filtreler",
    "menu.rf": "FSPL, link bütçesi, anten",
    "menu.datasheet": "Datasheet bul ve indir",
    "menu.helpall": "Tüm komutların kılavuzu",
    "menu.language": "Dili değiştir",
    "menu.update": "Son sürüme güncelle",
    "menu.subtitle": "elektro KOMUT --help",

    # --- dil ------------------------------------------------------------------------------
    "lang.help": (
        "Arayüz dilini göster veya değiştir.\n\n"
        "Örnekler:\n"
        "  elektro language          (dilleri listele)\n"
        "  elektro language de       (Almancayı varsayılan yap)\n"
        "  elektro --lang ru ohm -v 5 -r 1k   (tek seferlik)"
    ),
    "lang.arg": "Kaydedilecek dil kodu",
    "lang.usage": "Değiştir: elektro language KOD   ·   tek seferlik: elektro --lang KOD ...",
    "lang.unknown": "bilinmeyen dil '{code}' (seçenekler: {options})",
    "lang.saved": "Dil {name} olarak ayarlandı.",
    "lang.save_failed": "{path} yazılamadı: {error}",
    "lang.env_override": "Not: ELEKTRO_LANG ortam değişkeni tanımlı ve öncelikli.",

    # --- kılavuz / güncelleme ------------------------------------------------------------
    "manual.help": "Tüm komutların ayrıntılı kılavuzu (sayfalayıcıda).",
    "manual.title": "Kullanım Kılavuzu",
    "manual.values": "Değerler mühendislik gösterimiyle yazılabilir:",
    "upd.help": "Elektro'yu GitHub'daki son sürüme günceller.",
    "upd.opt.force": "Sürüm aynı olsa da yeniden kur",
    "upd.fetch_failed": "GitHub'dan sürüm bilgisi alınamadı. İnternet bağlantını kontrol et.",
    "upd.installed": "Kurulu",
    "upd.up_to_date": "Zaten güncel.",
    "upd.pipx": "pipx ile kurulmuş. Yeni kurulum betiğine geçmek için:",
    "upd.dev": "Geliştirme kurulumu görünüyor; repo klasöründe [cyan]git pull[/] yeterli.",
    "upd.updating": "Güncelleniyor…",
    "upd.failed": "güncelleme başarısız",
    "upd.done": "elektro {version} kuruldu.",

    # --- ohm -------------------------------------------------------------------------------
    "ohm.help": (
        "Ohm kanunu: V, I, R, P'den herhangi ikisini ver, diğerlerini hesaplasın.\n\n"
        "V = I·R    P = V·I = I²·R = V²/R\n\n"
        "Parametresiz çalıştırılırsa soru sorarak ilerler.\n\n"
        "Örnekler:\n"
        "  elektro ohm -v 12 -r 1k\n"
        "  elektro ohm -i 20m -p 0.5\n"
        "  elektro ohm"
    ),
    "ohm.opt.v": "Gerilim (V)",
    "ohm.opt.i": "Akım (A), örn: 20m",
    "ohm.opt.r": "Direnç (Ω), örn: 4k7",
    "ohm.opt.p": "Güç (W)",
    "ohm.need_two": "en az 2 değer gerekli",
    "ohm.negative": "direnç ve güç negatif olamaz",
    "ohm.div_zero": "sıfıra bölme — girilen değerlerle devre tanımsız",
    "ohm.conflict": "Verilen değerler birbiriyle tutarsız; ilk iki değer esas alındı.",
    "ohm.title": "Ohm Kanunu",
    "ohm.voltage": "Gerilim (V)",
    "ohm.current": "Akım (I)",
    "ohm.resistance": "Direnç (R)",
    "ohm.power": "Güç (P)",
    "ohm.wizard": "Ohm Kanunu Sihirbazı — bilmediğin değeri boş bırak (Enter)",
    "ohm.ask.v": "Gerilim V",
    "ohm.ask.i": "Akım I",
    "ohm.ask.r": "Direnç R",
    "ohm.ask.p": "Güç P",

    # --- direnç ----------------------------------------------------------------------------
    "res.help": "Direnç renk kodu, SMD kodu ve standart değerler.",
    "res.help_long": (
        "Direnç renk kodu çözücü.\n\n"
        "Bant sırası: rakamlar → çarpan → tolerans → (sıcaklık katsayısı).\n"
        "Renkler kısa kod (k s r a…), IEC kodu (bn bk rd gd…) ya da Türkçe,\n"
        "İngilizce, Almanca veya Rusça ad olarak yazılabilir.\n\n"
        "Örnekler:\n"
        "  elektro resistor k s r a          (1 kΩ ±%5)\n"
        "  elektro resistor sari mor siyah kahverengi kahverengi\n"
        "  elektro resistor encode 4k7\n"
        "  elektro resistor smd 103"
    ),
    "res.decode.help": "Renk bantlarından direnç değerini bulur.",
    "res.decode.arg": "Renk bantları (3-6 adet)",
    "res.encode.help": "Direnç değerinden renk kodunu üretir.",
    "res.encode.arg": "Direnç, örn: 4k7, 220, 1M",
    "res.encode.opt.bands": "Bant sayısı (4 veya 5)",
    "res.encode.opt.tol": "Tolerans % (varsayılan: 4 bantta 5, 5 bantta 1)",
    "res.encode.bad_bands": "bant sayısı 4 veya 5 olmalı",
    "res.encode.title": "Renk Kodu",
    "res.smd.help": "SMD direnç üzerindeki kodu çözer (3/4 hane ve EIA-96).",
    "res.smd.arg": "SMD kodu: 103, 4R7, 1002, 01C",
    "res.smd.title": "SMD Direnç",
    "res.table.help": "Renk kodu referans tablosu.",
    "res.table.title": "Direnç Renk Kodları",
    "res.table.footer": "Tolerans bandı yoksa ±%20. Örnek: elektro resistor k s r a",
    "res.col.code": "Kod",
    "res.col.color": "Renk",
    "res.col.digit": "Rakam",
    "res.col.mult": "Çarpan",
    "res.col.tol": "Tolerans",
    "res.unknown_color": "bilinmeyen renk '{code}'",
    "res.band_count": "3, 4, 5 veya 6 bant girilmeli",
    "res.bad_digit": "{pos}. bant ({color}) rakam bandı olamaz",
    "res.bad_mult": "çarpan bandı {color} olamaz",
    "res.bad_tol": "tolerans bandı {color} olamaz",
    "res.bad_tempco": "sıcaklık katsayısı bandı {color} olamaz",
    "res.cannot_encode": "{value} renk koduyla yazılamaz",
    "res.bad_tol_value": "geçersiz tolerans %{tol} (seçenekler: {options})",
    "res.eia96_range": "EIA-96 kodu 01-96 arasında olmalı",
    "res.smd_invalid": "'{code}' SMD kodu anlaşılamadı (örnek: 103, 4R7, 1002, 01C)",
    "res.see_table": "Renkler için: elektro resistor table",
    "res.title": "Direnç",
    "res.value": "Değer",
    "res.tolerance": "Tolerans",
    "res.range": "Aralık",
    "res.tempco": "Sıcaklık kats.",
    "res.bands": "Bantlar",
    "res.codes": "Kodlar",
    "res.code": "Kod",
    "res.note": "Not",
    "res.rounded": "{value} {bands} bantla tam yazılamıyor, yuvarlandı",
    "res.nearest_std": "En yakın standart",

    # --- seri / paralel ------------------------------------------------------------------
    "combine.series.help": (
        "Seri bağlı elemanların toplamı (varsayılan: direnç).\n\n"
        "Örnekler:\n"
        "  elektro series 1k 2k2 470\n"
        "  elektro series 100n 100n --cap"
    ),
    "combine.parallel.help": (
        "Paralel bağlı elemanların eşdeğeri (varsayılan: direnç).\n\n"
        "Örnekler:\n"
        "  elektro parallel 1k 1k\n"
        "  elektro parallel 10u 22u --cap"
    ),
    "combine.arg.series": "Eleman değerleri, örn: 1k 2k2 470",
    "combine.arg.parallel": "Eleman değerleri, örn: 1k 1k",
    "combine.opt.cap": "Kondansatör olarak hesapla",
    "combine.opt.ind": "Bobin olarak hesapla",
    "combine.item": "{n}. eleman",
    "combine.total": "Toplam",
    "combine.series_title": "Seri Bağlantı",
    "combine.parallel_title": "Paralel Bağlantı",

    # --- gerilim bölücü --------------------------------------------------------------------
    "div.help": (
        "Gerilim bölücü: Vout = Vin · R2 / (R1 + R2)\n\n"
        "R1 ve R2 verilirse çıkışı hesaplar; --vout verilirse standart değerlerden\n"
        "en iyi R1/R2 çiftlerini önerir.\n\n"
        "Örnekler:\n"
        "  elektro divider --vin 12 --r1 10k --r2 4k7\n"
        "  elektro divider --vin 5 --vout 3.3\n"
        "  elektro divider --vin 12 --vout 3.3 --series E12"
    ),
    "div.opt.vin": "Giriş gerilimi (V)",
    "div.opt.r1": "Üst direnç (Vin ile çıkış arası)",
    "div.opt.r2": "Alt direnç (çıkış ile toprak arası)",
    "div.opt.vout": "Hedef çıkış (R1/R2 önerisi için)",
    "div.opt.series": "Öneri için E serisi",
    "div.opt.load": "Çıkışa bağlı yük direnci",
    "div.range": "0 < Vout < Vin olmalı",
    "div.need": "--r1 ve --r2 ya da --vout verilmeli",
    "div.none": "uygun çift bulunamadı",
    "div.title": "Gerilim Bölücü",
    "div.ratio": "Oran",
    "div.current": "Akım",
    "div.unloaded": "Yüksüz Vout",
    "div.col.error": "Hata",
    "div.col.current": "Akım",

    # --- LED ----------------------------------------------------------------------------------
    "led.help": (
        "LED ön direnci hesabı.\n\n"
        "Örnekler:\n"
        "  elektro led --vs 5\n"
        "  elektro led --vs 12 --vf 3.1 -i 15m -n 3"
    ),
    "led.opt.vs": "Besleme gerilimi (V)",
    "led.opt.vf": "LED ileri gerilimi (V). Kırmızı ~2, mavi/beyaz ~3",
    "led.opt.if": "LED akımı (A), örn: 20m",
    "led.opt.count": "Seri bağlı LED sayısı",
    "led.opt.series": "Önerilecek E serisi",
    "led.supply_low": "besleme ({vs} V) LED gerilim düşümünden ({drop} V) büyük olmalı",
    "led.current_pos": "akım pozitif olmalı",
    "led.title": "LED Direnci",
    "led.calc_r": "Hesaplanan R",
    "led.suggested": "Önerilen ({series})",
    "led.real_i": "Gerçek akım",
    "led.power": "Direnç gücü",
    "led.rating": "Önerilen güç sınıfı",
    "led.rating_high": "> 10 W (farklı çözüm düşün)",
    "led.efficiency": "Verim",

    # --- E serisi ------------------------------------------------------------------------------
    "eseries.help": (
        "Bir değere en yakın standart (E3…E192) değerleri gösterir.\n\n"
        "Örnekler:\n"
        "  elektro eseries 4k8\n"
        "  elektro eseries 3.3u -s E12"
    ),
    "eseries.arg": "Aranan değer, örn: 4k8",
    "eseries.opt.series": "Sadece bu seri (örn: E24)",
    "eseries.title": "{value} için standart değerler",
    "eseries.col.series": "Seri",
    "eseries.col.lower": "Alt",
    "eseries.col.upper": "Üst",
    "eseries.col.nearest": "En yakın",
    "eseries.col.error": "Hata",

    # --- kondansatör ----------------------------------------------------------------------------
    "cap.help": (
        "Seramik kondansatör kodunu çözer ya da değerden kod üretir.\n\n"
        "Örnekler:\n"
        "  elektro cap 104       → 100 nF\n"
        "  elektro cap 472K      → 4.7 nF ±%10\n"
        "  elektro cap 22n       → 223"
    ),
    "cap.arg": "Kod (104, 472K) veya değer (100n)",
    "cap.bad_code": "3 haneli kod bekleniyor (örn: 104, 472K)",
    "cap.title": "Kondansatör",
    "cap.code": "Kod",
    "cap.value": "Değer",
    "cap.tolerance": "Tolerans",
    "cap.not_ceramic": "bu değer muhtemelen seramik kondansatör değil",

    # --- filtreler ----------------------------------------------------------------------------
    "flt.help": "RC/RL/LC/RLC filtre analizi ve tasarımı.",
    "flt.response": "Frekans yanıtı",
    "flt.gain": "Kazanç",
    "flt.phase": "Faz",
    "flt.need_two": "{opts} değerlerinden tam olarak ikisini ver",
    "flt.opt.r": "Direnç (Ω), örn: 1k",
    "flt.opt.c": "Kapasitans (F), örn: 100n",
    "flt.opt.l": "Endüktans (H), örn: 10m",
    "flt.opt.fc": "Kesim frekansı (Hz), örn: 1k",
    "flt.opt.f0": "Rezonans frekansı (Hz)",
    "flt.fc": "Kesim frekansı (fc)",
    "flt.omega": "Açısal frekans (ωc)",
    "flt.tau": "Zaman sabiti (τ)",
    "flt.r": "Direnç (R)",
    "flt.c": "Kapasitans (C)",
    "flt.l": "Endüktans (L)",
    "flt.f0": "Rezonans frekansı (f₀)",
    "flt.center": "Merkez frekans (f₀)",
    "flt.bw": "Bant genişliği (BW)",
    "flt.q": "Kalite faktörü (Q)",
    "flt.lower": "Alt kesim",
    "flt.upper": "Üst kesim",
    "flt.rc.help": (
        "RC filtre (varsayılan alçak geçiren). R, C, fc'den ikisini ver.\n\n"
        "fc = 1 / (2πRC)    τ = RC\n\n"
        "Örnekler:\n"
        "  elektro filter rc --r 1k --c 100n\n"
        "  elektro filter rc --fc 1k --c 10n          (R'yi bulur)\n"
        "  elektro filter rc --r 10k --fc 50 --high   (C'yi bulur)"
    ),
    "flt.rc.opt.high": "Yüksek geçiren (C seri, R toprağa)",
    "flt.rc.title_low": "RC Alçak Geçiren Filtre",
    "flt.rc.title_high": "RC Yüksek Geçiren Filtre",
    "flt.rc.note1": "fc'de kazanç -3 dB, faz {phase}; eğim 20 dB/dekad.",
    "flt.rc.note2": "τ süresinde kondansatör son değerinin %63'üne ulaşır, ~5τ'da tamamen dolar.",
    "flt.rl.help": (
        "RL filtre (varsayılan yüksek geçiren). R, L, fc'den ikisini ver.\n\n"
        "fc = R / (2πL)    τ = L / R\n\n"
        "Örnekler:\n"
        "  elektro filter rl --r 1k --l 10m\n"
        "  elektro filter rl --r 100 --fc 10k --low"
    ),
    "flt.rl.opt.low": "Alçak geçiren (L seri, R toprağa)",
    "flt.rl.title_low": "RL Alçak Geçiren Filtre",
    "flt.rl.title_high": "RL Yüksek Geçiren Filtre",
    "flt.lc.help": (
        "LC rezonans. L, C, f'den ikisini ver.\n\n"
        "f₀ = 1 / (2π√(LC))    Z₀ = √(L/C)\n\n"
        "Örnekler:\n"
        "  elektro filter lc --l 10u --c 100n\n"
        "  elektro filter lc --f 433.92M --c 10p     (L'yi bulur)"
    ),
    "flt.lc.title": "LC Rezonans",
    "flt.lc.reactance": "Reaktans (XL = XC)",
    "flt.lc.z0": "Karakteristik empedans",
    "flt.lc.note": "Seri LC rezonansta empedans minimum, paralel LC (tank) rezonansta maksimumdur.",
    "flt.rlc.help": (
        "Seri RLC bant geçiren filtre (çıkış R üzerinden).\n\n"
        "f₀ = 1 / (2π√(LC))   BW = R / (2πL)   Q = f₀ / BW\n\n"
        "Örnek:\n"
        "  elektro filter rlc --r 10 --l 1m --c 100n"
    ),
    "flt.rlc.title": "Seri RLC Bant Geçiren",
    "flt.rlc.note": "Yüksek Q → dar bant, yüksek seçicilik. Düşük Q → geniş bant.",
    "flt.notch.help": (
        "Bant durduran (notch): sinyal yolunda paralel LC tankı, çıkış R üzerinden.\n\n"
        "f₀ = 1 / (2π√(LC))   Q = R / (2πf₀L)\n\n"
        "Örnek (50 Hz şebeke gürültüsü):\n"
        "  elektro filter notch --r 1k --l 1.013 --c 10u"
    ),
    "flt.notch.opt.r": "Yük direnci (Ω)",
    "flt.notch.title": "Bant Durduran (Notch)",
    "flt.notch.f0": "Söndürme frekansı (f₀)",
    "flt.notch.note": "İdeal elemanlarla f₀'da zayıflama sonsuzdur; gerçekte bobin direnci sınırlar.",
    "flt.theory.help": "Filtre türleri ve formüllerin özeti.",
    "flt.theory.title": "Filtre Teorisi",
    "flt.theory.body": (
        "[bold]Alçak geçiren[/]  RC: R seri, C toprağa   ·  RL: L seri, R toprağa\n"
        "[bold]Yüksek geçiren[/] RC: C seri, R toprağa   ·  RL: R seri, L toprağa\n"
        "[bold]Bant geçiren[/]   Seri RLC, çıkış R üzerinden (rezonansta Z minimum)\n"
        "[bold]Bant durduran[/]  Paralel LC tankı sinyal yolunda (rezonansta Z maksimum)\n\n"
        "fc(RC) = 1/(2πRC)     fc(RL) = R/(2πL)\n"
        "f₀(LC) = 1/(2π√(LC))  Q = f₀/BW\n"
        "1. derece filtre: fc'de -3 dB, 20 dB/dekad eğim"
    ),

    # --- RF ----------------------------------------------------------------------------------
    "rf.help": "RF: FSPL, link bütçesi, dalga boyu ve birim dönüşümleri.",
    "rf.metavar.freq": "FREKANS",
    "rf.metavar.dist": "MESAFE",
    "rf.opt.freq": "Frekans. Yalın sayı MHz: 868, 2.4G, 433.92M",
    "rf.opt.dist": "Mesafe. Yalın sayı km: 5, 800m, 12km",
    "rf.bad_distance": "'{text}' mesafe olarak anlaşılamadı (örn: 5, 2.5km, 800m)",
    "rf.positive": "frekans ve mesafe pozitif olmalı",
    "rf.freq": "Frekans",
    "rf.dist": "Mesafe",
    "rf.wavelength": "Dalga boyu",
    "rf.fspl.help": (
        "Serbest uzay yol kaybı (ITU-R P.525).\n\n"
        "FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 20·log₁₀(4π/c)\n\n"
        "Örnekler:\n"
        "  elektro rf fspl -f 868 -d 5\n"
        "  elektro rf fspl -f 2.4G -d 300m"
    ),
    "rf.fspl.title": "Serbest Uzay Yol Kaybı",
    "rf.fspl.note": "Link marjını görmek için: elektro rf link --help",
    "rf.link.help": (
        "Link bütçesi: alınan güç, link marjı ve teorik maksimum menzil.\n\n"
        "Prx = Ptx + Gtx + Grx − FSPL − kayıplar\n\n"
        "Örnekler:\n"
        "  elektro rf link -f 868 -d 10 --tx 14 --sens -137\n"
        "  elektro rf link -f 2.4G -d 500m --tx 20 --gtx 5 --grx 5 --sens -90 --loss 3"
    ),
    "rf.link.opt.tx": "Verici gücü (dBm)",
    "rf.link.opt.gtx": "Verici anten kazancı (dBi)",
    "rf.link.opt.grx": "Alıcı anten kazancı (dBi)",
    "rf.link.opt.sens": "Alıcı hassasiyeti (dBm)",
    "rf.link.opt.loss": "Kablo/konnektör/ortam kayıpları toplamı (dB)",
    "rf.link.title": "Link Bütçesi",
    "rf.link.prx": "Alınan güç",
    "rf.link.sens": "Hassasiyet",
    "rf.link.margin": "Link marjı",
    "rf.link.solid": "sağlam",
    "rf.link.marginal": "sınırda",
    "rf.link.no_link": "BAĞLANTI YOK",
    "rf.link.range0": "Maks. menzil (0 dB marj)",
    "rf.link.range10": "Maks. menzil (10 dB marj)",
    "rf.link.note1": "Serbest uzay varsayımıdır; engeller, Fresnel bölgesi ve sönümleme menzili ciddi azaltır.",
    "rf.link.note2": "Pratikte 10-20 dB marj bırakılması önerilir.",
    "rf.wave.help": (
        "Dalga boyu ve temel anten boyları.\n\n"
        "Örnekler:\n"
        "  elektro rf wave -f 433.92\n"
        "  elektro rf wave -f 2.4G --vf 0.95"
    ),
    "rf.wave.opt.vf": "Hız faktörü (koaksiyel için ~0.66-0.85, tel anten ~0.95)",
    "rf.wave.bad": "frekans pozitif ve 0 < vf ≤ 1 olmalı",
    "rf.wave.title": "Dalga Boyu",
    "rf.wave.dipole": "λ/2 dipol (toplam)",
    "rf.wave.monopole": "λ/4 monopol / GP",
    "rf.conv.help": (
        "RF birim dönüşümü (güç ve empedans uyumu).\n\n"
        "Örnekler:\n"
        "  elektro rf convert 14 dbm w\n"
        "  elektro rf convert 0.1 w\n"
        "  elektro rf convert 1.5 vswr"
    ),
    "rf.conv.arg.value": "Değer",
    "rf.conv.arg.src": "Kaynak birim: dbm dbw w mw uw vswr rl gamma",
    "rf.conv.arg.dst": "Hedef birim (boşsa hepsi)",
    "rf.conv.vswr": "VSWR ≥ 1 olmalı",
    "rf.conv.rl": "return loss ≥ 0 dB olmalı",
    "rf.conv.gamma": "|Γ| 0 ile 1 arasında olmalı",
    "rf.conv.power_pos": "güç pozitif olmalı",
    "rf.conv.no_path": "{src} → {dst} dönüşümü yok",
    "rf.conv.unknown": "bilinmeyen birim '{unit}'",
    "rf.conv.l.rl": "Return loss",
    "rf.conv.l.mismatch": "Uyumsuzluk kaybı",
    "rf.conv.l.reflected": "Yansıyan güç",

    # --- dijital -----------------------------------------------------------------------------
    "dig.help": "Dijital: sayı tabanları, mantık kapıları, boolean ifadeler.",
    "dig.base_range": "taban 2 ile 36 arasında olmalı",
    "dig.conv.help": (
        "Sayı tabanları arası dönüşüm (2-36).\n\n"
        "Hedef verilmezse ikili, sekizli, onlu ve onaltılı gösterimi birlikte verir.\n\n"
        "Örnekler:\n"
        "  elektro logic convert 255\n"
        "  elektro logic convert 0xFF -t 2\n"
        "  elektro logic convert 1010 -f 2\n"
        "  elektro logic convert --bits 8 -- -5"
    ),
    "dig.conv.arg": "Sayı: 255, 0xFF, 0b1010, 0o17, 1Fh",
    "dig.conv.opt.from": "Kaynak taban (varsayılan: önekten ya da 10)",
    "dig.conv.opt.to": "Sadece bu tabana çevir",
    "dig.conv.opt.bits": "Bit genişliği (negatifler için ikiye tümleyen)",
    "dig.conv.invalid": "'{value}' geçerli bir sayı değil",
    "dig.conv.in_base": " (taban {base})",
    "dig.conv.overflow": "{n} değeri {bits} bite sığmaz ({lo} … {hi})",
    "dig.conv.base": "taban {base}",
    "dig.conv.title": "Sayı Dönüşümü",
    "dig.dec": "Onlu",
    "dig.hex": "Onaltılı",
    "dig.bin": "İkili",
    "dig.oct": "Sekizli",
    "dig.bits": "Bit sayısı",
    "dig.unsigned": "İşaretsiz",
    "dig.truth.help": (
        "Mantık kapısı çıkışı veya (giriş verilmezse) doğruluk tablosu.\n\n"
        "Örnekler:\n"
        "  elektro logic truth xor\n"
        "  elektro logic truth nand -a 1 -b 1"
    ),
    "dig.truth.arg": "Kapı: {gates}",
    "dig.truth.opt.a": "Giriş A (0/1)",
    "dig.truth.opt.b": "Giriş B (0/1)",
    "dig.truth.unknown": "bilinmeyen kapı '{gate}' (seçenekler: {gates})",
    "dig.expr.help": (
        "Boolean ifadenin doğruluk tablosu ve minterm listesi.\n\n"
        "Operatörler: & (VE), | (VEYA), ^ (XOR), ~ (DEĞİL). and/or/xor/not ve ve/veya/değil de yazılabilir.\n\n"
        "Örnekler:\n"
        "  elektro logic expr \"A & B | ~C\"\n"
        "  elektro logic expr \"(A xor B) ve C\""
    ),
    "dig.expr.arg": "Boolean ifade, örn: \"A & B | ~C\"",
    "dig.expr.invalid": "ifade anlaşılamadı: {expr}",
    "dig.expr.unsupported": "desteklenmeyen öğe: {node}",
    "dig.expr.const": "sabit olarak sadece 0 ve 1 kullanılabilir",
    "dig.expr.too_many": "en fazla 6 değişken destekleniyor",

    # --- 555 -------------------------------------------------------------------------------------
    "555.help": "NE555 zamanlayıcı: astable ve monostable.",
    "555.astable.help": (
        "Astable (osilatör) mod.\n\n"
        "f = 1.44 / ((R1 + 2R2)·C)    D = (R1 + R2) / (R1 + 2R2)\n\n"
        "Örnekler:\n"
        "  elektro 555 astable --r1 1k --r2 10k --c 10u\n"
        "  elektro 555 astable -f 1k -d 60 --c 10n     (R1, R2'yi bulur)"
    ),
    "555.mono.help": (
        "Monostable (tek darbe) mod. R, C, t'den ikisini ver.\n\n"
        "t = 1.1 · R · C\n\n"
        "Örnekler:\n"
        "  elektro 555 mono --r 100k --c 10u\n"
        "  elektro 555 mono --t 5 --c 100u     (R'yi bulur)"
    ),
    "555.opt.r1": "R1 (VCC–DIS arası)",
    "555.opt.r2": "R2 (DIS–THR/TRIG arası)",
    "555.opt.c": "Zamanlama kondansatörü",
    "555.opt.r": "Zamanlama direnci",
    "555.opt.t": "Darbe süresi (s)",
    "555.opt.freq": "Hedef frekans (tasarım modu)",
    "555.opt.duty": "Hedef görev oranı % (tasarım modu)",
    "555.duty_range": ("klasik 555 astable'da görev oranı %50'den büyük olmalı "
                       "(daha düşük oran için R2'ye paralel diyot kullanılır)"),
    "555.need": "--r1 ve --r2 ya da --freq verilmeli",
    "555.mono.need": "--r, --c ve --t'den tam olarak ikisini ver",
    "555.design.title": "555 Astable Tasarım",
    "555.r1_calc": "R1 (hesap)",
    "555.r2_calc": "R2 (hesap)",
    "555.real_freq": "Gerçek frekans",
    "555.real_duty": "Gerçek görev oranı",
    "555.range_warn": "Uyarı: R1 ≥ 1 kΩ ve R2 ≤ 1 MΩ aralığı önerilir; kondansatör değerini değiştir.",
    "555.astable.title": "555 Astable",
    "555.freq": "Frekans",
    "555.period": "Periyot",
    "555.t_high": "Yüksek süre",
    "555.t_low": "Düşük süre",
    "555.duty": "Görev oranı",
    "555.mono.title": "555 Monostable",
    "555.pulse": "Darbe süresi",

    # --- datasheet -----------------------------------------------------------------------------
    "ds.help": (
        "Komponent datasheet'ini bulup bulunduğun klasöre indirir.\n\n"
        "Önce üretici sitelerine, sonra LCSC parça veritabanına, en son\n"
        "DuckDuckGo aramasına bakar. İnen dosyanın gerçekten PDF olduğu doğrulanır.\n\n"
        "Örnekler:\n"
        "  elektro datasheet lm358\n"
        "  elektro datasheet ams1117 --open\n"
        "  elektro datasheet 2n2222 -o transistor.pdf\n"
        "  elektro datasheet esp32 --list"
    ),
    "ds.arg.part": "Parça adı, örn: lm358, ne555, ams1117, esp32",
    "ds.opt.output": "Kayıt yolu (varsayılan: <parça>_datasheet.pdf)",
    "ds.opt.open": "İndirdikten sonra PDF'i aç",
    "ds.opt.list": "İndirmeden bulunan adayları listele",
    "ds.opt.force": "Dosya varsa üzerine yaz",
    "ds.opt.max": "Denenecek en fazla aday sayısı",
    "ds.step.maker": "Üretici siteleri kontrol ediliyor",
    "ds.step.lcsc": "LCSC/JLCPCB parça veritabanı aranıyor",
    "ds.step.ddg": "DuckDuckGo'da aranıyor",
    "ds.step.ddg_blocked": "DuckDuckGo şu an bot koruması gösteriyor, atlandı",
    "ds.no_opener": "'{opener}' bulunamadı, dosyayı elle aç: {path}",
    "ds.empty": "parça adı boş olamaz",
    "ds.candidates": "'{part}' için adaylar:",
    "ds.no_candidates": "Aday bulunamadı.",
    "ds.exists": "Dosya zaten var",
    "ds.use_force": "Tekrar indirmek için --force kullan.",
    "ds.no_dir": "klasör yok: {path}",
    "ds.searching": "'{part}' için datasheet aranıyor",
    "ds.downloaded": "İndirildi",
    "ds.try_next": "PDF alınamadı, sıradaki deneniyor",
    "ds.cancelled": "İptal edildi.",
    "ds.nothing": "Hiçbir kaynakta sonuç bulunamadı.",
    "ds.check_net": "İnternet bağlantını ya da parça adını kontrol et.",
    "ds.all_failed": "Bulunan adayların hiçbirinden PDF indirilemedi.",
    "ds.manual": "Elle aramak için:",
}

# --- 0.4: yeni komutlar -----------------------------------------------------------------
MESSAGES.update({
    "cli.opt.json": "Sonuçları JSON olarak yaz (betikler için)",
    "panel.power": "Güç & iletkenler",
    "panel.embedded": "Gömülü sistemler",
    "menu.switch": "Anahtar olarak transistör",
    "menu.charge": "RC/RL dolma eğrisi",
    "menu.regulator": "Voltaj regülatörü",
    "menu.battery": "Batarya ömrü",
    "menu.thermal": "Isı ve soğutucu",
    "menu.wire": "Kablo kesiti, gerilim düşümü",
    "menu.trace": "PCB yol genişliği",
    "menu.uart": "UART baud hatası",
    "menu.pwm": "Timer/PWM kayıtları",
    "menu.adc": "ADC gerilim ↔ kod",
    "menu.i2c": "I²C pull-up direnci",
    "menu.crc": "CRC / checksum",
    "menu.calc": "Birimli hesap makinesi",
    "menu.unit": "Birim dönüştürücü",
    "time.min": "dk",
    "time.hours": "saat",
    "time.days": "gün",
    "time.months": "ay",

    # regülatör
    "reg.help": (
        "Voltaj regülatörü: ayarlılarda direnç hesabı, lineerlerde harcanan güç.\n\n"
        "Ayarlı: lm317, lm1117, ams1117, lm2596, xl4015, mp1584\n"
        "Sabit: 7805, 7812, ams1117-3.3 …\n\n"
        "Örnekler:\n"
        "  elektro regulator lm317 --vout 5\n"
        "  elektro regulator lm317 --r1 240 --r2 720\n"
        "  elektro regulator 7805 --vin 12 -i 500m\n"
        "  elektro regulator ams1117-3.3 --vin 5 -i 300m"
    ),
    "reg.arg": "Regülatör, örn: lm317, 7805, ams1117-3.3",
    "reg.opt.vout": "Hedef çıkış gerilimi (ayarlı regülatörler)",
    "reg.opt.vin": "Giriş gerilimi",
    "reg.opt.iout": "Yük akımı",
    "reg.opt.r1": "R1 (OUT ile ADJ/FB arası); varsayılan: datasheet değeri",
    "reg.opt.r2": "R2 (ADJ/FB ile toprak arası) — Vout'u hesaplar",
    "reg.unknown": "bilinmeyen regülatör '{name}' (bilinenler: {options})",
    "reg.vout_low": "çıkış referans geriliminden ({vref} V) büyük olmalı",
    "reg.need_vout": "--vout ya da çıkışı hesaplamak için --r2 ver",
    "reg.vout": "Çıkış gerilimi",
    "reg.r2_calc": "R2 (hesap)",
    "reg.dropout": "Tipik düşüm (dropout)",
    "reg.headroom": "Vin − Vout",
    "reg.dropout_warn": "Vin − Vout = {headroom} V, tipik düşüm geriliminin ({dropout} V) altında; çıkış düşebilir.",
    "reg.power": "Harcanan güç",
    "reg.efficiency": "Verim",
    "reg.switching_note": "Anahtarlamalı regülatör: kayıp verime bağlıdır (tipik %80-95), datasheet'e bak.",
    "reg.heat_note": "1 W üstü çoğu kılıfta soğutucu ister — kontrol için: elektro thermal --help",

    # batarya
    "bat.help": (
        "Kapasite ve ortalama akımdan (ya da aktif/uyku profilinden) batarya ömrü.\n\n"
        "Örnekler:\n"
        "  elektro battery 2000 -i 15m\n"
        "  elektro battery 1200 --active 45m --active-time 2 --sleep 20u --sleep-time 58"
    ),
    "bat.arg": "Kapasite (mAh)",
    "bat.opt.current": "Ortalama akım (A), örn: 15m",
    "bat.opt.active": "Aktifken çekilen akım (A)",
    "bat.opt.active_time": "Her döngüde aktif süre (s)",
    "bat.opt.sleep": "Uykudayken çekilen akım (A)",
    "bat.opt.sleep_time": "Her döngüde uyku süresi (s)",
    "bat.opt.derate": "Kapasitenin kullanılabilir oranı (yaşlanma, sıcaklık, kesme gerilimi)",
    "bat.need": "-i ya da --active --active-time --sleep --sleep-time değerlerinin hepsini ver",
    "bat.title": "Batarya Ömrü",
    "bat.capacity": "Kapasite",
    "bat.usable": "Kullanılabilir",
    "bat.avg_current": "Ortalama akım",
    "bat.life": "Tahmini ömür",
    "bat.note": "Kendi kendine deşarj ve regülatörün boşta akımı hesaba katılmadı.",

    # ısıl
    "th.help": (
        "Jonksiyon sıcaklığı ve gereken soğutucu.\n\n"
        "Tj = Ta + P · (Rθjc + Rθcs + Rθsa)   ya da   Tj = Ta + P · Rθja\n\n"
        "Örnekler:\n"
        "  elektro thermal -p 2 --rth-ja 62 --ta 40          (soğutucusuz, TO-220)\n"
        "  elektro thermal -p 5 --rth-jc 3 --rth-sa 8\n"
        "  elektro thermal -p 5 --rth-jc 3 --ta 50           (gereken soğutucu)"
    ),
    "th.opt.power": "Harcanan güç (W)",
    "th.opt.ta": "Ortam sıcaklığı (°C)",
    "th.opt.tjmax": "Maksimum jonksiyon sıcaklığı (°C)",
    "th.opt.rja": "Soğutucusuz jonksiyon-ortam ısıl direnci (°C/W)",
    "th.opt.rjc": "Jonksiyon-kılıf ısıl direnci (°C/W)",
    "th.opt.rcs": "Kılıf-soğutucu (ısı pedi/macun) (°C/W)",
    "th.opt.rsa": "Soğutucu-ortam (°C/W)",
    "th.need": "--rth-ja ya da --rth-jc (--rth-sa ile veya onsuz) ver",
    "th.title": "Isıl Hesap",
    "th.power": "Güç",
    "th.total": "Toplam Rθ",
    "th.need_sa": "Gereken soğutucu Rθsa ≤",
    "th.impossible": "mümkün değil — gücü azalt",
    "th.margin": "Tj max'a kalan pay",
    "th.margin_note": "Bu değerin rahatça altında bir soğutucu seç (~%20-30 pay).",
    "th.over": "Jonksiyon sıcaklığı maksimumu aşıyor!",

    # kablo
    "wire.help": (
        "Bakır kablo: AWG ↔ mm², direnç, gerilim düşümü ve kayıp.\n\n"
        "Örnekler:\n"
        "  elektro wire --awg 22 -l 3 -i 2\n"
        "  elektro wire --mm2 1.5 -l 10 -i 10 --round-trip"
    ),
    "wire.opt.awg": "Kablo kalınlığı (AWG)",
    "wire.opt.mm2": "Kesit (mm²)",
    "wire.opt.length": "Uzunluk (yalın sayı = m): 3, 50cm, 10ft",
    "wire.opt.current": "Akım (A)",
    "wire.opt.round_trip": "Uzunluğu iki kez say (gidiş + dönüş iletkeni)",
    "wire.opt.temp": "İletken sıcaklığı (°C)",
    "wire.metavar.length": "UZUNLUK",
    "wire.bad_length": "'{text}' uzunluk olarak anlaşılamadı (örn: 3, 50cm, 10ft)",
    "wire.need": "--awg ya da --mm2'den birini ver",
    "wire.title": "Bakır Kablo",
    "wire.diameter": "Çap",
    "wire.area": "Kesit",
    "wire.r_per_m": "Metre başına direnç",
    "wire.resistance": "Direnç",
    "wire.drop": "Gerilim düşümü",
    "wire.loss": "Güç kaybı",
    "wire.density": "Akım yoğunluğu",
    "wire.hot": "Akım yoğunluğu yüksek; kablo ısınabilir (> 6 A/mm²).",
    "wire.note": "Tek telli bakır; çok telli kablonun direnci biraz daha yüksektir.",

    # PCB yolu
    "trace.help": (
        "IPC-2221'e göre PCB yol genişliği (ya da bir yolun taşıyabileceği akım).\n\n"
        "Örnekler:\n"
        "  elektro trace -i 3\n"
        "  elektro trace -i 5 --rise 20 --oz 2\n"
        "  elektro trace -w 0.5 --internal -l 40mm"
    ),
    "trace.opt.current": "Akım (A)",
    "trace.opt.width": "Yol genişliği mm (akımı hesaplar)",
    "trace.opt.rise": "İzin verilen sıcaklık artışı (°C)",
    "trace.opt.oz": "Bakır ağırlığı (oz/ft²): 0.5, 1, 2",
    "trace.opt.internal": "İç katman (varsayılan dış katman)",
    "trace.opt.length": "Yol uzunluğu (yalın sayı = m): 40mm, 0.1",
    "trace.need": "-i ya da -w'den birini ver",
    "trace.title": "PCB Yolu (IPC-2221)",
    "trace.width": "Genişlik",
    "trace.current": "Akım",
    "trace.thickness": "Bakır",
    "trace.layer": "Katman",
    "trace.internal": "iç",
    "trace.external": "dış",
    "trace.rise": "Sıcaklık artışı",
    "trace.note": "IPC-2221 temkinlidir; yüksek akımlarda IPC-2152'ye de bak.",

    # transistör anahtar
    "sw.help": "Anahtar olarak transistör: BJT taban direnci, MOSFET kapı sürme.",
    "sw.opt.vdrive": "Sürme gerilimi (örn: GPIO 3.3 ya da 5 V)",
    "sw.bjt.help": (
        "Doyumda çalışan BJT (NPN) anahtar: taban direnci ve kayıplar.\n\n"
        "Ib = Ic / hFE · k     Rb = (Vsürme − Vbe) / Ib\n\n"
        "Örnekler:\n"
        "  elektro switch bjt --ic 500m -v 3.3\n"
        "  elektro switch bjt --vcc 12 --rload 24 -v 5 --hfe 150"
    ),
    "sw.bjt.opt.ic": "Kollektör (yük) akımı",
    "sw.bjt.opt.hfe": "Minimum akım kazancı hFE (datasheet'ten)",
    "sw.bjt.opt.overdrive": "Sağlam doyum için aşırı sürme katsayısı k (2-5)",
    "sw.bjt.opt.vbe": "Baz-emiter gerilimi (V)",
    "sw.bjt.opt.vcesat": "Kollektör-emiter doyum gerilimi (V)",
    "sw.bjt.opt.vcc": "Besleme gerilimi (--rload ile, --ic yerine)",
    "sw.bjt.opt.rload": "Yük direnci (--vcc ile)",
    "sw.bjt.need": "--ic ya da --vcc ve --rload ver",
    "sw.bjt.vdrive_low": "sürme gerilimi Vbe'den ({vbe} V) büyük olmalı",
    "sw.bjt.title": "BJT Anahtar",
    "sw.bjt.ib": "Gereken Ib",
    "sw.bjt.rb_calc": "Rb (hesap)",
    "sw.bjt.rb_std": "Rb (E12, bir alt)",
    "sw.bjt.forced_beta": "Zorlanmış β (Ic/Ib)",
    "sw.bjt.p_transistor": "Transistör kaybı",
    "sw.bjt.p_rb": "Rb gücü",
    "sw.bjt.gpio_warn": "{ib} taban akımı çoğu MCU bacağı için fazla; Darlington ya da MOSFET kullan.",
    "sw.bjt.note": "Endüktif yüklerde (röle, motor) yüke paralel serbest geçiş diyotu ekle.",
    "sw.fet.help": (
        "MOSFET kapı sürme: kapı akımı, anahtarlama süresi ve kayıplar.\n\n"
        "Örnekler:\n"
        "  elektro switch mosfet -v 10 --qg 40n --rg 10 -f 100k\n"
        "  elektro switch mosfet -v 5 --qg 20n -f 20k --id 5 --rds 20m --vds 24"
    ),
    "sw.fet.opt.qg": "Toplam kapı yükü Qg (C), örn: 40n",
    "sw.fet.opt.rg": "Kapı direnci (Ω)",
    "sw.fet.opt.fsw": "Anahtarlama frekansı (Hz)",
    "sw.fet.opt.id": "Drain akımı (A)",
    "sw.fet.opt.rds": "İletim direnci Rds(on) (Ω)",
    "sw.fet.opt.vds": "Kesimdeyken drain-source gerilimi (V)",
    "sw.fet.title": "MOSFET Kapı Sürme",
    "sw.fet.ipeak": "Tepe kapı akımı",
    "sw.fet.tsw": "Anahtarlama süresi (≈ Qg/Ig)",
    "sw.fet.pgate": "Kapı sürme gücü",
    "sw.fet.pcond": "İletim kaybı",
    "sw.fet.psw": "Anahtarlama kaybı (yaklaşık)",
    "sw.fet.ptotal": "Toplam kayıp",
    "sw.fet.slow": "Anahtarlama periyodun %10'undan uzun sürüyor; kapı sürücü ya da daha küçük Rg kullan.",
    "sw.fet.logic_level": "5 V altı sürme: lojik seviye MOSFET kullan (Rds(on) 2.5-4.5 V'ta belirtilmiş).",
    "sw.fet.note": "Tahmindir; gerçek anahtarlama süresi Miller platosuna ve sürücüye de bağlıdır.",

    # dolma
    "chg.help": (
        "Zamana göre RC kondansatör dolması / RL bobin akımı.\n\n"
        "v(t) = Vs + (V0 − Vs) · e^(−t/τ)\n\n"
        "Örnekler:\n"
        "  elektro charge --r 10k --c 100u --v 5\n"
        "  elektro charge --r 10k --c 100u --v 5 --to 3.3      (3.3 V'a kadar süre)\n"
        "  elektro charge --r 10k --c 100u --v 0 --v0 5 --t 1  (boşalma)\n"
        "  elektro charge --r 10 --l 1m --v 12                 (RL akımı)"
    ),
    "chg.opt.r": "Direnç (Ω)",
    "chg.opt.c": "RC için kapasitans (F)",
    "chg.opt.l": "RL için endüktans (H)",
    "chg.opt.v": "Uygulanan (son) gerilim (V)",
    "chg.opt.v0": "Kondansatörün başlangıç gerilimi (V)",
    "chg.opt.to": "Hedef gerilim: ne kadar sürede ulaşılır",
    "chg.opt.t": "Zaman (s): bu andaki değer",
    "chg.need": "--c (RC) ya da --l (RL)'den birini ver",
    "chg.unreachable": "hedefe hiç ulaşılmaz (başlangıç ile son değer arasında değil)",
    "chg.title_rc": "RC Dolma",
    "chg.title_rl": "RL Akımı",
    "chg.final": "Son değer",
    "chg.value_at": "{time} anındaki değer",
    "chg.time_to": "{target} için süre",
    "chg.note": "1τ sonunda değişimin {pct}'ü tamamlanır; 5τ'da pratikte biter.",

    # microstrip
    "ms.help": (
        "Mikroşerit hat: istenen empedans için yol genişliği ya da bir genişliğin empedansı (Hammerstad).\n\n"
        "Örnekler:\n"
        "  elektro rf microstrip --z0 50                   (1.6 mm FR4)\n"
        "  elektro rf microstrip --z0 50 --h 0.2 --er 4.2 -f 2.4G\n"
        "  elektro rf microstrip -w 3"
    ),
    "ms.opt.z0": "Hedef empedans (Ω)",
    "ms.opt.width": "Yol genişliği (mm) — Z0'ı hesaplar",
    "ms.opt.h": "Toprak düzlemine olan dielektrik kalınlığı (mm)",
    "ms.opt.er": "Bağıl dielektrik sabiti εr (FR4 ≈ 4.2-4.6)",
    "ms.need": "--z0 ya da --width'ten birini ver",
    "ms.range": "empedans ulaşılabilir aralığın dışında",
    "ms.title": "Mikroşerit Hat",
    "ms.width": "Yol genişliği",
    "ms.lambda": "Hat üzerindeki dalga boyu",
    "ms.note": "Bakır kalınlığı ve lehim maskesi hesaba katılmadı; son değer için üreticinin hesaplayıcısını kullan.",

    # LoRa
    "lora.help": (
        "LoRa havada kalma süresi, veri hızı, hassasiyet ve görev döngüsü sınırı (Semtech AN1200.13).\n\n"
        "Örnekler:\n"
        "  elektro rf lora --sf 9 -p 20\n"
        "  elektro rf lora --sf 12 --bw 125k --cr 4/8 -p 51"
    ),
    "lora.opt.sf": "Yayılma faktörü (7-12)",
    "lora.opt.bw": "Bant genişliği (Hz): 125k, 250k, 500k",
    "lora.opt.cr": "Kodlama oranı: 4/5 … 4/8",
    "lora.opt.payload": "Veri uzunluğu (bayt)",
    "lora.opt.preamble": "Preamble uzunluğu (sembol)",
    "lora.opt.no_crc": "Veri CRC'si olmadan",
    "lora.opt.implicit": "Örtük başlık (implicit header) modu",
    "lora.opt.duty": "Görev döngüsü sınırı % (AB 868 MHz: 1)",
    "lora.opt.nf": "Alıcı gürültü figürü (dB)",
    "lora.bad_cr": "kodlama oranı 4/5, 4/6, 4/7 ya da 4/8 olmalı",
    "lora.airtime": "Havada kalma süresi",
    "lora.symbol": "Sembol süresi",
    "lora.bitrate": "Veri hızı",
    "lora.sensitivity": "Hassasiyet (yaklaşık)",
    "lora.per_hour": "{duty} ile saatte paket",
    "lora.interval": "her",
    "lora.on": "açık",
    "lora.off": "kapalı",
    "lora.note": "LDRO (düşük veri hızı optimizasyonu) sembol süresi 16 ms'yi aşınca otomatik açılır.",

    # Fresnel
    "fresnel.help": (
        "Birinci Fresnel bölgesi ve görüş hattı için gereken anten yüksekliği.\n\n"
        "r₁ = √(λ·d₁·d₂ / D)\n\n"
        "Örnekler:\n"
        "  elektro rf fresnel -f 868 -d 10\n"
        "  elektro rf fresnel -f 2.4G -d 3 --at 500m"
    ),
    "fresnel.opt.at": "Engelin vericiye uzaklığı (varsayılan: orta nokta)",
    "fresnel.opt.k": "Etkin dünya yarıçapı katsayısı (standart atmosfer 4/3)",
    "fresnel.bad_at": "nokta iki anten arasında olmalı",
    "fresnel.title": "Fresnel Bölgesi",
    "fresnel.point": "Nokta (d₁ / d₂)",
    "fresnel.r1": "1. Fresnel yarıçapı",
    "fresnel.r60": "%60 açıklık",
    "fresnel.bulge": "Dünya eğriliği",
    "fresnel.need": "Gereken açıklık",
    "fresnel.note": "Antenler arasındaki çizgi, o noktadaki engellerin bu kadar üstünden geçmeli.",

    # koaksiyel
    "coax.help": (
        "Bir frekansta koaksiyel kablo kaybı (tipik değerler).\n\n"
        "Kablolar: RG-58, RG-174, RG-316, RG-213, RG-6, LMR-195, LMR-240, LMR-400, LMR-600\n\n"
        "Örnekler:\n"
        "  elektro rf coax rg58 -f 868 -l 5\n"
        "  elektro rf coax lmr400 -f 2.4G -l 20m"
    ),
    "coax.arg": "Kablo tipi, örn: rg58, lmr400",
    "coax.opt.length": "Kablo uzunluğu (yalın sayı = m): 5, 150cm, 30ft",
    "coax.metavar.length": "UZUNLUK",
    "coax.unknown": "bilinmeyen kablo '{name}' (bilinenler: {options})",
    "coax.per100": "100 m başına kayıp",
    "coax.loss": "Toplam kayıp",
    "coax.delivered": "İletilen güç",
    "coax.delay": "Gecikme",
    "coax.electrical": "Elektriksel uzunluk",
    "coax.note": "Tipik değerlerdir; kablonun kendi datasheet'ine bak. Her konnektör ~0.1-0.3 dB ekler.",

    # MCU ortak
    "mcu.opt.clock": "Çevre birimi saati (Hz), örn: 16M, 72M",
    "mcu.opt.mcu": "Mikrodenetleyici ailesi: avr, stm32, generic",
    "mcu.unknown": "bilinmeyen MCU ailesi '{mcu}' (seçenekler: {options})",

    # UART
    "uart.help": (
        "UART baud hızı kaydı ve hatası.\n\n"
        "--baud verilmezse yaygın hızların tablosu gösterilir.\n\n"
        "Örnekler:\n"
        "  elektro uart -c 16M -b 115200\n"
        "  elektro uart -c 16M\n"
        "  elektro uart -c 72M -b 921600 -m stm32"
    ),
    "uart.opt.baud": "Baud hızı",
    "uart.opt.oversample": "--mcu generic için örnekleme katı",
    "uart.col.baud": "Baud",
    "uart.col.mode": "Mod",
    "uart.col.register": "Kayıt",
    "uart.col.actual": "Gerçek",
    "uart.col.error": "Hata",
    "uart.impossible": "mümkün değil",
    "uart.note": "±%2'ye kadar hata genelde çalışır; güvenilirlik için ±%1'in altında tut.",

    # PWM
    "pwm.help": (
        "Bir frekans için timer/PWM ön bölücüsü ve periyot kaydı.\n\n"
        "Örnekler:\n"
        "  elektro pwm -c 16M -f 20k                 (AVR Timer1)\n"
        "  elektro pwm -c 16M -f 1k --bits 8\n"
        "  elektro pwm -c 72M -f 20k -m stm32 -d 25"
    ),
    "pwm.opt.freq": "PWM frekansı (Hz)",
    "pwm.opt.bits": "Timer genişliği, bit (8, 16, 32)",
    "pwm.opt.duty": "Görev oranı % (karşılaştırma değerini hesaplar)",
    "pwm.bad": "saat ve frekans pozitif olmalı; bit 8, 10, 16 ya da 32 olmalı",
    "pwm.impossible": "bu frekans bu saat/timer ile üretilemez",
    "pwm.prescaler": "Ön bölücü",
    "pwm.actual": "Gerçek frekans",
    "pwm.error": "Hata",
    "pwm.resolution": "Çözünürlük",
    "pwm.steps": "adım",
    "pwm.compare": "{duty} için karşılaştırma değeri",
    "pwm.low_res": "Çözünürlük 8 bitin altında; frekansı düşür ya da saati yükselt.",

    # ADC
    "adc.help": (
        "ADC/DAC: LSB değeri, gerilim ↔ kod dönüşümü, ideal SNR.\n\n"
        "V = kod · Vref / 2ᴺ\n\n"
        "Örnekler:\n"
        "  elektro adc -b 12 --vref 3.3 --code 2048\n"
        "  elektro adc -b 10 --vref 5 --volt 1.2"
    ),
    "adc.opt.bits": "Çözünürlük (bit)",
    "adc.opt.vref": "Referans gerilimi (V)",
    "adc.opt.code": "Dijital kod → gerilim",
    "adc.opt.volt": "Gerilim → dijital kod",
    "adc.steps": "Adım",
    "adc.snr": "İdeal SNR",
    "adc.voltage_of": "{code} kodunun gerilimi",
    "adc.code_of": "{volt} için kod",
    "adc.code_range": "kod 0 ile {max} arasında olmalı",
    "adc.clipped": "Gerilim 0 … Vref dışında; kod kırpıldı.",
    "adc.note": "Bazı datasheet'ler bölen olarak 2ᴺ − 1 kullanır; fark 1 LSB'dir.",

    # I2C
    "i2c.help": (
        "Hat kapasitansı ve hıza göre I²C pull-up direnci aralığı.\n\n"
        "Rmin = (Vdd − 0.4 V) / Iol     Rmax = tr / (0.8473 · Cb)\n\n"
        "Örnekler:\n"
        "  elektro i2c --cb 200p\n"
        "  elektro i2c --vdd 5 --cb 100p -s 100k"
    ),
    "i2c.opt.vdd": "Pull-up besleme gerilimi (V)",
    "i2c.opt.cb": "Toplam hat kapasitansı (F), örn: 200p (cihaz başına ≈10 pF + kablo)",
    "i2c.opt.speed": "Hat hızı: 100k, 400k ya da 1M",
    "i2c.bad_speed": "hız 100k, 400k ya da 1M olmalı",
    "i2c.cb_limit": "I²C standardı en fazla 400 pF hat kapasitansına izin verir.",
    "i2c.impossible": "uygun direnç yok: bu hız için hat kapasitansı çok yüksek",
    "i2c.suggested": "Önerilen (E12)",
    "i2c.note": "Küçük R = daha hızlı kenarlar ama daha çok akım; Rmin ile Rmax arasında kal.",

    # CRC
    "crc.help": (
        "Bir bayt dizisinin CRC'si ve basit checksum'ları.\n\n"
        "Örnekler:\n"
        "  elektro crc \"01 03 00 00 00 0A\"\n"
        "  elektro crc 0x31323334 -a modbus\n"
        "  elektro crc \"123456789\" --text"
    ),
    "crc.arg": "Hex bayt olarak veri (\"01 03 0A\", 0x01030A) ya da --text ile metin",
    "crc.opt.text": "Veriyi metin olarak al (UTF-8)",
    "crc.opt.algo": "Sadece bu algoritma (örn: modbus, crc-32)",
    "crc.bad_hex": "geçersiz hex veri (iki haneli hex çiftleri kullan, örn: \"01 03 0A\")",
    "crc.unknown": "bilinmeyen algoritma '{algo}' (seçenekler: {options})",
    "crc.title": "{n} baytın CRC'si",
    "crc.col.algo": "Algoritma",
    "crc.col.bytes": "Baytlar (gönderim sırası)",

    # hesap makinesi
    "calc.help": (
        "Mühendislik gösterimini ve birimleri anlayan hesap makinesi.\n\n"
        "Operatörler: + − * / ^ ( )   Fonksiyonlar: sqrt log ln exp sin cos tan db dbp par\n"
        "Sabitler: pi e c.  par(a, b, …) = paralel eşdeğer.\n\n"
        "Örnekler:\n"
        "  elektro calc \"12V / (4k7 + 1k)\"\n"
        "  elektro calc \"1 / (2*pi*sqrt(10u * 100n))\" -u Hz\n"
        "  elektro calc \"par(1k, 2k2, 4k7)\" -u Ω\n"
        "  elektro calc \"db(3.3 / 0.1)\""
    ),
    "calc.arg": "İfade (kabukta tırnak içinde yaz)",
    "calc.opt.unit": "Sonuçla gösterilecek birim (V, A, Ω, Hz …)",
    "calc.syntax": "ifade anlaşılamadı",
    "calc.unknown_name": "bilinmeyen ad '{name}'",
    "calc.unsupported": "ifadede desteklenmeyen öğe",
    "calc.div_zero": "sıfıra bölme",
    "calc.complex": "sonuç karmaşık sayı",

    # birim
    "unit.help": (
        "Günlük elektronik işleri için birim dönüştürücü.\n\n"
        "Sıcaklık: c f k · Uzunluk: m cm mm um in mil ft · dB: db pratio vratio\n"
        "Kablo: awg mm2 · Bakır: oz · Açı: deg rad · Frekans: hz rpm\n\n"
        "Örnekler:\n"
        "  elektro unit 25 c\n"
        "  elektro unit 10 mil mm\n"
        "  elektro unit 6 db\n"
        "  elektro unit 22 awg"
    ),
    "unit.arg.value": "Değer",
    "unit.arg.src": "Kaynak birim ({units})",
    "unit.arg.dst": "Hedef birim (boşsa hepsi)",
    "unit.unknown": "bilinmeyen birim '{unit}' (seçenekler: {options})",
    "unit.no_path": "{src} → {dst} dönüşümü yok",
    "unit.below_zero": "mutlak sıfırın altında",
    "unit.power_ratio": "güç oranı",
    "unit.voltage_ratio": "gerilim oranı",
    "unit.period": "periyot (s)",

    # datasheet önbelleği
    "ds.opt.history": "Daha önce indirilen datasheet'leri listele (önbellek)",
    "ds.from_cache": "Önbellekte bulundu, indirmeye gerek yok.",
    "ds.cache_source": "önbellek",
    "ds.cache_empty": "Datasheet önbelleği boş.",
    "ds.cache_title": "İndirilen datasheet'ler",
    "ds.col.part": "Parça",
    "ds.col.size": "Boyut",
    "ds.col.date": "Tarih",
})
