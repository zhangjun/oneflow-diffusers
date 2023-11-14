""" printer """
import warnings

class Printer:
    """  Printer """
    def __init__(self, color):
        self.color = color

    def __call__(self, *args, **kwargs):
        return f"\033[{self.color}m" + f"{args} {kwargs}" + "\033[0m"


def print_red(*args, **kwargs):
    """ print_red """
    output = Printer(31)(*args, **kwargs)
    warnings.warn(output)


def print_green(*args, **kwargs):
    """ print_green """
    output = Printer(32)(*args, **kwargs)
    # warnings.warn(output)
    print(output)


def print_yellow(*args, **kwargs):
    """ print_yellow """
    output = Printer(33)(*args, **kwargs)
    print(output)


if __name__ == "__main__":
    print_red("This is red text")
    print_green("This is green text")
