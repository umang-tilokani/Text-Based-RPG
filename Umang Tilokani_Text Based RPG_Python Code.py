from random import *


def main():
    pass


if __name__ == '__main__':
    main()


class Character:
    def __init__(self):
        self.name = ""
        self.health = 1
        self.health_max = 1

    def do_damage(self, enemy):
        damage = min(max(randint(0, self.health) - randint(0, enemy.health), 0), enemy.health)
        enemy.health = enemy.health - damage
        if damage == 0:
            print("%s evades %s's attack." % (enemy.name, self.name))
        else:
            print("%s hurts %s!" % (self.name, enemy.name))
        return enemy.health <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        self.name = 'Zombie'
        self.health = randint(1, player.health)


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.health = 10
        self.health_max = 10

    def quit(self):
        print(self.name, " is unable to get out of the maze, and dies of boredom.\nR.I.P. %s" % self.name)
        self.health = 0

    def help(self):
        print(list(Commands.keys()))

    def status(self):
        print("Player's health: %d/%d" % (self.health, self.health_max))

    def tired(self):
        print("%s feels tired." % self.name)
        self.health = max(1, self.health - 1)

    def rest(self):
        if self.state != 'normal':
            print("%s is facing death and can't rest now!" % self.name)
            self.enemy_attacks()
        else:
            print("%s rests." % self.name)
            if randint(0, 1):
                self.enemy = Enemy(self)
                print("%s is rudely awakened by a %s!" % (self.name, self.enemy.name))
                self.state = 'fight'
                self.enemy_attacks()
            else:
                if self.health < self.health_max:
                    self.health = self.health + 1
                else:
                    print("%s slept too much." % self.name)
                    self.health = self.health - 1

    def explore(self):
        if self.state != 'normal':
            print("%s is too busy right now to explore." % self.name)
            self.enemy_attacks()
        else:
            print("%s explores a twisty passage." % self.name)
            if randint(0, 1):
                self.enemy = Enemy(self)
                print("%s encounters a %s!" % (self.name, self.enemy.name))
                self.state = 'fight'
            else:
                if randint(0, 1):
                    self.tired()

    def flee(self):
        if self.state != 'fight':
            print("%s runs in circles for a while." % self.name)
            self.tired()
        else:
            if randint(1, self.health + 5) > randint(1, self.enemy.health):
                print("%s flees from the %s." % (self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
            else:
                print("%s couldn't escape from the %s!" % (self.name, self.enemy.name))
                self.enemy_attacks()

    def attack(self):
        if self.state != 'fight':
            print("%s swats the air, without notable results." % self.name)
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print("%s executes the %s!" % (self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
                if randint(0, self.health) < 10:
                    self.health = self.health + 1
                    self.health_max = self.health_max + 1
                    print("%s feels stronger!" % self.name)
            else:
                self.enemy_attacks()

    def enemy_attacks(self):
        if self.enemy.do_damage(self):
            print("%s was slaughtered by the %s!!!\nR.I.P." % (self.name, self.enemy.name))


Commands = {'quit': Player.quit, 'help': Player.help, 'status': Player.status, 'rest': Player.rest,
            'explore': Player.explore, 'flee': Player.flee, 'attack': Player.attack}


print('''
==============================================================
                     ROLE PLAYING GAME
==============================================================
  In this game, a player enters a Mystery Maze in search for 
 adventure. What type of adventure you ask? The player enters
 the maze in search of Zombies and to kill as many as he can!
==============================================================
                         COMMANDS:

1) 'explore' - To explore the Mystery Maze
2) 'attack' - To fight the Zombies
3) 'flee' - To run from the Zombies
4) 'rest' - To recharge the players health
5) 'status' - To check players health status
6) 'quit' - To quit the game

~ Remember to type 'help' incase you need it further in game ~
==============================================================
                      ALL THE BEST!!
==============================================================
                Game By - Umang Tilokani
==============================================================
''')


p = Player()
p.name = input("\nEnter your player's name: ")
print("\n", p.name, "enters a Mystery Maze.")


while p.health > 0:
    line = input(">")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in list(Commands.keys()):
            if args[0] == c[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print("%s doesn't understand the suggestion." % p.name)
