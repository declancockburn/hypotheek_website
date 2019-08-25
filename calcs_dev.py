
import pandas as pd
import numpy as np

# TODO: make a bunch of options. BTR, first house vs renting savings... how to structure

# TODO: Make a start month.
# TODO: Make a mortgage interest deduction based on time
# TODO: Make a summary sheet, and explanation

#later:
# TODO: make a box 3 subtraction, networth.
# TODO: make a box 1 subtraction, house value.

# Questions/options: Can you deduct mo

# TODO: fix savings


class CalcMortgage:
    house_init_value = 310000
    house_value_appreciation_rate = 1
    own_payment = 34000
    principal_mortg = 290000
    mrtg_int_rate = 1.6

    savings_per_month = 0
    ETF_int_rate = 7
    years = 30

    init_rent_pm = 1000
    rent_appreciation = 2

    start_date = pd.to_datetime("November 2019")
    # principal_mortg = FloatField("Mortgage Amount")
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
        self.princ_compnd_factor = None
        self.compnd_monthly = None
        self.mrtg_int_rate /= 100
        self.house_value = self.calc_house_val()
        self.calc_linear()
        self.calc_ann()
        self.etf_invst_factors()

    def calc_rental(self):
        y = self.years
        rent = self.init_rent_pm
        i = self.rent_appreciation / 100 + 1
        t = [x for x in np.arange(1 / 12, y + 1 / 12, 1 / 12)]

        counter = 1
        rent_lst = []
        for n in t:
            rent_lst.append(rent)
            if counter % 12 == 0:
                rent *= i
            counter += 1
        return rent_lst

    @staticmethod


    @staticmethod
    def calc_interest_deduction(value, year, interest_payment):
        def calc_property_tax(v, y):
            tax = v * 0.65 / 100
            reduction = 1 - (y - 2019) * 0.0333
            return tax * reduction / 100

        """49% of what?"""
        deductible = interest_payment - calc_property_tax(value, year) / 12
        print(deductible)
        rate = 49 - (year - 2019) * 3
        print(rate)
        if rate > 0:
            return (deductible * rate / 100) * 0.52
        else:
            return 0
        # TODO needs work




    def calc_house_val(self):
        y = self.years
        i = self.house_value_appreciation_rate / 100
        val = self.house_init_value
        # Make a list of months
        t = [x for x in np.arange(1 / 12, y + 1 / 12, 1 / 12)]
        house_val_lst = []
        # For each month, add on the monthly interest of the current house value.
        for m in t:
            house_val_lst.append(val)
            val = val*(1 + i/12)
        return house_val_lst

    def calc_ann(self):
        """
        formula:
        PV = r (1-(1+i)**(-n))/i
        PV = present value (i.e. mortgage principal)
        r = repayment cost
        n = number of repayments
        i = interest (per repayment)
        """
        p = self.principal_mortg
        i = self.mrtg_int_rate / 12
        n = self.years * 12
        r = p / (
                (1 - (1 + i) ** (-n)) / i
        )
        # "principal after" monthly payment, this is used to calculate mortgage deduction
        p_after = r * (1 - (1 + i) ** (-(n - 1))) / i
        data = [[p, r, p_after]]
        for m in range(n - 1, 0, -1):
            pv = r * (1 - (1 + i) ** (-m)) / i
            pv_after = r * (1 - (1 + i) ** (-(m - 1))) / i
            data.append([pv, r, pv_after])

        df = pd.DataFrame(data, columns=["Mrtg_Principal", 'Monthly_Mrtg_Pay', "Prn_After"])
        df["Mrtg_Deduction_payment"] = df["Mrtg_Principal"] - df["Prn_After"]
        df["Mrtg_Interest_payment"] = df['Monthly_Mrtg_Pay'] - df["Mrtg_Deduction_payment"]
        df.drop("Prn_After", axis=1, inplace=True)
        df["Month#"] = df.index.values + 1
        new_order = ["Month#", "Mrtg_Principal", 'Monthly_Mrtg_Pay', "Mrtg_Deduction_payment", "Mrtg_Interest_payment"]
        self.df_ann = df[new_order]
        self.df_ann = self.df_ann.round(2)
        self.total_ann = np.sum(self.df_ann['Monthly_Mrtg_Pay'])

    def calc_linear(self):
        p = self.principal_mortg
        n = self.years
        payment = round(p / (n * 12), 2)
        total = 0
        df_data = []
        for m in range(n * 12):
            interest = round((p / 12) * self.mrtg_int_rate, 2)
            df_data.append([m + 1, p, payment, interest, interest + payment])
            p = round(p - payment, 2)
            total += round(payment + interest, 2)
        self.df_lin = pd.DataFrame(data=df_data, columns=["Month#", "Mrtg_Principal", "Mrtg_Deduction_payment", "Mrtg_Interest_payment", 'Monthly_Mrtg_Pay'])
        new_order = ["Month#", "Mrtg_Principal", "Mrtg_Deduction_payment", "Mrtg_Interest_payment", 'Monthly_Mrtg_Pay']
        self.df_lin = self.df_lin[new_order]
        self.total_lin = np.sum(self.df_lin['Monthly_Mrtg_Pay'])
        # return f"Total = {final}<br><br>{df.to_html()}"
        #todo: add bruto vs netto

    def etf_invst_factors(self):
        y = self.years
        r = self.ETF_int_rate / 100
        n = 12
        A = []
        X = []
        for t in np.arange(1/12,y+1/12,1/12):
            A.append((1 + r/n)**(n*t))
            X.append((((1 + r/n)**(n*t) - 1) / (r/n)) * (1+r/n))
        self.princ_compnd_factor = A
        self.compnd_monthly = X

        # test = [x for x in range(len(A))]
        # t2 = pd.Series(test)*pd.Series(X)
        # print()
        # self.df_ann = self.bring_dfs_together(self.df_ann)
        # self.df_lin = self.bring_dfs_together(self.df_lin)
        """
        A = P (1 + r/n)**(nt)
        A = the future value of the investment/loan, including interest
        P = the principal investment amount (the initial deposit or loan amount)
        r = the annual interest rate (decimal)
        n = the number of times that interest is compounded per unit t
        t = the time the money is invested or borrowed for
        
        per month cont: A + PMT × {[(1 + r/n)**(nt) - 1] / (r/n)} × (1+r/n)
        """

    def compound_savings(self, in_list):
        out_list = [(0 if in_list[0] < 1 else in_list[0])]
        prev_amount_orig = out_list[0]
        prev_amount = out_list[0]
        for amount in in_list:
            if prev_amount > 0:
                new_amount = prev_amount * (1 + (self.ETF_int_rate / 100) / 12) + (amount - prev_amount_orig)
                out_list.append(new_amount)
                prev_amount = new_amount
                prev_amount_orig = amount
            else:
                out_list.append(0)
                prev_amount_orig = amount
                prev_amount = amount
        return out_list[1:]


