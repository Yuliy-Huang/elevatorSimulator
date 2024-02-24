import sys
sys.path.append('/Users/huangyao/PycharmProjects/elevatorSimulator')

from views.building import Building
from views.elevator import Elevator

bottom = -1
top = 10
building = Building(bottom, top)
elevator = Elevator(bottom, top)


def elevator_start():
    while True:
        print('------ 当前楼层 ：{}'.format(elevator.current_floor), flush=True)
        current_floor_data = building.get_data_by_index(elevator.current_floor)
        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)

        building.update_floor_data(elevator.current_floor, elevator.run_elevator(furthest_floor, current_floor_data))
        print('------ 楼的 floor_data ------', flush=True)
        print(building.floor_data, flush=True)

        # if (elevator.is_up and furthest_floor > elevator.current_floor) or (not elevator.is_up and furthest_floor < elevator.current_floor):
        #     elevator.move()
        #     print('------ move ------', flush=True)

        if building.is_elevator_pause() and elevator.person_data.empty:
            print('******* break ******** {}'.format(elevator.current_floor), flush=True)
            break
        else:
            elevator.move()
            print('------ move ------', flush=True)


if __name__ == '__main__':
    elevator_start()
