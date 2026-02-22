import pandas as pd

def preprocessing(line,classification):
   data = {"processed_log": line, "classfication":classification}
   df = pd.DataFrame([data])
   df.to_csv('data/combined_dataset.csv', sep = "|", index = False, header= False, mode = "a")
   df.to_csv('data/juice_shop.csv', sep = "|", index = False, header= False, mode = "a")