class FirstHouse(CalcMortgage):
    """This compares buying first house vs renting over many years"""
    house_init_value = 305000
    # This number includes
    house_value_appreciation_rate = 1
    # Here all own payment: downpayment, fees etc.
    own_payment = 5000+16500+2000+13800
    principal_mortg = 285000
    mrtg_int_rate = 1.54

    init_rent_pm = 1000
    rent_appreciation = 2

    savings_per_month = 0
    ETF_int_rate = 7
    years = 30

    def __init__(self):
        super().__init__()
        self.bring_dfs_together(self.df_lin)
        self.bring_dfs_together(self.df_ann)
        self.summary = self.gather_results()

    def bring_dfs_together(self, df):
        A = self.princ_compnd_factor
        X = self.compnd_monthly
        dp = [self.own_payment] * len(df)
        # df['NM_if_savings_invested'] = pd.Series([self.savings_per_month]*len(df)) * X
        # df['NM_total_savings'] = df['NM_if_downpayment_invstd'] + df['NM_if_savings_invested']

        # df['M_rent_minus_mrtg_plus_savings'] = df['Rent'] - df['Monthly_Mrtg_Pay'] + [self.savings_per_month]*len(df)
        # temp_rent_delta_series = [v if v > 0 else 0 for v in df['M_rent_minus_mrtg_plus_savings'].values]
        # temp_rent_delta_series = pd.Series(temp_rent_delta_series)
        # df['M_rent_delta_savings_invstd'] = temp_rent_delta_series * pd.Series(X)
        # df['M_rent_delta_savings_invstd'] = df['M_rent_minus_mrtg_plus_savings'] * pd.Series(X)
        df['rent_monthly_pay'] = self.calc_rental()
        df['rent_minus_mrtg'] = df['rent_monthly_pay'] - df['Monthly_Mrtg_Pay']
        # df['M_monthly_delta'] = df['rent_minus_mrtg']
        df['M_house_value'] = self.calc_house_val()
        df['M_house_value_owned'] = df['M_house_value'] - df['Mrtg_Principal']
        df['M_delta_reg_savings'] = df['rent_minus_mrtg'].cumsum()
        # Make the reg savings compound with interest rate. P
        df["M_savings_compounded"] = self.compound_savings(df['M_delta_reg_savings'].values)
        df['M_net_worth'] = df['M_house_value_owned'] + df["M_savings_compounded"]
        df['NM_if_downpayment_invstd'] = pd.Series(A) * pd.Series(dp)
        # df['M_total_net_worth'] = df['M_rent_delta_savings_invstd'] + df['M_house_value_owned']
        return df.round(2)

    def gather_results(self):
        ann = self.df_ann
        lin = self.df_lin
        x = (ann["M_net_worth"] - ann["NM_if_downpayment_invstd"])
        y = (lin["M_net_worth"] - lin["NM_if_downpayment_invstd"])
        ann_be = round(x[x>0].index[0]/12, 1)
        lin_be = round(y[y>0].index[0]/12, 1)

        df = pd.DataFrame(data=[
            ["<<INPUTS>>", None],
            ["House Initial Value", self.house_init_value],
            ["House Appreciation Rate %", self.house_value_appreciation_rate],
            ["Own Payment", self.own_payment],
            ["Mortgage Amount", self.principal_mortg],
            ["Mortgage Interest Rate %", self.mrtg_int_rate * 100],
            ["", None],
            ["Average initial rent pm", self.init_rent_pm],
            ["Rent increase % per year", self.rent_appreciation],
            ["", None],
            ["Expected ETF return rate %", self.ETF_int_rate],
            ["Regular Monthly Savings (in any case)", self.savings_per_month],
            ["Number of years", self.years],
            ["", None],
            ["<<RESULTS>>", None],
            ["INVESTING ONLY: This assumes no other networth other than \"Down payment\" + regular savings", None],
            [f"Net worth after {self.years} years, saving \"annuity\" payments", ann['NM_if_downpayment_invstd'].values[-1]],
            [f"Networth after {self.years} years, saving \"linear\" payments", lin['NM_if_downpayment_invstd'].values[-1]],
            ["", None],
            ["BTR ONLY: This assumes any rent (minus mortgage) profits get invested in ETFs, and includes property value", None],
            [f"Net worth after {self.years} years, with \"annuity\" mortgage", ann['M_net_worth'].values[-1]],
            [f"Net worth after {self.years} years, with \"linear\" mortgage", lin['M_net_worth'].values[-1]],
            ["Break even point Annuity", f"{ann_be} years"],
            ["Break even point Linear", f"{lin_be} years"]
        ])
        return df


