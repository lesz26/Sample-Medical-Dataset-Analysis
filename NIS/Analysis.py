import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

#Accepts set independent and dependent variables, 
def log_reg(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    X_col = X
    X = np.array(X)
    y = np.array(y)
    X = sm.add_constant(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state=0)
    model = sm.GLM(y_train, X_train, family= sm.families.Binomial())
    logistic_reg = model.fit(method = 'bfgs', maxiter = 500)
    print(logistic_reg.summary())
    print(logistic_reg.pvalues)
    predicted = logistic_reg.predict(X_test)
    
    dataframe_1 = pd.DataFrame()
    #Creates dataframe column with independent variable names
    for i in range(0, len(X_col.columns)):
        if (logistic_reg.pvalues[i+1] < 0.01):
            p = '<0.01'
        else:
            p = round(logistic_reg.pvalues[i+1], 2)
        new_frame = pd.DataFrame({'Ind_Var' : 
            [X_col.columns[i]], 'Coef': [str(round(np.exp(logistic_reg.params[i+1]),2)) + 
        ' [' + str(round(np.exp(logistic_reg.conf_int(alpha= 0.05, cols=None)[i+1][0]),2))  + ', ' +
        str(round(np.exp(logistic_reg.conf_int(alpha= 0.05, cols=None)[i+1][1]),2)) +
        ']'], 'P-Val': [p]})
        dataframe_1 = pd.concat([dataframe_1, new_frame], axis = 0)   
    
    dataframe_1 = dataframe_1.sort_values(by=['Coef'], ascending=False)
    print(roc_auc_score(y_test, predicted))
    return dataframe_1
