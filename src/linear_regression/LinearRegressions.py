import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy.stats import f, t, norm
from pathlib import Path
from scipy import optimize



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
        self.residuals = None
        self.sigma_squared = None
        self.beta = None

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
        self.residuals = residuals
        self.sigma_squared = sigma_squared
        self.beta = beta
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
        self.beta = None
        self.XTX_inv = None

    def fit(self):
        pass


class LinearRegressionML:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self.params = None
        self.hess_inv = None

    def fit(self):
        X = np.column_stack((np.ones(len(self.right_hand_side)), self.right_hand_side))
        init_params = np.ones(X.shape[1]) * 0.1
        def neg_log_likelihood(params):
            beta = params[1:]  # Extract beta coefficients
            mu = np.dot(X, params)
            residuals = self.left_hand_side - mu
            sigma_sq = np.var(residuals)
            log_likelihood = -0.5 * len(residuals) * np.log(2 * np.pi * sigma_sq)
            log_likelihood -= 0.5 * np.sum(residuals ** 2) / sigma_sq
            return -log_likelihood
        result = optimize.minimize(neg_log_likelihood, init_params, method='L-BFGS-B')
        self.params = result.x
        self.hess_inv = result.hess_inv.todense()

    def get_params(self):
        return pd.Series(self.params, name='Beta coefficients')

    def get_pvalues(self):
        X = np.column_stack((np.ones(len(self.right_hand_side)), self.right_hand_side))
        beta = self.params
        residuals = self.left_hand_side - np.dot(X, beta)
        sigma_squared = np.var(residuals)
        se = np.sqrt(np.diag(np.linalg.inv(self.hess_inv)) * sigma_squared)
        t_stats = beta / se
        df = len(self.left_hand_side) - self.right_hand_side.shape[1]
        p_values = 2 * (1 - t.cdf(np.abs(t_stats), df))
        p_values = pd.Series(p_values, name='P-values for the corresponding coefficients')
        return p_values

    def get_model_goodness_values(self):
        X = np.column_stack((np.ones(len(self.right_hand_side)), self.right_hand_side))
        beta = self.params
        y_hat = np.dot(X, beta)
        y_mean = np.mean(self.left_hand_side)
        total_ss = np.sum((self.left_hand_side - y_mean) ** 2)
        explained_ss = np.sum((y_hat - y_mean) ** 2)
        rsquared = explained_ss / total_ss
        n = len(self.left_hand_side)
        k = X.shape[1] - 1
        adjusted_rsquared = 1 - ((1 - rsquared) * (n - 1) / (n - k - 1))
        return f'Centered R-squared: {rsquared:.3f}, Adjusted R-squared: {adjusted_rsquared:.3f}'