## Конспекты статей 
- **Accurate and Robust Feature Importance Estimation under Distribution Shifts, 2020**  [[paper]](https://arxiv.org/pdf/2009.14454.pdf)
  - описывается подход к оценке важности признаков для нейросетей: основная сеть обучается совместно с дополнительной (second net), у которой:
    - цель - научиться предсказывать loss основной сети
    - input - латентные представления после некоторых слоёв основной сети
    - loss
      - contrastive training - сохраняем правильное упорядочивание пар скоров
      - dropout calibration - hinge loss + доверительные интервалы
  - используется Granger определение причинности (связь между признаком и целевой переменной сущетсвует, если качество только ухудшится при отбрасывании данного признака)
  - важность признака - разница предсказаний вспомогательной сети с его маскированием и без  
  *Итог*:
    - на 15-30 % лучше качество, чем у Shap
    - при увеличении различия распределения x_test, по сравнению с x_train, loss second net монотонно растёт
    - подход устойчивей при сильных изменениях x_test Deep_Shap'а в 2 раза

- **Feature Importance Ranking for Deep Learning, 2020** [[paper]](https://arxiv.org/pdf/2010.08973.pdf)
  - рассматривается две сети operator net и selector net, маски для признаков - бинарные вектора (1 - берем признак, 0 - нет), оптимальное кол-во признаков - гиперпараметр
  - обучение происходит поочередно
  - operator net:
    - цель - обучение с учителем конкретной задачи
    - input - x и маска признаков
    - loss - соответствующий задаче
  - selector net:
    - цель - предсказать loss operator net
    - input - маска признаков
    - loss - l2 с loss'ом, переданным от operator net
  - важность признака - соответствующая компонента градиента loss'а selector net'а в точке оптимального набора признаков
  - процесс построения оптимального набора очень долгий  
  *Итог*:
    - в среднем лучше качество на синтетических данных
    - лучшее RFE, BAHSIC, mRMR, CCM на 4-ёх benchmark датасетах

- **Knockoffs for the mass: new feature importance statistics with false discovery guarantees, 2019** [[paper]](https://arxiv.org/pdf/1807.06214.pdf)
  - аппроксимируется распределение данных (только признаки) байесовскими сетями
  - используется аугментация выборки определённым образом (чтобы не выходить за исходное распределение)
  - вместо того, чтобы перемешивать значения признака (в permutation importance), берется взвешенная сумма исходного признака и соответствующего признака из аугментированной выборки
  - важность признака - площадь под кривой (y - доля правильно отобранных признаков, x - параметр взвешенной суммы) для некоторого диапазона (например, [0, 10])
  - FDR в реальности нельзя оценить, предполагается, что мы хорошо моделируем распределение выборки

- **A Unified Approach to Interpreting Model Predictions, 2017** [[paper]](https://proceedings.neurips.cc/paper/2017/file/8a20a8621978632d76c43dfd28b67767-Paper.pdf)
  - рассматривается семейство аддитивных explanation models
  - в данном классе существует единственная explanation model, удовлетворяющая свойствам:
    - local accuracy - совпадение значений f(x) и exp_model(x')
    - missingness - признак, не присутствующий в x, будет иметь нулевую важность
    - consistency - признак во всевозможных комбинациях остальных имеет не меньшее значение на изменение выхода f, чем на f' -> его важность для f >= важность для f'
  - считать такую explanation model дорого
  - Linear LIME + Kernel SHAP дают истинные значения SHAP values
  - в случае f = max, можно за квадрат размерности признаков SHAP посчитать (пользуемся свойствами max)
  - Deep SHAP - вместо важности в DeepLIFT подставляем SHAP важность для промежуточных расчётах  
  *Итог*:
    - обобщили предыдущие методы
    - на реальной задаче SHAP важность совпала с человеческой
    - для конкретных моделей улучшили время расчёта

- **Learning Important Features Through Propagating Activation Differences, 2017** [[paper]](https://arxiv.org/pdf/1704.02685.pdf)
  - метод основан на разнице значений нейронов между начальным значением (reference) и конечным
  - разделяются положительный и отрицательный вклады в целевую переменную
  - важность признака линейно зависит от разницы x - x_reference
  - важность - shapley value с количеством разбиений 2
  - x_reference выбирается в зависимости от задачи  
  *Итог*:
    - использование разности x - x_reference позволяет информации распространяться когда градиент равен нулю
    - gradients, gradients*input, guided backprop, rescale rule теряют зависимости в ходе вычисления важности в некоторых случаях в отличии от предложенного reveal_cancel rule

- **CXPlain: Causal Explanations for Model Interpretation under Uncertainty, 2019** [[paper]](https://arxiv.org/pdf/1910.12336.pdf)
  - используется Granger's definition of causality (в реальности, исходя только из данных, нельзя проверить)
    - все признаки релевантные
    - признак временно предшествует метке (для того, чтобы получить метку, нужна информация о признаке)
  - истинная важность признака - нормированная разница ошибок объясняемой модели на x_mask и x_reference
  - обучается explanation model (подходящая решаемой задаче)
    - цель - предсказать важность признаков
    - input - маскированный элемент x_train
    - loss - расстояние Кульбака — Лейблера между истинным и предсказанным распределениями важностей признаков
  - для устойчивости обучаем ансамбль explanation_models (на сэмплированных выборках), предсказанная важность - медиана предсказаний ансамбля, а точность - интерквантильный размах  
  *Итог*:
    - точность оценки важности коррелирует с ошибкой ранжирования важности признаков
    - при небольшой мощности ансамбля (5) хорошо оценивается точность explanation_model
    - качество лучше на 20%, быстрее x100, чем Shap, Lime на Mnist и ImageNet
    - качество сильно зависит от устройства explanation_model

- **Bias in random forest variable importance measures, 2017** [[paper]](https://link.springer.com/content/pdf/10.1186/1471-2105-8-25.pdf)
  - имплементирован метод построения дерева (ctree), где выбор переменной осуществляется путем минимизации значения p критерия независимости условного вывода, сравнимого, например, с тестом χ2 со степенью свободы, равной числу категорий признака
  - лучше себя показывает, чем rf в синтетических экспериментах (с/без бутстрэпом, способ сэмплинга)
  - bias в важности признаков в rf возникает из-за того, что признаки с большим количество уникальных значений располагаются ближе к корню дерева
  - рассматривается две оценки важности признака
    - количество узлов, в которых используется признак для разделения выборки (selection frequency)
    - permutation importance
    - Gini importance (большой bias)  
  *Итоги экспериментов*:
    - сэмплинг с возвратом сильно смещает selection frequency в сторону признаков с большим числом уникальных значений
    - permutation importance более устойчив

- **Grouped variable importance with random forests and application to multiple functional data analysis, 2015** [[paper]](https://arxiv.org/pdf/1411.4170.pdf)
  - рассматривается оценка важности группы признаков с теоретической и практической стороны
  - теоретическая сторона
    - (признаки, целевая переменная) - случайный вектор
    - важность признака - разница квадратичного риска с заменой/без замены признака на одинакового распределенный признак, но не зависящий от остальных и целевой переменной
    - в определённых условиях важность группы признаков пропорциональна дисперсии функции (=модель) от этой группы
  - практическая сторона
    - важность группы признаков - oob + случайная перестановка строк для столбцов из группы
    - используется RFE
  - с помощью вейвлет декомпозиции можно получить различные разбиения коэффициентов на группы
  - для отбора некоторых групп не применим алгоритм RFE, т.к. существует общая составляющая, вносящая большой вклад -> делим интересующий параметр на сетку и вычисляем важность в конкретных точках  
  *Итоги экспериментов*:  
    - оценка важности согласовывается как с синтетическими экспериментами, так и с реальными

- **Correlation and variable importance in random forests, 2017** [[paper]](https://arxiv.org/pdf/1310.5726.pdf)
  - продолжение вышеописанной работы 
  - эмпирическая важность признака при использовании purely rf для независимых признаков сходится экспоненциально к теоретической при стремлении количества итераций разбиения узла дерева и мощности тренировочной выборки так, чтобы отношение первого ко второму стремилось к 0 
  - даже сильно коррелирующие признаки с целевой переменной могут получить малую важность из-за корреляции между собой  
  *Итоги экспериментов*:
    - NRFE и RFE в целом имеют одинаковое качество
    
      
  

### Fisher A, Rudin C, Dominici F (2018) [All models are wrong but many are useful: Variable importance for black-box, proprietary, or misspecified prediction models, using model class reliance](https://arxiv.org/pdf/1801.01489.pdf)
**Идея** - будем искать важность группы признаков $X_{1}$ не для одной хорошей модели (reference model), а для класса моделей  
**Датасет** - iid  

***Введём несколько определений***:
*a population ε-Rashomon set*:  $\mathcal{R}(\epsilon):= \left\{f \in \mathcal{F}: \mathbb{E} L(f, Z) \leq \mathbb{E} L\left(f_{\text {ref }}, Z\right)+\epsilon\right\}$  
*model relience*: $M R(f):=\frac{\text { Expected loss of } f \text { under noise }}{\text { Expected loss of } f \text { without noise }}$  
*a population-level model class reliance (MCR) range*: $\left[M C R_{-}(\epsilon), M C R_{+}(\epsilon)\right]:=\left[\min _{f \in \mathcal{R}(\epsilon)} M R(f), \max _{f \in \mathcal{R}(\epsilon)} M R(f)\right]$  
*the set of functions $\mathcal{G}_{r}$ as an $r$ -margin-expectation-cover*: if for any $f \in \mathcal{F}$ and any distribution $D,$ there exists $g \in \mathcal{G}_{r}$ such that $ \mathbb{E}_{Z \sim D}|L(f, Z)-L(g, Z)|$  
*the covering number $\mathcal{N}(\mathcal{F}, r)$*: to be the size of the smallest $r$ -margin-expectationcover for $\mathcal{F}$  
> **_NOTE:_** If $M C R_{+}(\epsilon)$ is low, then no well-performing model in $\mathcal{F}$ places high importance on $X_{1},$ and $X_{1}$ can be discarded at low cost regardless of future modeling decisions. Similarly for $M C R_{-}(\epsilon)$.  

***Возможны следующие вариации empirical MR:***  
$\widehat{M R}(f):=\frac{\hat{e}_{\text {switch }}(f)}{\hat{e}_{\text {orig }}(f)}$  
$\begin{aligned} \hat{e}_{\text {divide }}(f):=\frac{1}{2\lfloor n / 2\rfloor} \sum_{i=1}^{\lfloor n / 2\rfloor} &\left[L\left\{f,\left(\mathbf{y}_{[i]}, \mathbf{X}_{1[i+\lfloor n / 2\rfloor, \cdot]}, \mathbf{X}_{2[i, \cdot]}\right)\right\}\right.\\ &+L\left\{f,\left(\mathbf{y}_{[i+\lfloor n / 2\rfloor]}, \mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[i+\lfloor n / 2\rfloor, \cdot]}\right)\right\} \end{aligned}$  
$\hat{e}_{\text {orig }}(f):=\frac{1}{n} \sum_{i=1}^{n} L\left\{f,\left(\mathbf{y}_{[i]}, \mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[i, \cdot]}\right)\right\}$  
$\hat{e}_{\text {switch }}(f):=\frac{1}{n(n-1)} \sum_{i=1}^{n} \sum_{j \neq i} L\left\{f,\left(\mathbf{y}_{[j]}, \mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[j, \cdot]}\right)\right\}$
> **_NOTE:_** The estimators $\hat{e}_{\text {orig }}(f), \hat{e}_{\text {switch }}(f)$ and $\hat{e}_{\text {divide }}(f)$ all belong to the well-studied class of U-statistics. Thus, under fairly minor conditions, *these estimators are unbiased, asymptotically normal, and have finite-sample probabilistic bounds*  

***We introduce three bounded loss assumptions:***  
**Assumption 1** (*Bounded individual loss*) For a given model $f \in \mathcal{F},$ assume that $0 \leq$ $L\left(f,\left(y, x_{1}, x_{2}\right)\right) \leq B_{\text {ind }}$ for any $\left(y, x_{1}, x_{2}\right) \in\left(\mathcal{Y} \times \mathcal{X}_{1} \times \mathcal{X}_{2}\right)$  
**Assumption 2** (*Bounded relative loss*) For a given model $f \in \mathcal{F},$ assume that $\mid L\left(f,\left(y, x_{1}, x_{2}\right)\right)-$ $L\left(f_{r e f},\left(y, x_{1}, x_{2}\right)\right) \mid \leq B_{\text {ref }}$ for any $\left(y, x_{1}, x_{2}\right) \in \mathcal{Z}$  
**Assumption 3** (*Bounded aggregate loss*) For a given model $f \in \mathcal{F},$ assume that $\mathbb{P}\{0<$ $\left.b_{\text {orig }} \leq \hat{e}_{\text {orig }}(f)\right\}=\mathbb{P}\left\{\hat{e}_{\text {switch }}(f) \leq B_{\text {switch }}\right\}=1$
> **_NOTE:_** some constants can be derived from others  

**Theorem 4** (*"Outer" MCR Bounds*) Given a constant $\epsilon \geq 0$, let $f_{+, \epsilon} \in \arg \max _{\mathcal{R}(\epsilon)} M R(f)$ and $f_{-, \epsilon} \in \arg \min _{\mathcal{R}(\epsilon)} M R(f)$ be prediction models that attain the highest and lowest model reliance among models in $\mathcal{R}(\epsilon)$. If $f_{+, \epsilon}$ and $f_{-, \epsilon}$ satisfy Assumptions 1, 2, 3 , then
$$
\begin{array}{c}
\mathbb{P}\left(M C R_{+}(\epsilon)>\widehat{M C R}_{+}\left(\epsilon_{\text {out }}\right)+\mathcal{Q}_{\text {out }}\right) \leq \delta, \text { and } \\
\mathbb{P}\left(M C R_{-}(\epsilon)<\widehat{M C R}_{-}\left(\epsilon_{\text {out }}\right)-\mathcal{Q}_{\text {out }}\right) \leq \delta \\
\text { where } \epsilon_{\text {out }}:=\epsilon+2 B_{\text {ref }} \sqrt{\frac{\log \left(3 \delta^{-1}\right)}{2 n}}, \text { and } \mathcal{Q}_{\text {out }}:=\frac{B_{\text {switch }}}{b_{\text {orig }}}-\frac{B_{\text {switch }}-B_{\text {ind }} \sqrt{\frac{\log \left(6 \delta^{-1}\right)}{n}}}{b_{\text {orig }}+B_{\text {ind }} \sqrt{\frac{\log \left(6 \delta^{-1}\right)}{2 n}}}
\end{array}
$$  

> **_NOTE:_**    
> - As $n$ increases, $\epsilon_{out}$ approaches $\epsilon$ and $\mathcal{Q}_{out}$ approaches zero
> - with high probability, the largest possible estimation error for $M R(f)$ across all models in $\mathcal{F}$ is bounded by $q(\delta, r, n)$, which can be made arbitrarily small by increasing $n$ and decreasing $r$
> - The  existence  of  this  uniform  bound  implies  that  it  is  feasible  to  train  a  model  and  to evaluate its importance using the *same data*  

**Theorem 6** (*"Inner" MCR Bounds*) Given constants $\epsilon \geq 0$ and $r>0,$ if Assumptions 1 , 2 and 3 hold for all $f \in \mathcal{F},$ and then
$$
\begin{array}{l}
\mathbb{P}\left(M C R_{+}(\epsilon)<\widehat{M C R}_{+}\left(\epsilon_{i n}\right)-\mathcal{Q}_{i n}\right) \leq \delta, \text { and } \\
\mathbb{P}\left(M C R_{-}(\epsilon)>\widehat{M C R}_{-}\left(\epsilon_{i n}\right)+\mathcal{Q}_{i n}\right) \leq \delta
\end{array}
$$  

***Calculating Empirical Estimates of MCR***  
- computing $\widehat{M C R}_{+}(\epsilon)$ however will require that we are able to minimize arbitrary linear combinations of $\hat{e}_{\text {orig }}(f)$ and $\hat{e}_{\text {switch }}(f)$
- we present bound functions $b_{-}$ and $b_{+}$ satisfying $b_{-}\left(\epsilon_{\mathrm{abs}}\right) \leq$ $\widehat{M R}(f) \leq b_{+}\left(\epsilon_{\text {abs }}\right)$ simultaneously for all $\left\{f, \epsilon_{\text {abs }}: \hat{e}_{\text {orig }}(f) \leq \epsilon_{\text {abs }}, f \in \mathcal{F}, \epsilon_{\text {abs }}>0\right\}$
- almost all of the results shown in this section, and those in Section 6.2 . also hold if we replace $\hat{e}_{\text {switch }}$ with $\hat{e}_{\text {divide }}$ throughout (see Eq 3.5), including in the definition of $\widehat{M R}$ and $\hat{h}_{-, \gamma}(f) .$  

***Binary Search for Empirical MR Lower Bound***
**Condition 8** (*Criteria to continue search for $\widehat{M R}$ lower bound*) $\hat{h}_{-, \gamma}\left(\hat{g}_{-, \gamma}\right) \geq 0$ and $\hat{e}_{\text {orig }}\left(\hat{g}_{-, \gamma}\right) \leq \epsilon_{a b s}$  
**Lemma 9** (*Lower bound for*) If $\gamma \in \mathbb{R}$ satisfies $\hat{h}_{-, \gamma}\left(\hat{g}_{-, \gamma}\right) \geq 0,$ then $f \in \mathcal{F}$ satisfying $\hat{e}_{\text {orig }}(f) \leq \epsilon_{a b s} .$
$$
\frac{\hat{h}_{-, \gamma}\left(\hat{g}_{-, \gamma}\right)}{\epsilon_{a b s}}-\gamma \leq \widehat{M R}(f)
$$ for all $f \in \mathcal{F}$ satisfying $\hat{e}_{\text {orig }}(f) \leq \epsilon_{a b s} .$ It also follows that  
$$
-\gamma \leq \widehat{M R}(f) \quad \text { for all } f \in \mathcal{F}
$$  
> **_NOTE:_**
> - Additionally, if $f=\hat{g}_{-, \gamma}$ and at least one of the inequalities in Condition 8 holds with equality, then top Eq holds with equality.
> - It remains to determine which value of $\gamma$ should be used in top Eq. The following lemma implies that this value can be determined by a binary search, given a particular value of interest for $\epsilon_{\mathrm{abs}}$  

**Lemma 10** (*Monotonicity for $\widehat{M R}$ lower bound binary search*) The following monotonicity results hold:  
1. $\hat{h}_{-, \gamma}\left(\hat{g}_{-, \gamma}\right) is monotonically increasing in \gamma$.  
2. $\hat{e}_{\text {orig }}\left(\hat{g}_{-, \gamma}\right)$ is monotonically decreasing in $\gamma$.  
3. Given $\epsilon_{a b s},$ the lower bound from $E q 6.1,\left\{\frac{\hat{h}_{-, \gamma}\left(\hat{g}_{-, \gamma}\right)}{\epsilon_{a b s}}-\gamma\right\},$ is monotonically decreasing in $\gamma$ in the range where $\hat{e}_{\text {oria }}\left(\hat{g}_{-, \gamma}\right) \leq \epsilon_{a b s},$ and increasing otherwise.  
> **_NOTE:_** the value of $\gamma$ resulting in the tightest lower bound from Eq 6.1 occurs when $\gamma$ is as low as possible while still satisfying Condition 8  

**Proposition 11** (*Nonnegative weights for $\widehat{M R}$ lower bound binary search*) Assume that $L$ and $\mathcal{F}$ satisfy the following conditions.
1. (Predictions are sufficient for computing the loss) The loss $L\left\{f,\left(Y, X_{1}, X_{2}\right)\right\}$ depends on the covariates $\left(X_{1}, X_{2}\right)$ only via the prediction function $f,$ that is, $L\left\{f,\left(y, x_{1}^{(a)}, x_{2}^{(a)}\right)\right\}=$  
$$
L\left\{f,\left(y, x_{1}^{(b)}, x_{2}^{(b)}\right)\right\} \text { whenever } f\left(x_{1}^{(a)}, x_{2}^{(a)}\right)=f\left(x_{1}^{(b)}, x_{2}^{(b)}\right)
$$
2. (Irrelevant information does not improve predictions) For any distribution $D$ satisfying $X_{1} \perp_{D}\left(X_{2}, Y\right)$, there exists a function $f_{D}$ satisfying
$$
\mathbb{E}_{D} L\left\{f_{D},\left(Y, X_{1}, X_{2}\right)\right\}=\min _{f \in \mathcal{F}} \mathbb{E}_{D} L\left\{f,\left(Y, X_{1}, X_{2}\right)\right\} and
$$
$$
f_{D}\left(x_{1}^{(a)}, x_{2}\right)=f_{D}\left(x_{1}^{(b)}, x_{2}\right) \text { for any } x_{1}^{(a)}, x_{1}^{(b)} \in \mathcal{X}_{1} \text { and } x_{2} \in \mathcal{X}_{2}
$$  
Let $\gamma=0$. Under the above assumptions, it follows that either (i) there exists a function $\hat{g}_{-, 0}$ minimizing $\hat{h}_{-, 0}$ that does not satisfy Condition $8,$ or $(ii)$ $\hat{e}_{\text {orig }}\left(\hat{g}_{-, 0}\right) \leq \epsilon_{a b s}$ and $\widehat{M R}\left(g_{-, 0}\right) \leq$ 1 for any function $\hat{g}_{-, 0}$ minimizing $\hat{h}_{-, 0}$.
> **_NOTE:_** tractability of our approach, as minimizing $\hat{h}_{-, \gamma}$ for $\gamma \geq 0$ is equivalent to minimizing reweighted empirical loss over an expanded sample of size $n^{2}$:  
> $$
> \hat{h}_{-, \gamma}(f)=\gamma \hat{e}_{\text {orig }}(f)+\hat{e}_{\text {switch }}(f)=\sum_{i=1}^{n} \sum_{j=1}^{n} w_{\gamma}(i, j) L\left\{f,\left(\mathbf{y}_{[i]}, \mathbf{X}_{1[j, \cdot]}, \mathbf{X}_{2[i, \cdot]}\right)\right\}, where
> $$  
> 
> $$
> w_{\gamma}(i, j)=\frac{\gamma 1(i=j)}{n}+\frac{1(i \neq j)}{n(n-1)} \geq 0
> $$  

***Binary Search for Empirical MR Upper Bound***
$\hat{h}_{+, \gamma}(f):=\hat{e}_{\text {orig }}(f)+\gamma \hat{e}_{\text {switch }}(f), \quad$ and $\quad \hat{g}_{+, \gamma, \mathcal{F}} \in \underset{f \in \mathcal{F}}{\arg \min } \hat{h}_{+, \gamma}(f)$
Given an observed sample, we define the following condition for a pair of values $\left\{\gamma, \epsilon_{\mathrm{abs}}\right\} \in$ $\mathbb{R}_{<0} \times \mathbb{R}_{>0},$ and argmin function $\hat{g}_{+, \gamma}:$  
**Condition 12** (*Criteria to continue search for $\widehat{M R}$ upper bound*) $\hat{h}_{+, \gamma}\left(\hat{g}_{+, \gamma}\right) \geq 0$ and $\hat{e}_{\text {orig }}\left(\hat{g}_{+, \gamma}\right) \leq \epsilon_{a b s}$  
> **_NOTE:_** We can now develop a procedure to upper bound $\widehat{M R}$, as shown in the next lemma.  

**Lemma 13** (*Upper bound for $\widehat{M R}$*) If $\gamma \in \mathbb{R}$ satisfies $\gamma \leq 0$ and $\hat{h}_{+, \gamma}\left(\hat{g}_{+, \gamma}\right) \geq 0,$ then  
$$
\widehat{M R}(f) \leq\left\{\frac{\hat{h}_{+, \gamma}\left(\hat{g}_{+, \gamma}\right)}{\epsilon_{a b s}}-1\right\} \gamma^{-1}
$$
for all $f \in \mathcal{F}$ satisfying $\hat{e}_{\text {orig }}(f) \leq \epsilon_{a b s} .$ It also follows that
$$
\widehat{M R}(f) \leq\left|\gamma^{-1}\right| \quad \text { for all } f \in \mathcal{F}
$$  
Additionally, if $f=\hat{g}_{+, \gamma}$ and at least one of the inequalities in Condition 12 holds with equality, then Eq 6.4 holds with equality.
**Lemma 14** (*Monotonicity for $\widehat{M R}$ upper bound binary search*) The following monotonicity results hold:  
1. $\hat{h}_{+, \gamma}\left(\hat{g}_{+, \gamma}\right)$ is monotonically increasing in $\gamma$.  
2. $\hat{e}_{\text {orig }}\left(\hat{g}_{+, \gamma}\right)$ is monotonically decreasing in $\gamma$ for $\gamma \leq 0,$ and Condition 12 holds for $\gamma=0$ and $\epsilon_{a b s} \geq \min _{f \in \mathcal{F}} \hat{e}_{\text {orig }}(f)$  
3. Given $\epsilon_{a b s},$ the upper boundary $\left\{\frac{\hat{h}_{+, \gamma}\left(\hat{g}_{+, \gamma}\right)}{\epsilon_{a b s}}-1\right\} \gamma^{-1}$ is monotonically increasing in in the range where $\hat{e}_{\text {orig }}\left(\hat{g}_{+, \gamma}\right) \leq \epsilon_{a b s}$ and $\gamma<0,$ and decreasing in the range where $\hat{e}_{\text {orig }}\left(\hat{g}_{+, \gamma}\right)>\epsilon_{a b s}$ and $\gamma<0$  
> **_NOTE:_** Together, the results from Lemma 14 imply that we can use a binary search across $\gamma \in \mathbb{R}$ to tighten the boundary on $\widehat{M R}$ from Lemma $13.$  

***Convex Models***
- **идея**: пусть функции параметризуются некоторым вектором переменных, разобьём это пространство на симплексы, на них h совпадает в вершинах с некоторой гиперплоскостью, заменяем h её, получаем нижнию оценку, так для всех подвыборок из пространства и индуктивно повторяем процедуру  

***MR & MCR for Linear Models, Additive Models***
Throughout this section, we assume that $\mathcal{X} \subset \mathbb{R}^{p}$ for $p \in \mathbb{Z}^{+},$ that $\mathcal{Y} \subset \mathbb{R}^{1},$ and that $L$ is the squared error loss function $L\left(f,\left(y, x_{1}, x_{2}\right)=\left(y-f\left(x_{1}, x_{2}\right)\right)^{2}\right.$.  
**Proposition 15** (*Interpreting $M R,$ and computing empirical MR for linear models*) For any prediction model $f,$ let $e_{\text {orig }}(f), e_{\text {switch }}(f), \hat{e}_{\text {orig }}(f),$ and $\hat{e}_{\text {switch }}(f)$ be defined based on the squared error loss $L\left(f,\left(y, x_{1}, x_{2}\right)\right):=\left(y-f\left(x_{1}, x_{2}\right)\right)^{2}$ for $y \in \mathbb{R}, x_{1} \in \mathbb{R}^{p_{1}},$ and $x_{2} \in \mathbb{R}^{p_{2}}$  
where $p_{1}$ and $p_{2}$ are positive integers. Let $\beta=\left(\beta_{1}, \beta_{2}\right)$ and $f_{\beta}$ satisfy $\beta_{1} \in \mathbb{R}^{p_{1}}, \beta_{2} \in \mathbb{R}^{p_{2}}$ and $f_{\beta}(x)=x^{\prime} \beta=x_{1}^{\prime} \beta_{1}+x_{2}^{\prime} \beta_{2} .$ Then  
$$
M R\left(f_{\beta}\right)=1+\frac{2}{e_{\text {orig }}\left(f_{\beta}\right)}\left\{\operatorname{Cov}\left(Y, X_{1}\right) \beta_{1}-\beta_{2}^{\prime} \operatorname{Cov}\left(X_{2}, X_{1}\right) \beta_{1}\right\}
$$  
and, for finite samples,
$$
\left.\hat{e}_{\text {switch }}\left(f_{\beta}\right)=\frac{1}{n}\left\{\begin{array}{l}
\mathbf{y}^{\prime} \mathbf{y}-2\left[\begin{array}{c}
\mathbf{X}_{1}^{\prime} \mathbf{W} \mathbf{y} \\
\mathbf{X}_{2}^{\prime} \mathbf{y}
\end{array}\right]^{\prime}
\end{array}\right] \beta+\beta^{\prime}\left[\begin{array}{cc}
\mathbf{X}_{1}^{\prime} \mathbf{X}_{1} & \mathbf{X}_{1}^{\prime} \mathbf{W} \mathbf{X}_{2} \\
\mathbf{X}_{2}^{\prime} \mathbf{W} \mathbf{X}_{1} & \mathbf{X}_{2}^{\prime} \mathbf{X}_{2}
\end{array}\right] \beta\right\}
$$  
where $\mathbf{W}:=\frac{1}{n-1}\left(\mathbf{1}_{n} \mathbf{1}_{n}^{\prime}-\mathbf{I}_{n}\right), \mathbf{1}_{n}$ is the $n$ -length vector of ones, and $\mathbf{I}_{n}$ is the $n \times n$
identity matrix.  
> **_NOTE:_** сложность вычисления растёт линейно (можно расписать)  

**Remark 16** (*Tractability of empirical MCR for linear model classes*) For any $f_{\beta} \in \mathcal{F}_{l m}$ and any fixed coefficients $\xi_{\text {orig }}, \xi_{\text {switch }} \in \mathbb{R},$ the linear combination  
$$
\xi_{\text {orig }} \hat{e}_{\text {orig }}\left(f_{\beta}\right)+\xi_{\text {switch }} \hat{e}_{\text {switch }}\left(f_{\beta}\right)
$$  
is proportional in $\beta$ to the quadratic function $-2 \mathbf{q}^{\prime} \beta+\beta^{\prime} \mathbf{Q} \beta,$ where
$$
\mathbf{Q}:=\xi_{\text {orig }} \mathbf{X}^{\prime} \mathbf{X}+\xi_{\text {switch }}\left[\begin{array}{cc}
\mathbf{X}_{1}^{\prime} \mathbf{X}_{1} & \mathbf{X}_{1}^{\prime} \mathbf{W} \mathbf{X}_{2} \\
\mathbf{X}_{2}^{\prime} \mathbf{W} \mathbf{X}_{1} & \mathbf{X}_{2}^{\prime} \mathbf{X}_{2}
\end{array}\right], \quad \mathbf{q}:=\left(\xi_{\text {orig }} \mathbf{y}^{\prime} \mathbf{X}+\xi_{\text {switch }}\left[\begin{array}{c}
\mathbf{X}_{1}^{\prime} \mathbf{W} \mathbf{y} \\
\mathbf{X}_{2}^{\prime} \mathbf{y}
\end{array}\right]^{\prime}\right)^{\prime}
$$  
and $\mathbf{W}:=\frac{1}{n-1}\left(\mathbf{1}_{n} \mathbf{1}_{n}^{\prime}-\mathbf{I}_{n}\right) .$
> **_NOTE:_**
>
> - Thus, minimizing $\xi_{\text {orig }} \hat{e}_{\text {orig }}\left(f_{\beta}\right)+\xi_{\text {switch }} \hat{e}_{\text {switch }}\left(f_{\beta}\right)$ is equivalent to an unconstrained (possibly non-convex) quadratic program.
> - $\mathcal{F}_{\operatorname{lm}, r_{\operatorname{lm}}}:=\left\{f_{\beta}: f_{\beta}(x)=x^{\prime} \beta, \quad \beta \in \mathbb{R}^{p}, \quad \beta^{\prime} \mathbf{M}_{\operatorname{lm}} \beta \leq r_{\operatorname{lm}}\right\}$
> - The resulting optimization problem is a (possibly non-convex) quadratic program withone  quadratic  constraint  

**Lemma 17** (*Loss upper bound for linear models*) If $\mathbf{M}_{l m}$ is positive definite, $Y$ is bounded within a known range, and there exists a known constant $r_{\mathcal{X}}$ such that $x^{\prime} \mathbf{M}_{l m}^{-1} x \leq r_{\mathcal{X}}$ for all $x \in\left(\mathcal{X}_{1} \times \mathcal{X}_{2}\right),$ then Assumption 1 holds for the model class $\mathcal{F}_{l m, r_{l m}},$ the squared error loss function, and the constant  
$$
B_{\text {ind }}=\max \left[\left\{\min _{y \in \mathcal{Y}}(y)-\sqrt{r_{\mathcal{X}} r_{l m}}\right\}^{2},\left\{\max _{y \in \mathcal{Y}}(y)+\sqrt{r_{\mathcal{X}} r_{l m}}\right\}^{2}\right]
$$  

***Regression Models in a Reproducing Kernel Hilbert Space***  
$$
\mathcal{F}_{\mathbf{D}, r_{k}}=\left\{f_{\alpha}: f_{\alpha}(x)=\mu+\sum_{i=1}^{R} k\left(x, \mathbf{D}_{[i, \cdot]}\right) \alpha_{[i]}, \quad\left\|f_{\alpha}\right\|_{k} \leq r_{k}, \quad \alpha \in \mathbb{R}^{R}\right\}
$$  
Above, the norm $\left\|f_{\alpha}\right\|_{k}$ is defined as  
$$
\left\|f_{\alpha}\right\|_{k}:=\sum_{i=1}^{R} \sum_{j=1}^{R} \alpha_{[i]} \alpha_{[j]} k\left(\mathbf{D}_{[i, \cdot]}, \mathbf{D}_{[j, \cdot]}\right)=\alpha^{\prime} \mathbf{K}_{\mathbf{D}} \alpha
$$  

***Calculating MCR***
For any two constants $\xi_{\text {orig }}, \xi_{\text {switch }} \in \mathbb{R},$ we can show that minimizing the linear combination $\xi_{\text {orig }} \hat{e}_{\text {orig }}\left(f_{\alpha}\right)+\xi_{\text {switch }} \hat{e}_{\text {switch }}\left(f_{\alpha}\right)$ over $\mathcal{F}_{\mathbf{D}, r_{k}}$ is equivalent to the minimization problem  
$$
\begin{array}{l}
\text { minimize } \quad \frac{\xi_{\text {orig }}}{n}\left\|\mathbf{y}-\mu-\mathbf{K}_{\text {orig }} \alpha\right\|_{2}^{2}+\frac{\xi_{\text {switch }}}{n(n-1)}\left\|\mathbf{y}_{\text {switch }}-\mu-\mathbf{K}_{\text {switch }} \alpha\right\|_{2}^{2} \\
\text { subject to } \alpha^{\prime} \mathbf{K}_{\mathbf{D}} \alpha<r_{k} .
\end{array}
$$  

***Upper Bounding the Loss***  
**Lemma 18** (*Loss upper bound for regression in a RKHS*) Assume that $Y$ is bounded within a known range, and there exists a known constant $r_{\mathbf{D}}$ such that $v(x)^{\prime} \mathbf{K}_{\mathbf{D}}^{-1} v(x) \leq r_{\mathbf{D}}$ for all $x \in\left(\mathcal{X}_{1} \times \mathcal{X}_{2}\right),$ where $v: \mathbb{R}^{p} \rightarrow \mathbb{R}^{R}$ is the function satisfying $v(x)_{[i]}=k\left(x, \mathbf{D}_{[i, \cdot]}\right) .$ Under these  
conditions, Assumption 1 holds for the model class $\mathcal{F}_{\mathrm{D}, r_{k}},$ the squared error loss function,  
and the constant  
$$
B_{i n d}=\max \left[\left\{\min _{y \in \mathcal{Y}}(y)-\left(\mu+\sqrt{r_{\mathrm{D}} r_{k}}\right)\right\}^{2},\left\{\max _{y \in \mathcal{Y}}(y)+\left(\mu+\sqrt{r_{\mathrm{D}} r_{k}}\right)\right\}^{2}\right]
$$  

***Model Reliance and Causal Effects***  
- Let $f_{0}(t, c):=\mathbb{E}(Y \mid C=c, T=t)$, $\operatorname{CATE}(c):=\mathbb{E}\left(Y_{1}-Y_{0} \mid C=c\right)$    
  Proposition 19 (Causal interpretations of MR) For any prediction model $f,$ let $e_{\text {orig }}(f)$ and $e_{\text {switch }}(f)$ be defined based on the squared error loss $L(f,(y, t, c)):=(y-f(t, c))^{2}$ If $\left(Y_{1}, Y_{0}\right) \perp T \mid C$ (conditional ignorability) and $0<\mathbb{P}(T=1 \mid C=c)<1$ for all values of c (positivity), then $M R\left(f_{0}\right)$ is equal to  
  $$
  1+\frac{\operatorname{Var}(T)}{\mathbb{E}_{T, C} \operatorname{Var}(Y \mid T, C)} \sum_{t \in\{0,1\}}\left\{\mathbb{E}\left(Y_{1}-Y_{0} \mid T=t\right)^{2}+\operatorname{Var}(\operatorname{CATE}(C) \mid T=t)\right\}
  $$  
  where $\operatorname{Var}(T)$ is the marginal variance of the treatment assignment.

***Conditional Importance:  Adjusting for Dependence Between $X{1}$ and $X{2}$***  
$e_{\text {cond }}(f):=\mathbb{E}_{X_{2}} \mathbb{E}_{\left(Y^{(b)}, X_{1}^{(a)}, X_{2}^{(b)}\right)}\left[L\left\{f,\left(Y^{(b)}, X_{1}^{(a)}, X_{2}^{(b)}\right)\right\} \mid X_{2}^{(a)}=X_{2}^{(b)}=X_{2}\right]$  
$C M R(f)=\frac{e_{\text {cond }}(f)}{e_{\text {orig }}(f)}$  
> **_NOTE:_** This means that CMR will not be influenced by impossible combinations of $x_{1}$ and $x_{2}$, while MR may be influenced by them

***Estimation of CMR by Weighting, Matching, or Imputation***  
$\hat{e}_{\text {weight }}(f):=\frac{1}{n(n-1)} \sum_{i=1}^{n} \sum_{j \neq i} w\left(\mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[j, \cdot]}\right) \times L\left\{f,\left(\mathbf{y}_{[j]}, \mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[j, \cdot]}\right)\right\}$  
> **_NOTE:_**  
> - $\hat{e}_{\text {weight }}(f)$ is unbiased for $e_{\text {cond }}(f)$ $\hat{e}_{\text {match }}(f):=\frac{1}{n(n-1)} \sum_{i=1}^{n} \sum_{j \neq i} \frac{1\left(\mathbf{X}_{2[j, \cdot]}=\mathbf{X}_{2[i, \cdot]}\right)}{\mathbb{P}\left(X_{2}=\mathbf{X}_{2[i, j)}\right.} \times L\left\{f,\left(\mathbf{y}_{[j]}, \mathbf{X}_{1[i, \cdot]}, \mathbf{X}_{2[j, \cdot]}\right)\right\}$
> - if the inverse probability weight $\mathbb{P}\left(X_{2}=\mathbf{X}_{2[i, \cdot}\right)^{-1}$ is known, then $\hat{e}_{\text {match }}(f)$ is unbiased for $e_{\text {cond }}(f)$ (see Appendix A.7).
> - However, when the covariate space is continuous or high dimensional, we typically cannotestimate  CMR  nonparametrically.
> - When the covariate space is continuous or high dimensional we define $\mu_{1}$ to be the conditional expectation function $\mu_{1}\left(x_{2}\right)=\mathbb{E}\left(X_{1} \mid X_{2}=x_{2}\right),$ and assume that the random residual $X$ $\mu_{1}\left(X_{2}\right)$ is independent of $X_{2}$. Under this assumption, it can be shown that
>   $$
>   e_{\text {cond }}(f)=\mathbb{E} L\left[f,\left(Y^{(b)},\left\{X_{1}^{(a)}-\mu_{1}\left(X_{2}^{(a)}\right)\right\}+\mu_{1}\left(X_{2}^{(b)}\right), X_{2}^{(b)}\right)\right]
>   $$  

***Simulations of Bootstrap Confidence Intervals***
**идея**:  
* 1 подход: возьмём ориг. датасет (20k записей), посчитаем на нем MCR, разделим весь датасет на 2 части training subset and analysis subset
  - на training subset: обучаем reference model
  - на analysis subset: сэмплируем выборку (500 times) и считаем $\widehat{M C R}(\epsilon)$, а после CI
- 2 подход (проще): cэмплируем выборку с ориг. датасета (500 times), делим его на 2 части:
  - на 1ой части обучаем модель
  - на 2ой оцениваем её $\widehat{M C R}(\epsilon)$, получаем CI  
**Итог**: 1 подход more robust to the misspecification of the models used to approximate Y and the model of Y itself  
    
***COMPAS score***  
The bootstrap 95% CI for $\widehat{M C R}(\epsilon)$ on “inadmissible variables” is **[1.00, 1.73]**  
For “admissible variables” the $\widehat{M C R}(\epsilon)$ range with a 95% bootstrap CI is equal to **[1.62, 3.96]**  
