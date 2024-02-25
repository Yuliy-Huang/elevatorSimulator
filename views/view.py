from flask import Blueprint, make_response, request
from views.elevatorStart import building, elevator
from views.building import Building
from views.elevator import Elevator
from views.randomData import InitFloorPeopleData
from views.elevatorStart import elevator_start
from views.elevatorStart import top, bottom, elevator, building
import pandas as pd
import json
import threading

elevator_blue = Blueprint('view', __name__)


@elevator_blue.route('/elevator_info')
def elevator_info():
    if not building:
        msg = 'error'
        res = {}
    else:
        msg = 'success'
        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)
        res = {
            'current_floor': elevator.current_floor,
            'furthest_floor': furthest_floor,
            'is_up': elevator.is_up,
            'persons': elevator.persons,
            'person_data': elevator.person_data.to_dict(orient='records'),
            'building_floor_data': building.floor_data.sort_values('current_floor').to_dict(orient='records') if len(building.floor_data) > 0 else []
        }
    return make_response({'msg': msg, 'data': res}, 200)


@elevator_blue.route('/open_door')
def open_door():
    elevator.door_open()
    return make_response(
        {'msg': 'success', 'data': {'persons': elevator.persons, 'current_floor': elevator.current_floor}},
        200)


@elevator_blue.route('/close_door')
def close_door():
    elevator.door_close()
    return make_response(
        {'msg': 'success', 'data': {'persons': elevator.persons, 'current_floor': elevator.current_floor}}, 200)


@elevator_blue.route('/start_elevator')
def start_elevator():
    generate_person = request.args.get('generate_person', 'yes')
    msg = 'elevator start success'
    if generate_person == 'yes':
        building.set_floor_data()

    thread = threading.Thread(target=elevator_start)
    thread.start()

    return make_response({'msg': msg, 'data': {
            'current_floor': elevator.current_floor,
            'is_up': elevator.is_up,
            'persons': elevator.persons,
            'person_data': elevator.person_data.to_dict(orient='records'),
            'building_floor_data': building.floor_data.sort_values('current_floor').to_dict(orient='records') if len(building.floor_data) > 0 else []
        }}, 200)


@elevator_blue.route('/elevator_pause')
def elevator_pause():
    building.clear_floor_data()
    elevator.clear_person_data()
    return make_response(
        {'msg': 'elevator stop success',
         'data': {
            'current_floor': elevator.current_floor,
            'is_up': elevator.is_up,
            'persons': elevator.persons,
            'person_data': elevator.person_data.to_dict(orient='records'),
            'building_floor_data': building.floor_data.sort_values('current_floor').to_dict(orient='records') if len(building.floor_data) > 0 else []
        }},
        200)


@elevator_blue.route('/call_elevator_inside', methods=['POST'])
def call_elevator_inside():
    print('call_elevator_inside --- request.form : ', request.form)
    req = request.get_data()
    reqData = json.loads(req)
    current_floor = reqData['current_floor']
    target_floor = reqData['target_floor']
    is_up = 1 if target_floor > current_floor else 0
    data = InitFloorPeopleData(bottom_floor=bottom, top_floor=top).one_person(current_floor, is_up,
                                                                              target_floor)
    elevator.update_elevator_data(pd.DataFrame(data), 'add')
    res = {
        'current_floor': elevator.current_floor,
        'is_up': elevator.is_up,
        'persons': elevator.persons,
        'person_data': elevator.person_data.to_dict(orient='records'),
        'building_floor_data': building.floor_data.sort_values('current_floor').to_dict(orient='records') if len(building.floor_data) > 0 else []
    }
    return make_response({'msg': 'success', 'data': res}, 200)


@elevator_blue.route('/call_elevator_outside', methods=['POST'])
def call_elevator_outside():
    print('call_elevator_outside --- request.form : ', request.form)
    req = request.get_data()
    reqData = json.loads(req)
    current_floor = reqData['current_floor']
    is_up = reqData['is_up']
    data = InitFloorPeopleData(bottom_floor=bottom, top_floor=top).one_person(current_floor, is_up, 0)
    building.set_one_person_data(data)
    res = {
        'current_floor': elevator.current_floor,
        'is_up': elevator.is_up,
        'persons': elevator.persons,
        'person_data': elevator.person_data.to_dict(orient='records'),
        'building_floor_data': building.floor_data.sort_values('current_floor').to_dict(orient='records') if len(building.floor_data) > 0 else []
    }
    return make_response({'msg': 'success', 'data': res}, 200)
