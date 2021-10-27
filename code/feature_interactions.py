class Feature_Interactions():
    """Feature Interactions for numeric table data.

    The FI value is the amount of the variance explained by
    the interaction (difference between observed and no-interaction Partial Dependence)

    Attributes
    ----------
    n_samples_one : int
        Amount of sampled data to calculate pd_one (see below)
    n_samples_all_exc_one : int
        Amount of sampled data to calculate pd_all_exc_one (see below)
    """

    def __init__(self, n_samples_one=1000, n_samples_all_exc_one=1000):
        self.n_samples_one = n_samples_one
        self.n_samples_all_exc_one = n_samples_all_exc_one

    def set_samples(self, n_samples_one=1000, n_samples_all_exc_one=1000):
        """Set the amount of samples.

        Parameters
        ----------
        n_samples_one : int
            Amount of sampled data to calculate pd_one (see below)
        n_samples_all_exc_one : int
            Amount of sampled data to calculate pd_all_exc_one (see below)
        """
        self.n_samples_one = n_samples_one
        self.n_samples_all_exc_one = n_samples_all_exc_one

    def calculate_interaction(self, clf, X, n_samples=100):
        """Finds feature interaction value for each column in X.

        Parameters
        ----------
        X : pandas frame
        clf : must have predict and decision function

        Returns
        -------
        H2_all : numpy array
            All feature interaction in the same column order as given in X
        """
        preds = clf.predict(X).reshape(-1, 1)
        pd_one_m = pd_one(clf, X, self.n_samples_one)
        pd_all_exc_one_m = pd_all_exc_one(clf, X, self.n_samples_all_exc_one)

        norm_term = np.sum(np.square(preds))

        H2_all = np.sum(np.square(preds - pd_one_m - pd_all_exc_one_m), axis=0) / norm_term

        return H2_all.ravel()

    def pd_all_exc_one(self, clf, X, n_samples=1000):
        """Computes matrix (X.shape[0] x X.shape[1]), where in (i,j) position value
        is equal to pdp(all_variables_except_j == values in row i)

        Parameters
        ----------
        X : pandas dataframe
        clf : must have predict function
        n_samples : int
            Amount of sampled data to calculate pd

        Returns
        -------
        answer : numpy array of shape (X.shape[0], X.shape[1])
        """

        answer = np.empty((X.shape[0], X.shape[1]))
        num_cols = len(X.columns)
        nunique = []
        for col_i in range(num_cols):
            uni = X.iloc[:, col_i].unique()
            if uni.shape[0] > n_samples:
                uni = np.random.choice(uni, n_samples, replace=False)
            nunique.append(uni)

        ind_r = 0
        for row in X.values:
            for i in range(num_cols):
                preds = []
                for uniq in nunique[i]:
                    mrow = row
                    mrow[i] = uniq
                    preds.append(clf.predict(mrow.reshape(1, -1)))
                answer[ind_r, i] = np.array(preds).mean()
            ind_r += 1
        return answer

    def pd_one(self, clf, X, n_samples=1000):
        """Computes matrix (X.shape[0] x X.shape[1]), where in (i,j) position value
        is equal to pdp(j_variable == value in row i)

        Parameters
        ----------
        X : pandas dataframe
        clf : must have predict function
        n_samples : int
            Amount of sampled data to calculate pd

        Returns
        -------
        answer : numpy array of shape (X.shape[0], X.shape[1])
        """
        answer = np.empty((X.shape[0], X.shape[1]))
        num_cols = len(X.columns)
        nunique = []
        for col_i in range(num_cols):
            nunique.append(X.iloc[:, col_i].unique())

        ind_r = 0
        for row in X.values:
            for i in range(num_cols):
                samples_not_i = np.empty((n_samples, num_cols - 1))
                for j in range(num_cols - 1):
                    add_ind = 0
                    if (j > i):
                        add_ind = 1

                    samples_not_i[:, j] = np.random.choice(nunique[j + add_ind], size=n_samples)

                data = np.hstack((samples_not_i[:, :j], np.full((n_samples, 1), row[i]), samples_not_i[:, j:]))
                answer[ind_r, i] = clf.predict(data).mean()
            ind_r += 1
        return answer
