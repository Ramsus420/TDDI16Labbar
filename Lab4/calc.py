#Antal körningar per år
körningar_per_år = 2 * 24 * 365

# Tider i sekunder per körning
brute_tid_per_körning = 6139.648
sort_tid_per_körning = 28.807

# Omvandla till timmar
brute_tid_per_körning_timmar = brute_tid_per_körning / 3600
sort_tid_per_körning_timmar = sort_tid_per_körning / 3600

# Total tid i timmar per år
brute_total_tid_timmar = brute_tid_per_körning_timmar * körningar_per_år
sort_total_tid_timmar = sort_tid_per_körning_timmar * körningar_per_år

# Energiförbrukning i kWh
idle_effekt_watt = 8
aktiv_effekt_watt = 36
extra_effekt_watt = aktiv_effekt_watt - idle_effekt_watt

# Energiförbrukning för brute-lösningen
brute_energi_kwh = (brute_total_tid_timmar * extra_effekt_watt / 1000) + (8760 - brute_total_tid_timmar) * idle_effekt_watt / 1000

# Energiförbrukning för sorteringslösningen
sort_energi_kwh = (sort_total_tid_timmar * extra_effekt_watt / 1000) + (8760 - sort_total_tid_timmar) * idle_effekt_watt / 1000

# Skillnad i energiförbrukning
energi_skillnad_kwh = brute_energi_kwh - sort_energi_kwh

print(f"Förbrukning av brute på ett år: {brute_energi_kwh:.2f} kWh")
print(f"Förbrukning av sortering på ett år: {sort_energi_kwh:.2f} kWh")
print(f"Skillnad: {energi_skillnad_kwh:.2f} kWh")