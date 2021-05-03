import pandas as pd
import re
from openpyxl import Workbook

from src.exceptions.WrongNormalizationMethodException import WrongNormalizationMethodException
from src.processing.normalization.dataset_normalizer import DatasetNormalizer
from src.processing.normalization.dataset_normalizer_factory import DatasetNormalizerFactory
from openpyxl.chart import LineChart, Reference

class ReportPredictionResultsExcelMaker(object):

    def __init__(self):
        self._dataset_normalizer_factory = DatasetNormalizerFactory()
        self._neat_settings_translations = {
            'HEADER_GENETIC_ALGORITHM': 'Параметры генетического алгоритма',
            'HEADER_EPOCH_CONTROL': 'Контроль эпох',
            'HEADER_ACTIVATION_FUNCTIONS': 'Настройки активационных функций:',
            'HEADER_NETWORK_SETTING': 'Настройки нейросети',
            'HEADER_NICHE_SETTING': 'Настройки нишинга',
            'HEADER_SPECIES_CONTROL': 'Контроль видообразования',
            'HEADER_LIFE_CONTROL': 'Контроль жизнеспособности',
            'PROBABILITY.MUTATION': 'Вероятность мутации',
            'PROBABILITY.CROSSOVER': 'Вероятность кроссинговера',
            'PROBABILITY.ADDLINK': 'Вероятность новой связи',
            'PROBABILITY.ADDNODE': 'Вероятность нового нейрона',
            'PROBABILITY.NEWACTIVATIONFUNCTION': 'Вероятность мутации актив. функции',
            'PROBABILITY.MUTATEBIAS': 'Вероятность мутации байеса',
            'PROBABILITY.TOGGLELINK': 'Вероятность включ/исключ. связи',
            'PROBABILITY.WEIGHT.REPLACED': 'Вероятность изменения веса',
            'GENERATOR.SEED': 'Семя генератора случ. чисел',
            'EXCESS.COEFFICIENT': 'Коэф-нт дополнительных генов (c1)',
            'DISJOINT.COEFFICIENT': 'Коэф-нт непересекающихся генов (c2)',
            'WEIGHT.COEFFICIENT': 'Коэф-нт средней разницы весов совпадающих генов (c3)',
            'COMPATABILITY.THRESHOLD': 'Пороговое значение соответствия особей внутри вида',
            'COMPATABILITY.CHANGE': 'Значение совместимости мутаций',
            'SPECIE.COUNT': 'Макс. количество видов',
            'SURVIVAL.THRESHOLD': 'Пороговое значение выживания',
            'SPECIE.AGE.THRESHOLD': 'Макс. время жизни особи',
            'SPECIE.YOUTH.THRESHOLD': 'Порог, до которого особь считается молодой',
            'SPECIE.OLD.PENALTY': 'Штраф для старой особи',
            'SPECIE.YOUTH.BOOST': 'Ускорение для молодой особи',
            'SPECIE.FITNESS.MAX': 'Максимальное значение приспособленности',
            'MAX.PERTURB': 'Макс. смащение весов',
            'MAX.BIAS.PERTURB': 'Макс. смещение байеса',
            'FEATURE.SELECTION': 'Отбор фич',
            'RECURRENCY.ALLOWED': 'Разрешить рекурентность',
            'INPUT.ACTIVATIONFUNCTIONS': 'Входной слой',
            'OUTPUT.ACTIVATIONFUNCTIONS': 'Выходной слой',
            'HIDDEN.ACTIVATIONFUNCTIONS': 'Скрытый слой',
            'ELE.EVENTS': 'Включить контроль вымирания',
            'ELE.SURVIVAL.COUNT': 'Extinction survival count',
            'ELE.EVENT.TIME': 'Время вымирания',
            'KEEP.BEST.EVER': 'Всегда сохранять лучшего',
            'EXTRA.FEATURE.COUNT': 'Дополнительные аллели',
            'POP.SIZE': 'Размер популяции',
            'NUMBER.EPOCHS': 'Количество эпох',
            'org.neat4j.neat.nn.core.functions.LinearFunction': 'y = x',
            'org.neat4j.neat.nn.core.functions.SigmoidFunction': 'sigmoid(x)',
            'org.neat4j.neat.nn.core.functions.TanhFunction': 'tg(x)',
            'TERMINATION.VALUE.TOGGLE': 'Включить прерывание',
            'TERMINATION.VALUE': 'Значение остановки'
        }



    def makeExcelReport(self, source_file: str,
                                    result_file: str,
                                    train_errors: list,
                                    test_errors: list,
                                    prediction_error,
                                    window_train_statistic: dict,
                                    columns: list,
                                    legend: dict,
                                    neat_settings: list,
                                    normalization_method: str,
                                    enable_log_transform: bool,
                                    prediction_period: int,
                                    prediction_window_size: int,
                                    train_end_index: int,
                                    test_end_index: int
                                    ):


        input_columns = []
        output_columns = []


        for column in columns:  # type: dict
            if column.get('columnType') == 'Output':
                output_columns.append(column.get("columnName"))
            if column.get('columnType') == 'Input':
                input_columns.append(column.get("columnName"))

        source_data_frame: pd.DataFrame = pd.read_csv(source_file, sep=';')
        prediction_data_frame: pd.DataFrame = pd.read_csv(result_file, sep=';')

        for column_name in output_columns:
            column_name_with_predicted_values = f'{column_name}.1'
            source_data_frame.insert(source_data_frame.columns.size, column_name_with_predicted_values, source_data_frame[column_name])


        prediction_data_frame: pd.DataFrame = self._denormalize_data(normalization_method, enable_log_transform, prediction_data_frame, source_data_frame)
        wb = Workbook()
        #regex = re.compile(r'[^\d\wА-Яа-я]', re.IGNORECASE)
        i = 0
        new_legend_data = self._calculate_legend(legend.get('data'), legend.get('increment').get('increment'), prediction_period)


        for column_name in output_columns: # type: str
            #sheet_name = re.sub(regex, '', column_name.strip().replace(" ", "_"))
            sheet = wb.active
            if i == 0:
                sheet.title = f'{i+1}_Целевой_показатель'
            else:
                wb.create_sheet(f'{i+1}_Целевой_показатель')
                sheet = wb[f'{i+1}_Целевой_показатель']
            i += 1
            sheet['A1'] = 'Прогноз целевого показателя:'
            sheet['B1'] = column_name
            sheet['A2'] = 'Ошибка прогнозирования:'
            sheet['B2'] = prediction_error
            sheet['A3'] = legend.get("header")
            sheet['B3'] = 'Факт'
            sheet['C3'] = 'Прогноз'
            column_name_with_predicted_values=f'{column_name}.1'
            source_end_address = self._write_vector_as_column("B",4, sheet, source_data_frame[column_name].values.data)
            predicted_end_address = self._write_vector_as_column("C",4, sheet, prediction_data_frame[column_name_with_predicted_values].values.data)
            legend_end_address = self._write_vector_as_column("A",4, sheet, new_legend_data)
            self._create_chart_for_factor_and_predicted_values(sheet, column_name, legend.get("header"), 'F1', 1,3,3,source_end_address)





        temp = '/tmp/report-1.xlsx'
        wb.save(temp)
        return temp

    def _write_vector_as_column(self, column: str, row: int, sheet, vector: list) -> int:
        end_address = ''
        for i, value in enumerate(vector):
            end_address = f'{column}{row+i}'
            sheet[end_address] = value
            end_address= row+i
        return end_address

    def _denormalize_data(self, normalization_method: str, log_transformed: bool, dataframe_to_denormalize: pd.DataFrame, source_data_frame: pd.DataFrame) -> pd.DataFrame:
        data_normalizer: DatasetNormalizer = self._dataset_normalizer_factory.getNormalizer(normalization_method)

        if data_normalizer is None:
            raise WrongNormalizationMethodException('{0} - method not found'.format(normalization_method))

        return data_normalizer.denormalize(dataframe_to_denormalize, source_data_frame,log_transformed)

    def _calculate_legend(self, legend_data: list, increment, prediction_period: int) -> list:
        new_legend_data = legend_data[:]

        for i in range(prediction_period):
            new_legend_data.append(new_legend_data[-1]+increment)

        return new_legend_data

    def _create_chart_for_factor_and_predicted_values(self, sheet, title, legend_name, chart_pos: str, data_start_column, data_start_row, data_end_column, data_end_row):
        c1 = LineChart()
        c1.title = title
        c1.style = 14
        c1.y_axis.title = 'Значения'
        c1.x_axis.title = legend_name

        data = Reference(sheet, min_col=data_start_column+1, min_row=data_start_row, max_col=data_end_column, max_row=data_end_row)
        c1.add_data(data, titles_from_data=True)


        # Style the lines
        s1 = c1.series[0]
        s1.marker.symbol = "triangle"
        s1.marker.graphicalProperties.solidFill = "FF0000"  # Marker filling
        s1.marker.graphicalProperties.line.solidFill = "FF0000"  # Marker outline

        s1.graphicalProperties.line.noFill = True

        s2 = c1.series[0]
        s2.graphicalProperties.line.solidFill = "00AAAA"
        s2.graphicalProperties.line.dashStyle = "sysDot"
        s2.graphicalProperties.line.width = 100050  # width in EMUs

        s2 = c1.series[1]
        s2.smooth = True  # Make the line smooth

        sheet.add_chart(c1, chart_pos)