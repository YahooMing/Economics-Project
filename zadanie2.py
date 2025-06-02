from openpyxl import Workbook

# Parametry kredytu
kwota_kredytu = 600_000
okres_lat = 15
oprocentowanie_roczne = 0.04  # 4% rocznie

# Obliczenia pomocnicze
liczba_miesiecy = okres_lat * 12
oprocentowanie_miesieczne = oprocentowanie_roczne / 12

# Rata annuitetowa
wysokosc_raty = (kwota_kredytu * oprocentowanie_miesieczne * (1 + oprocentowanie_miesieczne) ** liczba_miesiecy) / \
                ((1 + oprocentowanie_miesieczne) ** liczba_miesiecy - 1)

# Inicjalizacja Excela
wb = Workbook()
arkusz = wb.active
arkusz.title = "Harmonogram spłaty"

# Nagłówki
naglowki = ["Miesiąc", "Rata całkowita", "Odsetki", "Kapitał", "Pozostałe saldo"]
arkusz.append(naglowki)

# Generowanie harmonogramu
pozostale_saldo = kwota_kredytu

for miesiac in range(1, liczba_miesiecy + 1):
    czesc_odsetkowa = pozostale_saldo * oprocentowanie_miesieczne
    czesc_kapitalowa = wysokosc_raty - czesc_odsetkowa
    pozostale_saldo -= czesc_kapitalowa

    arkusz.append([
        miesiac,
        round(wysokosc_raty, 2),
        round(czesc_odsetkowa, 2),
        round(czesc_kapitalowa, 2),
        round(max(pozostale_saldo, 0), 2)
    ])

# Zapis do pliku
wb.save("harmonogram_kredytu.xlsx")
