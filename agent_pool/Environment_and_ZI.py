import numpy as np
import pandas as pd

# Create a DataFrame initialized with lists of values
def everyday_df_initialisation(ID, Price, Quantity,Side, Strategy, Constraint):
    df = pd.DataFrame(index=['Producer ID', 'Price', 'Quantity', 
                             'Side', 'Strategy', 'Constraint'],
                      columns=['B1', 'B2', 'S1', 'S2'] ).fillna('N/A')
    df.loc['Producer ID'] = ID
    df.loc['Price'] = Price
    df.loc['Quantity'] = Quantity
    df.loc['Side'] = Side
    df.loc['Strategy'] = Strategy
    df.loc['Constraint'] = Constraint
    return(df)

class Zero_Intellegence:
    def ZI(mu, volatility):
        return list(np.random.normal(mu, volatility, 4))



class Everyday_Table:
    def __init__(self, ID, Price, Quantity,Side, Strategy, Constraint):
        self.ID = ID
        self.Price = Price
        self.Quantity = Quantity
        self.Side = Side
        self.Strategy = Strategy
        self.Constraint = Constraint
        
    def everyday_df_initialisation(self):
        df = pd.DataFrame(index=['Producer ID', 'Price', 'Quantity', 
                                 'Side', 'Strategy', 'Constraint'],
                          columns=['B1', 'B2', 'S1', 'S2'] ).fillna('N/A')
        df.loc['Producer ID'] = self.ID
        df.loc['Price'] = self.Price
        df.loc['Quantity'] = self.Quantity
        df.loc['Side'] = self.Side
        df.loc['Strategy'] = self.Strategy
        df.loc['Constraint'] = self.Constraint
        return(df)
    

ID = ['B1','B2','S1','S2']
Price = Zero_Intellegence.ZI(1.55, 0.5) #pound
Quantity = Zero_Intellegence.ZI(3, 1) #liter
Side = ['B', 'B', 'S', 'S']
Strategy = ['ZI','ZI','ZI','ZI']
Constraint = ['a','b','c','d']

# Output Sample
table = Everyday_Table(ID, Price, Quantity,Side, Strategy, Constraint)
Output = table.everyday_df_initialisation()
