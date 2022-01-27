import math
from pydantic import BaseModel, validator, PositiveInt, constr, PositiveFloat, NonNegativeFloat, NonNegativeInt
from datetime import datetime
from typing import Optional, List
import pytz

# точность округления значений расстояний, м
length_tolerance_m = 1e-5
# точность округления значений углов, радиан
angle_tolerance_rad = 1e-9

# используемые системы координат в формате astropy
astropy_frames = {
    # Международная земная система координат (International Terrestrial Reference System)
    # неинерциальная (вращающаяся), с осью Oz, ориентированной по оси вращения Земли,
    # с осью Ox, лежащей в плоскости гринвичского меридиана.
    # Соответствует ГСК-2011 (ГОСТ 32453-2017). В старой литературе называется Гринвичской системой координат.
    'itrs': 'МЗСК(ITRS)',
    # Геоцентрическая небесная система координат (Geocentric Celestial Reference System)
    # инерциальная с началом в центре Земли, с осью Oz, ориентированной по оси врещения Земли в эпоху J2000.0
    'gcrs': 'ГНСК(GCRS)',
    # Барицентрическая небесная система координат (International Celestial Reference System)
    # инерциальная с началом в центре масс Солнечной системы, с осью Oz, ориентированной по оси врещения Земли
    # в эпоху J2000.0
    'icrs': 'БНСК(ICRS)',
    # Абсолютная геоцентрическая экваториальная система координат (True equator mean equinox)
    # псевдоинерциальная с началом в центре Земли, с осью Ox, направленной в среднюю точку весеннего равноденствия,
    # с осью Oz, ориентированной по оси вращения Земли. За рубежом используется для расчета TLE.
    # Соответствует АГСК
    'teme': 'АГСК(TEME)',
    # Гелиоцентрическая небесная система координат (Heliocentric Celestial Reference System)
    # инерциальная с началом в центре Солнца, с осью Oz, ориентированной по оси врещения Земли
    # в эпоху J2000.0
    'hcrs': 'ГЛНСК(HCRS)',
    # Орбитальная система координат(Orbital Reference System)
    # неинерциальная система координат, начало совпадает с центром масс станции.
    # ось OY направлена на центр Земли;
    # ось OX перпендикулярна оси OY и направлена в сторону движения  КА  по  орбите
    'ors':  'ОСК(ORS)'
}


# noinspection PyMethodParameters
class StatusVector(BaseModel):
    """
    Представляет вектор состояния в заданной системе прямоугольных координат
    """
    # идентификатор в БД (если есть)
    status_vector_id: Optional[int]
    # составляющие радиус-вектора:
    x: float
    y: float
    z: float
    # составляющие скорости:
    v_x: Optional[float]
    v_y: Optional[float]
    v_z: Optional[float]
    # момент времени наблюдения (важно для движущихся систем координат)
    time: datetime
    frame: str
    is_impulse: Optional[bool] = False
    comment: Optional[str]

    # @validator('frame')
    # def _validate_frame(cls, val: str):
    #     val = val.lower()
    #     astropy_frames_lower = map(lambda x: x.lower(), astropy_frames)
    #     if val not in astropy_frames_lower:
    #         raise ValueError(f'Система координат "{val}" не найдена в справочнике')
    #     return val

    @validator('time')
    def _time_to_utc(cls, val: datetime):
        result = datetime(val.year, val.month, val.day, val.hour, val.minute, val.second, val.microsecond, pytz.utc)
        return result

    # максимальная точность определения координат, определяемая константой length_tolerance_m
    @validator('x', 'y', 'z', 'v_x', 'v_y', 'v_z')
    def _round_length(cls, val: float):
        if val is not None:
            round_base = round(math.log10(1/length_tolerance_m))
            return round(val, round_base)


# noinspection PyMethodParameters
class Impulse(BaseModel):
    """
    Представляет импульс (мгновенное изменение скорости) системе прямоугольных координат
    """
    delta_v_x: Optional[float]
    delta_v_y: Optional[float]
    delta_v_z: Optional[float]


