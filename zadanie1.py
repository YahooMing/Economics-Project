def r_r(r, r_i): 
    """Wzór na realną stopę procentową."""
    r_r = (1 + r) / (1 + r_i) - 1
    return r_r

def pva_n(pmt, r, n): 
    """Wzór na pva_n"""
    czynnik = (1 - 1 / (1 + r) ** n) / r
    ret = pmt * czynnik
    return ret

def pmt(fva_n, r, n):
    """Wzór na pmt."""
    mianownik = (1 + r)**(n + 1) - (1 + r)
    ret = fva_n * r / mianownik
    return ret

wyplata = 2000

# scenariusze stóp procentowych
scenariusz1 = r_r(0.04, 0.045)  # stopa nominalna 4%, inflacja 4,5%
scenariusz2 = r_r(0.02, 0.04) # stopa nominalna 2%, inflacja 4%
scenariusz3 = r_r(0.04, 0.02) # stopa nominalna 4%, inflacja 2%

# okres wypłat: 300 miesięcy (25 lat)
pv_opt = pva_n(wyplata, scenariusz1 / 12, 300)
pv_umiark = pva_n(wyplata, scenariusz2 / 12, 300)
pv_pesym = pva_n(wyplata, scenariusz3 / 12, 300)

# okres akumulacji: 480 miesięcy (40 lat)
rata_opt = pmt(pv_opt, scenariusz1 / 12, 480)
rata_umiark = pmt(pv_umiark, scenariusz2 / 12, 480)
rata_pesym = pmt(pv_pesym, scenariusz3 / 12, 480)

print("\n======Scenariusz 1======")
print(f"Stopa realna : {round(scenariusz1 * 100, 2)} %")
print(f"Wartość bieżąca : {pv_opt:.2f}")
print(f"Wymagana rata : {rata_opt:.2f} \n")

print("======Scenariusz 2======")
print(f"Stopa realna: {round(scenariusz2 * 100, 2)} %")
print(f"Wartość bieżąca: {pv_umiark:.2f}")
print(f"Wymagana rata: {rata_umiark:.2f} \n")

print("======Scenariusz 3======")
print(f"Stopa realna: {round(scenariusz3 * 100, 2)} %")
print(f"Wartość bieżąca: {pv_pesym:.2f}")
print(f"Wymagana rata: {rata_pesym:.2f} \n")




