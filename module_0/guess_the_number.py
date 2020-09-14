import numpy as np


def score_game(game_core):
    """Run the game 1000 times to find out how fast it finds guessed number"""
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Current algorithm detects the number on average"
          f" in {score} attempts")
    return score


def game_core_v1(number):
    # General idea is to split function into two: when secret number is even
    # and when it's uneven. Then, using attribute of divisibility by 3 and
    # simple comparing, we can move prediction faster to the desired number.
    predict = np.random.randint(1, 101)

    def even(predict):
        """
        'Even' sub-function's being activated when secret number is even.
        On the first level it checks 2 conditions: is predicted number greater
        then secret and is secret number divisible by 3. On second - it tests
        predicted number's divisibility by 3 and 2, adding/deducting
        3, 2 or 1 to current prediction, and increases iteration count by 1.
        """
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
        """
        'Uneven' sub-function's being activated when secret number is uneven.
        On the first level it checks 2 conditions: is predicted number greater
        then secret and is secret number divisible by 3. On second - it tests
        predicted number's divisibility by 3 and 2, adding/deducting
        3, 2 or 1 to current prediction, and increases iteration count by 1.
        """
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