# noinspection PyMethodParameters
class KeplerianElements(BaseModel):
    """
    Представляет кеплеровы элементы оскулирующей орбиты
    """
    # фокальный параметр, м
    semilatus_rectum: Optional[PositiveFloat]
    # большая полуось, м
    semimajor_axe: Optional[PositiveFloat]
    # малая полуось, м
    semiminor_axe: Optional[PositiveFloat]
    # эксцентриситет
    eccentricity: Optional[NonNegativeFloat]
    # наклонение, радиан
    inclination: Optional[float]
    # долгота восходящего узла, радиан
    longitude_ascending_node: Optional[float]
    # аргумент перицентра, радиан
    argument_periapsis: Optional[float]
    # истинная аномалия, радиан
    true_anomaly: Optional[float]
    # средняя аномалия, радиан
    mean_anomaly: Optional[float]

    # максимальная точность определения координат, определяемая константой length_tolerance_m
    @validator('semilatus_rectum', 'semimajor_axe', 'semiminor_axe')
    def _round_length(cls, val: float):
        if val is not None:
            round_base = round(math.log10(1 / length_tolerance_m))
            return round(val, round_base)
        else:
            return

    # максимальная точность определения углов, определяемая константой angle_tolerance_rad
    @validator('inclination', 'longitude_ascending_node', 'argument_periapsis', 'true_anomaly', 'mean_anomaly')
    def _round_angle(cls, val: float):
        if val is not None:
            round_base = round(math.log10(1/angle_tolerance_rad))
            return round(val, round_base)
        else:
            return


# noinspection PyMethodParameters
class AdditionalBallistics(BaseModel):
    """
    Представляет дополнительные баллистические параметры
    """
    # высота над поверхностью Земли
    height: Optional[float]
    # модуль радиус-вектора
    magnitude: Optional[NonNegativeFloat]
    # номер витка на момент эпохи
    revolution_number: Optional[NonNegativeInt]

    # максимальная точность определения координат, определяемая константой length_tolerance_m
    @validator('height', 'magnitude')
    def _round_length(cls, val: float):
        if val is not None:
            round_base = round(math.log10(1 / length_tolerance_m))
            return round(val, round_base)


class StandardBallisticInformation(BaseModel):
    """
    Представляет стандартную баллистическую информацию (СБИ)
    """
    status_vector: StatusVector
    keplerian_elements: Optional[KeplerianElements]
    additional_ballistics: Optional[AdditionalBallistics]


class StretchRequest(BaseModel):
    """
    Класс данных для запроса протяжки вектора состояния
    """
    user_id: constr(min_length=1)
    status_vector: StatusVector
    calculate_time: PositiveInt
    dt: PositiveFloat
    ascending_nodes_only: bool


class StretchResult(BaseModel):
    """
    Класс данных для ответа на тестовый запрос
    """
    status_vectors: List[StatusVector]
    errors: Optional[List[dict]]


class User(BaseModel):
    """
    Класс данных представления пользователя
    """
    user_id: int
    role_id: int
    department_id: int
    login: str
    encrypted_password: str
    first_name: str
    last_name: str
    patronymic_name: str
    email: str
    phone: Optional[str]
    is_valid: bool
    comment: Optional[str]


class Frame(BaseModel):
    """
    Класс данных представления системы координат
    """
    frame_id: int
    code_astropy: str
    name_ru: str
    name_ru_short: str
    name_en: str
    name_en_short: str
    comment: Optional[str]


class SpaceObject(BaseModel):
    """
    Класс данных представления космического объекта
    """
    space_object_id: int
    norad_catalog_id: Optional[str]
    nssdc_catalog_id: Optional[str]
    rus_catalog_id: Optional[str]
    n_ka: Optional[int]
    name_ru: str
    name_en: str
    name_ru_short: str
    name_en_short: str
    mass: float
    effective_cross_sectional_area: float
    comment: Optional[str]


