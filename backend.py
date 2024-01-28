from data.data_gen import data_generator



if __name__ == "__main__":
    df = data_generator()

    df_length_per_hour = df.groupby('Hour').size()
    df_length_per_hour[df_length_per_hour<10] = 0
    print(df_length_per_hour.describe(include='all'))
