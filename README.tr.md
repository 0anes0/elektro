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
elektro unit 25 c                            # °C/°F/K, mil/mm, dB, AWG …
```

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
