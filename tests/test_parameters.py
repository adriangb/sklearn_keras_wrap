import os

import numpy as np
import pytest

from sklearn.base import clone
from tensorflow.python.keras.testing_utils import get_test_data

from scikeras.wrappers import KerasClassifier
from scikeras.wrappers import KerasRegressor

from .mlp_models import dynamic_classifier
from .mlp_models import dynamic_regressor


# Defaults
INPUT_DIM = 5
HIDDEN_DIM = 5
TRAIN_SAMPLES = 10
TEST_SAMPLES = 5
NUM_CLASSES = 2
BATCH_SIZE = 5
EPOCHS = 1


class TestRandomState:
    @pytest.mark.parametrize(
        "random_state", [0, 123, np.random.RandomState(0)],
    )
    @pytest.mark.parametrize(
        "estimator",
        [
            KerasRegressor(
                build_fn=dynamic_regressor,
                loss=KerasRegressor.root_mean_squared_error,
            ),
            KerasClassifier(build_fn=dynamic_classifier),
        ],
    )
    def test_random_states(self, random_state, estimator):
        """Tests that the random_state parameter correctly
        engages deterministric training and prediction.
        """
        (X, y), (_, _) = get_test_data(
            train_samples=TRAIN_SAMPLES,
            test_samples=TEST_SAMPLES,
            input_shape=(INPUT_DIM,),
            num_classes=NUM_CLASSES,
        )

        # With seed
        estimator.set_params(random_state=random_state)
        estimator.fit(X, y)
        y1 = estimator.predict(X)
        estimator.fit(X, y)
        y2 = estimator.predict(X)
        assert np.allclose(y1, y2)

        if isinstance(estimator, KerasRegressor):
            # Without seed, regressors should NOT
            # give the same results
            # Classifiers _may_ give the same classes
            estimator.set_params(random_state=None)
            estimator.fit(X, y)
            y1 = estimator.predict(X)
            estimator.fit(X, y)
            y2 = estimator.predict(X)
            assert not np.allclose(y1, y2)

    @pytest.mark.parametrize(
        "estimator",
        [
            KerasRegressor(
                build_fn=dynamic_regressor,
                loss=KerasRegressor.root_mean_squared_error,
            ),
            KerasClassifier(build_fn=dynamic_classifier),
        ],
    )
    @pytest.mark.parametrize("pyhash", [None, "0", "1"])
    @pytest.mark.parametrize("gpu", [None, "0", "1"])
    def test_random_states_env_vars(self, estimator, pyhash, gpu):
        """Tests that the random state context management correctly
        handles TF related env variables.
        """
        (X, y), (_, _) = get_test_data(
            train_samples=TRAIN_SAMPLES,
            test_samples=TEST_SAMPLES,
            input_shape=(INPUT_DIM,),
            num_classes=NUM_CLASSES,
        )

        if "random_state" in estimator.get_params():
            estimator.set_params(random_state=None)
        estimator1 = clone(estimator)
        estimator2 = clone(estimator)
        if "random_state" in estimator1.get_params():
            estimator1.set_params(random_state=0)
        if "random_state" in estimator2.get_params():
            estimator2.set_params(random_state=0)
        if gpu is not None:
            os.environ["TF_DETERMINISTIC_OPS"] = gpu
        else:
            if os.environ.get("TF_DETERMINISTIC_OPS"):
                os.environ.pop("TF_DETERMINISTIC_OPS")
        if pyhash is not None:
            os.environ["PYTHONHASHSEED"] = pyhash
        else:
            if os.environ.get("PYTHONHASHSEED"):
                os.environ.pop("PYTHONHASHSEED")
        estimator1.fit(X, y)
        estimator2.fit(X, y)
        if gpu is not None:
            assert os.environ["TF_DETERMINISTIC_OPS"] == gpu
        else:
            assert "TF_DETERMINISTIC_OPS" not in os.environ
        if pyhash is not None:
            assert os.environ["PYTHONHASHSEED"] == pyhash
        else:
            assert "PYTHONHASHSEED" not in os.environ
        y1 = estimator1.predict(X)
        y2 = estimator2.predict(X)
        assert np.allclose(y1, y2)
        if gpu is not None:
            assert os.environ["TF_DETERMINISTIC_OPS"] == gpu
        else:
            assert "TF_DETERMINISTIC_OPS" not in os.environ
        if pyhash is not None:
            assert os.environ["PYTHONHASHSEED"] == pyhash
        else:
            assert "PYTHONHASHSEED" not in os.environ


def test_sample_weights():
    """Checks that the sample_weight parameter has the intended effect.
    """

    # build estimator
    estimator = KerasClassifier(
        build_fn=dynamic_classifier,
        hidden_layer_sizes=(100,),
        epochs=10,
        random_state=0,
    )
    estimator1 = clone(estimator)
    estimator2 = clone(estimator)

    # we create 20 points
    X = np.array([1] * 10000).reshape(-1, 1)
    y = [1] * 5000 + [-1] * 5000

    # heavily weight towards y=1 points
    sw_first_class = [0.8] * 5000 + [0.2] * 5000
    # train estimator 1 with weights
    estimator1.fit(X, y, sample_weight=sw_first_class)
    # train estimator 2 without weights
    estimator2.fit(X, y)
    # estimator1 should tilt towards y=1
    # estimator2 should predict about equally
    average_diff_pred_prob_1 = np.average(
        np.diff(estimator1.predict_proba(X), axis=1)
    )
    average_diff_pred_prob_2 = np.average(
        np.diff(estimator2.predict_proba(X), axis=1)
    )
    assert average_diff_pred_prob_2 < average_diff_pred_prob_1

    # equal weighting
    sw_equal = [0.5] * 5000 + [0.5] * 5000
    # train estimator 1 with weights
    estimator1.fit(X, y, sample_weight=sw_equal)
    # train estimator 2 without weights
    estimator2.fit(X, y)
    # both estimators should have about the same predictions
    np.testing.assert_allclose(
        actual=estimator1.predict_proba(X), desired=estimator2.predict_proba(X)
    )


def test_build_fn_default_params():
    """Tests that default arguments arguments of
    `build_fn` are registered as hyperparameters.
    """
    est = KerasClassifier(build_fn=dynamic_classifier)
    params = est.get_params()
    # (100, ) is the default for dynamic_classifier
    assert params["hidden_layer_sizes"] == (100,)

    est = KerasClassifier(
        build_fn=dynamic_classifier, hidden_layer_sizes=(200,)
    )
    params = est.get_params()
    assert params["hidden_layer_sizes"] == (200,)