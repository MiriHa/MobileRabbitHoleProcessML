import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

path_questionnaire = r'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\rawData\data_MobileRabbitHole.csv'
path_raw = r'M:\+Dokumente\PycharmProjects\RabbitHoleProcess\data\rawData'

que_MRH1 = ['SD01', 'SD02_01', 'SD10', 'SD10_09', 'SD14']

milkGreen = '#0BCB85'
milkGreenDark = '#267355'
blueish = '#0378C5'
LightBlackishGray = '#6E707C'
DarkBlackishGray = '#6E707C'

matplotlib.rcParams["figure.dpi"] = 250
size = 11
ticksize = 11
legendsize = 11
plt.rc('font', size=size)  # controls default text size
plt.rc('axes', titlesize=size)  # fontsize of the title
plt.rc('axes', labelsize=size)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=ticksize)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=ticksize)  # fontsize of the y tick labels
plt.rc('legend', fontsize=legendsize)  # fontsize of the legend


def MRH_questionnaire_1():
    """
    Get statistics about demographics from questionnaires, calculate means
    Look at absentmined and general use score, check for normal distribution, make a paired ttest
    :return:
    """
    df_MRH1_raw = pd.read_csv(f'{path_raw}\MRH1.csv', sep=',')
    df_MRH2 = pd.read_csv(f'{path_raw}\MRH2.csv', sep=',')

    studIDs_mrh2 = df_MRH2['IM01_01']
    df_MRH1 = df_MRH1_raw.loc[df_MRH1_raw['IM01_01'].isin(studIDs_mrh2)]

    mean_age = df_MRH1['SD02_01'].mean()
    mean_gender = df_MRH1['SD01'].mean()
    val_count_age = df_MRH1['SD02_01'].value_counts()
    val_count_gender = df_MRH1['SD01'].value_counts()  # .sort_values(by=['correct_timestamp'], ascending=True, inplace=True)
    val_education = df_MRH1['SD10'].value_counts()

    print(mean_age)
    # 26.70967741935484
    # Just completed: 25.4
    print(mean_gender)
    # 1.2580645161290323
    # just completed: 1.2666666666666666
    print(val_count_age)

    print(val_count_gender)
    # 1:    23
    # 2:    8
    # just completed:
    # 1:    11
    # 2:    4
    print(val_education)

    # df_demograhpics = df_MRH1[:, ['SD02_01', 'SD01', 'SD10']]
    df_MRH1.describe().to_csv(fr'{path_raw}\MRH1_stats.csv')

    df_MRH1.SD02_01.dropna().astype('int64')
    df_MRH2.drop(df_MRH2.index[df_MRH2['IM01_01'] == 'BR22NO'], inplace=True)
    df_MRH1.drop(df_MRH1_raw.index[df_MRH1_raw['IM01_01'] == 'BR22NO'], inplace=True)
    # p = df_MRH1.SD02_01.value_counts(ascending=True).plot(kind = 'barh')
    # p = df_MRH1.SD01.value_counts().sort_index(axis=0).plot(kind = 'bar')

    absentminded = df_MRH1.loc[:, df_MRH1.columns.str.startswith('AB01')]
    general = df_MRH1.loc[:, df_MRH1.columns.str.startswith('AB02')]

    age = df_MRH1.loc[:, df_MRH1.columns.str.startswith('SD02_01')]
    gender = df_MRH1.loc[:, df_MRH1.columns.str.startswith('SD01')]

    print(absentminded.mean(axis=1))
    print(general.mean(axis=1))

    absentminded.hist()
    plt.show()
    general.hist()
    plt.show()

    k, p = stats.normaltest(absentminded)
    k1, p1 = stats.normaltest(general)
    k2, p2 = stats.normaltest(age)
    k3, p3 = stats.normaltest(gender)
    alpha = 0.05  # 1e-3
    print("normaltests")
    print("absentminded:", p)
    #    [0.67839887 0.47155547 0.90070218 0.73904268 0.39381979 0.22951735
    # 0.1396033  0.10960204 0.55445724 0.25119982 0.40092371 0.15104378
    # 0.75717849]
    # newer
    # [0.38109716 0.67456587 0.39003318 0.91103961 0.45712203 0.38518097
    # 0.57706751 0.32467301 0.71280548 0.2069535  0.65445096 0.11530959
    # 0.44832527]
    print("general", p1)
    #  [0.04559977 0.77212013 0.40138207 0.10396851 0.50288916 0.33793807
    #     # 0.1247074  0.37327643 0.01125694 0.43596354]
    #     newer
    # [0.01189665 0.91573161 0.34772621 0.22316487 0.12998592 0.35738561
    #  0.19171388 0.15131763 0.08837857 0.45434457]
    print("age", p2)
    # age [0.00067594] < alpha  not normal distrubted
    print("gender", p3)
    # gender [0.02488306] < alpha  not normal distributed

    # if(p < alpha):
    # f the p-val is very small, it means it is unlikely that the data came from a normal distribution. For example:
    #     print ("Not normal distribution")


