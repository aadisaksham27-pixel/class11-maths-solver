"""Standalone school physics calculation functions used by app.py."""
import math

def _nz(v, name):
    v=float(v)
    if v == 0: raise ValueError(f"{name} cannot be zero.")
    return v

def speed(distance,time): return float(distance)/_nz(time,"Time")
def velocity(displacement,time): return float(displacement)/_nz(time,"Time")
def acceleration(change_in_velocity,time): return float(change_in_velocity)/_nz(time,"Time")
def final_velocity(initial_velocity,acceleration_value,time): return float(initial_velocity)+float(acceleration_value)*float(time)
def displacement(initial_velocity,time,acceleration_value): return float(initial_velocity)*float(time)+0.5*float(acceleration_value)*float(time)**2
def final_velocity_squared(initial_velocity,acceleration_value,displacement_value): return math.sqrt(float(initial_velocity)**2+2*float(acceleration_value)*float(displacement_value))
def average_velocity(initial_velocity,final_velocity_value): return (float(initial_velocity)+float(final_velocity_value))/2
def force(mass,acceleration_value): return float(mass)*float(acceleration_value)
def mass_from_force(force_value,acceleration_value): return float(force_value)/_nz(acceleration_value,"Acceleration")
def acceleration_from_force(force_value,mass): return float(force_value)/_nz(mass,"Mass")
def weight(mass,gravity=9.8): return float(mass)*float(gravity)
def normal_force(mass,gravity=9.8): return float(mass)*float(gravity)
def work(force_value,displacement_value): return float(force_value)*float(displacement_value)
def work_at_angle(force_value,displacement_value,angle): return float(force_value)*float(displacement_value)*math.cos(math.radians(float(angle)))
def kinetic_energy(mass,velocity_value): return 0.5*float(mass)*float(velocity_value)**2
def potential_energy(mass,gravity,height): return float(mass)*float(gravity)*float(height)
def mechanical_energy(kinetic_energy_value,potential_energy_value): return float(kinetic_energy_value)+float(potential_energy_value)
def power(work_value,time): return float(work_value)/_nz(time,"Time")
def power_from_force(force_value,velocity_value): return float(force_value)*float(velocity_value)
def momentum(mass,velocity_value): return float(mass)*float(velocity_value)
def velocity_from_momentum(momentum_value,mass): return float(momentum_value)/_nz(mass,"Mass")
def impulse(force_value,time): return float(force_value)*float(time)
def change_in_momentum(final_momentum,initial_momentum): return float(final_momentum)-float(initial_momentum)
def total_momentum(mass1,velocity1,mass2,velocity2): return float(mass1)*float(velocity1)+float(mass2)*float(velocity2)
def final_velocity_after_sticking(mass1,velocity1,mass2,velocity2): return total_momentum(mass1,velocity1,mass2,velocity2)/(float(mass1)+float(mass2))
def gravitational_force(mass1,mass2,distance): return 6.67430e-11*float(mass1)*float(mass2)/float(distance)**2
def gravitational_acceleration(mass,distance): return 6.67430e-11*float(mass)/float(distance)**2
def escape_velocity(mass,radius): return math.sqrt(2*6.67430e-11*float(mass)/float(radius))
def pressure(force_value,area): return float(force_value)/_nz(area,"Area")
def force_from_pressure(pressure_value,area): return float(pressure_value)*float(area)
def area_from_pressure(force_value,pressure_value): return float(force_value)/_nz(pressure_value,"Pressure")
def density(mass,volume): return float(mass)/_nz(volume,"Volume")
def mass_from_density(density_value,volume): return float(density_value)*float(volume)
def volume_from_density(mass,density_value): return float(mass)/_nz(density_value,"Density")
def liquid_pressure(density_value,gravity,depth): return float(density_value)*float(gravity)*float(depth)
def buoyant_force(density_value,gravity,volume): return float(density_value)*float(gravity)*float(volume)
def centripetal_force(mass,velocity_value,radius): return float(mass)*float(velocity_value)**2/_nz(radius,"Radius")
def centripetal_acceleration(velocity_value,radius): return float(velocity_value)**2/_nz(radius,"Radius")
def angular_velocity(angle,time): return float(angle)/_nz(time,"Time")
def linear_velocity_from_angular(angular_velocity_value,radius): return float(angular_velocity_value)*float(radius)
def heat_energy(mass,specific_heat,temperature_change_value): return float(mass)*float(specific_heat)*float(temperature_change_value)
def temperature_change(heat,mass,specific_heat): return float(heat)/(float(mass)*_nz(specific_heat,"Specific heat"))
def specific_heat_from_heat(heat,mass,temperature_change_value): return float(heat)/(float(mass)*_nz(temperature_change_value,"Temperature change"))
def latent_heat_energy(mass,latent_heat): return float(mass)*float(latent_heat)
def wave_speed(frequency,wavelength): return float(frequency)*float(wavelength)
def wavelength_from_speed(wave_speed_value,frequency): return float(wave_speed_value)/_nz(frequency,"Frequency")
def frequency_from_speed(wave_speed_value,wavelength): return float(wave_speed_value)/_nz(wavelength,"Wavelength")
def frequency_from_period(period): return 1/_nz(period,"Period")
def period_from_frequency(frequency): return 1/_nz(frequency,"Frequency")
def ohms_law(current=None,resistance=None,voltage=None):
    supplied=sum(v is not None for v in (current,resistance,voltage))
    if supplied < 2: raise ValueError("Provide any two of voltage, current, and resistance.")
    if voltage is None: return float(current)*float(resistance)
    if current is None: return float(voltage)/_nz(resistance,"Resistance")
    if resistance is None: return float(voltage)/_nz(current,"Current")
    return float(voltage)
def electrical_power(voltage,current): return float(voltage)*float(current)
def electrical_power_from_resistance(current,resistance): return float(current)**2*float(resistance)
def electrical_power_from_voltage(voltage,resistance): return float(voltage)**2/_nz(resistance,"Resistance")
def electrical_energy(power_value,time): return float(power_value)*float(time)
def resistance_series(*resistances): return sum(float(x) for x in resistances)
def resistance_parallel(*resistances):
    vals=[float(x) for x in resistances]
    if any(v==0 for v in vals): return 0.0
    return 1/sum(1/v for v in vals)
def current_from_charge(charge,time): return float(charge)/_nz(time,"Time")
def charge_from_current(current,time): return float(current)*float(time)
def capacitance(charge,voltage): return float(charge)/_nz(voltage,"Voltage")
def capacitor_energy(capacitance_value,voltage): return 0.5*float(capacitance_value)*float(voltage)**2
def kmh_to_ms(speed_kmh): return float(speed_kmh)/3.6
def ms_to_kmh(speed_ms): return float(speed_ms)*3.6
def celsius_to_kelvin(celsius): return float(celsius)+273.15
def kelvin_to_celsius(kelvin): return float(kelvin)-273.15
def celsius_to_fahrenheit(celsius): return float(celsius)*9/5+32
def fahrenheit_to_celsius(fahrenheit): return (float(fahrenheit)-32)*5/9
