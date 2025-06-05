import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Загрузка таблицы с данными
apb_data = pd.read_csv('approbation_data.csv')

# Функция для удаления ненужных столбцов и переименования оставшихся столбцов для удобства работы
def main():
    apb_data.drop(columns=['В данном поле вы можете оставить свои замечания или пожелания для лабораторной работы по RC4.',
                           'В данном поле вы можете оставить свои замечания или пожелания для лабораторной работы по KASUMI.'],
                  inplace=True)
    apb_data.rename(columns={'Оценка качества теоретического материала (RC4) / Оцените понятность теоретического материала (RC4)': 'theory_rc4',
                             'Оценка качества теоретического материала (RC4) / Оцените понятность приведенного примера (RC4)': 'example_rc4',
                             'Оценка качества теоретического материала (RC4) / Оцените понятность формулировки задания (RC4)': 'task_rc4',
                             'Оценка сложности задания (RC4) / Насколько, по вашему мнению, задание было сложным (RC4)': 'task_difficulty_rc4',
                             'Оценка качества теоретического материала (KASUMI) / Оцените понятность теоретического материала (KASUMI)': 'theory_kasumi',
                             'Оценка качества теоретического материала (KASUMI) / Оцените понятность формулировки задания (KASUMI)': 'task_kasumi',
                             'Оценка сложности задания (KASUMI) / Насколько, по вашему мнению, задание было сложным (KASUMI)': 'task_difficulty_kasumi'},
                    inplace=True)

# Функция для создания гистограмм по оценкам теоретических и практических частей лабораторных работ
def create_histplots():
    # Создаем таблицу для построения гистограмм по метрикам для RC4
    hist_data_rc4 = pd.DataFrame({'value': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']})
    for name in ['theory_rc4', 'example_rc4', 'task_rc4', 'task_difficulty_rc4']:
        hist_data_rc4[name] = [apb_data.loc[apb_data[name] == i].loc[:, name].count() for i in range(1, 11)]
    hist_data_rc4.rename(columns={'theory_rc4': 'Понятность теории',
                                  'example_rc4': 'Понятность примера',
                                  'task_rc4': 'Понятность задания',
                                  'task_difficulty_rc4': 'Сложность задания'},
                         inplace=True)

    # Создаем таблицу для построения гистограмм по метрикам для KASUMI
    hist_data_kasumi = pd.DataFrame({'value': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']})
    for name in ['theory_kasumi', 'task_kasumi', 'task_difficulty_kasumi']:
        hist_data_kasumi[name] = [apb_data.loc[apb_data[name] == i].loc[:, name].count() for i in range(1, 11)]
    hist_data_kasumi.rename(columns={'theory_kasumi': 'Понятность теории',
                                     'task_kasumi': 'Понятность задания',
                                     'task_difficulty_kasumi': 'Сложность задания'},
                            inplace=True)

    # Гистограммы с оценками теории по RC4
    fig_rc4_theory, (ax_rc4_1, ax_rc4_2, ax_rc4_3) = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for ax_rc4, name in zip([ax_rc4_1, ax_rc4_2, ax_rc4_3], ['Понятность теории', 'Понятность примера', 'Понятность задания']):
        sns.histplot(hist_data_rc4, x='value', weights=name, ax=ax_rc4)
        ax_rc4.set_title(name)
        ax_rc4.set_xlabel('Оценка')
        ax_rc4.set_ylabel('Количество оценок')

    # Гистограммы с оценками теории по KASUMI
    fig_kasumi_theory, (ax_kasumi_1, ax_kasumi_2) = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
    for ax_kasumi, name in zip([ax_kasumi_1, ax_kasumi_2], ['Понятность теории','Понятность задания']):
        sns.histplot(hist_data_kasumi, x='value', weights=name, ax=ax_kasumi)
        ax_kasumi.set_title(name)
        ax_kasumi.set_xlabel('Оценка')
        ax_kasumi.set_ylabel('Количество оценок')

    # Гистограмма оценок сложности задания по RC4
    fig_rc4_practice, ax_rc4_practice = plt.subplots(figsize=(4, 4))
    sns.histplot(hist_data_rc4, x='value', weights='Сложность задания', ax=ax_rc4_practice)
    ax_rc4_practice.set_title('Сложность задания RC4')
    ax_rc4_practice.set_xlabel('Оценка')
    ax_rc4_practice.set_ylabel('Количество оценок')

    # Гистограмма оценок сложности задания по KASUMI
    fig_kasumi_practice, ax_kasumi_practice = plt.subplots(figsize=(4, 4))
    sns.histplot(hist_data_kasumi, x='value', weights='Сложность задания', ax=ax_kasumi_practice)
    ax_kasumi_practice.set_title('Сложность задания KASUMI')
    ax_kasumi_practice.set_xlabel('Оценка')
    ax_kasumi_practice.set_ylabel('Количество оценок')

    # Сохранение созданных гистограмм в виде .png изображений
    fig_rc4_theory.savefig('RC4_Оценка_Теории.png')
    fig_kasumi_theory.savefig('KASUMI_Оценка_Теории.png')
    fig_rc4_practice.savefig('RC4_Оценка_Сложности_Практики.png')
    fig_kasumi_practice.savefig('KASUMI_Оценка_Сложности_Практики.png')

# Функция для вывода средних значений по каждой метрики
def data_mean():
    print(apb_data.mean().round(2))

if __name__ == '__main__':
    main()
    print(apb_data.corr().to_excel('test.xlsx'))