from data.data_gen import TEMarket



if __name__ == "__main__":
    market = TEMarket()
    
    df = market.data_generator()

    df_length_per_hour = df.groupby('Hour').size()
    df_length_per_hour[df_length_per_hour<10] = 0
    market.summary(df_length_per_hour)
