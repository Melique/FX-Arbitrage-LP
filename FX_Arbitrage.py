import numpy as np
import pandas as pd
import pulp

class FX_Arbitrage:
    """
    A class to find FX arbitrage through linear programming

    """
    def __init__(self, date, rates):
        """
        Args:
            date (datetime): date of the exchange rates
            rates (pandas.DataFrame): DataFrame of the rates for the date
        """
        self.date = date
        self.rates = rates
    
    def form_lp(self):
        """ Make the linear program (LP) given the rates. Creates a new 
            attribute called model
        """
        model = pulp.LpProblem("FX_Arbitrage", pulp.LpMaximize)
    
        n = len(self.rates.columns)
        I = J = range(1, n+1)
        x = pulp.LpVariable.dicts("x", (I, J), lowBound = 0, cat="Continuous")
        y = pulp.LpVariable.dicts("y", I, lowBound = 0, cat="Continuous")

        for i in range(n):
            del x[i+1][i+1]

        y[1].upBound = 1
        targets = np.arange(1, n+1)

        #add the objective function
        model += y[1]

        #add the constraints
        for target in targets:
            vars_ = [x[i][target] for i in x if i != target]
            temp = [x[target][i] for i in x if i != target]
            vars_.extend(temp)

            coeffs = self.rates.iloc[:,target-1].values.tolist()
            del coeffs[target-1]
            ones = np.repeat(-1, n-1).tolist()
            coeffs.extend(ones)

            model += pulp.LpAffineExpression([(vars_[i], coeffs[i]) for i in range(2*n-2)]) == y[target]

        self.model = model
    
    def is_arbitrage(self):
        """Solves the LP model and determines if there is an arbitrage.

        Returns: Bool
        """
        self.model.solve()
        return True if pulp.value(self.model.objective) else False
    
    def find_arbitrage(self):
        """Finds arbitrage if it exist.

        Returns:
            A dict with key being date and value being pulp.pulp.LpVariable if 
            an arbitrage exist or 0 otherwise.
        """
        if self.is_arbitrage():
            return {self.date : self.model.variables()}
        else:
            return {self.date : 0}