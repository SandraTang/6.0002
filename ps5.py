# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name: Sandra Tang
# Collaborators:
# Time:

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2000)
TESTING_INTERVAL = range(2000, 2017)

"""
Begin helper code
"""
class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = np.sum(((x - np.mean(x))**2))
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

##########################
#    End helper code     #
##########################

def linear_regression(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Args:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """
    #TODO
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    numerator = 0
    denominator = 0
    for i in range(len(x)):
    	numerator += (x[i] - x_mean) * (y[i] - y_mean)
    	denominator += (x[i] - x_mean)**2
    m = numerator / denominator
    b = y_mean - (m * x_mean)
    return (m, b)


def get_squared_error(x, y, m, b):
    '''
    Calculates the squared error of the linear regression model given the set
    of data points.

    Args:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    '''
    se = 0
    for i in range(len(x)):
    	y_prime = m * x[i] + b
    	se += (y[i] - y_prime)**2
    return se


def generate_models(x, y, degrees):

    """
    Generates a list of polynomial regression models with degrees specified by
    degrees for the given set of data points

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for i in degrees:
    	models.append(np.polyfit(x, y, i))
    return models


def evaluate_models_on_training(x, y, models, display_graphs):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (i.e. the model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        Degree of your regression model,
        R-squared of your model evaluated on the given data points,
        and standard error/slope (if this model is linear).

    R-squared and standard error/slope should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed


    Returns:
        A list holding the R-squared value for each model
    """

    r_values = []
    for coeffs in models:
        y_preds = []
        isLinear = True
        #yields: y_predictions and isLinear
        for i in x:
            y_temp = np.polyval(coeffs, i)
            y_preds.append(y_temp)
            if len(coeffs) > 2:
                    isLinear = isLinear and False
            # #highest degree to lowest
            # #e.g. 2 3 5 2
            # #is.. 3 2 1 0
            # #so.. len() - index - 1
            # for j in range(len(coeffs)):
            #     y_temp += coeffs[j]*(x[i]**(len(coeffs) - j - 1)) 
            #     if (len(coeffs) - j - 1) > 1 and coeffs[j] > 0:
            #         isLinear = isLinear and False
            # y_preds.append(y_temp)
        #each model has an r_value associated with it
        y_preds = np.array(y_preds)
        r_score = round(r2_score(y, y_preds), 4)
        r_values.append(r_score)
        #graphing
        if display_graphs:
            plt.plot(x, y, 'bo', label = 'Measured')
            plt.plot(x, y_preds, 'r-', label = 'Best First Curve')
            plt.xlabel('Year')
            plt.ylabel('Temperature')
            if isLinear:
                # b = linear_regression(x, y)[1]
                # y_preds += b
                se = round(standard_error_over_slope(x, y, y_preds, coeffs), 4)
                plt.title("Degree of regression model: " + str(len(coeffs)-1) + "\nR-squared of model evaluated on the given data points: " + str(r_score) + "\nStandard Error Over Slope: " + str(se))
            else:
                plt.title("Degree of regression model: " + str(len(coeffs)-1) + "\nR-squared of model evaluated on the given data points: " + str(r_score))
            plt.show()
    return r_values



def generate_cities_averages(dataset, cities, years):
    """
    For each year in the given range of years, computes the average of the
    annual temperatures in the given cities.

    Args:
        dataset: instance of Dataset
        cities: a list of the names of cities to include in the average
            annual temperature calculation
        years: a list of years to evaluate the average annual temperatures at

    Returns:
        a 1-d numpy array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    averages = []
    for year in years:
        temps = []
        for city in cities:
            all_temps = dataset.get_daily_temps(city, year)
            temps.append(np.sum(all_temps)/len(all_temps))
        averages.append(sum(temps)/len(temps))
    return np.array(averages)


def find_trend(x, y, length, positive_slope):
    """
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope with the sign specified by positive_slope and j-i = length.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have the same slope (within the
        acceptable tolerance), (2,5) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    if len(x) < length:
        return None
    coeffs = generate_models(x[0:length], y[0:length], [1])
    extreme = coeffs[0][0]
    extreme_i = 0
    for i in range(len(x)-length):
        coeffs = generate_models(x[i:i+length], y[i:i+length], [1])[0][0]
        if not abs(extreme - coeffs) <= 10**(-8):
            if positive_slope:
                if coeffs > extreme:
                    extreme = coeffs
                    extreme_i = i
            else:
                if coeffs < extreme:
                    extreme = coeffs
                    extreme_i = i
    if positive_slope:
        if extreme <= 0:
            return None
    else:
        if extreme >= 0:
            return None
    return (extreme_i, extreme_i+length)

def get_rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    num = 0
    for i in range(len(y)):
        num += (y[i] - estimated[i])**2
    num /= len(y)
    num = num ** 0.5
    return num
    


def evaluate_models_on_testing(x, y, models, display_graphs):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    rs = []
    for coeffs in models:
        y_preds = []
        #yields: y_predictions and isLinear
        for i in range(len(x)):
            y_temp = 0
            #highest degree to lowest
            #e.g. 2 3 5 2
            #is.. 3 2 1 0
            #so.. len() - index - 1
            for j in range(len(coeffs)):
                y_temp += coeffs[j]*(x[i]**(len(coeffs) - j - 1))
            y_preds.append(y_temp)
        #each model has an r_value associated with it
        y_preds = np.array(y_preds)
        rm = round(get_rmse(y, y_preds), 4)
        rs.append(rm)
        #graphing
        if display_graphs:
            plt.plot(x, y, 'bo', label = 'Measured')
            plt.plot(x, y_preds, 'r-', label = 'Best First Curve')
            plt.xlabel('Year')
            plt.ylabel('Temperature')
            plt.title("Degree of regression model: " + str(len(coeffs)-1) + "\nRMSE: " + str(rm))
            plt.show()
    return rs

if __name__ == '__main__':

    # pass

    # Problem 4A
    data = Dataset('data.csv')
    x = np.array(range(1961, 2017))
    y = []
    for i in x:
        y.append(data.get_temp_on_date('PORTLAND', 12, 25, i))
    y = np.array(y)
    model = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, model, True)

    # # Problem 4B

    y = generate_cities_averages(data, ['PORTLAND'], x)
    y = np.array(y)
    model = generate_models(x, y, [1])
    evaluate_models_on_training(x, y, model, True)

    # # Problem 5B

    years = range(1961, 2017)
    y = generate_cities_averages(data, ['PHOENIX'], years)
    window = find_trend(years, y, 30, True)
    window_years = years[window[0] : window[1]]
    y = y[window[0] : window[1]]
    # print(window_years)
    # print(linear_regression(window_years, y))
    model = generate_models(window_years, y, [1])
    evaluate_models_on_training(window_years, y, model, True)


    # # Problem 5C
    y = generate_cities_averages(data, ['PHOENIX'], years)
    window = find_trend(years, y, 15, False)
    window_years = years[window[0] : window[1]]
    y = y[window[0] : window[1]]
    # print(window_years)
    # print(linear_regression(window_years, y))
    model = generate_models(window_years, y, [1])
    evaluate_models_on_training(window_years, y, model, True)

    # Problem 6B

    # Use the Dataset class to generate a training set of the national annual average temperature for the years in TRAINING_INTERVAL.
    # Fit the training set to polynomials of degree 2 and 10 with generate_models and plot the results with evaluate_models_on_training.

    #1961-1999
    x = range(1961, 2000)
    y = generate_cities_averages(data, CITIES, x)
    models = generate_models(x, y, [2, 10])
    evaluate_models_on_training(x, y, models, True)

    # Use the Dataset class to generate a test set of the national annual average temperature for the years in TESTING_INTERVAL.
    # Evaluate the predictions of each model obtained in the previous section and plot the results with evaluate_models_on_testing. 
    # Read the docstring carefully to make sure you use the function correctly.

    testing_x = range(2000, 2017)
    y = generate_cities_averages(data, CITIES, testing_x)
    evaluate_models_on_training(testing_x, y, models, True)