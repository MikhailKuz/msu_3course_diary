## Feature importance libs

| Name | Explainable model | Description |
|:--:|:--:|--|
| [rfpimp](https://github.com/parrt/random-forest-importances) | sklearn | include permutation and drop-column importance measures |
| [eli5](https://eli5.readthedocs.io/en/latest/index.html) | sklearn<br/>XGBoost<br/>LightGBM<br/>CatBoost<br/>lightning<br/>sklearn-crfsuite<br/>Keras<br/>(embedded interpretation)<br/><br/>black box<br/>(simple interpretation) | <ul> <li>sklearn<ul><li>linear estimators - explain weights</li><li>decision trees, ensembles - feature weights are calculated by following decision paths in trees of an ensemble</li><li>transformation pipelines</li><li>reversing hashing trick - can find feature correspondence with InvertableHashingVectorizer</li><li>text highlighting -  if the document is vectorized using CountVectorizer, TfIdfVectorizer or HashingVectorizer</li></ul></li> <li>XGBoost/LightGBM<ul><li>gain feature importance - the average gain of the feature when it is used in trees (default)</li><li>weight/split feature importance -  the number of times a feature is used to split the data across all trees</li><li>cover/weight feature importance - the average coverage of the feature when it is used in trees</li></ul> <li>CatBoost<ul><li>calls catboost.explain_weights_catboost() for interpretation</li></ul><li>lightning<ul><li>same as in sklearn for linear estimators </li></ul><li>Keras<ul><li>explains image classifications through Grad-CAM</li></ul></li><li>black box<ul><li>lime</li><li>permutation importance</li></ul> </ul> |
| [cxplain](https://github.com/d909b/cxplain) | black box | a CXPlain model consists of four main components: <ul><li>The model to be explained which can be any type of machine-learning model, including black-box models, such as neural networks and ensemble models</li><li>The model builder that defines the structure of the explanation model to be used to explain the explained model</li><li>The masking operation that defines how CXPlain will internally simulate the removal of input features from the set of available features</li><li>The loss function that defines how the change in prediction accuracy incurred by removing an input feature will be measured by CXPlain</li></ul> |
| [QII](https://github.com/hovinh/QII) | black box | determine the Quantity of interest that we want to evaluate: <ul><li>Define a trained classifier inheriting the QIIPredictor, with predict() method to output quantity of interest.</li><li>Define a QuantityOfInterest instance with appropriate way to compute quantity of interest from output of QIIPredictor.predict()</li></ul> use QII to compute Shapley/Banzhaf values for each chosen feature/set. |
| [mcr](https://github.com/aaronjfisher/mcr) | black box | given a set of models of interest (a model class), this package finds the models that rely as much, or as little as possible on variables of interest, while still performing well. More information you can find in [Fisher et al., 2019](https://www.jmlr.org/papers/v20/18-760.html). |
| [breakDown](https://github.com/MI2DataLab/pyBreakDown) | back box | approximate Shapley values by sequentially choosing variable to add to the set of relaxed features |
| [alibi](https://docs.seldon.io/projects/alibi/en/stable/index.html) | - | - |
| [FeatureImportanceDL](https://github.com/maksym33/FeatureImportanceDL) | - | - |
| [shap](https://github.com/slundberg/shap) | - | - |
| [deeplift](https://github.com/kundajelab/deeplift) | - | - |
| [lime](https://github.com/marcotcr/lime) | - | - |

More [libs](https://github.com/jphall663/awesome-machine-learning-interpretability#explainability--or-fairness-enhancing-software-packages)

## Pros and Cons of the methods

| Name | Pluses | Minuses |
|:--:|:--:|--|
| permutation importance | <ul><li>*fast* (no need to refit model)</li><li>*model free*</li><li>saves *marginal distribution*</li><ul> | <ul><li>weak to *strong* correlation [[link](https://towardsdatascience.com/stop-permuting-features-c1412e31b63f)] </li><ul> |
