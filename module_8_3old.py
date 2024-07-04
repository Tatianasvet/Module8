class InvalidDataException(Exception):
    def __init__(self, message='', wrong_data=None):
        self.message = message
        self.wrong_data = wrong_data

    def __str__(self):
        return (f'Получены неверные данные: {self.wrong_data}\n'
                f'{self.message}\n'
                f'Попробуйте ввести заново')


class ProcessingException(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class Pincode:

    def __init__(self, *numbers):
        self.__pin = []
        if len(numbers) != 4:
            raise InvalidDataException('Неверное количество аргументов', numbers)
        for number in numbers:
            self._check_number(number)
            self.__pin.append(number)

    def _check_number(self, number):
        if type(number) is not int:
            raise InvalidDataException('Это не циферка', number)
        elif number < 0:
            raise InvalidDataException('Принимаем только положительные числа', number)
        elif number > 9:
            raise InvalidDataException('Слишком большое число. Должно быть от 0 до 9', number)

    def __eq__(self, other):
        for i in range(4):
            if self.__pin[i] != other.__pin[i]:
                return False
        return True


class Action:

    def __init__(self):
        self.__pincode = Pincode(0, 0, 0, 0)

    def set_pin(self):
        success = False
        while not success:
            try:
                potential_pin = input('\nВведите новый pin: ')
                pin_sequence = self.__pin_parse(potential_pin)
                self.__pincode = Pincode(*pin_sequence)
                print('Новый pin успешно записан!')
                success = True
            except InvalidDataException as exc:
                print(exc)

    def __pin_parse(self, str_pin):
        result = []
        try:
            for i in range(len(str_pin)):
                result.append(int(str_pin[i]))
        except ValueError as exc:
            raise InvalidDataException('Вы ввели что-то не то. Должны быть только цифры', str_pin)
        return result

    def verification(self):
        attempt = 1
        while attempt <= 3:
            try:
                new_potential_pin = input('\nВведите pin: ')
                new_pin_sequence = self.__pin_parse(new_potential_pin)
                check_pin = Pincode(*new_pin_sequence)
                if not check_pin == self.__pincode:
                    raise ProcessingException('Неверный pin')
                else:
                    print('Верификация успешно пройдена!')
                    return 0
            except (InvalidDataException, ProcessingException) as exc:
                print(exc)
                print('Вы ввели неверный pin.\n'
                      f'Осталось попыток: {3 - attempt}')
                attempt += 1
        raise ProcessingException('Вы исчерпали лимит попыток')

    def act(self):
        choice = input('Выберие действие:\n'
                     '1 – установить новый pin\n'
                     '2 – пройти верификацию\n'
                     '3 – закончить сеанс\n'
                     'Мой выбор: ')
        match choice:
            case '1':
                self.set_pin()
                return True
            case '2':
                self.verification()
                return True
            case '3':
                return False
            case _:
                raise InvalidDataException('Такого варианта не предлагалось', choice)


A = Action()
working = True
while working:
    try:
        working = A.act()
    except InvalidDataException as exc:
        print(exc)
    except ProcessingException as exc:
        print(exc)
        working = False
    finally:
        print(f'\n{'#':-^40}\n')



