import sys
import time

sys.path.append('/Users/huangyao/PycharmProjects/elevatorSimulator')

from views.building import Building
from views.elevator import Elevator
import threading


bottom = -1
top = 10
building = Building(bottom, top)
elevator = Elevator(bottom, top)
pause_event = threading.Event()


def elevator_start():
    while True:
        if pause_event.isSet():
            print("****---- 电梯线程已被暂停 ----****")
            continue
        print('------ 当前楼层 ：{}'.format(elevator.current_floor), flush=True)
        current_floor_data = building.get_data_by_index(elevator.current_floor)
        print('------ 当前楼的 floor_data ------', flush=True)
        print(current_floor_data, flush=True)

        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)

        person_not_in = elevator.run_elevator(furthest_floor, current_floor_data)

        building.update_floor_data(elevator.current_floor, person_not_in)
        print('------ 更新后楼的 floor_data ------', flush=True)
        print(building.floor_data, flush=True)

        if building.is_elevator_pause() and elevator.person_data.empty:
            elevator.auto_reverse()
            print('******* break ******** {}, *** is_up : {}'.format(elevator.current_floor, elevator.is_up), flush=True)
            break
        else:
            elevator.move()
            print('************** move *************** elevator.current_floor: {}'.format(elevator.current_floor), flush=True)


def pause_elevator():
    pause_event.set()
    print('************** pause_elevator')


def restart_elevator():
    pause_event.clear()
    print('************** restart_elevator')


if __name__ == '__main__':
    elevator_start()
