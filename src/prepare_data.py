import pandas as pd
import numpy as np

def clean_and_prepare_data(input_path="data/vgsales.csv", output_path="data/vgsales_cleaned.csv"):
    df = pd.read_csv(input_path)
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]
    df = df.dropna(subset=['Year']).copy()
    df['Year'] = df['Year'].astype(int)
    df = df[(df['Year'] >= 1980) & (df['Year'] <= 2017)]

    def get_manufacturer(platform):
        nintendo = ['NES', 'SNES', 'N64', 'GC', 'Wii', 'WiiU', 'GB', 'GBA', 'DS', '3DS']
        sony = ['PS', 'PS2', 'PS3', 'PS4', 'PSP', 'PSV']
        microsoft = ['XB', 'X360', 'XOne']
        sega = ['GEN', 'SAT', 'DC', 'GG', 'SCD']
        pc = ['PC']
        if platform in nintendo:
            return 'Nintendo'
        elif platform in sony:
            return 'Sony'
        elif platform in microsoft:
            return 'Microsoft'
        elif platform in sega:
            return 'Sega'
        elif platform in pc:
            return 'PC'
        else:
            return 'Outros'

    df['Manufacturer'] = df['Platform'].apply(get_manufacturer)
    df['Decade'] = (df['Year'] // 10) * 10
    df['Decade_Label'] = df['Decade'].astype(str) + "s"

    def get_generation(year):
        if year < 1983:
            return "2ª Geração (Atari 2600)"
        elif year < 1987:
            return "3ª Geração (8-bits / NES)"
        elif year < 1993:
            return "4ª Geração (16-bits / SNES / Mega Drive)"
        elif year < 1998:
            return "5ª Geração (32/64-bits / PS1 / N64)"
        elif year < 2005:
            return "6ª Geração (PS2 / Xbox / GameCube)"
        elif year < 2012:
            return "7ª Geração (PS3 / X360 / Wii)"
        else:
            return "8ª Geração (PS4 / XOne / WiiU)"

    df['Generation'] = df['Year'].apply(get_generation)
    df.to_csv(output_path, index=False)

    plat_year = df.groupby(['Platform', 'Manufacturer', 'Year'])['Global_Sales'].sum().reset_index()
    piv_plat = plat_year.pivot(index=['Platform', 'Manufacturer'], columns='Year', values='Global_Sales').fillna(0).cumsum(axis=1).reset_index()
    piv_plat.rename(columns={'Platform': 'Plataforma', 'Manufacturer': 'Fabricante'}, inplace=True)
    piv_plat.to_csv('data/flourish_bar_chart_race_platforms.csv', index=False)

    pub_year = df.groupby(['Publisher', 'Year'])['Global_Sales'].sum().reset_index()
    top_pubs = df.groupby('Publisher')['Global_Sales'].sum().nlargest(15).index
    pub_filtered = pub_year[pub_year['Publisher'].isin(top_pubs)]
    piv_pub = pub_filtered.pivot(index='Publisher', columns='Year', values='Global_Sales').fillna(0).cumsum(axis=1).reset_index()
    piv_pub.rename(columns={'Publisher': 'Publicadora'}, inplace=True)
    piv_pub.to_csv('data/flourish_bar_chart_race_publishers.csv', index=False)

    return df

if __name__ == "__main__":
    clean_and_prepare_data()
