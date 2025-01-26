from random import randint
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)
        
        self.img = self.get_img()
        self.name = self.get_name()
        
        types = ["normal", "wizard", "fighter"]
        self.type = randint(0, 2)  # Случайный выбор из 3 типов
        self.type = types[self.type]

        self.hp = self.get_hp()
        self.attack_power = self.get_attack()
        self.level = 1
        
        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_default']  # Ссылка на изображение
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        else:
            return "Pikachu"

    # Метод для получения HP покемона через API
    def get_hp(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['stats'][0]['base_stat']  # HP находится в первом элементе stats
        else:
            return 35  # HP Пикачу

    # Метод для получения атаки покемона через API
    def get_attack(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['stats'][1]['base_stat']  # Атака находится во втором элементе stats
        else:
            return 55  # Атака Пикачу

    def level_up(self):
        """Увеличивает уровень покемона"""
        self.level += 1
        self.hp += 5
        self.attack += 3

    def attack(self, enemy):
        """Атака покемона в зависимости от его типа"""
        if self.type == "wizard":
            return self.attack_wizard(enemy)
        elif self.type == "fighter":
            return self.attack_fighter(enemy)
        else:
            return self.attack_normal(enemy)

    # Атака для обычного покемона
    def attack_normal(self, enemy):
        if enemy.hp > self.attack_power:
            enemy.hp -= self.attack_power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}: {enemy.name} потерял {self.attack_power} HP."
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! {enemy.name} побежден."

    # Атака для волшебника
    def attack_wizard(self, enemy):
        total_damage = self.attack_power + self.magic_power
        if enemy.hp > total_damage:
            enemy.hp -= total_damage
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}: {enemy.name} потерял {total_damage} HP благодаря магии."
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! {enemy.name} побежден магией."

    # Атака для бойца
    def attack_fighter(self, enemy):
        super_boost = randint(5, 15)
        self.attack_power += super_boost
        result = self.attack_normal(enemy)
        self.attack_power -= super_boost
        return result + f"\nБоец применил супер-атаку силой: {super_boost}"

    # Метод класса для получения информации
    def info(self):
        return (f"Имя твоего покемона: {self.name}\n"
                f"HP: {self.hp}\n"
                f"Атака: {self.attack_power}\n"
                f"Уровень: {self.level}\n"
                f"Тип покемона: {self.type}")

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

# Наследник Wizard
class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.magic_power = randint(15, 25)  # Магическая сила

    def attack(self, enemy):
        total_damage = self.attack_power + self.magic_power
        if enemy.hp > total_damage:
            enemy.hp -= total_damage
            return (f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}: "
                    f"{enemy.name} потерял {total_damage} HP благодаря магии.")
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! {enemy.name} побежден магией."

# Наследник Fighter
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.critical_chance = randint(1, 5)  # Шанс критического удара (20%)

    def attack(self, enemy):
        super_boost = randint(5, 15)
        self.attack_power += super_boost
        result = super().attack(enemy)
        self.attack_power -= super_boost
        return result + f"\nБоец применил супер-атаку силой: {super_boost} "

