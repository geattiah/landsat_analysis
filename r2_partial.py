import pingouin as pg
import pandas as pd
import numpy as np
from statsmodels.api import OLS
#import pingouin as pg

import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import summary
# Custom function (calculate and output statistics of regression analysis)

def get_lr_stats(x, y_true, y_pred, coef, intercept, alpha=0.05):
    
    n   = len(x)
    k   = len(x.columns)
    ssr = sum((y_pred - np.mean(y_true))**2) # Regression square sum SSR
    sse = sum((y_true - y_pred)**2)          # Sum of squared residuals SSE
    sst = ssr + sse                              # Total square sum SST
    msr = ssr / k                                # Mean square regression MSR
    mse = sse / (n-k-1)                          # Mean square residual MSE
    
    R_square = ssr / sst                                   # Determination coefficient R^2
    Adjusted_R_square = 1-(1-R_square)*((n-1) / (n-k-1))   # Determination coefficient of adjustment
    Multiple_R = np.sqrt(R_square)                         # Complex correlation coefficient   
    Se = np.sqrt(sse/(n - k - 1))                          # Standard error of estimation
    
    loglike = log_like(y_true, y_pred)[0]
    AIC = 2*(k+1) - 2 * loglike                  # (k+1) represents k regression parameters or coefficients and 1 intercept parameter
    BIC = -2*loglike + (k+1)*np.log(n)  
    
    # Significance test of linear relationship
    F  = (ssr / k) / (sse / ( n - k - 1 ))            # Test statistic F (test of linear relationship)
    pf = scipy.stats.f.sf(F, k, n-k-1)                # Significance F for test, i.e. significance F
    Fa = scipy.stats.f.isf(alpha, dfn=k, dfd=n-k-1)   # F critical value
    
    # Significance test of regression coefficient
    stat = param_test_stat(x, Se, intercept, coef, alpha=alpha)
    
    # Output statistics of regression analysis
    print('='*80)
    print('df_Model:{}  df_Residuals:{}'.format(k, n-k-1), '\n')
    print('loglike:{}  AIC:{}  BIC:{}'.format(round(loglike,3), round(AIC,1), round(BIC,1)), '\n')
    print('SST:{}  SSR:{}  SSE:{}  MSR:{}  MSE:{}  Se:{}'.format(round(sst,4),
                                                                 round(ssr,4),
                                                                 round(sse,4),
                                                                 round(msr,4),
                                                                 round(mse,4),
                                                                 round(Se,4)), '\n')
    
    print('Multiple_R:{}  R_square:{}  Adjusted_R_square:{}'.format(round(Multiple_R,4),
                                                                    round(R_square,4),
                                                                    round(Adjusted_R_square,4)), '\n')
    print('F:{}  pf:{}  Fa:{}'.format(round(F,4), pf, round(Fa,4)))
    
    print('='*80)
    print(stat)
    print('='*80)
    
    return 0


csv = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Projects\Lake_surface_temperature\output\csv\max_temperature.csv"

df = pd.read_csv(csv)
print(df)

print(df.columns)

df = df.drop(df[(df['Lake_Area']< 0.05)].index)
df = df.drop(df[(df['HyLak_Depth']< 0.05)].index)
df = df.drop(df[(df['HyLak_Elevation']< 0.05)].index)

df['log_area'] = np.log(df['Lake_Area'])
df['log_depth'] = np.log(df['HyLak_Depth'])
df['log_elevation'] = np.log(df['HyLak_Elevation'])
df['log_x'] = round(df['x'],2)
df['log_y'] = round(df['y'],2)
df['log_volume'] = np.log(df['HyLak_Volume'])


x = df[['log_area']]#'log_depth','log_elevation','log_volume','log_x','log_y']]
y = df['Mean_Temperature']

# # #role = pg.partial_corr(data=df, x='Mean_Temperature', y='log_volume', covar=['log_y','log_area','log_depth','log_elevation','log_x'],
# #                 method='spearman').round(3)

# # # #print(role)


from sklearn.model_selection import train_test_split
x_train, x_test, y_train,y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)

mlr = LinearRegression()  

import statsmodels.api as sm
lm = sm.OLS(y_train, x_train)
model = lm.fit()
#aov_table = lm(model)
#print(aov_table)

mlr.fit(x_train, y_train)
print(model.summary())

print("Intercept: ", mlr.intercept_)
print("Coefficients:")
print(list(zip(x, mlr.coef_)))

#Prediction of test set
y_pred_mlr= mlr.predict(x_test)
#Predicted values
print("Prediction for test set: {}".format(y_pred_mlr))

mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_mlr})
mlr_diff.head()

#Model Evaluation
from sklearn import metrics
meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
print('R squared: {:.2f}'.format(mlr.score(x,y)*100))
print('Mean Absolute Error:', meanAbErr)
print('Mean Square Error:', meanSqErr)
print('Root Mean Square Error:', rootMeanSqErr)

get_lr_stats(x_train,y_pred_mlr,y_test,mlr.coef_,mlr.intercept_,alpha=0.05)