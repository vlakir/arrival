import requests
import json
import urllib3
from funnydeco import benchmark
from datetime import datetime
import pytz


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = 'https://localhost:7443'
# host = 'https://192.168.9.100:7443'


url_dummy = f'{host}/api/v1/pydantic.json'
url_login = f'{host}/api/v1/login.json'
url_stretches = f'{host}/api/v1/stretches.json'
url_stretch_edit = f'{host}/api/v1/stretch_edit.json'
url_stretch_delete = f'{host}/api/v1/stretch_delete.json'
url_frames = f'{host}/api/v1/frames.json'
url_sbis = f'{host}/api/v1/sbis.json'
url_do_stretch = f'{host}/api/v1/do_stretch.json'
url_space_objects = f'{host}/api/v1/space_objects.json'
url_user = f'{host}/api/v1/user.json'
url_import = f'{host}/api/v1/import.json'
url_num_sbros = f'{host}/api/v1/num_sbros.json'
url_export = f'{host}/api/v1/export.json'
url_follow_the_sun = f'{host}/api/v1/follow_the_sun.json'
url_glue_stretch = f'{host}/api/v1/glue_stretch.json'
url_settings = f'{host}/api/v1/settings.json'


headers = {'Content-type': 'application/json'}


token = '84980637-164d-4571-a3a2-c0e1216547ac'


params_dummy = {
                    "foo": 8,
                    "bar": 4
                }

params_login = {
                    "token": token,
                    "login": "vlakir",
                    "password": "123456789",
                }


params_stretches = {
                    "token": token,
                    "user_id": 1,
                    # "filter_imported": True
                    }

params_stretch_edit = {
                        "token": token,
                        "stretch": {
                            "stretch_id": 1,
                            "name": "Тестовая протяжка",
                            "space_object_id": 1,
                            "project_id": 1,
                            "user_id": 1,
                            "comment": "Тестовая протяжка из одного вектора, чтобы было от чего плясать"
                        },
                      }

params_stretch_delete = {
                        "token": token,
                        "stretch_id": 0
                        }

params_frames = {
                    "token": token,
                }

params_sbis = {
                    "token": token,
                    "stretch_id": 2353,
              }


params_do_stretch = {
                        "token": token,
                        "stretch": {
                            "name": "Протяжка из pinger 21",
                            "space_object_id": 1,
                            "project_id": 1,
                            "user_id": 1,
                            "comment": ""
                        },
                        "status_vector": {
                            "x": 563193.21089,
                            "y": 6776010.5125,
                            "z": 0.0,
                            "v_x": -4241.33291,
                            "v_y": 346.64011,
                            "v_z": 6007.73281,
                            "time": datetime(2021, 8, 2, 8, 15, 17, 0, pytz.utc).isoformat(),
                            "frame": 'itrs'
                        },
                        "revolution_number": 4000,
                        "period": 10 * 93 * 60,
                        "timestep": 60,
                        "ascending_nodes_only": False,
                        "f81": 125,
                        "kp": 1.6
                   }

params_space_objects = {
                            "token": token,
                       }

params_user = {
                    "token": token,
                    "user_id": 1
                }

params_import = {
                    "token": token,
                    "user_id": 1,
                    "num_sbros": 14799
                }

params_num_sbros = {
                        "token": token,
                   }

params_export = {
                    "token": token,
                    "stretch_id": 1
                }

params_follow_the_sun = {
                            "token": token,
                            "status_vector_sat_ascending_node": {
                                "x": 4951.209053138 * 1000,
                                "y": -4653.856628012 * 1000,
                                "z": 0.0,
                                "v_x": 2.896991154055 * 1000,
                                "v_y": 3.110415318743 * 1000,
                                "v_z": 6.001929490957 * 1000,
                                "time": datetime(2021, 7, 23, 20, 33, 25).isoformat(),
                                "frame": 'itrs'
                            },
                            "time_m": 60,
                          }


params_glue_stretch = {
                        "token": token,
                        "stretch_id": 419,
                        "period": 15 * 93 * 60,
                        "timestep": 60,
                        "f81": 125,
                        "kp": 1.6
                      }

# params_settings = {
#                         "token": token,
#                         "settings": {
#                             "logging_level": "DEBUG",
#                             "max_log_files_size_mb": 10,
#                             "max_log_files_back_up_count": 5,
#                             "protocol": "https",
#                             "listen_port": 7443,
#                             "ode_solver": "fehlberg5",
#                             "calculate_perturbations": False,
#                             "workdb_host": "192.168.9.100",
#                             "workdb_port": 5432,
#                             "workdb_username": "postgres",
#                             "workdb_password": "begemot2014",
#                             "workdb_base": "postgres",
#                             "workdb_schema": "kmm",
#                             "olddb_host": "192.168.15.63",
#                             "olddb_port": "1521",
#                             "olddb_username": "oper",
#                             "olddb_password": "vpm",
#                             "olddb_base": "gogu",
#                             "olddb_schema": "oper"
#                         }
#                       }

params_settings = {
                        "token": token,
                        "settings": None
                      }


# noinspection PyUnusedLocal
@benchmark
def requester(url: str, params: dict, print_benchmark=False, benchmark_name='') -> None:
    response = requests.post(url, verify=False, data=json.dumps(params), headers=headers)
    print('Ответ сервера:')
    print(f'Статус - {response.status_code}')
    print(json.dumps(response.json(), sort_keys=False, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    print_bench = True
    bench_name = 'Запрос к API-серверу'

    # requester(url_dummy, params_dummy, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_login, params_login, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_stretches, params_stretches, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_stretch_edit, params_stretch_edit, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_stretch_delete, params_stretch_delete, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_frames, params_frames, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_sbis, params_sbis, print_benchmark=print_bench, benchmark_name=bench_name)
    requester(url_do_stretch, params_do_stretch, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_space_objects, params_space_objects, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_user, params_user, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_import, params_import, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_num_sbros, params_num_sbros, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_export, params_export, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_follow_the_sun, params_follow_the_sun, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_glue_stretch, params_glue_stretch, print_benchmark=print_bench, benchmark_name=bench_name)
    # requester(url_settings, params_settings, print_benchmark=print_bench, benchmark_name=bench_name)
