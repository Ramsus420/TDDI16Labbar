# Antal körningar per år
runs_per_year = 2 * 24 * 365

# Tider i sekunder per körning
brute_time_per_run = 6139.648
sort_time_per_run = 28.807

# Omvandla till timmar
brute_time_per_run_hours = brute_time_per_run / 3600
sort_time_per_run_hours = sort_time_per_run / 3600

# Total tid i timmar per år
brute_total_time_hours = brute_time_per_run_hours * runs_per_year
sort_total_time_hours = sort_time_per_run_hours * runs_per_year

# Energiförbrukning i kWh
idle_power_watts = 8
active_power_watts = 36
extra_power_watts = active_power_watts - idle_power_watts

# Energiförbrukning för brute-lösningen
brute_energy_kwh = (brute_total_time_hours * extra_power_watts / 1000) + (8760 - brute_total_time_hours) * idle_power_watts / 1000

# Energiförbrukning för sorteringslösningen
sort_energy_kwh = (sort_total_time_hours * extra_power_watts / 1000) + (8760 - sort_total_time_hours) * idle_power_watts / 1000

# Skillnad i energiförbrukning
energy_difference_kwh = brute_energy_kwh - sort_energy_kwh

print(f"Förbrukning av brute på ett år: {brute_energy_kwh:.2f} kWh")
print(f"Förbrukning av sortering på ett år: {sort_energy_kwh:.2f} kWh")
print(f"Skillnad: {energy_difference_kwh:.2f} kWh")