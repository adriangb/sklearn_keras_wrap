# History

## 0.2.1 (2020-12-06)

Thank you to @stsievert for your continued support and contributions!

Release notes:

* Support autoencoders and more general use cases via BaseWrapper (#123)
* Fix slowdown caused by sample_weight processing
(reported in [DaskML#764](https://github.com/dask/dask-ml/issues/764), fixed in #123)
* Documentation improvements (#134, #135, #145 and #138)
* Fix the `initialize` method in KerasClassifier (#140)

## 0.2.0 (2020-10-03)

* Move data transformations to a Scikit-Learn Transformer based interface (#88)
* Add Keras parameters to BaseWrapper.__init__ (loss, optimizer, etc) (#47, #55)
* Remove needless checks/array creation (#63, #59)
* Make pre/post processing functions public (#42)
* Some stability around `BaseWrapper.__call__` (#35)
* Cleanup around loss names (#38, #35)
* Parameter routing (#67)
* Rename build_fn to model with deprecation cycle (#98)
* Add ability for SciKeras to compile models (#66)
* `class_weights` parameter (#52, #103)
* `classes` param for `partial_fit` (#69, #104)
* Provide an epochs parameter (#51, #114)
* Updated docs, now hosted on RTD (#58, #73)
* Checks to make sure models are correctly compiled (#86, #100, #88)

## 0.1.8 (2020-06-30)

* Add support for partial fitting and warm starts (#17, thank you @stsievert!).
* Add support for random states via the `random_state` parameter (#27).
* Scikit-Learn SLEP10 compliance (#26).
* Fix unnecessary data reshaping warnings (#23).

## 0.1.7 (2020-05-18)

* Versioning fix.

## 0.1.6 (2020-05-18)

* Rename repo.
* Derive BaseWrapper from BaseEstimator.
* Python 3.8 support.

## 0.1.5.post1 (2020-05-13)

* Deprecate Python 3.5 (#11).
* Fix prebuilt model bug (#5).
* Clean up serialization (#7).
* Implement scikit-learn estimator tests (#10).

## 0.1.4 (2020-04-12)

* Offload output type detection for classification to `sklearn.utils.multiclass.type_of_target`.
* Add documentation.
* Some file cleanup.

## 0.1.3 (2020-04-11)

* First release on PyPI.
