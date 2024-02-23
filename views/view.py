from flask import Blueprint, make_response, request
from views.elevatorStart import building, elevator
from views.building import Building
from views.elevator import Elevator
from views.randomData import InitFloorPeopleData

elevator_blue = Blueprint('view', __name__)

bottom = -1
top = 20
building = Building(bottom, top)
elevator = Elevator(bottom, top)


@elevator_blue.route('/elevator_info')
def elevator_info():
    furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)
    res = {
        'current_floor': elevator.current_floor,
        'furthest_floor': furthest_floor,
        'is_up': elevator.is_up,
        'persons': elevator.persons,
        'person_data': elevator.person_data,
        'building_floor_data': building.floor_data.to_dict(orient='records')
    }
    return make_response({'msg': 'success', 'data': {'data': res}}, 200)


@elevator_blue.route('/elevator_pause')
def elevator_pause():
    building.floor_data = building.floor_data.drop(range(len(building.floor_data)))
    elevator.person_data = elevator.person_data.drop((range(len(elevator.person_data))))
    return make_response(
        {'msg': 'success', 'data': {'data': {'persons': elevator.persons, 'current_floor': elevator.current_floor}}},
        200)


@elevator_blue.route('/open_door')
def open_door():
    elevator.door_open_or_close()
    return make_response({'msg': 'success', 'data': {'data': {'persons': elevator.persons, 'current_floor': elevator.current_floor}}}, 200)


@elevator_blue.route('/close_door')
def close_door():
    elevator.door_open_or_close()
    return make_response({'msg': 'success', 'data': {'persons': elevator.persons, 'current_floor': elevator.current_floor}}, 200)


@elevator_blue.route('/start_elevator')
def start_elevator():
    msg = 'success'
    print('------ 当前楼层 ：', elevator.current_floor)
    data = building.get_data_by_index(elevator.current_floor)
    furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)
    building.update_floor_data(elevator.current_floor, elevator.run_elevator(furthest_floor, data))
    print('------ 楼的 floor_data ------')
    print(building.floor_data)
    res = {'current_floor_data': data, 'building_data': building.floor_data}

    if building.is_elevator_pause() and elevator.person_data.empty:
        msg = 'error'
        res = {'data': 'Elevator is paused'}
        print('******* break ********')

    return make_response({'msg': msg, 'data': res}, 200)


@elevator_blue.route('/call_elevator_inside')
def call_elevator_inside():
    current_floor = request.args.get('current_floor')
    target_floor = request.args.get('target_floor')
    is_up = request.args.get('is_up')
    weight = request.args.get('weight')
    data = InitFloorPeopleData(bottom_floor=bottom, top_floor=top).one_person(current_floor, is_up, weight, target_floor)
    building.set_one_person_data(data)
    res = {
        'current_floor': elevator.current_floor,
        'is_up': elevator.is_up,
        'persons': elevator.persons,
        'person_data': elevator.person_data,
        'building_floor_data': building.floor_data.to_dict(orient='records')
    }
    return make_response({'msg': 'success', 'data': {'data': res}}, 200)


@elevator_blue.route('/call_elevator_outside')
def call_elevator_outside():
    current_floor = request.args.get('current_floor')
    is_up = request.args.get('is_up')
    data = InitFloorPeopleData(bottom_floor=bottom, top_floor=top).one_person(current_floor, is_up)
    building.set_one_person_data(data)
    res = {
        'current_floor': elevator.current_floor,
        'is_up': elevator.is_up,
        'persons': elevator.persons,
        'person_data': elevator.person_data,
        'building_floor_data': building.floor_data.to_dict(orient='records')
    }
    return make_response({'msg': 'success', 'data': res}, 200)
