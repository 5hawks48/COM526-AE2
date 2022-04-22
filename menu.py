import solver
from ImageRecognition import image_processing
import benchmarking


def guess_menu():
    while True:
        print("\nChoose guess type:")
        print("1: Normal 1-9 Array")
        print("2: Random Array")
        print("3: Most to least common")
        print("4: Least to most common")
        option = ''
        try:
            option = int(input('Select item:'))
        except:
            print("Invalid option. Please try again")
        if option == 1:
            return solver.normal_guesses
        if option == 2:
            return solver.randomised_guesses
        if option == 3:
            return solver.get_order_by_most_common
        if option == 4:
            return solver.get_order_by_least_common


def solver_menu():
    while True:
        print("\nSolver Menu")
        print("1: Begin")
        print("2: Quit")
        option = ''
        try:
            option = int(input('Select item:'))
        except:
            print("Invalid option. Please try again")
        if option == 1:
            quiz_count = ''
            try:
                # TODO: Specific quiz
                quiz_count = int(input('How many quizzes to solve:'))
            except:
                print("Invalid option. Please try again")
            guess_type = guess_menu()
            print("Solving...\n")
            try:
                solver.run(quiz_count, 1, guess_type, False)
            except ValueError as err:
                print(err)
            # run_multithreaded(2)
        if option == 2:
            print("Returning to home")
            break


def image_recognition_menu():
    # enter path
    # r"ImageRecognition/sudoku.jpg"
    path = input("Enter the image path (e.g. ImageRecognition/sudoku.jpg): ")
    # guess type
    guess_type = guess_menu()
    try:
        image_processing.run(path, guess_type)
    except FileNotFoundError as err:
        print(err)


if __name__ == "__main__":
    while True:
        print("\nMenu")
        print("1: Solve quizzes")
        print("2: Image recognition")
        print("3: Run benchmark")
        print("4: Quit")
        option = ''
        try:
            option = int(input('Select item:'))
        except:
            print("Invalid option. Please try again")
        if option == 1:
            solver_menu()
        if option == 2:
            image_recognition_menu()
        if option == 3:
            quiz_count = ''
            try:
                quiz_count = int(input('How many quizzes to solve:'))
            except:
                print("Invalid option. Please try again")
            benchmarking.benchmark_multithread(quiz_count)
        if option == 4:
            print("Quitting...")
            exit()
