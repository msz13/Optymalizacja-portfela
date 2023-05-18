import numpy as np
from dataclasses import dataclass 


goals = {
        5: {
        'cost': 10800,
        'max_outflow': 1
        }
    }

'''
transakcje 
| rodzaj        | ilosc shares | wartość | prowizja |
|wpłata         | 0 | 10000 | 0 |
|zakup          | 50 | 9900| 5 |
| sprzedarz     | 50 | 12000 | 6 |
|wyplata - cel1 | 0 | 12000| 0 |
'''

'''
INDEX-T 0 - T
wpłaty
kupno/sprzedarz
wypłata - cel1
wypłata - cel2
wypłata cel3
'''

@dataclass
class Transaction:
    delta_shares: np.array
    outflows: int = 0

def transactions(inflow, shares_owned, assets_weights, prices, goal = (0,0)):
    
    goal_target = 0
    goal_max_outflow_percent = 0

    if (goal is not None):
        goal_target = goal[0] 
        goal_max_outflow_percent = goal[1]

    current_assets_value = shares_owned * prices
    current_value = np.sum(current_assets_value, 1)
    goal_allocation = current_value * goal_max_outflow_percent

    outflows = np.round(np.where(goal_allocation >= goal_target, goal_target, goal_allocation),2)  
     
    expected_value = current_value + inflow - outflows
    #max_outflow_value = current_value * goal_max_outflow_percent
    
    delta_value = expected_value.reshape((2,1)) * assets_weights - current_assets_value
    
    delta_shares =  np.fix(delta_value / prices)

    #outflows = np.round(np.abs(np.sum(delta_shares * prices,axis=1)),2)
    
    return Transaction(delta_shares, outflows)
    


class PortfoliosSimulator:

    def __init__(self) -> None:
        pass

    def set_params(self, assets_prices, assets_weights, inflows, goals):
        self.__prices = assets_prices
        self.__assets_weights = assets_weights        
        self.__inflows = inflows
        self.__goals = goals
        self.T = np.max(list(self.__goals.keys()))+1
        self.__shares = np.zeros((self.__prices.shape[0],self.__prices.shape[2]))

    def get_porfolio_final_value(self):
        return np.sum(self.__shares * self.__prices[:,-1],1)
    
    def get_outflows(self):
        return self.__outflows
    
    def get_shares(self):
        return self.__shares
                     
    
    def run(self):          
       
        self.__outflows = np.zeros((1,2))


        for t in range (self.T):
            transaction = transactions(self.__inflows[t], self.__shares, self.__assets_weights,self.__prices[:,t], self.__goals.get(t))
            self.__shares += transaction.delta_shares
            if (self.__goals.get(t) is not None):
                self.__outflows[0] = transaction.outflows

        