class SecondHouse(CalcMortgage):
    """This compares buying a 2nd house and renting it vs investing money"""

    house_init_value = 310000
    house_value_appreciation_rate = 1

    down_payment = 34000
    principal_mortg = 290000
    mrtg_int_rate = 1.6

    init_rent_pm = 1
    rent_appreciation = 0

    savings_per_month = 0
    ETF_int_rate = 7
    years = 30

    def __init__(self):
        super().__init__()
        self.calc_rental()
        self.calc_savings()
        self.gather_results()

    def calc_rental(self):
        y = self.years
        rent = self.init_rent_pm
        i = self.rent_appreciation / 100 + 1
        t = [x for x in np.arange(1 / 12, y + 1 / 12, 1 / 12)]

        counter = 1
        rent_lst = []
        for n in t:
            rent_lst.append(rent)
            if counter % 12 == 0:
                rent *= i
            counter += 1
        return rent_lst
        self.df_ann['Rent'] = rent_lst
        self.df_lin['Rent'] = rent_lst

    def bring_dfs_together(self, df):
        A = self.princ_compnd_factor
        X = self.compnd_monthly
        dp = [self.down_payment]*len(df)
        df['NM_if_downpayment_invstd'] = pd.Series(A) * pd.Series(dp)
        df['NM_if_savings_invested'] = pd.Series([self.savings_per_month]*len(df)) * X
        df['NM_total_savings'] = df['NM_if_downpayment_invstd'] + df['NM_if_savings_invested']

        df['M_rent_minus_mrtg_plus_savings'] = df['Rent'] - df['Monthly_Mrtg_Pay'] + [self.savings_per_month]*len(df)
        # temp_rent_delta_series = [v if v > 0 else 0 for v in df['M_rent_minus_mrtg_plus_savings'].values]
        # temp_rent_delta_series = pd.Series(temp_rent_delta_series)
        # df['M_rent_delta_savings_invstd'] = temp_rent_delta_series * pd.Series(X)
        df['M_rent_delta_savings_invstd'] = df['M_rent_minus_mrtg_plus_savings'] * pd.Series(X)
        df['M_house_value'] = self.calc_house_val()
        df['M_house_value_owned'] = df['M_house_value'] - df['Mrtg_Principal']
        df['M_total_net_worth'] = df['M_rent_delta_savings_invstd'] + df['M_house_value_owned']
        return df.round(2)

    def gather_results(self):
        ann = self.df_ann
        lin = self.df_lin
        x = (ann["M_total_net_worth"] - ann["NM_total_savings"])
        y = (lin["M_total_net_worth"] - lin["NM_total_savings"])
        ann_be = round(x.index[0]/12, 1)
        lin_be = round(y.index[0]/12, 1)

        df = pd.DataFrame(data=[
            ["<<INPUTS>>", None],
            ["House Initial Value", self.house_init_value],
            ["House Appreciation Rate %", self.house_value_appreciation_rate],
            ["Down Payment", self.down_payment],
            ["Mortgage Amount", self.principal_mortg],
            ["Mortgage Interest Rate %", self.mrtg_int_rate * 100],
            ["", None],
            ["Average initial rent pm", self.init_rent_pm],
            ["Rent increase % per year", self.rent_appreciation],
            ["", None],
            ["Expected ETF return rate %", self.ETF_int_rate],
            ["Regular Monthly Savings (in any case)", self.savings_per_month],
            ["Number of years", self.years],
            ["", None],
            ["<<RESULTS>>", None],
            ["INVESTING ONLY: This assumes no other networth other than \"Down payment\" + regular savings", None],
            [f"Net worth after {self.years} years, saving \"annuity\" payments", ann['NM_total_savings'].values[-1]],
            # [f"Networth after {self.years} years, saving \"linear\" payments", lin['NM_total_savings'].values[-1]],
            ["", None],
            ["BTR ONLY: This assumes any rent (minus mortgage) profits get invested in ETFs, and includes property value", None],
            [f"Net worth after {self.years} years, with \"annuity\" mortgage", ann['M_total_net_worth'].values[-1]],
            [f"Net worth after {self.years} years, with \"linear\" mortgage", lin['M_total_net_worth'].values[-1]],
            ["Break even point Annuity", f"{ann_be} years"],
            ["Break even point Linear", f"{lin_be} years"]
        ])

        # with pd.ExcelWriter('output.xlsx') as writer:
        writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
        df.to_excel(writer, "Summary")
        self.df_ann.to_excel(writer, "Annuity")
        self.df_lin.to_excel(writer, "Linear")
        workbook = writer.book
        worksheet = writer.sheets["Summary"]
        # set the column width as per your requirement
        worksheet.set_column('B:B', 50)
        worksheet = writer.sheets["Annuity"]
        worksheet.set_column('C:O', 15)
        worksheet.set_column('D:E', 20)
        worksheet.set_column('H:O', 25)
        worksheet = writer.sheets["Linear"]
        worksheet.set_column('C:O', 15)
        worksheet.set_column('D:E', 20)
        worksheet.set_column('H:O', 25)
        writer.save()


c = FirstHouse()
lin = c.df_lin
ann = c.df_ann

tot_lin = c.total_lin
tot_ann = c.total_ann
summary = c.summary

# with open('inputs.txt'):







# ## ann.to_excel("160k_annuity_2.82.xlsx")
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
# df = pd.DataFrame(data, columns=["Mrtg_Principal", 'Monthly_Mrtg_Pay', "Prn_After"])
# df["Mrtg_Deduction_payment"] = df["Mrtg_Principal"] - df["Prn_After"]
# df["Mrtg_Interest_payment"] = df['Monthly_Mrtg_Pay'] - df["Mrtg_Deduction_payment"]
# df["Month#"] = df.index.values + 1
#
#
