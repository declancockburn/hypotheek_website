
import pandas as pd
import numpy as np


class CalcMortgage():

    principal = 260000
    int_rate = 2.1
    years = 30
    # principal = FloatField("Mortgage Amount")
    # int_rate = FloatField("Interest Rate %")
    # years = IntegerField("Years")
    # submit = SubmitField('Calculate')
    # start_date = DateField("Start Date", id='datepick')

    #todo make a date field

    def __init__(self):
        self.df_lin = None
        self.df_ann = None
        self.total_lin = None
        self.total_ann = None
        self.int_rate /= 100
        self.calc_linear()
        self.calc_ann()
        print(self.df_ann.head(10))

    def calc_linear(self):
        p = self.principal
        n = self.years
        payment = round(p / (n * 12), 2)
        total = 0
        df_data = []
        for m in range(n * 12):
            interest = round((p / 12) * self.int_rate, 2)
            df_data.append([m + 1, p, payment, interest, interest + payment])
            p = round(p - payment, 2)
            total += round(payment + interest, 2)
        self.df_lin = pd.DataFrame(data=df_data, columns=["Month", "Principal", "Deduction", "Interest", "Monthly_Pay"])
        new_order = ["Month", "Principal", "Monthly_Pay", "Deduction", "Interest"]
        self.df_lin = self.df_lin[new_order]
        self.total_lin = np.sum(self.df_lin["Monthly_Pay"])
        # return f"Total = {final}<br><br>{df.to_html()}"

    def calc_ann(self):
        """
        formula:
        PV = R (1-(1+i)**(-n))/i
        PV = present value
        R = repayment cost
        n = number of repayments
        i = interest (per repayment)
        """
        rep_cost = self.principal

        p = self.principal
        i = self.int_rate / 12
        n = self.years * 12

        rep_cost = p / (
                (1 - (1 + i) ** (-n)) / i
        )
        p_after = rep_cost * (1 - (1 + i) ** (-(n - 1))) / i
        data = [[p, rep_cost, p_after]]
        for m in range(n - 1, 0, -1):
            pv = rep_cost * (1 - (1 + i) ** (-m)) / i
            pv_after = rep_cost * (1 - (1 + i) ** (-(m - 1))) / i
            data.append([pv, rep_cost, pv_after])
            print(pv)

        df = pd.DataFrame(data, columns=["Principal", "Monthly_Pay", "Prn_After"])
        df["Deduction"] = df["Principal"] - df["Prn_After"]
        df["Interest"] = df["Monthly_Pay"] - df["Deduction"]
        df.drop("Prn_After", axis=1, inplace=True)
        df["Month"] = df.index.values + 1
        new_order = ["Month", "Principal", "Monthly_Pay", "Deduction", "Interest"]
        self.df_ann = df[new_order]
        self.df_ann = self.df_ann.round(2)
        self.total_ann = np.sum(self.df_ann["Monthly_Pay"])


c = CalcMortgage()
lin = c.df_lin
ann = c.df_ann

tot_lin = c.total_lin
tot_ann = c.total_ann
# ##
# import pandas as pd
#
#
# p = 300000
# i = 2.1
# n = 30
#
# n = n*12
# i = (i/100)/12
# rep_cost = p / (
#         (1 - (1 + i) ** (-n)) / i
# )
# p_after = rep_cost*(1 - (1+i)**(-(n-1)))/i
# data = [[p, rep_cost, p_after]]
# for m in range(n-1, 0, -1):
#     pv = rep_cost*(1 - (1+i)**(-m))/i
#     pv_after = rep_cost*(1 - (1+i)**(-(m-1)))/i
#     data.append([pv, rep_cost, pv_after])
#     print(pv)
#
# df = pd.DataFrame(data, columns=["Principal", "Monthly_Pay", "Prn_After"])
# df["Deduction"] = df["Principal"] - df["Prn_After"]
# df["Interest"] = df["Monthly_Pay"] - df["Deduction"]
# df["month"] = df.index.values + 1
#
#
