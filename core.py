import sys
from PyQt5.QtWidgets import QApplication
from GUI import *
from Classes import *
from fighting_system import *
from mode_select import *

game = QApplication(sys.argv)
app = App()


def game_start():
    """ Hide start button and add some another """
    app.label.setText('Now the Game begins!\n\n')
    global player
    player = 0
    player = Player()
    app.startbtn.hide()
    app.grid.addWidget(app.invbtn, 3, 1)
    app.invbtn.show()
    main_mode(app)


def load_clicked():
    try:
        with open('save.txt', 'r') as f:
            pre_load = []
            for x in f.readline().split(','):
                pre_load.append(int(x))

            global player
            player = Player()
            player.exp = pre_load[0]
            player.lvl_up()

            app.startbtn.hide()
            app.loadbtn.hide()
            app.grid.addWidget(app.invbtn, 3, 1)
            app.label.setText('Load successful!\n')
            app.invbtn.show()

            main_mode(app)

    except FileNotFoundError:
        app.label.setText('There is no saves!')
    except (IndexError, ValueError):
        app.label.setText('Save corrupted!')


def save_clicked():
    with open('save.txt', 'w') as f:
        f.write('%s,%s' % (player.wpninventory, player.exp))


def find_clicked():
    player.find_opponent()
    fight_mode(app)
    app.label.setText('Your opponent is %s\n\n' % (player.opponent.name))


def inv_clicked():
    app.label.setText('You weapon is %s\n' % (player.weapon[0]))
    app.label.setText(app.label.text() + 'You armor is %s\n\n' % (player.armor[0]))
    for x in player.wpninventory:
        app.wpnbox.addItem(x[0])
    for x in player.armorinventory:
        app.armorbox.addItem(x[0])
    inv_mode(app)


def change_armor():
    for x in player.armorinventory:
        if x[0] == app.armorbox.currentText():
            player.armor = x
            player.dodge = player.armor[2]
            break
    app.label.setText(app.label.text() + 'You armor is %s\n\n' % (player.armor[0]))


def change_weapon():
    for x in player.wpninventory:
        if x[0] == app.wpnbox.currentText():
            player.weapon = x
            player.crit = player.weapon[2]
            break
    app.label.setText(app.label.text() + 'You weapon is %s\n\n' % (player.weapon[0]))


def exit_inv():
    if player.opponent:
        fight_mode(app)
        app.invbtn.show()
    else:
        main_mode(app)
        app.invbtn.show()


def atk_clicked():
    startlvl = player.lvl
    app.label.setText(app.label.text() + attack(player))
    if pobeditel(player) != 'nothing' and pobeditel(player):
        main_mode(app)
        player.health = player.starthealth
        player.exp += 1
        player.opponent = ''
        player.lvl_up()
        if player.lvl > startlvl:
            app.label.setText(app.label.text() + 'Level up! Your lvl is now %s\n' % player.lvl)
        app.label.setText(app.label.text() + '\nCongratulations! You win!\nHealth restored\nExp +1\n\n')
    elif pobeditel(player) == 'nothing':
        pass
    else:
        dead_mode(app)


def esc_clicked():
    if pobeg(player):
        app.label.setText(app.label.text() + 'You escaped c:\n\n')
        main_mode(app)
    else:
        app.label.setText(app.label.text() +
                          'Escape failed :c\nYou get %s damage\n\n' % player.opponent.attack)
        if player.health < 1:
            dead_mode(app)


def sr_clicked():
    app.label.setText('You found %s\n' % (player.search_weapon()))


def map_clicked():
    app.label.setText('Your location is %s\n\n' % player.location[0])
    for loc in locations:
        app.mapbox.addItem(loc[0])
    map_mode(app)


def change_loc():
    for loc in locations:
        if app.mapbox.currentText() == loc[0]:
            player.location = loc
            break
    app.label.setText(app.label.text() + 'Your location is %s\n\n' % player.location[0])


def hide_map():
    main_mode(app)


app.startbtn.clicked.connect(game_start)
app.loadbtn.clicked.connect(load_clicked)

app.fndbtn.clicked.connect(find_clicked)
app.srbtn.clicked.connect(sr_clicked)
app.savebtn.clicked.connect(save_clicked)
app.invbtn.clicked.connect(inv_clicked)

app.escbtn.clicked.connect(esc_clicked)
app.atkbtn.clicked.connect(atk_clicked)

app.extinvbtn.clicked.connect(exit_inv)
app.cngwpnbtn.clicked.connect(change_weapon)
app.cngarmorbtn.clicked.connect(change_armor)

app.mapbtn.clicked.connect(map_clicked)
app.cnglocbtn.clicked.connect(change_loc)
app.extmapbtn.clicked.connect(hide_map)

sys.exit(game.exec_())
