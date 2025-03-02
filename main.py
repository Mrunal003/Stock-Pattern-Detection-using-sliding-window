import pandas as pd
import numpy as np
from fastpip import pip
from scipy.stats import spearmanr
import sys


def getPattern(df_list, filepath):
    """
    Outputs the file containing start_time, end_time and Pattern identified in that time period.
    :param df_list:  Dataframe containing information of each day.
    :param filepath: Path of input file.
    :return: Output file as csv.
    """

    result = []
    for i in range(len(df_list)):
        start, end, ans = findPattern(df_list[i]['close'])
        if ans != 'No pattern':
            result.append([df_list[i]['date'].iloc[start], df_list[i]['date'].iloc[end], ans])

    outputFile = pd.DataFrame(result, columns=['start', 'end', 'pattern'])
    outputFile.to_csv(f"Pattern_{filepath}")


def renderFile(filepath):
    """
    Reads the file and splits the data based on date.
    :param filepath: Path of input file.
    :return: Dataframe containing information of each day.
    """

    df = pd.read_csv(filepath)
    df_list = []
    df_index = []

    for i in range(len(df)):
        if df.iloc[i][0] == 0:
            df_index.append(i)

    for i in range(len(df_index) - 1):
        df_list.append(df[df_index[i]:df_index[i + 1]])

    return df_list


def POS_PAT(pattern, pip_point):
    """
    Rule Based Approach for applying further checks on our patterns
    :param pattern: Pattern that is identified.
    :param pip_point: PIP (Perceptually Important Points) for the Pattern.
    :return: True, if the conditions match, otherwise False.
    """

    diff = max(pip_point) - min(pip_point)
    sorted_res = sorted(pip_point)
    max1 = sorted_res[-1]       # Maximum value of all the PIP points
    max2 = sorted_res[-2]       # Second Maximum value of all the PIP points
    min1 = sorted_res[0]        # Minimum value of all the PIP points
    min2 = sorted_res[1]        # Second Minimum value of all the PIP points

    if pattern == 'Head and shoulders':
        if abs(pip_point[1] - pip_point[5]) < np.mean([pip_point[1], pip_point[5]])*0.1 and abs(pip_point[2] - pip_point[4]) < np.mean([pip_point[2], pip_point[4]])*0.1 and pip_point[3] == max1:
            return True
    elif pattern == 'Reverse Head and shoulders':
        if abs(pip_point[1] - pip_point[5]) < np.mean([pip_point[1], pip_point[5]])*0.1 and abs(pip_point[2] - pip_point[4]) < np.mean([pip_point[2], pip_point[4]])*0.1 and pip_point[3] == min1:
            return True
    elif pattern == 'Double Top':
        if max1 - max2 < diff * 0.2 and pip_point[1] + pip_point[3] == max1 + max2 and pip_point[1] > pip_point[0] and pip_point[3] > pip_point[4]:
            return True
    elif pattern == 'Double Bottom':
        if min2 - min1 < diff * 0.2 and pip_point[1] + pip_point[3] == min1 + min2 and pip_point[1] < pip_point[0] and pip_point[3] < pip_point[4]:
            return True
    return False


def findPattern(data):
    """
    Function to calculate start_time, end_time and Pattern Identified for a particular day.
    :param data: 'close' value of a particular day.
    :return: start_time, end_time and Pattern Identified.
    """

    max_coef = 0
    ans = ""
    res = []
    dates_index = []

    MATCH_PAT1 = {
        'Reverse Head and shoulders': [6.5, 2.5, 4.5, 1, 4.5, 2.5, 6.5],
        'Head and shoulders': [1.5, 5.5, 3.5, 7, 3.5, 5.5, 1.5]

    }
    MATCH_PAT2 = {
        'Double Top': [1.5, 6.5, 5, 6.5, 1.5],
        'Double Bottom': [6.5, 1.5, 3, 1.5, 6.5]

    }
    for k in range(10, 15):
        points = []
        for i in range(len(data)):
            p = [i, data.iloc[i]]
            points.append(p)
        pip_points = pip(points, k)

        x = []
        y = []
        x_pip = []
        y_pip = []
        for i in points:
            x.append(i[0])
            y.append(i[1])
        for i in pip_points:
            x_pip.append(i[0])
            y_pip.append(i[1])

        for i in range(len(y_pip) - 6):
            mydata = y_pip[i:i + 7]
            for key, value in MATCH_PAT1.items():
                coef, p = spearmanr(value, mydata)
                if coef > max_coef:
                    max_coef = coef
                    ans = key
                    if x_pip[i + 6] - x_pip[i] >= 36:
                        dates_index = [x_pip[i], x_pip[i + 5]]
                    else:
                        dates_index = [x_pip[i], x_pip[i + 6]]
                    res = mydata
    for k in range(8, 10):
        points = []
        for i in range(len(data)):
            p = [i, data.iloc[i]]
            points.append(p)
        pip_points = pip(points, k)

        x = []
        y = []
        x_pip = []
        y_pip = []
        for i in points:
            x.append(i[0])
            y.append(i[1])
        for i in pip_points:
            x_pip.append(i[0])
            y_pip.append(i[1])

        for i in range(len(y_pip) - 4):
            mydata = y_pip[i:i + 5]
            for key, value in MATCH_PAT2.items():
                coef, p = spearmanr(value, mydata)
                if coef > max_coef:
                    max_coef = coef
                    ans = key
                    if x_pip[i + 4] - x_pip[i] >= 36:
                        dates_index = [x_pip[i], x_pip[i + 4]]
                    else:
                        dates_index = [x_pip[i], x_pip[i + 3]]
                    res = mydata
    if max_coef > 0.85 and POS_PAT(ans, res):
        return dates_index[0], dates_index[1], ans
    return -1, -1, "No pattern"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please pass <TestData.csv> as argument in the command line!\n")
        sys.exit()
    filepath = sys.argv[1]
    df_list = renderFile(filepath)
    getPattern(df_list, filepath)
