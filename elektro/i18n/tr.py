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
