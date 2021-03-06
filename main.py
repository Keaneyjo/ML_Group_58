
# Title:
from models.linear import linear
from models.ridge import ridge
from models.lasso import lasso
from models.knn import kNN
from summary.dummy import dummy_
from scraping.formatting import format_listings_for_models, open_csv
import matplotlib.pyplot as plt
from scraping.formatting import csv_for_models, get_distance
from sklearn.linear_model import *
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
# Firstly, should web scrap
print("Attempting web scapping from daft.ie")


def main():
    # Code below searches for new daft listings which are residential rent
    # listings = pull_properties(SearchType.RESIDENTIAL_RENT)
    # Comment out the line below if you want to exclude shared rent
    # listings2 = pull_properties(SearchType.SHARING)
    # Combine the two searches together, and format them into a csv friendly format
    # accommodation = format_listing(listings[0] + listings2[0], listings[1] + listings2[1])
    # accommodation = format_listing(listings[0], listings[1])
    # Then inserts into a csv file so we don't have to search each time
    # format_to_csv(accommodation)
    inputs_and_outputs = format_listings_for_models()
    # Open csv into accommodation dictionary
    # Comment everything above, and uncomment everything below if you don't want to search each time
    accommodation = open_csv('scraping/houses.csv')
    scatter_plots(accommodation)

    cValues = [0.01, 1, 10, 30, 50, 100, 150, 200]
    #  Call models (models should have different
    #  folds, training/testing, different C values, AKA all the different types we used in past assignments):
    ## Linear
    linear_error, linear_std = linear()
    #linear_error = [linear_error] * (len(cValues))
    #linear_std = [linear_std] * (len(cValues))
    ## LASSO
    lasso_error, lasso_std = lasso()
    ## Ridge
    ridge_error, ridge_std = ridge()
    ## kNN
    kNN_error, kNN_std = kNN()
    print(np.min(np.array(kNN_error)))
    ## dummy
    dummy_error = dummy_()
    dummy_error = [dummy_error] * (len(cValues))

    # Summary Methods
    #plt.errorbar(cValues, linear_error, yerr=linear_std, label="Linear Error")
    plt.errorbar(cValues, lasso_error, yerr=lasso_std, label="LASSO Error")
    plt.errorbar(cValues, ridge_error, yerr=ridge_std, label="Ridge Error")
    plt.errorbar(cValues, dummy_error, label="Dummy Error")

    plt.xlabel("C")
    plt.ylabel("Mean Square Error")
    plt.title("Error of Different Algorithms")
    plt.legend()
    plt.show()






def scatter_plots(accommodation):
    # four variables: bedrooms, bathrooms, BER, distance
    prices, bedrooms, bathrooms, distance = [], [], [], []
    prices_BER, BER = [], []
    for index in accommodation:
        prices.append(index['price'])
        bedrooms.append(index['bedrooms'])
        bathrooms.append(index['bathrooms'])
        distance.append(index['distance'])
        # if (index['BER'] != "NA") and (type(index['BER']) != float):
        #     prices_BER.append(index['price'])
        #     BER.append(BER_convert(index['BER'], index))
        # if(index['BER'] != "NA") and (type(index['BER']) != float):
        if ((index['BER'] != "NA") and (0 <= index['BER'] and index['BER'] <= 14)):
            prices_BER.append(index['price'])
            BER.append(index['BER'])
    # Prices VS Bedrooms
    plt.scatter(bedrooms, prices, c='b', label="Prices VS Bedrooms")
    plt.title("Prices VS Bedrooms")
    plt.ylabel("Price")
    plt.xlabel("# Bedrooms")
    plt.show()
    # Prices VS Bathrooms
    plt.scatter(bathrooms, prices, c='g', label="Prices VS Bathrooms")
    plt.title("Prices VS Bathrooms")
    plt.ylabel("Price")
    plt.xlabel("# Bathrooms")
    plt.show()
    # Prices VS Distance
    plt.scatter(distance, prices, c='r', label="Prices VS Distance")
    plt.title("Prices VS Distance")
    plt.ylabel("Price")
    plt.xlabel("Distance")
    plt.show()
    # Prices VS BER
    plt.scatter(BER, prices_BER, c='black', label="Prices VS BER")
    plt.title("Prices VS BER")
    plt.ylabel("Price")
    plt.xlabel("BER Score, [Higher Score => Better BER]")
    plt.show()


def BER_convert(rating, index):
    # SI_666 = BER Exempt
    score = 0
    if rating == 'SI_666':
        return score
    elif rating == 'F':
        return 2
    elif rating == 'G':
        return 1
    try:
        rate = list(rating)
        temp = int(rate[1])
        score = temp
        if rate[0] == 'A':
            return score + 10
        elif rate[0] == 'B':
            return score + 7
        elif rate[0] == 'C':
            return score + 4
        elif rate[0] == 'D':
            return score + 3
        elif rate[0] == 'E':
            return score + 1
        else:
            print("Error: BER rating missing")
    except:
        print(rating)
        print(index)

main()
