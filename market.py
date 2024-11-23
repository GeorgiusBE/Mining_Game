# import libraries
import random

class Market:
    '''
    A class to generate SDPA coin and electricity market price

    ...

    Attributes
    ----------
    sdpa_price : float
        The market price of SDPA coin
    elec_price : float
        The per unit market price of electricity

    Methods
    -------
    new_sdpa_price()
        Generate SDPA market price
    new_elec_price()
        Generate per unit market price of electricity 
    '''

    def __init__(self):
        '''
        Initialize Market class with an initial SDPA coin price.
        '''
        
        # price of sdpa on day 1
        self.sdpa_price = 50
        pass
    
    # generate new sdpa price
    def new_sdpa_price(self):
        '''
        Generate SDPA coin market price.

        The coin's daily return is randomly generated from the Normal distribution
        with mean 0.01 and std. 0.005, i.e. N~(0.01, 0.005).
        
        Returns
        -------
        float
            The newly generated SDPA coin market price
        '''

        # generate new sdpa market price
        self.sdpa_price *= (1 + random.gauss(0.01, 0.005))
        return self.sdpa_price
    
    # generate new electricity unit price
    def new_elec_price(self):
        '''
        Generate per unit market price of electricity.

        The per unit market price of electricity is drawn from a Uniform distribution, i.e. U~(1.5, 3.5)
        
        Returns
        -------
        float
            The newly generated per unit market price of electricity
        '''

        self.elec_price = random.uniform(1.5, 3.5)
        return self.elec_price