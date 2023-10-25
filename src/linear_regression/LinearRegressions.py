import pandas as pd
import statsmodels.api as sm


class LinearRegressionSM:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self._model = None

    def fit(self):
        self.right_hand_side = sm.add_constant(self.right_hand_side)
        self._model = sm.OLS(self.left_hand_side, self.right_hand_side).fit()

    def get_params(self):
        params = self._model.params
        return pd.Series(params, name='Beta coefficients')

    def get_pvalues(self):
        pvalues = self._model.pvalues
        return pd.Series(pvalues, name='P-values for the corresponding coefficients')

    def get_wald_test_result(self, restrictions_matrix):
        result = self._model.wald_test(restrictions_matrix)
        f_value = result.statistic
        p_value = result.pvalue
        return 'F-value: ' + str(round(f_value, 3)) + ', P-value: ' + str(round(p_value, 3))

    def get_model_goodness_values(self):
        ars = self._model.rsquared_adj
        ak = self._model.aic / 100
        by = self._model.bic / 100
        return "Adjusted R-squares: " + str(round(ars, 3)) + ", Akaike IC: " + str(round(ak, 3)) + ", Bayes IC: " + str(round(by, 3))