from tkinter import *
import table, ball, bat

x_velocity = 10
y_velocity = 10
score_left = 0
score_right = 0
first_serve = True

window=Tk()
window.title("My Ping Pong")

my_table = table.Table(window, net_color="blue", vertical_net=True)

my_ball = ball.Ball(table=my_table, x_speed=x_velocity, y_speed=y_velocity,
                    width=24, height=24, color="red", x_start=288, y_start=188)

bat_L = bat.Bat(table=my_table, width=15, height=100, x_posn=20, y_posn=150, color="orange")
bat_R = bat.Bat(table=my_table, width=15, height=100, x_posn=575, y_posn=150, color="yellow")

def game_flow():
    global first_serve
    global score_left
    global score_right
    if(first_serve == True):
        my_ball.stop_ball()
        first_serve = False
    bat_L.detect_collision(my_ball)
    bat_R.detect_collision(my_ball)
    


    if(my_ball.x_posn <= 3):
        my_ball.stop_ball()
        my_ball.start_position()
        bat_L.start_position()
        bat_R.start_position()
        my_table.move_item(bat_L.rectangle, 20, 150, 35, 250)
        my_table.move_item(bat_R.rectangle, 575, 150, 590, 250)
        score_left = score_left + 1
        if(score_left >= 10):
            score_left = "W"
            score_right = "L"
        first_serve = True
        my_table.draw_score(score_left, score_right)
    if(my_ball.x_posn + my_ball.width >= my_table.width - 3):
        my_ball.stop_ball()
        my_ball.start_position()
        bat_L.start_position()
        bat_R.start_position()
        my_table.move_item(bat_L.rectangle, 20, 150, 35, 250)
        my_table.move_item(bat_R.rectangle, 575, 150, 590, 250)
        score_right = score_right + 1
        if(score_right >= 10):
            score_right = "W"
            score_left = "L"
        first_serve=True
        my_table.draw_score(score_left, score_right)

    my_ball.move_next()
    window.after(50, game_flow)

def restart_game(master):
    global score_left
    global score_right
    my_ball.start_ball(x_speed=x_velocity, y_speed=0)
    if(score_left == "W" or score_right == "L"):
        score_left = 0
        score_right = 0
    my_table.draw_score(score_left, score_right)

def reset_game(master):
    global score_left
    global score_right
    my_ball.stop_ball()
    my_ball.start_position()
    bat_L.start_position()
    bat_R.start_position()
    score_left = str(0)
    score_right = str(0)

window.bind("a", bat_L.move_up)
window.bind("z", bat_L.move_down)
window.bind("<Up>", bat_R.move_up)
window.bind("<Down>", bat_R.move_down)
window.bind("<space>", restart_game)
window.bind("r", reset_game)
    
game_flow()

window.mainloop()
