<div align="center">
  <h1>⚡ ELEKTRO</h1>
  <p><i>Terminal tabanlı Elektrik-Elektronik Mühendisliği aracı</i></p>

  [English](https://github.com/0anes0/elektro/blob/main/README.md) · **Türkçe**

  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![License](https://img.shields.io/badge/license-GPLv3-green.svg)
  ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)
  ![Languages](https://img.shields.io/badge/dil-EN%20%7C%20TR%20%7C%20DE%20%7C%20RU-orange.svg)
  [![test](https://github.com/0anes0/elektro/actions/workflows/test.yml/badge.svg)](https://github.com/0anes0/elektro/actions/workflows/test.yml)
</div>

---

**Elektro**; Ohm kanunu, direnç renk kodları, filtre tasarımı, RF link bütçesi, 555 zamanlayıcı
gibi günlük elektronik hesaplarını terminalden hızlıca yapmanı ve komponent datasheet'lerini tek
komutla indirmeni sağlar.

Tüm değerler mühendislik gösterimiyle yazılabilir: `4k7`, `100n`, `2.2u`, `10M`, `1meg`, `1R5`, `100nF`, `1kΩ`

Arayüz **Türkçe, İngilizce, Almanca ve Rusça** kullanılabilir.

## 🛠️ Kurulum

```bash
curl -fsSL https://raw.githubusercontent.com/0anes0/elektro/main/install.sh | bash
```

Betik; `~/.local/share/elektro` altında ayrı bir sanal ortam kurar ve `elektro` komutunu
`~/.local/bin` içine bağlar. Sistem Python'una dokunmaz, pipx gerekmez. Daha önce pipx ile
kurduysan eski kurulumu kendisi kaldırır.

Gereksinim: **Python 3.9+** (Debian/Ubuntu'da ayrıca `python3-venv`).

<details>
<summary>Repo'dan kurulum, güncelleme, kaldırma</summary>

```bash
git clone https://github.com/0anes0/elektro.git
cd elektro
./install.sh                 # kur
elektro update               # GitHub'daki son sürüme güncelle
./install.sh --uninstall     # kaldır
```

Kabuk otomatik tamamlama (bash/zsh/fish): `elektro --install-completion`
</details>

## 🌍 Dil

Elektro varsayılan olarak sistem dilini (`LANG`) kullanır; desteklenmiyorsa İngilizceye geçer.

```bash
elektro language             # dilleri listele
elektro language tr          # Türkçeyi varsayılan olarak kaydet
elektro --lang de ohm -v 5 -r 1k   # tek seferlik
ELEKTRO_LANG=ru elektro      # ortam değişkeniyle
```

Öncelik sırası: `--lang` → `ELEKTRO_LANG` → kayıtlı ayar (`~/.config/elektro/config.json`) → sistem dili → İngilizce.

## 🚀 Kullanım

`elektro` yazınca komut menüsü, `elektro KOMUT --help` ile ayrıntı, `elektro helpall` ya da
`man elektro` ile tüm kılavuz açılır.

Her komut `--json` ile makine okunur çıktı verir: `elektro ohm -v 12 -r 1k --json`

### Rapor çıktısı

Sonuçları ödev, laboratuvar raporu veya not için tablo olarak al:

```bash
elektro ohm -v 12 -r 1k --md                 # Markdown tablo
elektro filter rc --r 1k --c 100n --latex    # LaTeX tabular
elektro cable -i 16 -l 25 --report lab.md    # lab.md dosyasının sonuna ekle (.tex → LaTeX)
elektro motor -p 7.5k --rpm 1450 --copy      # çıktıyı panoya kopyala
```

`--report` ile terminalde normal çıktı da görünür; her komut, çalıştırılan komut satırıyla birlikte
dosyaya eklenir. `--plot` ile kaydedilen grafikler Markdown raporuna resim olarak girer.

### Terminal arayüzü (TUI)

```bash
elektro tui
```

Soldaki ağaçtan (ya da `Ctrl+F` ile arayarak) bir komut seç; seçenekleri form olarak açılır, komut
satırı sen yazdıkça oluşur. `Enter` / `Ctrl+R` çalıştırır, sonuç alttaki panelde renkli görünür.
Komut satırına istediğin `elektro` komutunu doğrudan da yazabilirsin.

| Tuş | İş |
|---|---|
| `F2` / `F3` / `F4` | Hesaplar / Devre / Geçmiş sekmesi |
| `Ctrl+R` | Çalıştır |
| `Ctrl+F` | Komut ara |
| `Ctrl+L` | Çıktıyı temizle |
| `Ctrl+Q` | Çık |

**Geçmiş** sekmesinde bir satıra `Enter` basınca komut yeniden yüklenir.

### Devre editörü ve simülatör

`elektro tui devre.json` ya da arayüzde `F3`: klavyeyle şema çiz, simüle et, sonucu grafikte gör.
Simülatör elektro'nun kendi çözücüsüdür (düğüm analizi, ek kurulum gerektirmez).

```
     A   B   C   D   E   F
  1  ·   ·   ·   ·   ·   ·
          5V        454.5mV
  2  ·   ●─[R1 10k]──●   ·
         +           │
  3  [V1 5V]     [R2 1k]
         │           │
  4  ·   ●───────────●   ·
       [GND]
```

| Tuş | İş |
|---|---|
| `r` `c` `l` `v` `i` `g` | direnç, kondansatör, bobin, gerilim/akım kaynağı, toprak koy |
| `d` `q` `f` `u` | diyot, BJT, MOSFET, op-amp koy |
| `n` | düğüm etiketi (ör. `VCC`, `OUT`): aynı adlı noktalar kablosuz bağlıdır, probe'da `V(OUT)` |
| `Ctrl+E` | hazır örnek devreler (bölücü, filtreler, doğrultucular, transistör ve op-amp devreleri) |
| `w` | kablo: imleci gezdir, `Enter` köşe koyar, `Esc` bitirir |
| `e` / `Enter` | değeri değiştir (`4k7`, `100n`; kaynakta `SINE(0 1 1k)`, `PULSE(0 5 0 1u 1u 0.5m 1m)`, `AC 1`) |
| `Ctrl+R` · `m` · `x` · `Ctrl+Z` | döndür · taşı · sil · geri al |
| `p` | probe: noktada gerilim `V(C3)`, elemanda akım `I(R1)` |
| `a` … `a` | iki düğüm arası akım `I(C1,C10)` |
| `o` … `o` | iki nokta arası eşdeğer direnç `R(A1,D1)` (yalnız dirençli devrelerde de çalışır) |
| `P` | probe yaz: `V(C3,E7)`, `P(R1)`, transistör ucu `I(Q1.B)` … |
| `s` | analiz: `.tran 10m`, `.ac dec 100 10 100k`, `.dc V1 0 5 0.1` (komut satırı + form) |
| `F5` | çöz; sonra her değişiklikte kendiliğinden yeniden çözülür |
| `F6` · `Tab` | grafik boyutu · grafiğe geç (`←`/`→` imleç, `m` genlik/faz) |
| `Ctrl+S` · `Ctrl+O` · `Ctrl+N` | kaydet · aç · yeni |

Yarı iletkenlerde değer, model adıdır (değiştirmek için `e`); ardından parametre de yazılabilir:

| Eleman | Modeller | Örnek |
|---|---|---|
| Diyot | 1N4148, 1N4007, 1N5819, LED, LED-GREEN, LED-BLUE, LED-WHITE, BZX3V3, BZX5V1, BZX12 | `1N4148`, `IS=1e-14 N=1.8` |
| BJT | 2N2222, 2N3904, BC547 (NPN) · 2N3906, BC557 (PNP) | `2N2222 BF=150` |
| MOSFET | 2N7000, IRFZ44N (N) · BS250, IRF9540 (P) | `NMOS VTO=2 KP=0.5` |
| Op-amp | ideal, LM358, LM741, TL072 + çıkış sınırı | `TL072 ±15`, `LM358 0..5` |

Doğrusal olmayan elemanlar Newton-Raphson yöntemiyle çözülür (diyot: Shockley + kırılma, BJT:
Ebers-Moll + Early, MOSFET: seviye-1, op-amp: GBW'li tek kutup + ray sınırı). Jonksiyon
kapasiteleri modellenmez; sonuçlar ön tasarım içindir.

Düğümler Excel hücreleri gibi adlandırılır (sol üst noktalarının adresi: `B2`, `E2`). Grafikte
probe'lar çizilir; hiç probe yoksa tüm düğüm gerilimleri. Aynı dosya terminalden de çözülür:

Örnekler ve SPICE netlist'leri de kullanılabilir. Bir `.cir` / `.sp` / `.net` dosyası açılınca
elemanlar ızgaraya dizilir ve düğüm etiketleriyle bağlanır; desteklenmeyen satırlar uyarıyla atlanır.

```bash
elektro examples                               # hazır örneklerin listesi
elektro examples rc_lowpass                    # rc_lowpass.json olarak kaydet
elektro tui devre.cir                          # SPICE netlist'ini şemaya aktar
elektro sim devre.cir                          # netlist'i doğrudan çöz
elektro sim devre.json                         # DC çalışma noktası + dosyadaki analiz
elektro sim devre.json -p "V(E2)" -p "I(B2,E2)"
elektro sim rc.json -a ".tran 5m" --plot rc.svg --csv rc.csv
elektro sim filtre.json -a ".ac dec 50 10 1meg" --plot bode.svg
elektro sim devre.json --spice > devre.cir     # SPICE netlist'i
```

### Etkileşimli mod, değişkenler, geçmiş

```bash
elektro shell                        # "elektro" yazmadan komut gir; Tab tamamlar, ↑ geri getirir
elektro set vin 12                   # bir değeri kaydet …
elektro ohm -v @vin -r 1k            # … her komutta @vin olarak kullan
elektro set rload 4k7 --local        # projeye özel (./.elektro.json)
elektro calc "vin / 2"               # calc'ta değişkenler adıyla da kullanılır
elektro vars                         # değişkenleri listele
elektro history                      # önceki hesaplar
elektro history --run 3              # birini tekrar çalıştır
```

### Temel

```bash
elektro ohm -v 12 -r 1k              # V, I, R, P'den herhangi ikisi
elektro ohm                          # soru sorarak (sihirbaz)

elektro resistor k s r a             # renk kodu → 1 kΩ ±%5  (3-6 bant)
elektro resistor sari mor siyah kahverengi kahverengi
elektro resistor encode 4k7          # değer → renk kodu
elektro resistor smd 01C             # SMD kodu (103, 4R7, 1002, EIA-96)
elektro resistor table               # renk tablosu

elektro 555 astable --r1 1k --r2 10k --c 10u
elektro 555 astable -f 1k -d 60 --c 10n      # frekanstan R1/R2 tasarla
elektro 555 mono --t 5 --c 100u

elektro logic convert 0xFF           # onlu/onaltılı/ikili/sekizli
elektro logic convert --bits 8 -- -5 # ikiye tümleyen
elektro logic truth xor
elektro logic expr "A & B | ~C"      # boolean ifade doğruluk tablosu
elektro logic simplify "A&B | A&~B"  # en sade SOP + Karnaugh haritası
elektro logic simplify -m 1,3,7,11,15 -d 0,2,5

elektro opamp noninv --gain 11       # standart Rf/Rg çiftleri
elektro opamp inv --rf 47k --rin 4k7 --vin 0.5 --gbw 1M
elektro opamp diff --gain 5

elektro switch bjt --ic 500m -v 3.3  # NPN anahtar için taban direnci
elektro switch mosfet -v 10 --qg 40n -f 100k   # kapı sürme ve kayıplar
elektro charge --r 10k --c 100u --v 5 --to 3.3 # RC dolma süresi + eğri
```

Direnç renkleri Türkçe kısa kodlarla (`s k r t sa y m mo g b a gu`), IEC kodlarıyla
(`bk bn rd og ye gn bu vt gy wh gd sr`) ya da dört dilden birinde adıyla (`kahverengi`, `brown`,
`braun`, `коричневый`) yazılabilir.

### Pasif elemanlar

```bash
elektro series 1k 2k2 470
elektro parallel 10u 22u --cap
elektro divider --vin 12 --r1 10k --r2 4k7
elektro divider --vin 5 --vout 3.3           # en iyi E24 R1/R2 çiftleri
elektro led --vs 12 --vf 3.1 -i 15m -n 3     # LED ön direnci + güç sınıfı
elektro eseries 4k8                          # en yakın standart değerler (E3-E192)
elektro cap 104                              # kondansatör kodu ↔ değer
elektro coil --l 1u --d 10                   # hava nüveli bobin sarım sayısı (Wheeler)
elektro crystal --cl 12p                     # kristal yük kondansatörleri
```

### Güç ve iletkenler

```bash
elektro regulator lm317 --vout 5             # ayarlı regülatör için R2
elektro regulator 7805 --vin 12 -i 500m      # lineer regülatörde harcanan güç
elektro battery 2000 -i 15m                  # batarya ömrü
elektro battery 1200 --active 45m --active-time 2 --sleep 20u --sleep-time 58
elektro thermal -p 5 --rth-jc 3 --ta 50      # gereken soğutucu
elektro wire --awg 22 -l 3 -i 2              # AWG ↔ mm², gerilim düşümü
elektro trace -i 3                           # PCB yol genişliği (IPC-2221)
elektro rectifier --vac 12 -i 1 --ripple 1   # köprü doğrultucu + filtre kondansatörü
elektro acpower --v 400 --p 15k --pf 0.82 --phases 3 --target-pf 0.95
elektro stardelta delta 10 20 30             # Δ → Y dönüşümü
```

### Tesisat ve makineler

```bash
elektro cable -i 16 -l 25                    # kablo kesiti: akım kapasitesi + gerilim düşümü
elektro cable -p 9k --phases 3 --pf 0.85 -l 40 --method C
elektro cable -i 120 --phases 3 -l 80 --material al --insulation xlpe --group 3
elektro breaker -i 14 --iz 21 --curve B --mm2 2.5 -l 30   # MCB seçimi, Zs, en büyük uzunluk
elektro breaker -i 40 --iz 50 --type fuse    # gG buşonlu sigorta
elektro shortcircuit --kva 630 --mm2 95 -l 50 --time 0.4  # Ik3, ip, Ik1, kesme kapasitesi
elektro transformer --v1 230 --v2 12 --va 50 # oran, akımlar, nüve kesiti, sarım, tel çapı
elektro motor -p 7.5k --rpm 1450             # akım, moment, kayma, kalkış akımı (Y-Δ)
```

Kablo kapasiteleri IEC 60364-5-52 tablolarındandır (A1, B1, C, D döşeme şekilleri; sıcaklık ve
gruplama düzeltmesiyle). Sonuçlar ön boyutlandırma içindir; proje için yönetmeliğe göre kontrol et.

### Filtreler

```bash
elektro filter rc --r 1k --c 100n            # fc + frekans yanıtı (genlik/faz)
elektro filter rc --fc 1k --c 10n            # iki değer ver, üçüncüsünü bulsun
elektro filter rc --r 10k --fc 50 --high
elektro filter rl --r 1k --l 10m
elektro filter lc --f 433.92M --c 10p
elektro filter rlc --r 10 --l 1m --c 100n
elektro filter notch --r 1k --l 1.013 --c 10u  # 50 Hz
elektro filter rc --r 1k --c 100n --plot bode.svg   # Bode grafiği kaydet
elektro charge --r 10k --c 100u --v 5 --plot charge.svg
```

### Sinyal

```bash
elektro wave sine --rms 230                  # tepe, ortalama, RMS, tepe/biçim faktörü
elektro wave pwm --vp 12 -d 25 -r 10         # PWM'in DC ve RMS değeri, yükteki güç
elektro wave square --vpp 5 --offset 2.5 --plot kare.svg
elektro fft osiloskop.csv                    # temel bileşen, harmonikler, THD, THD+N
elektro fft adc.txt --rate 48k --window flattop --plot spektrum.svg
```

`fft` osiloskop CSV'lerini (Rigol, Siglent, Tektronix), `;` ile ayrılmış ve virgüllü ondalık
dosyaları ve tek sütunlu ham verileri okur. Örnekleme hızı zaman sütunundan veya dosya
başlığından alınır; yoksa `--rate` ver.

Grafikler ek bir kütüphane gerektirmeden SVG olarak yazılır. `.png` / `.pdf` için matplotlib'i
elektro'nun ortamına kur: `~/.local/share/elektro/venv/bin/pip install matplotlib`.

### RF

Frekans için yalın sayı **MHz**, mesafe için yalın sayı **km** kabul edilir (`2.4G`, `800m` de olur).

```bash
elektro rf fspl -f 868 -d 5
elektro rf link -f 868 -d 10 --tx 14 --sens -137   # link marjı ve maks. menzil
elektro rf wave -f 433.92                          # dalga boyu, anten boyları
elektro rf convert 14 dbm w
elektro rf convert 1.5 vswr                        # |Γ|, return loss, uyumsuzluk kaybı
elektro rf lora --sf 9 -p 20                       # LoRa havada kalma süresi, hassasiyet
elektro rf fresnel -f 868 -d 10                    # Fresnel bölgesi / anten yüksekliği
elektro rf microstrip --z0 50 --h 1.6 --er 4.4     # 50 Ω yol genişliği
elektro rf coax lmr400 -f 2.4G -l 20m              # kablo kaybı
```

### Gömülü sistemler

```bash
elektro uart -c 16M -b 115200                # baud kaydı ve hata (avr/stm32)
elektro pwm -c 72M -f 20k -m stm32 -d 25     # ön bölücü, ARR, karşılaştırma değeri
elektro adc -b 12 --vref 3.3 --code 2048     # ADC kod ↔ gerilim
elektro i2c --cb 200p -s 400k                # I²C pull-up aralığı
elektro crc "01 03 00 00 00 0A"              # CRC-8/16/32, Modbus, checksum
```

### Araçlar

```bash
elektro calc "12V / (4k7 + 1k)"              # mühendislik gösterimli hesap makinesi
elektro calc "par(1k, 2k2, 4k7)" -u Ω
elektro calc "230∠0 / (10 + zl(100m, 50))" -u A        # karmaşık sayılar ve fazörler
elektro calc "100 + zl(10m, 1k) || zc(1u, 1k)" -u Ω -f 1k  # empedans → seri R + L/C
elektro unit 25 c                            # °C/°F/K, mil/mm, dB, AWG …
elektro pinout                               # bacak bağlantısı bilinen parçalar
elektro pinout ne555                         # entegre / transistör bacakları (çevrimdışı)
```

`calc` içinde `j` sanal birimdir (`3+4j`, `3+j4`), `10∠30` kutupsal gösterimdir (derece), `||`
paralel bağlamadır. Fonksiyonlar: `re im abs arg conj polar zl zc`.

### Datasheet indirici

```bash
elektro datasheet lm358
elektro datasheet ams1117 --open       # indir ve aç
elektro datasheet esp32 --list         # indirmeden adayları göster
elektro datasheet 2n2222 -o transistor.pdf
elektro datasheet --history            # daha önce indirilen (önbellekteki) datasheet'ler
```

Sırasıyla üretici sitelerine (TI, Espressif, onsemi, Diodes, Nexperia), LCSC/JLCPCB parça
veritabanına ve DuckDuckGo'ya bakar. İnen dosyanın gerçekten PDF olduğu doğrulanır; hiçbir
kaynak çalışmazsa elle arama bağlantıları verilir. İndirilenler `~/.cache/elektro/` altında
saklanır; aynı parça bir dahaki sefere anında gelir.

## 🧪 Geliştirme

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

Çeviriler `elektro/i18n/` klasöründe (`en.py` kaynak dil). Testler her dilde her anahtarın aynı
yer tutucularla bulunduğunu kontrol eder.

PyPI'ye yayın (paket adı `elektro-cli`): PyPI'de bu repo için bir *Trusted Publisher* tanımla
(workflow `publish.yml`, environment `pypi`), sonra `__version__` ile aynı etiketi gönder:
`git tag v0.4.0 && git push origin v0.4.0`.

## 📄 Lisans

[GPLv3](https://github.com/0anes0/elektro/blob/main/LICENSE) © Ahmet Enes KAYMAK
