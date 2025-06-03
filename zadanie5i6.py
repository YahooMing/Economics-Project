import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Wczytanie danych z plików CSV
df_cdr = pd.read_csv("cdr_w.csv", parse_dates=['Data'])
df_allegro = pd.read_csv("ale_w.csv", parse_dates=['Data'])

# Sortowanie i przygotowanie danych
for df in [df_cdr, df_allegro]:
    df.sort_values("Data", inplace=True)
    df.rename(columns={"Zamkniecie": "Close"}, inplace=True)
    df["Return"] = df["Close"].pct_change()
    df.dropna(inplace=True)

# Filtrowanie danych od 2024 roku i tworzenie kopii
df_cdr = df_cdr[df_cdr["Data"].dt.year >= 2024].copy()
df_allegro = df_allegro[df_allegro["Data"].dt.year >= 2024].copy()

# Funkcja analizy akcji
def analyze_stock(name, returns):
    avg = returns.mean()
    risk = returns.std()
    sharpe = avg / risk if risk else np.nan
    print(f"\n{name}:")
    print(f"Średnia tygodniowa stopa zwrotu: {avg:.2%}")
    print(f"Ryzyko (odchylenie standardowe): {risk:.2%}")
    print(f"Współczynnik Sharpe’a: {sharpe:.4f}")
    return avg, risk, sharpe

# Analiza spółek
r_cdr = analyze_stock("CD Projekt", df_cdr["Return"])
r_allegro = analyze_stock("Allegro", df_allegro["Return"])

# Skumulowane zwroty przy inwestycji początkowej 1000 zł
df_cdr["Cumulative"] = 1000 * (1 + df_cdr["Return"]).cumprod()
df_allegro["Cumulative"] = 1000 * (1 + df_allegro["Return"]).cumprod()

# Wykres: linia + punkty
plt.figure(figsize=(10, 6))

plt.plot(df_cdr["Data"], df_cdr["Cumulative"], label="CD Projekt", color='blue', linewidth=2)
plt.scatter(df_cdr["Data"], df_cdr["Cumulative"], color='blue', s=25)

plt.plot(df_allegro["Data"], df_allegro["Cumulative"], label="Allegro", color='green', linewidth=2)
plt.scatter(df_allegro["Data"], df_allegro["Cumulative"], color='green', s=25)

plt.title("Skumulowany zwrot z inwestycji od 2024 roku (1000 zł)")
plt.xlabel("Data")
plt.ylabel("Wartość inwestycji [zł]")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Łączenie danych po dacie i liczenie kowariancji
returns = pd.merge(
    df_cdr[["Data", "Return"]],
    df_allegro[["Data", "Return"]],
    on="Data",
    suffixes=("_cdr", "_allegro")
).dropna()

cov = returns[["Return_cdr", "Return_allegro"]].cov()

# Funkcja minimalizacji wariancji portfela
def port_var(weights):
    w1, w2 = weights[0], 1 - weights[0]
    return w1**2 * cov.iloc[0, 0] + w2**2 * cov.iloc[1, 1] + 2 * w1 * w2 * cov.iloc[0, 1]

# Optymalizacja wag portfela
res = minimize(port_var, x0=[0.5], bounds=[(0, 1)])
w_cdr_opt = res.x[0]
w_allegro_opt = 1 - w_cdr_opt
std_port = np.sqrt(res.fun)

# Wyniki optymalizacji
print(f"\nOptymalny portfel (minimalne ryzyko):")
print(f"- CD Projekt: {w_cdr_opt:.2%}")
print(f"- Allegro: {w_allegro_opt:.2%}")
print(f"- Odchylenie standardowe portfela: {std_port:.2%}")