def general_absentminded_use():
    """
    Calculate the general and absentminded use score form questions
    """
    df_MRH1_raw = pd.read_csv(f'{path_raw}\MRH1.csv', sep=',')
    df_MRH2 = pd.read_csv(f'{path_raw}\MRH2.csv', sep=',')
    #  FOR ju05 not mu but ab, ha07fl uppercase, br220 no in mrh1

    df_MRH2.drop(df_MRH2.index[df_MRH2['IM01_01'] == 'BR22NO'], inplace=True)
    df_MRH1_raw.drop(df_MRH1_raw.index[df_MRH1_raw['IM01_01'] == 'BR22NO'], inplace=True)
    # Select only users that are in both questionnaires
    studIDs_mrh2 = df_MRH2['IM01_01']
    df_MRH1 = df_MRH1_raw.loc[df_MRH1_raw['IM01_01'].isin(studIDs_mrh2)]

    df_MRH1 = df_MRH1.sort_values('IM01_01')
    df_MRH2 = df_MRH2.sort_values('IM01_01')

    df_MRH1.reset_index(drop=True, inplace=True)
    df_MRH2.reset_index(drop=True, inplace=True)

    mrh1_absentminded = df_MRH1.loc[:, df_MRH1.columns.str.startswith('AB01')]
    mrh1_general = df_MRH1.loc[:, df_MRH1.columns.str.startswith('AB02')]
    mean_mrh1_absentmineded = mrh1_absentminded.mean(axis=1)
    mean_mrh1_general = mrh1_general.mean(axis=1)

    mrh2_absentminded = df_MRH2.loc[:, df_MRH2.columns.str.startswith('AB01')]
    mrh2_general = df_MRH2.loc[:, df_MRH2.columns.str.startswith('AB02')]
    mean_mrh2_absentmineded = mrh2_absentminded.mean(axis=1)
    mean_mrh2_general = mrh2_general.mean(axis=1)

    print(mean_mrh1_absentmineded)
    print(mean_mrh2_absentmineded)
    print(mean_mrh1_absentmineded.mean())
    print(mean_mrh2_absentmineded.mean())
    print(mean_mrh1_general.mean())
    print(mean_mrh2_general.mean())

    stat_absentminded, p_absentminded = stats.ttest_rel(mean_mrh1_absentmineded, mean_mrh2_absentmineded)
    stat_general, p_general = stats.ttest_rel(mean_mrh1_general, mean_mrh2_general)

    print(stat_absentminded, p_absentminded)  # 2.2244055078094105 0.04308068974121597  newer  3.3727893009427348 0.00262594927608339
    print(stat_general, p_general)  # 0.759395726885135 0.4602122087200744  newer 1.0283034705551917 0.31450055033018165

    # df2_cols = df2.columns.drop('stdev')
    # out = [stats.ttest_ind(df2.loc[i, df2_cols], row, equal_var=True, nan_policy='omit')
    #    for i, row in df1.drop(columns=['stdev','Ctrl average']).iterrows()]
    # col = mrh2_general.columns
    # ttest = [stats.ttest_rel(mrh2_general.loc[i, col], row, nan_policy='omit') for i, row in mrh1_general.iterrows()]
    # '[Ttest_relResult(statistic=-0.28734788556634544, pvalue=0.7803523356242351), Ttest_relResult(statistic=0.6882472016116853, pvalue=0.5086464915963445), Ttest_relResult(statistic=-1.6269784336399213, pvalue=0.13818475535118327), Ttest_relResult(statistic=0.0, pvalue=1.0), Ttest_relResult(statistic=-1.9639610121239315, pvalue=0.0811261888458405), Ttest_relResult(statistic=0.4285714285714286, pvalue=0.6783097418055797), Ttest_relResult(statistic=1.5, pvalue=0.16785065605707486), Ttest_relResult(statistic=0.6882472016116853, pvalue=0.5086464915963445), Ttest_relResult(statistic=-3.0736305843324923, pvalue=0.013275877464573012), Ttest_relResult(statistic=-3.279648999660727, pvalue=0.009534613041301043), Ttest_relResult(statistic=1.9639610121239317, pvalue=0.0811261888458405), Ttest_relResult(statistic=-2.7136021011998723, pvalue=0.023856384540122025), Ttest_relResult(statistic=-0.8017837257372731, pvalue=0.44333185016966015), Ttest_relResult(statistic=-1.5, pvalue=0.16785065605707486), Ttest_relResult(statistic=3.086974532565159, pvalue=0.012992786487757368)]

    for i, row in mrh1_general.iterrows():
        col = mrh2_general.columns
        result_general = stats.ttest_rel(mrh2_general.loc[i, col], row, nan_policy='omit')
        df_MRH2.loc[i, 'general_use_mean_mrh1'] = row[col].mean()
        df_MRH2.loc[i, 'general_use_mean_mrh2'] = mrh2_general.loc[i, col].mean()
        df_MRH2.loc[i, 'general_use_ttest_stat'] = result_general[0]
        df_MRH2.loc[i, 'general_use_ttest_p-value'] = result_general[1]

    for i, row in mrh1_absentminded.iterrows():
        col = mrh2_absentminded.columns
        result_absentminded = stats.ttest_rel(mrh2_absentminded.loc[i, col], row, nan_policy='omit')
        df_MRH2.loc[i, 'absentminded_use_mean_mrh1'] = row[col].mean()
        df_MRH2.loc[i, 'absentminded_use_mean_mrh2'] = mrh2_absentminded.loc[i, col].mean()
        df_MRH2.loc[i, 'absentminded_ttest_stat'] = result_absentminded[0]
        df_MRH2.loc[i, 'absentminded_use_ttest_p-value'] = result_absentminded[1]

    df_MRH2.to_csv(f'{path_raw}\MRH2_new.csv')

    # As the p-value comes out to be less than 0.05 hence we reject the null hypothesis.
    # So, we have enough proof to claim that the true mean test score is different for cars before and after applying the different engine oil.


