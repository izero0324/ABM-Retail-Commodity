from agent_pool.Environment_and_ZI import Everyday_Table

#your own data
ID = ['CustomerA','CustomerB','SellerA','SellerB']
Price = [2,4,3,5] #pound
Quantity = [1,3,2,4] #liter
Side = ['B', 'B', 'S', 'S']
Strategy = ['ZI','ZIP8','Minmax','Maximin']
Constraint = ['a','b','c','d']


table = Everyday_Table(ID, Price, Quantity,Side, Strategy, Constraint)
Output = table.everyday_df_initialisation()
print(Output)



