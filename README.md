# Дневник
_Формулы корректно отображаются на [этом сайте](https://upmath.me/)_

#### 27/09/2020 - повторил 2 первые главы [курса](https://stepik.org/course/54098/promo)
##### Глава 1
- Генерация текста:
   - через поиск похожих
   - по шаблону
   - с помощью нейросетей
- При векторном разряженном представлении документа теряется зависимость слов
- Предиктивные модели (BERT, Transformer и т.п.) не требуют размеченной выборки
- Сходство текстов можно определить как долю совпадающих путей, проходимых в графовых представлениях текстов   
- В классификации с текстами:
   - большой длины линейные модели дают основное качество
   - короткими, в зависимости от объема gold_labels:
     - малый объем - ядерные методы
     - совсем нет - системы правил
- В эксплоративном анализе применяются методы тематического регулирования: LDA, ARTM

##### Глава 2
- В подходе с TF-IDF не используется информация о метках документов => теряем часть информация, если она есть


#### 04/10/2020 - прочитал обзорную [статью](https://arxiv.org/pdf/1802.02871.pdf) про online learning
- В большенстве случаев рассматривается бинарная классификация и задача оптимизации $$ R_{T}=\sum_{t=1}^{T} \ell_{t}\left(\mathbf{w}_{t}\right)-\min _{\mathbf{w}} \sum_{t=1}^{T} \ell_{t}(\mathbf{w}) $$, причём $$min$$ ищется для $$w$$, не зависящего от $$t$$
- В Contextual Bandits минимизируется $$ R_{T}(f)=\sum_{t=1}^{T}\left[\ell_{I_{t}, t}-\ell_{t}\left(f^{*}\right)\right] $$, где $$ f^{*}=\arg \inf _{f \in \mathcal{F}} \ell_{D}(f) $$, &nbsp; $$ I_{t} \in \overline{1, k} $$ - действие выбранное на t шаге
- Есть ссылка на потенциально интересную [статью](https://arxiv.org/pdf/1711.03705.pdf) про online deep learning


#### 12/10/2020 - прочитал [статью](https://papers.nips.cc/paper/4928-understanding-variable-importances-in-forests-of-randomized-trees.pdf) про variable importances in forests of randomized trees
- Ограничения в работе: неповторение в детях признаков родителей, выборка полностью описывающая распределение $$ P(X_1, ..., X_p, Y) $$ , бесконечное кол-во полных рандомизированных деревьев
- Если выбираем на этапе деления рандомно один признак и глубина дерева >= кол-во рел. признаков -> важность признака == 0 <-> он нерелевантный
- Если выбираем > 1 признака и из них максимизирующий уменьшение энтропии -> появляется маскирующий эффект: некоторые релевантные признаки могут иметь сильно меньшую важность по сравнению с похожими рел. признаками
    - Добавление нерелевантных может сказаться на важности релевантных

#### 26/10/2020 - прочитал [пример](https://scikit-learn.org/stable/modules/permutation_importance.html), [пример](https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html#sphx-glr-auto-examples-inspection-plot-permutation-importance-py), [пример](https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html#sphx-glr-auto-examples-inspection-plot-permutation-importance-multicollinear-py) с sklearn про permutation feature importance и из [источника](https://machinelearningmastery.com/calculate-feature-importance-with-python/#:~:text=Feature%20importance%20refers%20to%20a,feature%20when%20making%20a%20prediction.), [источника](https://towardsdatascience.com/interpretable-machine-learning-1dec0f2f3e6b) про важность признаков
- impurity-based feature importance for trees are strongly biased and favor high cardinality features
- если в датасете есть скоррелированные признаки, то в подходе permutation importance таким признакам будет даваться малый вес
    - решение проблемы: иерархическая кластеризация по корреляциям рангового порядка Спирмена, выбор порога и сохранение одного объекта из каждого кластера
- в случае random forest если сложность модели велика по сравнению с данными, алгоритм может переобучиться и даже рандомные признаки будут играть большую роль
- drop column метод вычислительно трудозатратный, но точный
- в методе lime особую роль играет подбор возбуждений экземпляра выборки