class Stretch(BaseModel):
    """
    Класс данных представления протяжки вектора состояния
    """
    stretch_id: Optional[int]
    name: str
    space_object_id: int
    n_nu: Optional[int]
    num_sbros: Optional[int]
    project_id: int
    user_id: int
    is_processing: bool = False
    begin_time: Optional[datetime]
    end_time: Optional[datetime]
    creation_time: Optional[datetime]
    comment: Optional[str]

    # noinspection PyMethodParameters
    @validator('begin_time', 'end_time')
    def _time_to_utc(cls, val: datetime):
        if val is not None:
            result = datetime(val.year, val.month, val.day, val.hour, val.minute, val.second, val.microsecond, pytz.utc)
        else:
            result = None

        return result


class LoginRequest(BaseModel):
    """
    Класс данных для запроса логина
    """
    token: str
    login: str
    password: str


class LoginResult(BaseModel):
    """
    Класс данных для ответа на запрос логина
    """
    user: Optional[User]
    errors: Optional[list]


class StretchesRequest(BaseModel):
    """
    Класс данных для запроса списка протяжек
    """
    token: str
    user_id: Optional[int]
    filter_imported: bool = False


class StretchesResult(BaseModel):
    """
    Класс данных для ответа на запрос списка протяжек
    """
    stretches: List[Stretch]
    errors: Optional[list]


class StretchEditRequest(BaseModel):
    """
    Класс данных для запроса на редактирование протяжки
    """
    token: str
    stretch: Stretch


class StretchEditResult(BaseModel):
    """
    Класс данных для ответа на редактирование протяжки
    """
    status: str  # 'passed' или 'failed'
    errors: Optional[list]


class StretchDeleteRequest(BaseModel):
    """
    Класс данных для запроса на удаление протяжки
    """
    token: str
    stretch_id: int


class StretchDeleteResult(BaseModel):
    """
    Класс данных для ответа на запрос на удаление протяжки
    """
    status: str  # 'passed' или 'failed'
    errors: Optional[list]


class FramesRequest(BaseModel):
    """
    Класс данных для запроса списка систем координат
    """
    token: str


class FramesResult(BaseModel):
    """
    Класс данных для ответа на запрос списка систем координат
    """
    frames: List[Frame]
    errors: Optional[list]


class SbisRequest(BaseModel):
    """
    Класс данных для запроса списка СБИ
    """
    token: str
    stretch_id: int


class SbisResult(BaseModel):
    """
    Класс данных для ответа на запрос списка СБИ
    """
    sbis: List[StandardBallisticInformation]
    errors: Optional[list]


class DoStretchRequest(BaseModel):
    """
    Класс данных для запроса на создание протяжки
    """
    token: str
    stretch: Stretch
    status_vector: StatusVector
    revolution_number: Optional[NonNegativeInt]
    period: int
    timestep: int
    ascending_nodes_only: bool
    f81: float = 0
    kp: float = 0
    is_multiprocess_mode: bool = True


class DoStretchResult(BaseModel):
    """
    Класс данных для ответа на запрос на создание протяжки
    """
    status: str  # 'passed' или 'failed'
    stretch_id: int
    errors: Optional[list]


class GlueStretchRequest(BaseModel):
    """
    Класс данных для запроса на склейку протяжки
    """
    token: str
    stretch_id: int
    timestep: int
    period: int
    f81: float = 0
    kp: float = 0
    impulse: Optional[Impulse]
    is_multiprocess_mode: bool = True


class GlueStretchResult(DoStretchResult):
    pass


class SpaceObjectsRequest(BaseModel):
    """
    Класс данных для запроса списка космических объектов
    """
    token: str


class SpaceObjectsResult(BaseModel):
    """
    Класс данных для ответа на запрос списка космических объектов
    """
    space_objects: List[SpaceObject]
    errors: Optional[list]


class UserRequest(BaseModel):
    """
    Класс данных для запроса логина
    """
    token: str
    user_id: int


