import pandas as pd  
import math

class Mppt:
    def __init__(self, n1, n2, modules):
        self.n1 = n1
        self.n2 = n2
        self.modules = modules
        self.numbers, self.posibles_combinations = {}, {}
        self.Mo_1, self.string_1, self.Mo_2, self.string_2 = [], [], [], []
        self.extrations()

    def extrations(self):
        for n in range(self.n1, (int(math.ceil(self.modules/2)) + 1)):
            self.numbers[n] = (self.modules - n)

    def combinations(self, key, values):
        for mpp1 in range(1, (int(math.ceil(self.modules/self.n1)) + 1)):
            for mpp2 in range(1, (int(math.ceil(self.modules/self.n1)) + 1)):
                if ((key % mpp1 == 0) and (values % mpp2 == 0)) and (mpp1):
                    if (key/mpp1 >= self.n1 and key/mpp1 <= self.n2) and (values/mpp2 >= self.n1 and values/mpp2 <= self.n2):
                        if key/mpp1 == values/mpp2:
                            if round(key/mpp1) in self.Mo_1 and (mpp1 + mpp2) in self.string_1:
                                continue
                            self.Mo_1.append(round(key/mpp1))
                            self.string_1.append(mpp1 + mpp2)
                            self.Mo_2.append(0)
                            self.string_2.append(0)
                            #print(f"I Found one result: {key/mpp1} modules of {mpp1 + mpp2} strings")
                        else:
                            if key/mpp1 > values/mpp2:
                                self.Mo_1.append(round(key/mpp1))
                                self.string_1.append(mpp1)
                                self.Mo_2.append(round(values/mpp2))
                                self.string_2.append(mpp2)
                            else:
                                self.Mo_2.append(round(key/mpp1))
                                self.string_2.append(mpp1)
                                self.Mo_1.append(round(values/mpp2))
                                self.string_1.append(mpp2)
                            #print(f"I Found one result: {key/mpp1} modules of {mpp1} strings and {values/mpp2} modules of {mpp2} strings")

    def sorting(self):
        # assign data of lists.  
        data = {'Mo_1': self.Mo_1, 'string_1': self.string_1,
                'Mo_2': self.Mo_2, 'string_2': self.string_2}  
        
        # Create DataFrame  
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=None, keep="first", inplace=False)
        df = df.sort_values(by=['Mo_1', 'Mo_2', 'string_1', 'string_2'],ascending=False, ignore_index=True)
        return(df)
