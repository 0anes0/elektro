<div align="center">
  <h1>⚡ ELEKTRO</h1>
  <p><i>Terminal tabanlı Elektrik-Elektronik Mühendisliği aracı</i></p>

  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![License](https://img.shields.io/badge/license-GPLv3-green.svg)
  ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)
  [![test](https://github.com/0anes0/elektro/actions/workflows/test.yml/badge.svg)](https://github.com/0anes0/elektro/actions/workflows/test.yml)
</div>

---

**Elektro**; Ohm kanunu, direnç renk kodları, filtre tasarımı, RF link bütçesi, 555 zamanlayıcı
gibi günlük elektronik hesaplarını terminalden hızlıca yapmanı ve komponent datasheet'lerini tek
komutla indirmeni sağlar.

Tüm değerler mühendislik gösterimiyle yazılabilir: `4k7`, `100n`, `2.2u`, `10M`, `1meg`, `1R5`, `100nF`, `1kΩ`

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

## 🚀 Kullanım

`elektro` yazınca komut menüsü, `elektro KOMUT --help` ile ayrıntı, `elektro helpall` ile
tüm kılavuz açılır.

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
```

### Pasif elemanlar

```bash
elektro series 1k 2k2 470
elektro parallel 10u 22u --cap
elektro divider --vin 12 --r1 10k --r2 4k7
elektro divider --vin 5 --vout 3.3           # en iyi E24 R1/R2 çiftleri
elektro led --vs 12 --vf 3.1 -i 15m -n 3     # LED ön direnci + güç sınıfı
elektro eseries 4k8                          # en yakın standart değerler (E3-E192)
elektro cap 104                              # kondansatör kodu ↔ değer
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
```

### RF

Frekans için yalın sayı **MHz**, mesafe için yalın sayı **km** kabul edilir (`2.4G`, `800m` de olur).

```bash
elektro rf fspl -f 868 -d 5
elektro rf link -f 868 -d 10 --tx 14 --sens -137   # link marjı ve maks. menzil
elektro rf wave -f 433.92                          # dalga boyu, anten boyları
elektro rf convert 14 dbm w
elektro rf convert 1.5 vswr                        # |Γ|, return loss, uyumsuzluk kaybı
```

### Datasheet indirici

```bash
elektro datasheet lm358
elektro datasheet ams1117 --open       # indir ve aç
elektro datasheet esp32 --list         # indirmeden adayları göster
elektro datasheet 2n2222 -o transistor.pdf
```

Sırasıyla üretici sitelerine (TI, Espressif, onsemi, Diodes, Nexperia), LCSC/JLCPCB parça
veritabanına ve DuckDuckGo'ya bakar. İnen dosyanın gerçekten PDF olduğu doğrulanır; hiçbir
kaynak çalışmazsa elle arama bağlantıları verilir.

## 🧪 Geliştirme

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## 📄 Lisans

[GPLv3](LICENSE) © Ahmet Enes KAYMAK