def influence():
    """
    Plot the results form the influence questions
    :return:
    """
    df_MRH2 = pd.read_csv(f'{path_raw}\MRH2.csv', sep=',')
    # TI01_01  influence: The Rabbit hole tracker application influenced my usual mobile phone interactions.
    # TI01_02 influence: Because of the rabbit hole tracker, I used my phone more than I usually do.
    # TI01_03 influence: Because of the rabbit hole tracker, I was more aware of my phone usage.
    # TI01_04 influence: Because of the rabbit hole tracker, I reduced my mobile phone usage time.
    # TI01_05 influence: The experience samplings / short questionnaires were shown to frequently.
    #
    # TI04_01: esm: I answered the experience samplings / short questionnaires correctly.
    # TI04_02: esm: The expereince sampling / short questionnaires annoyed me so much so that I just speeded through.

    df_list1 = [(df_MRH2.TI04_01, 'I answered the experience samplings correctly.'),
                (df_MRH2.TI04_02, 'The experience sampling annoyed me so much so that I just speeded through.'),
                (df_MRH2.TI01_05, 'The experience samplings were shown too frequently.')]

    df_list2 = [(df_MRH2.TI01_01, 'The Rabbit hole tracker application influenced my usual mobile phone interactions.'),
                (df_MRH2.TI01_02, 'Because of the rabbit hole tracker, I used my phone more than I usually do.'),
                (df_MRH2.TI01_03, ' Because of the rabbit hole tracker, I was more aware of my phone usage.'),
                (df_MRH2.TI01_05, ' Because of the rabbit hole tracker, I reduced my mobile phone usage time.')]

    nrow = 2
    ncol = 2

    bars = (1, 2, 3, 4, 5, 6, 7)
    bars_labels = ('1', '2', '3', ' 4', '5', '6', '7')
    bars_labels_alt = ('1 Strongly disagree', '2', '3', ' 4', '5', '6', '7 Strongly agree')
    bars_labels_all = ('Strongly disagree', 'Disagree', 'Somewhat disagree', ' Neutral', 'Somewhat agree', 'Agree', 'Strongly agree')
    fig, axes = plt.subplots(nrow, ncol)

    plot_bar(df_MRH2.TI01_01, bars=bars, labels=bars_labels, axes=axes[0, 0], title='a) The Rabbit hole tracker application influenced \nmy usual mobile phone interactions.')

    plot_bar(df_MRH2.TI01_02, bars=bars, labels=bars_labels, axes=axes[0, 1], title='b) Because of the rabbit hole tracker, \nI used my phone more than I usually do.')

    plot_bar(df_MRH2.TI01_03, bars=bars, labels=bars_labels, axes=axes[1, 0], title='c) Because of the rabbit hole tracker, \nI was more aware of my phone usage.')

    plot_bar(df_MRH2.TI01_04, bars=bars, labels=bars_labels, axes=axes[1, 1], title='d) Because of the rabbit hole tracker, \nI reduced my mobile phone usage time.')

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)
    plt.show()

    nrow = 3
    fig, axes = plt.subplots(nrow)
    plot_bar(df_MRH2.TI01_05, bars=bars, labels=bars_labels, axes=axes[0], title='a) The experience samplings  were shown to frequently.')
    plot_bar(df_MRH2.TI04_01, bars=bars, labels=bars_labels, axes=axes[1], title='b) I answered the experience samplings correctly.')
    plot_bar(df_MRH2.TI04_02, bars=bars, labels=bars_labels, axes=axes[2], title='c) The experience sampling annoyed me \n so much so that I just speeded through.')
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.6)
    plt.show()

    nrow = 2
    bars3 = (1, 2, 3)
    bars_labels3 = ('At home', 'At work/ school/ university', 'Other places')
    bars5 = (1, 2, 3, 4, 5)
    bars_labels5 = ('At home', 'At work/ school/ \nuniversity', 'Other places', ' While travelling', 'On the way to work/ \n school/ university')
    fig, axes = plt.subplots(nrow)
    plot_bar(df_MRH2.TI02, bars=bars3, labels=bars_labels3, axes=axes[0], title='a) Where do you mainly use a WLAN network as an Internet connection?', xlabelcustom="")
    plot_bar(df_MRH2.TI03, bars=bars5, labels=bars_labels5, axes=axes[1], title='b) Where do you mainly use a mobile internet connection?', xlabelcustom="")
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.6)
    plt.show()


