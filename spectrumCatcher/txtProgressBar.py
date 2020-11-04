def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def printProgressBar2 (iteration, total, iteration1, total1, prefix = '', suffix = '',  prefix1 = '', suffix1 = '' , decimals = 1, length = 100, length1 = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent  = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    percent1 = ("{0:." + str(decimals) + "f}").format(100 * (iteration1 / float(total1)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    filledLength1 = int(length1 * iteration1 // total1)
    bar1 = fill * filledLength1 + '-' * (length1 - filledLength1)

    print(f'\r{prefix} |{bar}| {percent}% {suffix} {prefix1} |{bar1}| {percent1}% {suffix1}', end = printEnd)
    # Print New Line on Complete
    if iteration1 == total1 and iteration == total: 
        print()

