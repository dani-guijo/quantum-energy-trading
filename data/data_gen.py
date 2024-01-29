import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm



def data_generator(loc=11.5,
                   scale=4.7,
                   size=15000,
                   hours=24,
                   min_value=10,
                   max_value=123,
                   price_min=8,
                   price_max=32,
                   quant_min=1,
                   quant_max=5
                   ):

    '''
    Generates a Pandas DataFrame with the specified parameters.
    
    Arguments:

    loc: Mean of the Gaussian distribution from which the data is generated.
    scale: Standard deviation of the Gaussian distribution from which the data is generated.
    size: Number of samples
    hours: Number of hours during which trading is possible.
    min_value: Minimum number of hourly transactions.
    max_value: Maximum number of hourly transactions.
    price_min: Minimum energy price in cents/KWh.
    price_max: Maximum energy price in cents/KWh.
    quant_min: Minimum value of the energy bid range.
    quant_max: Maximum value of the energy bid range.

    return: Pandas DataFrame

    '''
    
    samples = np.random.normal(loc=loc, scale=scale, size=size)
    hours = np.arange(hours)
    min_value = min_value
    max_value = max_value

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
                'Price (cents/KWh)': np.random.uniform(price_min, price_max, size=num_prosumers),
                'Quantity (KW)': np.random.uniform(quant_min, quant_max, size=num_prosumers)
            })

        # Generate consumer asks
            consumer_asks = pd.DataFrame({
                'Hour': hour,
                'Participant': np.arange(num_prosumers, num_prosumers + num_consumers),
                'Type': 'Ask',
                'Price (cents/KWh)': np.random.uniform(price_min, price_max, size=num_consumers),
                'Quantity (KW)': np.random.uniform(quant_min, quant_max, size=num_consumers)
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



if __name__ == "__main__":
    df = data_generator()

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