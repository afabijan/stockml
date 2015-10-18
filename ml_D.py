import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
from matplotlib import style
import pandas as pd
style.use("ggplot")
FEATURES = ['DE Ratio', 'Trailing P/E', 'Price/Sales', 'Price/Book', 'Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity', 'Revenue Per Share', 'Market Cap', 'Enterprise Value', 'Forward P/E', 'PEG Ratio', 'Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Revenue', 'Gross Profit', 'EBITDA', 'Net Income Avl to Common ', 'Diluted EPS', 'Earnings Growth', 'Revenue Growth', 'Total Cash', 'Total Cash Per Share', 'Total Debt', 'Current Ratio', 'Book Value Per Share', 'Cash Flow', 'Beta', 'Held by Insiders', 'Held by Institutions', 'Shares Short (as of', 'Short Ratio', 'Short % of Float', 'Shares Short (prior ']


def Build_Data_set():
    data_df = pd.DataFrame.from_csv("key_stats.csv")
    #data_df = data_df[:1000]
    X = np.array(data_df[FEATURES].values)#.tolist())
    print X[:,1]
    y = (data_df["Status"].replace("underperform",0).replace("outperform",1).values.tolist())
    X = preprocessing.scale(X)
    return X,y

def Analysis():
    test_size = 1000
    X,y = Build_Data_set()

    print (len(X))

    #print y
    clf = svm.SVC(kernel = "linear", C = 1.0)
    print "startin fit"
    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1,test_size+1):
        #print "prediction ", clf.predict(X[-x])[0]
        #print y[-x]
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count += 1

    #print "correct_count ", correct_count
    #print "test_size", test_size
    Accuracy = correct_count / float(test_size)
    Accuracy = 100.00 * Accuracy
    print "Accuracy: ", Accuracy




    w = clf.coef_[0]
    a = -w[0] / w[1]

    xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    yy = a * xx - clf.intercept_[0] / w[1]

    h0 = plt.plot(xx,yy, "k-", label="non-weighted")

    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.ylabel("Trailing P/E")
    plt.xlabel("DE Ration")
    plt.show()


Analysis()
