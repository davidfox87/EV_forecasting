from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class MonthofYear(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def month_vector(self, month):
        v = np.zeros(12)
        v[month-1] = 1
        return v
    
    def transform(self, X):
        return np.stack([self.month_vector(d) for d in X.index.month])


    
class DayofWeek(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def day_vector(self, day):
        v = np.zeros(7)
        v[day] = 1
        return v
    
    def transform(self, X):
        return np.stack([self.day_vector(d) for d in X.index.dayofweek])

class Weekend(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.expand_dims(((X.index.dayofweek > 4.)*1.0), axis=1)
        

class FourierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, period=10):
        self.period = period


    def fit(self, X, y=None):
        return self

    def _get_trig_args(self, X):
        trig_args = (2 * np.pi / self.period) * np.arange(
            1, 1 + 1, 1
        )
        
        time = np.arange(X.shape[0])
        trig_args = trig_args[np.newaxis, :] * time[:, np.newaxis]
        return trig_args

    def transform(self, X, y=None):
        trig_args = self._get_trig_args(X)
        cos = np.cos(trig_args)
        sin = np.sin(trig_args)
        fourier_terms = np.hstack((cos, sin))
        return fourier_terms



class RollingMeanTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, window=5):
        self.window = window
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.rolling(window=self.window, min_periods=1, center=True).mean()

    
class TrendTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, shift=0):
        self.shift = shift

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.expand_dims(np.arange(self.shift, self.shift + X.shape[0]), axis=1)