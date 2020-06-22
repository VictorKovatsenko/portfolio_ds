import numpy as np


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


def game_core_v1(number):
    predict = np.random.randint(1, 101)

    # General idea is to split function into two: when hidden number is even and when it's uneven. Then,
    # using attribute of divisibility by 3 and simple comparing, we can move prediction faster to the desired
    # number.

    def even(predict):
        """ 'Even' sub-function's being activated when hidden number is even. On the first level it checks 2
        conditions: is predicted number greater then hidden at current iteration and is hidden number divisible by 3.
        On second - it tests predicted number's divisibility by 3 and 2, adding/deducting '3' '2' or '1' to
        prediction, and increases iteration count by 1 """
        global count
        count = 1
        while number != predict:
            count += 1
            if number > predict and number % 3 == 0:
                if predict % 3 == 0:
                    predict += 3
                else:
                    if predict % 2 == 0:
                        predict += 2
                    else:
                        predict += 1
            elif number > predict and number % 3 != 0:
                if predict % 3 == 0:
                    predict += 1
                else:
                    if predict % 2 == 0:
                        predict += 2
                    else:
                        predict += 3
            elif number < predict and number % 3 == 0:
                if predict % 3 == 0:
                    predict -= 3
                else:
                    if predict % 2 == 0:
                        predict -= 1
                    else:
                        predict -= 2
            elif number < predict and number % 3 != 0:
                if predict % 3 == 0:
                    predict -= 2
                else:
                    if predict % 2 == 0:
                        predict -= 2
                    else:
                        predict -= 1
            return count

    def uneven(predict):
        """ 'Uneven' sub-function's being activated when hidden number is uneven. On the first level it checks 2
        conditions: is predicted number greater then hidden at current iteration and is hidden number divisible by 3.
        On second - it tests predicted number's divisibility by 3 and 2, adding/deducting '3' '2' or '1' to
        prediction, and increases iteration count by 1 """
        global count
        count = 1
        while number != predict:
            count += 1
            if number > predict and number % 3 == 0:
                if predict % 3 == 0:
                    predict += 3
                else:
                    if predict % 2 == 0:
                        predict += 1
                    else:
                        predict += 2
            elif number > predict and number % 3 != 0:
                if predict % 3 == 0:
                    predict += 1
                else:
                    if predict % 2 == 0:
                        predict += 3
                    else:
                        predict += 2
            elif number < predict and number % 3 == 0:
                if predict % 3 == 0:
                    predict -= 3
                else:
                    if predict % 2 == 0:
                        predict -= 1
                    else:
                        predict -= 2
            elif number < predict and number % 3 != 0:
                if predict % 3 == 0:
                    predict -= 1
                else:
                    if predict % 2 == 0:
                        predict -= 3
                    else:
                        predict -= 2
        return count

    if number % 2 == 0:
        even(predict)
    else:
        uneven(predict)
    return count


score_game(game_core_v1)