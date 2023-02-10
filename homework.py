class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"%.3f" % (self.duration)} ч.; '
                f'Дистанция: {"%.3f" % (self.distance)} км; '
                f'Ср. скорость: {"%.3f" % (self.speed)} км/ч; '
                f'Потрачено ккал: {"%.3f" % (self.calories)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    S_IN_H = 3600
    M_IN_H = 60

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных при беге калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_KF_1 = 0.035
    CALORIES_KF_2 = 0.029
    KMH_MC = 0.278
    SM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных при хотьбе калорий."""

        speed_m_s = self.get_mean_speed() * self.KMH_MC
        height_m = self.height / self.SM_IN_M
        duration_m = self.duration * 60
        return ((self.CALORIES_KF_1 * self.weight + (speed_m_s**2
                / height_m) * self.CALORIES_KF_2 * self.weight) * duration_m)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_CONST = 1.1
    SW_CONST = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных при плавании калорий."""
        return ((self.get_mean_speed() + self.SPEED_CONST)
                * self.SW_CONST * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_data = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return type_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
