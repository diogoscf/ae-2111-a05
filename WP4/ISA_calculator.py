from math import exp

print(
    f"        **** ISA calculator **** \n\n1. Calculate ISA for altitude in meters (press ENTER for default)\n2. Calculate ISA for altitude in feet\n3. Calculate ISA for altitude in FL"
)

stop = False
vui1 = False
vui2 = False
T_0 = 288.15
p_0 = 101325
rho_0 = 1.225
g_0 = 9.80665
R = 287.0
gamma = 1.4
C_offset = 273.15


def troposphere(h):
    t_1 = T_0 + -0.0065 * (h)
    p_1 = p_0 * (t_1 / T_0) ** (-g_0 / (-0.0065 * R))
    return t_1, p_1


def tropopause(h):
    p_2 = p_1 * exp((-g_0 / (R * t_1)) * (h - 11000))
    return p_2


def stratosphere(h):
    t_3 = t_1 + 0.0010 * (h - 20000)
    p_3 = p_2 * (t_3 / t_1) ** (-g_0 / (0.0010 * R))
    return t_3, p_3


def stratosphere2(h):
    t_4 = t_3 + 0.0028 * (h - 32000)
    p_4 = p_3 * (t_4 / t_3) ** (-g_0 / (0.0028 * R))
    return t_4, p_4


def stratopause(h):
    p_5 = p_4 * exp((-g_0 / (R * t_4)) * (h - 47000))
    return p_5


def mesosphere(h):
    t_6 = t_4 + -0.0028 * (h - 51000)
    p_6 = p_5 * (t_6 / t_4) ** (-g_0 / (-0.0028 * R))
    return t_6, p_6


def mesosphere2(h):
    t_7 = t_6 + -0.0020 * (h - 71000)
    p_7 = p_6 * (t_7 / t_6) ** (-g_0 / (-0.0020 * R))
    return t_7, p_7


def get_density(temp, pressure):
    rho = pressure / (R * temp)
    return rho


def local_speed_of_sound(temp):
    lss = (gamma * R * temp) ** 0.5
    return lss


def main():
    pass


while not stop:
    while not vui1:
        try:
            u = int(input("\n\nEnter your choice: ") or "1")
            if u == 1 or u == 2 or u == 3:
                vui1 = True
            else:
                print("Not a valid choice, try again")
        except ValueError:
            print("You made a typo. Enter 1, 2, or 3.")

    while not vui2:
        try:
            h = float(input("Enter altitude: "))
            if u == 1 or u == "":
                h = h
            elif u == 2:
                h = h * 0.3048
            else:
                h = h * 100 * 0.3048
            if 0 <= h <= 86000:
                vui2 = True
            else:
                print("Not a valid altitude, try between 0 and 86 000 m.")
        except ValueError:
            print("You made a typo. Try a real number.")

    if 0 <= h <= 11000.0:
        t_1, p_1 = troposphere(h)
        temp = round(t_1, 2)
        temp_C = round(t_1 - C_offset, 2)
        pressure = round(p_1, 1)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_1, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_1), 2)
    elif 11000.0 < h <= 20000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(h)
        temp = round(t_1, 2)
        temp_C = round(t_1 - C_offset, 2)
        pressure = round(p_2, 1)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_1, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_1), 2)
    elif 20000 < h <= 32000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(20000)
        t_3, p_3 = stratosphere(h)
        temp = round(t_3, 2)
        temp_C = round(t_3 - C_offset, 2)
        pressure = round(p_3, 2)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_3, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_3), 2)
    elif 32000 < h <= 47000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(20000)
        t_3, p_3 = stratosphere(32000)
        t_4, p_4 = stratosphere2(h)
        temp = round(t_4, 2)
        temp_C = round(t_4 - C_offset, 2)
        pressure = round(p_4, 2)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_4, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_4), 2)
    elif 47000 < h <= 51000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(20000)
        t_3, p_3 = stratosphere(32000)
        t_4, p_4 = stratosphere2(47000)
        p_5 = stratopause(h)
        temp = round(t_4, 2)
        temp_C = round(t_4 - C_offset, 2)
        pressure = round(p_5, 2)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_4, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_4), 2)
    elif 51000 < h <= 71000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(20000)
        t_3, p_3 = stratosphere(32000)
        t_4, p_4 = stratosphere2(47000)
        p_5 = stratopause(51000)
        t_6, p_6 = mesosphere(h)
        temp = round(t_6, 2)
        temp_C = round(t_6 - C_offset, 2)
        pressure = round(p_6, 2)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_6, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_6), 2)
    elif 71000 < h <= 86000:
        t_1, p_1 = troposphere(11000)
        p_2 = tropopause(20000)
        t_3, p_3 = stratosphere(32000)
        t_4, p_4 = stratosphere2(47000)
        p_5 = stratopause(51000)
        t_6, p_6 = mesosphere(71000)
        t_7, p_7 = mesosphere2(h)
        temp = round(t_7, 2)
        temp_C = round(t_7 - C_offset, 2)
        pressure = round(p_7, 2)
        pressure_per = round(pressure / p_0 * 100, 1)
        density = round(get_density(t_7, pressure), 4)
        density_per = round(density / rho_0 * 100, 1)
        speed_of_sound = round(local_speed_of_sound(t_7), 2)
    else:
        print("This is not a valid altitude")

    print(f"\nTemperature: \t\t{temp} K \t({temp_C} °C)")
    print(f"Pressure: \t\t{pressure} Pa \t({pressure_per}% SL)")
    print(f"Density: \t\t{density} kg/m3 \t({density_per}% SL)")
    print(f"Local speed of sound: \t{speed_of_sound} m/s\n")

    end = input("Do you want to run again? y/n: ")
    if end == "y":
        vui2 = False
    else:
        stop = True
