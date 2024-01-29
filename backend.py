from data.data_gen import TEMarket



if __name__ == "__main__":
    market = TEMarket()
    
    df = market.data_generator()

    market.summary(df)
