import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


class TEMarket():
    """
    Class to create a Transactive Energy Market scenario.
    """

    def __init__(self,
                 hours=24,
                 min_players=10,
                 max_players=123,
                 min_price=8,
                 max_price=32,
                 min_bid=1,
                 max_bid=5):

        """
        Attributes:

        hours: Number of hours during which trading is possible.
        min_players: Minimum number of hourly transactions.
        max_players: Maximum number of hourly transactions.
        min_price: Minimum energy price in cents/KWh.
        max_price: Maximum energy price in cents/KWh.
        min_bid: Minimum value of the energy bid range.
        max_bid: Maximum value of the energy bid range.
        min_ask: Minimum value of the energy ask range.
        max_ask: Maximum value of the energy ask range.
        """

        self.hours = hours
        self.min_players = min_players
        self.max_players = max_players
        self.min_price = min_price
        self.max_price = max_price
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.min_ask = max_bid
        self.max_ask = 2*max_bid

    def data_generator(self,
                    loc=11.5,
                    scale=4.7,
                    size=15000
                    ):

        '''
        Generates a Pandas DataFrame with the specified parameters.
        
        Arguments:

        loc: Mean of the Gaussian distribution from which the data is generated.
        scale: Standard deviation of the Gaussian distribution from which the data is generated.
        size: Number of samples.

        return: Pandas DataFrame
        '''
        
        samples = np.random.normal(loc=loc, scale=scale, size=size)
        hours = np.arange(self.hours)
        min_value = self.min_players
        max_value = self.max_players

        participants_dict_per_hourdict={}
        for hour in hours:
            participants_dict_per_hourdict[f"{hour}"] = 0
            for sample in samples:
                if np.abs(sample - hour)<.5:
                    participants_dict_per_hourdict[f"{hour}"]+=1 
        participants_by_hour = np.asarray(list(participants_dict_per_hourdict.values()))
        participants_by_hour = participants_by_hour/np.max(participants_by_hour) * max_value

        #either we set the values below min_value to min_value or throw it a away
        #participants_by_hour[participants_by_hour<min_value] = 0
        #participants_by_hour = np.clip(participants_by_hour/np.max(participants_by_hour) * max_value, a_min=min_value, a_max=max_value)

        columns = ['Hour', 'Participant', 'Type', 'Price (cents/KWh)', 'Quantity (KW)']
        df = pd.DataFrame(columns=columns)

        # Generate bids and asks for each hour
        for hour in hours:
            num_prosumers = int(participants_by_hour[hour]//2)
            num_consumers = int(participants_by_hour[hour] - num_prosumers)


            if participants_by_hour[hour] >= min_value:
            # Generate prosumer bids
                prosumer_bids = pd.DataFrame({
                    'Hour': hour,
                    'Participant': np.arange(num_prosumers),
                    'Type': 'Bid',
                    'Price (cents/KWh)': np.random.uniform(self.min_price, self.max_price, size=num_prosumers),
                    'Quantity (KW)': np.random.uniform(self.min_bid, self.max_bid, size=num_prosumers)
                })

            # Generate consumer asks
                consumer_asks = pd.DataFrame({
                    'Hour': hour,
                    'Participant': np.arange(num_prosumers, num_prosumers + num_consumers),
                    'Type': 'Ask',
                    'Price (cents/KWh)': np.random.uniform(self.min_price, self.max_price, size=num_consumers),
                    'Quantity (KW)': np.random.uniform(self.min_ask, self.max_ask, size=num_consumers)
                })
            else:
                # Generate prosumer bids
                prosumer_bids = pd.DataFrame({
                    'Hour': hour,
                    'Participant': [None],
                    'Type': 'Bid',
                    'Price (cents/KWh)': 0,
                    'Quantity (KW)': 0
                })

            # Generate consumer asks
                consumer_asks = pd.DataFrame({
                    'Hour': hour,
                    'Participant': [None],
                    'Type': 'Ask',
                    'Price (cents/KWh)': 0,
                    'Quantity (KW)': 0
                })
            

            # Concatenate prosumer bids and consumer asks
            hour_data = pd.concat([prosumer_bids, consumer_asks], ignore_index=True)

            # Add the generated data to the main DataFrame
            df = pd.concat([df, hour_data], ignore_index=True)

            df["Participant"]
        # Sort the DataFrame based on hour and participant
        df.sort_values(by=['Hour', 'Participant'], inplace=True, ignore_index=True)

        return df


    def summary(self, df: DataFrame):
        """
        Writes a summary of the dataset.
        """

        print("Transactive Energy Market Summary\n")
        print("--------------------------------------\n")
        print(f"Number of samples: {len(df)}\n")
        print(f"Hourly Transactions Range: [{self.min_players}, {self.max_players}]\n")
        print(f"Price Range (cents/KWh): [{self.min_price}, {self.max_price}]\n")
        print(f"Bid Range (KWh): [{self.min_bid}, {self.max_bid}]")
        print(f"Ask Range (KWh): [{self.min_ask}, {self.max_ask}]")



if __name__ == "__main__":
    market = TEMarket()
    
    df = market.data_generator()

    market.summary(df)

    df_length_per_hour = df.groupby('Hour').size()
    df_length_per_hour[df_length_per_hour<10] = 0
    plt.bar(df_length_per_hour.index, df_length_per_hour.values, color='blue', alpha=0.7,edgecolor='black', label='data')
    plt.plot(df_length_per_hour.index,123*
              norm.pdf(df_length_per_hour.index, loc = 11.5, scale = 4.7)/
              max(norm.pdf(df_length_per_hour.index, loc = 11.5, scale = 4.7)),
              'r-', lw=5, alpha=0.6, label='Gaussian pdf')
    plt.legend()
    plt.xlabel('Hours')
    plt.ylabel('Number of Participants')
    plt.title('Number of Participants for Each Hour')
    plt.show()