# noinspection PyMethodParameters
class UserResult(BaseModel):
    """
    Класс данных для ответа на запрос логина
    """
    user: Optional[User]
    errors: Optional[list]

    @validator('user')
    def _validate_user(cls, val: str):
        val.encrypted_password = 'скрыт в целях безопасности'
        return val


class NY(BaseModel):
    """
    Класс представления данных из таблицы OPER.NY старой БД
    """
    n_nu: int
    num_sbros: Optional[int]
    n_ka: Optional[int]
    data: Optional[datetime]
    rx: float
    ry: float
    rz: float
    vx: float
    vy: float
    vz: float
    a: Optional[float]
    e: Optional[float]
    i: Optional[float]
    ome: Optional[float]


class ImportRequest(BaseModel):
    """
    Класс данных для запроса импорта данных из старой БД
    """
    token: str
    user_id: int
    num_sbros: int


class ImportResult(BaseModel):
    """
    Класс данных для ответа на запрос импорта данных из старой БД
    """
    stretch_id: int
    new_sbi_number: int
    errors: Optional[list]


class NumSbrosRequest(BaseModel):
    """
    Класс данных для запроса списка уникальных значений num_sbros из старой БД
    """
    token: str


class NumSbrosResult(BaseModel):
    """
    Класс данных для ответа на запрос списка уникальных значений num_sbros из старой БД
    """
    num_sbros_list: List[int]
    errors: Optional[list]


class ExportRequest(BaseModel):
    """
    Класс данных для запроса экспорта данных в старую БД
    """
    token: str
    stretch_id: int


class ExportResult(BaseModel):
    """
    Класс данных для ответа на запрос экспорта данных в старую БД
    """
    num_sbros: int
    new_records_number: int
    errors: Optional[list]


class FollowTheSunRequest(BaseModel):
    """
    Класс данных для запроса векторов состояния ИСЗ и Солнца
    """
    token: str
    status_vector_sat_ascending_node: StatusVector
    time_m: int


class FollowTheSunResult(BaseModel):
    """
    Класс данных для ответа на запрос векторов состояния ИСЗ и Солнца
    """
    sat_status_vectors: Optional[List[StatusVector]]
    sun_status_vectors: Optional[List[StatusVector]]
    sun_status_vectors_ors: Optional[List[StatusVector]]
    errors: Optional[list]


class Settings(BaseModel):
    logging_level: Optional[str]  # уровень логгирования
    max_log_files_size_mb: Optional[PositiveInt]  # максимальный размер log-файлов, MB
    max_log_files_back_up_count: Optional[PositiveInt]  # количество архивов log-файлов
    protocol: Optional[str]  # протокол api-сервера
    listen_port: Optional[int]  # порт api-сервера
    ode_solver: Optional[str]  # метод решения ОДУ
    calculate_perturbations: Optional[bool]  # учитывать влияние атмосферы и геопотенциала
    workdb_host: Optional[str]  # хост БД КММ
    workdb_port: Optional[PositiveInt]  # порт БД КММ
    workdb_username: Optional[str]  # логин БД КММ
    workdb_password: Optional[str]  # пароль БД КММ
    workdb_base: Optional[str]  # имя БД КММ
    workdb_schema: Optional[str]  # схема БД КММ
    olddb_host: Optional[str]  # порт БД ГОГУ
    olddb_port: Optional[PositiveInt]  # логин БД ГОГУ
    olddb_username: Optional[str]  # логин БД ГОГУ
    olddb_password: Optional[str]  # пароль БД ГОГУ
    olddb_base: Optional[str]  # имя БД ГОГУ
    olddb_schema: Optional[str]  # схема БД ГОГУ


class SettingsRequest(BaseModel):
    """
    Класс данных для запроса установок
    """
    token: str
    settings: Optional[Settings]


class SettingsResult(BaseModel):
    """
    Класс данных для ответа на запрос установок
    """
    settings: Settings
    errors: Optional[list]
