from flask import Flask, render_template
import json
import random
import copy

import logging

app = Flask(__name__)

user_db = {}
data_db = {}

default_list = [_ for _ in range(1, 101)]

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/room/<user>')
def room_page(user):
    return render_template(
        'room.html',
        data={
            'user': user,
        }
    )


@app.route('/api/join/<user>')
def join_user(user):
    user_db[user] = 1
    logging.info("Join user {}, user count is {}".format(user, len(user_db)))
    return create_response()


@app.route('/api/leave/<user>')
def leave_user(user):
    user_db.pop(user, None)
    logging.info("Leave user {}, user count is {}".format(user, len(user_db)))
    return create_response()


@app.route('/adminApi/leaveAll')
def leave_user_all():
    user_db = {}
    data_db = {}
    logging.info("Init user db")
    return create_response()


@app.route('/adminApi/startGame')
def start_game():
    list_ = copy.deepcopy(default_list)
    random.shuffle(list_)
    i = 0
    for name, _ in user_db.items():
        data_db[name] = list_[i]
        i = i + 1
    logging.info("Game Start")
    logging.info(data_db)
    return create_response()


@app.route('/api/getNumber/<user>')
def get_number(user):
    return create_response(
        {'value': data_db.get(user) or '-1' }
    )


@app.route('/adminApi/getAllNumber')
def get_all_numbers():
    result = []
    for usr, value in data_db.items():
        result.append(
            {
                'name': usr,
                'value': value,
            }
        )
    return create_response({'result': result})


@app.route('/adminApi/getAllUser')
def get_all_users():
    result = []
    for usr, value in user_db.items():
        result.append(
            {
                'name': usr,
                'value': value,
            }
        )
    return create_response({'result': result})


def create_response(data={}):
    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
