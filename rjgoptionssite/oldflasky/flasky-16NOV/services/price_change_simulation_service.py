
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

    ######################

    def get_simmulation_data(self, df, weeks=60):
        weeks_list, prices, three_week_volatility = self.calculate_simmulate_price_change(df, weeks)
        start,low,median,high = self.calculate_prediction_stats(prices)
        return {"start":start,"low":low,"median":median,"high":high,"weeks":weeks_list,"prices":prices}
        #stage2_prices, lastw_mean, lastw_std = self.calculate_stdev(prices, three_week_volatility)



    def get_simmulation_plots(self, df, weeks=60):
        self.plottingUtilService.clean_files("static/img/*.png")
        plot1_filename = self.plottingUtilService.generate_filename("static/img/graph", ".png")
        plot2_filename = self.plottingUtilService.generate_filename("static/img/graph", ".png")

        weeks_list, prices, three_week_volatility =  self.calculate_simmulate_price_change(df, weeks)
        stage2_prices, lastw_mean, lastw_std = self.calculate_stdev(prices, three_week_volatility)

        self.draw_simul_plot(weeks_list,prices,plot1_filename)
        self.draw_stdev_plot(stage2_prices, lastw_mean, lastw_std, plot2_filename)
        return plot1_filename, plot2_filename, stage2_prices


    def calculate_prediction_stats(self,prices):
        prediction_start = prices[0]
        prediction_high = prediction_start
        prediction_low = prediction_start
        sum = 0
        for price in prices:
            sum += price
            if price < prediction_low:
                prediction_low = price
            if price > prediction_high:
                prediction_high = price
        prediction_median = sum / len(prices)

        return prediction_start,prediction_low,prediction_median,prediction_high

    def calculate_simmulate_price_change(self, df, weeks=60):

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
        return weeks_list,prices,three_week_volatility


    def calculate_stdev(self,prices,three_week_volatility):
        expected_3week_shift = prices[-1] * three_week_volatility / 100
        shift = expected_3week_shift * self.volatility_multiplier
        stage2_prices = []
        for fp in range(self.period2_simul_count):
            final_price = sct.norm.ppf(random.random(), prices[-1], shift)
            stage2_prices.append(round(final_price, 2))

        lastw_results = pd.DataFrame(data=stage2_prices, columns=["price"])
        lastw_mean = float(lastw_results.mean())
        lastw_std = float(lastw_results.std())
        return stage2_prices,lastw_mean,lastw_std

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


