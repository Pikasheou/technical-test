class Tank:
    def __init__(self, name, armor, armor_penetration, armor_type):
        self.name = name.lower().replace(' ', '-')
        self.armor = armor
        self.armor_penetration = armor_penetration
        self.armor_type = armor_type
        if not (armor_type == 'chobham' or armor_type == 'composite' or armor_type == 'ceramic'):
            raise Exception('Invalid armor type %s' % (armor_type))

    def set_name(self, name):
        self.name = name

    def vulnerable(self, tank):
        real_armor = self.armor
        if self.armor_type == 'chobham':
            real_armor += 100
        else:
            real_armor += 50
        return real_armor <= tank.armor_penetration

    def __repr__(self):
        return self.name


def swap_armor(tank_1, tank_2):
    tank_1.armor, tank_2.armor = tank_2.armor, tank_1.armor

tank1_armor = 600
tank2_armor = 620

m1_1 = Tank('tank-1', tank1_armor, 670, 'chobham')
m1_2 = Tank('tank-2',tank2_armor, 670, 'chobham')
if m1_1.vulnerable(m1_1):
    print('Vulnerable to self')

swap_armor(m1_1, m1_2)
if m1_1.armor != tank2_armor or m1_2.armor != tank1_armor:
    print('The armor swap does not work')

tanks = []
for i in range(5):
    tanks.append(Tank('tank{}_small'.format(i), 400 + 60 * i, 400, 'composite'))

def test_any_tank_safe(shooter, test_vehicles=[]):
    for tank in test_vehicles:
        if not tank.vulnerable(shooter):
            print("The tank {} is safe".format(tank))
            return
    print("No tank is safe")

test_any_tank_safe(m1_1, tanks)