class LinearRegressionGLS:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self._model = None
        self.beta = None
        self.XTX_inv = None

    def fit(self):
        v_inv = self.get_v_inv()
        ones_column = np.ones((len(self.right_hand_side), 1))
        self.right_hand_side = np.concatenate((ones_column, self.right_hand_side), axis=1)
        self.left_hand_side = np.expand_dims(self.left_hand_side, axis=1)
        ones_columns_left = np.ones((len(self.left_hand_side), 3))
        self.left_hand_side = np.concatenate((ones_columns_left, self.left_hand_side), axis=1)
        left = self.right_hand_side
        right = self.left_hand_side
        v_inv_x = np.dot(v_inv, left.T).T
        beta = np.linalg.inv(v_inv_x.T @ left) @ v_inv_x.T @ right
        # beta = np.linalg.inv(left.T @ v_inv @ left) @ left.T @ v_inv @ right
        residuals = right - left @ beta
        se = np.sqrt(np.diagonal(np.linalg.inv(left.T @ v_inv @ left)) * (residuals @ residuals) / (len(right) - left.shape[1]))
        t_stat = beta / se
        p_values = 2 * (1 - t.cdf(np.abs(t_stat), df=len(right) - left.shape[1]))
        self._model = {'beta': beta, 'se': se, 't_stat': t_stat, 'p_values': p_values}

    def get_v_inv(self):
        # OLS modell
        ols = LinearRegressionNP(self.left_hand_side, self.right_hand_side)
        ols.fit()
        sigma_squared = ols.sigma_squared
        square_of_err = np.power(ols.residuals, 2)

        # új modell becslése
        new_ols = LinearRegressionNP(np.log(square_of_err), self.right_hand_side)
        new_ols.fit()

        # becsült értékek - logaritmikus négyzetes hibák
        log_squared_err = np.power(np.e, new_ols.beta)

        # invertálás kétféleképpen:
        log_squared_err_inv = np.power(log_squared_err * 1.0, -1)

        # v inverz mátrix
        v_inv_matrix = np.diag(log_squared_err_inv)

        return v_inv_matrix

    def get_params(self):
        params = self._model['beta']
        return pd.Series(params, name='Beta coefficients')

    def old_fit(self):
        XTX_inv = np.linalg.inv(np.dot(self.right_hand_side.T, self.right_hand_side))
        beta = np.dot(np.dot(XTX_inv, self.right_hand_side.T), self.left_hand_side)
        residuals = self.left_hand_side - np.dot(self.right_hand_side, beta)
        sigma_squared = np.sum(residuals ** 2) / (len(self.left_hand_side) - self.right_hand_side.shape[1])

        new_rhs = np.concatenate((np.log(sigma_squared), self.right_hand_side))
        XTX_inv_new = np.linalg.inv(np.dot(new_rhs.T, new_rhs))
        beta_feasible_gls = np.dot(np.dot(XTX_inv_new, new_rhs.T), np.log(sigma_squared))
        v_inv_matrix = np.diag(1 / sigma_squared)
        XTX_inv_gls = np.linalg.inv(np.dot(np.dot(new_rhs.T, v_inv_matrix), new_rhs))
        beta_gls = np.dot(np.dot(XTX_inv_gls, new_rhs.T), np.log(sigma_squared))
        self._model = {'beta_feasible_gls': beta}

    def ml_fit(self):
        ones_column = np.ones((len(self.right_hand_side), 1))
        self.right_hand_side = np.concatenate((ones_column, self.right_hand_side), axis=1)
        self.left_hand_side = np.expand_dims(self.left_hand_side, axis=1)
        y = self.left_hand_side
        x = self.right_hand_side

        # ez gondolom analitikus
        XTX_inv = np.linalg.inv(np.dot(x.T, x))
        beta = np.dot(XTX_inv, np.dot(x.T, y))
        yxb = (y - x * beta)
        sigma = np.power(len(y), -1) * np.dot(yxb.T, yxb)
        lfunc = - len(x) / 2 * np.log(2 * np.pi) - len(x) / 2 * np.log(sigma ** 2) - 1 / (2 * sigma ** 2) * np.dot(
            (y - x * beta).T, (y - x * beta))

        # minimalizálás-optimalizálás
        optimize.minimize(lfunc, x, method='L-BFGS-B')
        self._model = {'beta': beta}

    def get_params(self):
        params = self._model['beta']
        return pd.Series(params, name='Beta coefficients')