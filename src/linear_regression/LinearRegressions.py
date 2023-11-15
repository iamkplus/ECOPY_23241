import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy.stats import f, t
from pathlib import Path


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
        f_value = result.statistic.item()
        p_value = result.pvalue.item()
        return f'F-value: {f_value:.2f}, p-value: {p_value:.3f}'

    def get_model_goodness_values(self):
        ars = self._model.rsquared_adj
        ak = self._model.aic
        by = self._model.bic
        return f"Adjusted R-squared: {ars:.3f}, Akaike IC: {ak:.2e}, Bayes IC: {by:.2e}"

class LinearRegressionNP:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self._model = None

    def fit(self):
        ones_column = np.ones((len(self.right_hand_side), 1))
        self.right_hand_side = np.concatenate((ones_column, self.right_hand_side), axis=1)

        XTX_inv = np.linalg.inv(np.dot(self.right_hand_side.T, self.right_hand_side))
        beta = np.dot(np.dot(XTX_inv, self.right_hand_side.T), self.left_hand_side)
        residuals = self.left_hand_side - np.dot(self.right_hand_side, beta)
        sigma_squared = np.sum(residuals ** 2) / (len(self.left_hand_side) - self.right_hand_side.shape[1])
        se = np.sqrt(np.diagonal(sigma_squared * XTX_inv))
        t_stat = beta / se
        p_values = 2 * (1 - f.cdf(np.abs(t_stat), len(self.left_hand_side) - self.right_hand_side.shape[1],
                                  len(self.left_hand_side) - len(beta)))
        self._model = {'beta': beta, 'se': se, 't_stat': t_stat, 'p_values': p_values}

    def get_params(self):
        params = self._model['beta']
        return pd.Series(params, name='Beta coefficients')

    def get_pvalues(self):
        t_stat = self._model['t_stat']
        df = len(self.left_hand_side) - self.right_hand_side.shape[1]
        p_values = 2 * (1 - t.cdf(np.abs(t_stat), df))
        return pd.Series(p_values, name='P-values for the corresponding coefficients')

    def get_wald_test_result(self, R):
        r = np.transpose(np.zeros((len(R))))
        term_1 = np.dot(R, self._model['beta']) - r
        term_2 = np.dot(np.dot(R, np.linalg.inv(np.dot(self.right_hand_side.T, self.right_hand_side))), np.transpose(R))
        XTX_inv = np.linalg.inv(np.dot(self.right_hand_side.T, self.right_hand_side))
        beta = np.dot(np.dot(XTX_inv, self.right_hand_side.T), self.left_hand_side)
        residuals = self.left_hand_side - np.dot(self.right_hand_side, beta)
        var = sigma_squared = np.sum(residuals ** 2) / (len(self.left_hand_side) - self.right_hand_side.shape[1])
        wald = (np.dot(np.transpose(term_1), np.dot(np.linalg.inv(term_2), term_1))/len(R))/var
        p_value = (1-f.cdf(wald, len(R), len(self.left_hand_side) - self.right_hand_side.shape[1]))
        return f'Wald: {wald:.3f}, p-value: {p_value:.3f}'

    def get_model_goodness_values(self):
        y_mean = np.mean(self.left_hand_side)
        sst = np.sum((self.left_hand_side - y_mean) ** 2)
        ssr = np.sum((self.left_hand_side - np.dot(self.right_hand_side, self._model['beta'])) ** 2)
        crs_numerator = sst - ssr
        crs_denominator = sst
        crs = 1 - (ssr / crs_denominator)
        ars = 1 - (1 - crs) * (len(self.left_hand_side) - 1) / (len(self.left_hand_side) - self.right_hand_side.shape[1])
        return f"Centered R-squared: {crs:.3f}, Adjusted R-squared: {ars:.3f}"

class LinearRegressionGLS:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self._model = None

    def fit(self):
        XTX_inv = np.linalg.inv(np.dot(self.right_hand_side.T, self.right_hand_side))
        beta = np.dot(np.dot(XTX_inv, self.right_hand_side.T), self.left_hand_side)
        residuals = self.left_hand_side - np.dot(self.right_hand_side, beta)
        squared_residuals = residuals ** 2
        sigma_squared = np.sum(residuals ** 2) / (len(self.left_hand_side) - self.right_hand_side.shape[1])

        new_rhs = np.concatenate((np.log(squared_residuals), self.right_hand_side))
        XTX_inv_new = np.linalg.inv(np.dot(new_rhs.T, new_rhs))
        beta_feasible_gls = np.dot(np.dot(XTX_inv_new, new_rhs.T), np.log(squared_residuals))
        v_inv_matrix = np.diag(1 / squared_residuals)
        XTX_inv_gls = np.linalg.inv(np.dot(np.dot(new_rhs.T, v_inv_matrix), new_rhs))
        beta_gls = np.dot(np.dot(XTX_inv_gls, new_rhs.T), np.log(squared_residuals))
        self._model = {'beta_feasible_gls': beta}
    def get_params(self):
        params = self._model['beta_feasible_gls']
        return pd.Series(params, name='Beta coefficients')