def plot_bar(df, bars, labels, title, axes, lable_rotation=0, xlabelcustom='Likert Scale (1=Strongly Disagree, 7=Strongly Agree)'):
    p = df.value_counts().reindex(bars, fill_value=0).sort_index(axis=0).plot(kind="bar", ax=axes, ylabel='Counts', xlabel=xlabelcustom, color=milkGreen, title=title)
    p.set_xticklabels(labels, rotation=lable_rotation)
    p.grid(axis='y', linestyle='--', linewidth=0.3)
    return p


def plot_subplots_bar(df_list, ncol, nrow):
    bars = (1, 2, 3, 4, 5, 6, 7)
    fig, axes = plt.subplots(nrow, ncol)
    count = 0
    for r in range(nrow):
        for c in range(ncol):
            print(df_list[count][1])
            df_list[count][0].value_counts().reindex(bars, fill_value=0).sort_index(axis=0).plot(kind="bar", ylabel='Counts', xlabel='Likert Scale (1=Strongly Disagree, 7=Strongly Agree)',
                                                                                                 color=milkGreen, title=df_list[count][1])
            plt.grid(axis='y', linestyle='--', linewidth=0.3)
            count += 1

    plt.show()


def seperate():
    """
    Seperate the resutls into results from questionnaire MRH1 and questionnaire MRH2
    :return:
    """
    df_qu = pd.read_csv(path_questionnaire, sep=',')
    df_MRH1 = df_qu[df_qu['QUESTNNR'] == 'MRH1']
    df_MRH2 = df_qu[df_qu['QUESTNNR'] == 'MRH2']

    df_MRH1.dropna(axis=1, how='all').to_csv(fr'{path_raw}\MRH1.csv')
    df_MRH2.dropna(axis=1, how='all').to_csv(fr'{path_raw}\MRH2.csv')


def reindex():
    """
    Reset the index for the seperated Questionnaire results
    :return:
    """
    df_MRH1 = pd.read_csv(f'{path_raw}\MRH1.csv', sep=',')
    df_MRH2 = pd.read_csv(f'{path_raw}\MRH2.csv', sep=',')

    df_MRH1.reset_index(drop=True, inplace=True)
    df_MRH2.reset_index(drop=True, inplace=True)

    df_MRH1.to_csv(f'{path_raw}\MRH1.csv')
    df_MRH2.to_csv(f'{path_raw}\MRH2.csv')


if __name__ == '__main__':
    # 1. Seperate and reindex the results for a better overview
    seperate()
    reindex()

    # Get statistics and plots
    MRH_questionnaire_1()

    # Check and TTest the use scores
    general_absentminded_use()

    # Get the plots for the influnce questions
    influence()
