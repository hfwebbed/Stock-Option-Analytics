
import scipy.stats as sct
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy


class PriceChangeSimulationService:

    def __init__(self,volatilityAnalysisService,plottingUtilService):
        self.volatilityAnalysisService = volatilityAnalysisService
        self.plottingUtilService = plottingUtilService

        self.dataframe_column = "Close"
        self.volatility_multiplier = math.sqrt(math.pi / 2)

        self.font = {'size': 7}
        self.alternate_colors =  ["green", "blue"]
        self.periods1 = 16
        self.periods2 = 1
        self.weeks_per_period = 3
        self.period2_simul_count = 100


    # v2
    def simmulate_price_change(self, df, weeks=60):

        self.plottingUtilService.clean_files("static/img/*.png")
        plot1_filename = self.plottingUtilService.generate_filename("static/img/graph",".png")
        plot2_filename = self.plottingUtilService.generate_filename("static/img/graph", ".png")

        last_close = df.iloc[0][self.dataframe_column]
        three_week_volatility = self.volatilityAnalysisService.calculate_volatility(df)["3week"]


        weeks_list = [0]
        prices = [last_close]
        for period in range(int(weeks / self.weeks_per_period) - 1):
            expected_3week_shift = prices[-1] * three_week_volatility / 100
            shift = expected_3week_shift * self.volatility_multiplier
            new_price = sct.norm.ppf(random.random(), prices[-1], shift)
            prices.append(round(new_price, 2))
            weeks_list.append(self.weeks_per_period * (period + 1))

        df = pd.DataFrame({"week": weeks_list , "prices":prices})

        self.draw_simul_plot(weeks_list, prices, plot1_filename)

        ####################################################################################

        expected_3week_shift = prices[-1] * three_week_volatility / 100
        shift = expected_3week_shift * self.volatility_multiplier
        stage2_prices = []
        for fp in range(self.period2_simul_count):
            final_price = sct.norm.ppf(random.random(), prices[-1], shift)
            stage2_prices.append(round(final_price, 2))

        w51_results = pd.DataFrame(data=stage2_prices, columns=["price"])
        w51_mean = float(w51_results.mean())
        w51_std = float(w51_results.std())
        self.draw_stdev_plot(stage2_prices, w51_mean, w51_std, plot2_filename)

        return plot1_filename, plot2_filename, stage2_prices


    def draw_simul_plot(self,x , y , filename):
        plt.rcParams["figure.figsize"] = (16, 6)
        plt.clf()
        plt.plot()
        plt.xlabel('weeks')
        plt.ylabel('price')
        plt.plot(x, y, color="#FF0000", markersize=4, marker="o")

        # calc the trendline
        polyfit = numpy.polyfit(x, y, 1)
        fx = numpy.poly1d(polyfit)
        plt.plot(x, fx(x), "b--")

        plt.xticks(x)

        ylim = plt.ylim()
        xlim = plt.xlim()
        axes = plt.gca()
        axes.set_ylim([ylim[0] - 5, ylim[1] + 5])
        axes.set_xlim([-2, xlim[1] + 1.5])
        label_x = plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) * 0.02

        xlab = [0]
        for pos in x:
            xlab.append(pos + self.weeks_per_period)

        for i in range(len(x)):
            plt.text(xlab[i], label_x, str(y[i]), fontdict=self.font, color=self.alternate_colors[i % 2], horizontalalignment='center')
        plt.savefig(filename)


    def draw_stdev_plot(self, prices, center_at, stdev_step, filename):

        price_buckets = []
        for std in range(-3, 4):
            bucket_top = center_at + std * stdev_step
            price_buckets.append(bucket_top)

        price_buckets.append(center_at + 6 * stdev_step)
        stdev_buckets = [0] * len(price_buckets)
        for price in prices:
            for pos, price_bucket in enumerate(price_buckets):
                if price < price_bucket:
                    stdev_buckets[pos] += 1
                    break

        keys2 = []
        for key in price_buckets:
            keys2.append(key - stdev_step * 0.75)

        plt.clf()
        plt.plot()
        plt.xlabel('stdevs away from avg')
        plt.ylabel('number of simmulations')
        plt.xticks(price_buckets)
        plt.bar(keys2, stdev_buckets, stdev_step * 0.5, color='r')
        axes = plt.gca()
        axes.set_xlim([center_at - 4 * stdev_step, center_at + 4 * stdev_step])
        plt.savefig(filename)

    # just quick and dirty verion ...
    """
    # old version
    def simmulate_price_change(self,df):

        import glob
        import os

        files = glob.glob('static/img/*.png')
        for filename in files:
            os.unlink(filename)


        filename1 = "static/img/graph" + str(random.randint(100000000, 999999999)) + ".png"
        filename2 = "static/img/graph" + str(random.randint(100000000, 999999999)) + ".png"

        last_close = df.iloc[0]['Close']

        #calculate mean for last year

        year_df = df[0:251]["Close"]
        avg = year_df.mean()
        stdev = year_df.std()
        price = last_close


        #print("avg",avg,"stdev",stdev,"price" ,price)

        graph_xlab = [-1.5]
        graph_x = [0]
        graph_y = [price]
        for iter in range(16):
            devi = stdev * price / avg
            price = sct.norm.ppf(random.random(), price, devi)
            graph_y.append(round(price,2))
            graph_x.append(3 * (iter + 1))
            graph_xlab.append(3 * (iter + 0.5))

        plt.clf()
        plt.plot()
        plt.xlabel('weeks')
        plt.ylabel('price')
        plt.plot(graph_x, graph_y, color="#FF0000",markersize=4,marker="o")

        plt.xticks(graph_x)

        font = {'family': 'normal',
                'size': 7}
        ylim = plt.ylim()
        xlim = plt.xlim()
        axes = plt.gca()
        axes.set_ylim([ylim[0] - 5, ylim[1] + 5])
        axes.set_xlim([xlim[0] - 1.5 , xlim[1]])
        bot = plt.ylim()[0] * 1.02

        colors = ["green","blue"]
        for i in range(len(graph_x)):
            plt.text(graph_xlab[i], bot , str(graph_y[i]), fontdict=font , color= colors[i % 2])
        plt.savefig(filename1)


        final_prices = []
        devi = stdev * price / avg
        for fp in range(100):
            final_price = sct.norm.ppf(random.random(), price, devi)
            final_prices.append(round(final_price,2))

        stdev_archetypes = {-3:0 , -2:0 , -1:0 , 0:0 , 1:0 , 2:0 , 3:0}
        for price in final_prices:
            ac = (price - last_close) / stdev
            ac = math.trunc(ac)
            if ac < -4:
                ac = -4
            if ac > 3:
                ac = 3

            if ac not in stdev_archetypes:
                stdev_archetypes[ac] = 0
            stdev_archetypes[ac] += 1

        keys = stdev_archetypes.keys()
        keys2 = []
        for key in keys:
            keys2.append(key + 0.25)

        plt.clf()
        plt.plot()
        plt.xlabel('stdevs away from avg')
        plt.ylabel('count of simmulations')
        plt.bar(keys2, stdev_archetypes.values(), 0.5, color='r')
        plt.savefig(filename2)


        return filename1,filename2,final_prices
    """
