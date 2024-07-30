from summa import summaDriver

for key, value in summaParts.items():
    summaDriver(
        rawSummaTextAddress=f"C:/Users/jackk/Projects/summa/data/st_raw_{value['snakeName']}.txt",
        summaPartStr=value['str'],
        destinationDirectory=f"C:/Users/jackk/Projects/website/summa/{value['camelName']}/"
    )