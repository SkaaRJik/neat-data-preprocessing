import json

import yaml
import logging
import logging.config
from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.processing.normalization.dataset_standard_normalizer import DatasetStandardNormalizer
from src.processing.verification.dataset_verification_pandas import DatasetVerificationPandas
from src.processing.report.ReportPredictionResultsExcelMaker import ReportPredictionResultsExcelMaker

from src.processing.normalization.dataset_min_max_normalizer import DatasetMinMaxNormalizer
from src.processing.normalization.dataset_normalizer import DatasetNormalizer
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.NormalizationDataConsumer import NormalizationDataConsumer
from src.rabbitmq.consumer.ReportResultConsumer import ReportResultConsumer
from src.rabbitmq.consumer.VerifyDocuementConsumer import VerifyDocumentConsumer
import traceback

from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger("infoLogger")

with open('../resources/application-dev.yml') as f:
    global_config = yaml.safe_load(f)

rabbitMqConfig: RabbitMQConfig = RabbitMQConfig(global_config)
sambaConfig: SambaConfig = SambaConfig(global_config)


def main():
    rabbitMqWorker: RabbitMQWorker = None
    sambaWorker: SambaWorker = None
    try:
        rabbitMqWorker: RabbitMQWorker = RabbitMQWorker(rabbitMqConfig)
        sambaWorker: SambaWorker = SambaWorker(sambaConfig)
        sambaWorker.connect()

        # config = rabbitMqConfig.INPUT_VERIFICATION_DOCUMENT_CONFIG
        # consumer = VerifyDocumentConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
        #                     routing_key=config.get("routingKey"),
        #                     exchange=config.get("exchange"), samba_worker=sambaWorker)
        # rabbitMqWorker.add_consumer(consumer)
        #
        # config = rabbitMqConfig.INPUT_NORMALIZE_DATA_CONFIG
        # consumer = NormalizationDataConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
        #                                   routing_key=config.get("routingKey"),
        #                                   exchange=config.get("exchange"), samba_worker=sambaWorker)
        # rabbitMqWorker.add_consumer(consumer)
        #
        # config = rabbitMqConfig.INPUT_REPORT_CONFIG
        # consumer = ReportResultConsumer(
        #     rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
        #     routing_key=config.get("routingKey"),
        #     exchange=config.get("exchange"), samba_worker=sambaWorker
        # )
        # rabbitMqWorker.add_consumer(consumer)
        #
        #
        #
        #
        #
        # rabbitMqWorker.run()


        #jsonReport = '{"experimentResultId":1,"model":{"neuronsLayers":[[{"lastActivation":0.0,"bias":-0.06277304412203968,"weights":null,"activationFunction":"y=x","id":1,"type":"INPUT","label":"Экологоемкость по воде (общий объем сточных вод на душу населения), куб.м/чел."},{"lastActivation":0.0,"bias":0.027043118062472327,"weights":null,"activationFunction":"y=x","id":2,"type":"INPUT","label":"Экологоемкость по отходам (общий объем отходов на душу населения), т/чел."},{"lastActivation":0.0,"bias":0.8289452695566921,"weights":null,"activationFunction":"y=x","id":3,"type":"INPUT","label":"Эко-интенсивность по воде, т/ USD"},{"lastActivation":0.0,"bias":-0.07874580301252741,"weights":null,"activationFunction":"y=x","id":4,"type":"INPUT","label":"Эко-интенсивность по отходам, т/ USD"},{"lastActivation":0.0,"bias":0.971737010003498,"weights":null,"activationFunction":"y=x","id":5,"type":"INPUT","label":"ВРП на душу населения, USD/чел."},{"lastActivation":0.0,"bias":0.5840949042795991,"weights":null,"activationFunction":"y=x","id":6,"type":"INPUT","label":"Валовой региональный продукт (в сопоставимых ценах), в процентах к предыдущему году"},{"lastActivation":0.0,"bias":0.41207981454362014,"weights":null,"activationFunction":"y=x","id":7,"type":"INPUT","label":"Инвестиции в основной капитал (ОК), в % к ВРП"},{"lastActivation":0.0,"bias":0.7871581484525875,"weights":null,"activationFunction":"y=x","id":8,"type":"INPUT","label":"Инвестиции в ОК на душу населения, USD/чел."},{"lastActivation":0.0,"bias":0.0917530340436025,"weights":null,"activationFunction":"y=x","id":9,"type":"INPUT","label":"Произ.пром.продук.на душу населения, USD/чел."},{"lastActivation":0.0,"bias":1.0637662444131002,"weights":null,"activationFunction":"y=x","id":10,"type":"INPUT","label":"Индексы промышлен. производства (в % к предыдущему году)"},{"lastActivation":0.0,"bias":0.013641003072678657,"weights":null,"activationFunction":"y=x","id":11,"type":"INPUT","label":"Инвестиции в ОК, направленные на охрану окружающей среды, в % к ВРП"},{"lastActivation":0.0,"bias":0.8864129763948984,"weights":null,"activationFunction":"y=x","id":12,"type":"INPUT","label":"Доля занятого насел. в экономике в общей числен.насел, %"},{"lastActivation":0.0,"bias":0.457140089917278,"weights":null,"activationFunction":"y=x","id":13,"type":"INPUT","label":"Уровень безработицы, %"},{"lastActivation":0.0,"bias":1.1420667531975202,"weights":null,"activationFunction":"y=x","id":14,"type":"INPUT","label":"Доля населения с доходами ниже прожиточного мин, в %"},{"lastActivation":0.0,"bias":0.6869837605402129,"weights":null,"activationFunction":"y=x","id":15,"type":"INPUT","label":"Среднедушевые доходы населения, USD/чел."}],[{"lastActivation":0.0,"bias":-0.36075730944593504,"weights":null,"activationFunction":"tanh(x)","id":32,"type":"HIDDEN","label":""},{"lastActivation":0.0,"bias":-0.3543554332984144,"weights":null,"activationFunction":"tanh(x)","id":35,"type":"HIDDEN","label":""},{"lastActivation":0.0,"bias":-0.242873512448979,"weights":null,"activationFunction":"tanh(x)","id":19,"type":"HIDDEN","label":""},{"lastActivation":0.0,"bias":-0.5393357154988833,"weights":null,"activationFunction":"tanh(x)","id":20,"type":"HIDDEN","label":""},{"lastActivation":0.0,"bias":0.9789485419295558,"weights":null,"activationFunction":"tanh(x)","id":53,"type":"HIDDEN","label":""},{"lastActivation":0.0,"bias":-0.39205510286182155,"weights":null,"activationFunction":"tanh(x)","id":25,"type":"HIDDEN","label":""}],[{"lastActivation":0.0,"bias":0.863656918344128,"weights":null,"activationFunction":"sigmoid(x)","id":16,"type":"OUTPUT","label":"Экологоемкость по воздуху (общий объем загрязнений на душу населения), т/чел."},{"lastActivation":0.0,"bias":0.7188885673486867,"weights":null,"activationFunction":"sigmoid(x)","id":17,"type":"OUTPUT","label":"Ожидаемая продолжительность жизни при рождении, лет"}]],"connections":[{"fromId":1,"toId":16,"weight":1.2583955789153078,"enabled":true},{"fromId":2,"toId":16,"weight":0.4016914971164335,"enabled":true},{"fromId":4,"toId":16,"weight":0.11738669060287688,"enabled":true},{"fromId":6,"toId":16,"weight":-0.14812638676911183,"enabled":true},{"fromId":7,"toId":16,"weight":0.6781774411599959,"enabled":true},{"fromId":9,"toId":16,"weight":-0.48014218954161203,"enabled":true},{"fromId":10,"toId":16,"weight":0.8615164109522069,"enabled":true},{"fromId":11,"toId":16,"weight":-0.6466541309369246,"enabled":true},{"fromId":13,"toId":16,"weight":-1.2703308037005803,"enabled":true},{"fromId":1,"toId":17,"weight":0.44612957540606524,"enabled":true},{"fromId":2,"toId":17,"weight":1.2029811156924572,"enabled":true},{"fromId":3,"toId":17,"weight":-0.5217562326629508,"enabled":true},{"fromId":4,"toId":17,"weight":-0.19918656269572887,"enabled":true},{"fromId":5,"toId":17,"weight":-0.053591351161347056,"enabled":true},{"fromId":6,"toId":17,"weight":-0.420563519292666,"enabled":true},{"fromId":7,"toId":17,"weight":0.8637520992336104,"enabled":true},{"fromId":8,"toId":17,"weight":-0.21827443649966027,"enabled":true},{"fromId":9,"toId":17,"weight":0.9060019900631229,"enabled":true},{"fromId":10,"toId":17,"weight":-0.8281975484081256,"enabled":true},{"fromId":11,"toId":17,"weight":-0.06439944828949806,"enabled":true},{"fromId":12,"toId":17,"weight":0.06114900424191194,"enabled":true},{"fromId":13,"toId":17,"weight":-0.23312038702807758,"enabled":true},{"fromId":14,"toId":17,"weight":-0.32241958885795885,"enabled":true},{"fromId":15,"toId":17,"weight":0.4910260297878226,"enabled":true},{"fromId":14,"toId":19,"weight":0.7429904160613672,"enabled":true},{"fromId":19,"toId":16,"weight":-0.5284112875993631,"enabled":true},{"fromId":12,"toId":25,"weight":0.7046389984305504,"enabled":true},{"fromId":25,"toId":16,"weight":-0.2631185247096087,"enabled":true},{"fromId":2,"toId":25,"weight":-0.14521787401531117,"enabled":true},{"fromId":5,"toId":32,"weight":-0.7246592360660662,"enabled":true},{"fromId":32,"toId":16,"weight":-0.7526879113474023,"enabled":true},{"fromId":3,"toId":25,"weight":0.23454377277720784,"enabled":true},{"fromId":8,"toId":53,"weight":0.7484139144699327,"enabled":true},{"fromId":53,"toId":16,"weight":-0.7322795747793109,"enabled":true},{"fromId":15,"toId":20,"weight":0.4874196187144342,"enabled":true},{"fromId":20,"toId":16,"weight":-0.2537145883841645,"enabled":true},{"fromId":7,"toId":25,"weight":0.05091991848190203,"enabled":true},{"fromId":3,"toId":35,"weight":0.9521092280188541,"enabled":true},{"fromId":35,"toId":16,"weight":0.883048603131658,"enabled":true}]},"trainErrors":[0.07529268853728657,0.11754640130955918,0.11754640130955918,0.11754640130955918,0.11754640130955918,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08393308123824289,0.08699282476742659,0.08651872830979639,0.08651872830979639,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.06589561834047983,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.07161847788281185,0.08115334695547408,0.08115334695547408,0.08115334695547408,0.08115334695547408,0.08115334695547408,0.08115334695547408,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07341627045772467,0.07412456977700728,0.07412456977700728,0.07412456977700728,0.07412456977700728,0.07412456977700728,0.07412456977700728,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308,0.06286318975798308],"testErrors":[0.1043210427957318,0.05643806567457532,0.05643806567457532,0.05643806567457532,0.05643806567457532,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.0761328291222309,0.06613789870148704,0.06388006610205783,0.06388006610205783,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.07465073845190026,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.06701360906217757,0.05594147684434451,0.05594147684434451,0.05594147684434451,0.05594147684434451,0.05594147684434451,0.05594147684434451,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05951143261943554,0.05563697724720828,0.05563697724720828,0.05563697724720828,0.05563697724720828,0.05563697724720828,0.05563697724720828,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511,0.06498950061413511],"predictionError":0.047219487104727634,"predictionResultFile":"user/EHKONOMIKA_I_POLITIKA/result-1.csv","windowTrainStatistic":{"targetSigns":[{"name":"Экологоемкость по воздуху (общий объем загрязнений на душу населения), т/чел."},{"name":"Ожидаемая продолжительность жизни при рождении, лет"}],"factorSigns":[{"name":"Экологоемкость по воде (общий объем сточных вод на душу населения), куб.м/чел.","columnType":"Input","trainError":0.03534133821060329,"testError":0.003768763876308465},{"name":"Экологоемкость по отходам (общий объем отходов на душу населения), т/чел.","columnType":"Input","trainError":0.01583060517144302,"testError":0.004020741611976844},{"name":"Эко-интенсивность по воде, т/ USD","columnType":"Input","trainError":0.009972890136299551,"testError":0.010016303031188042},{"name":"Эко-интенсивность по отходам, т/ USD","columnType":"Input","trainError":0.014684809890737638,"testError":0.008058327115280315},{"name":"ВРП на душу населения, USD/чел.","columnType":"Input","trainError":0.013253331479231478,"testError":0.018577452330627364},{"name":"Валовой региональный продукт (в сопоставимых ценах), в процентах к предыдущему году","columnType":"Input","trainError":0.0626888238797559,"testError":0.026741417882942875},{"name":"Инвестиции в основной капитал (ОК), в % к ВРП","columnType":"Input","trainError":0.04510929384012308,"testError":0.027035503471657063},{"name":"Инвестиции в ОК на душу населения, USD/чел.","columnType":"Input","trainError":0.052545008977414855,"testError":0.0174135555346899},{"name":"Произ.пром.продук.на душу населения, USD/чел.","columnType":"Input","trainError":0.025817045819687287,"testError":0.03880015443953266},{"name":"Индексы промышлен. производства (в % к предыдущему году)","columnType":"Input","trainError":0.04405110562268393,"testError":0.04358727554123524},{"name":"Инвестиции в ОК, направленные на охрану окружающей среды, в % к ВРП","columnType":"Input","trainError":0.05835969761167677,"testError":0.0453069743126948},{"name":"Доля занятого насел. в экономике в общей числен.насел, %","columnType":"Input","trainError":0.03353779363235413,"testError":0.01505691196824477},{"name":"Уровень безработицы, %","columnType":"Input","trainError":0.02780607672850915,"testError":0.004901641566274977},{"name":"Доля населения с доходами ниже прожиточного мин, в %","columnType":"Input","trainError":0.014928431233398607,"testError":0.009164020986204896},{"name":"Среднедушевые доходы населения, USD/чел.","columnType":"Input","trainError":0.009050659776822583,"testError":0.013723124692737742},{"name":"Экологоемкость по воздуху (общий объем загрязнений на душу населения), т/чел.","columnType":"Output","trainError":0.0463682146665913,"testError":0.06371816441802143},{"name":"Ожидаемая продолжительность жизни при рождении, лет","columnType":"Output","trainError":0.018735554399101993,"testError":0.005007897451577972}]},"projectId":2,"projectFolder":"user/EHKONOMIKA_I_POLITIKA","verifiedFile":"user/EHKONOMIKA_I_POLITIKA/ver-source.csv","experimentId":1,"columns":[{"columnType":"Output","columnName":"Экологоемкость по воздуху (общий объем загрязнений на душу населения), т/чел."},{"columnType":"Input","columnName":"Экологоемкость по воде (общий объем сточных вод на душу населения), куб.м/чел."},{"columnType":"Input","columnName":"Экологоемкость по отходам (общий объем отходов на душу населения), т/чел."},{"columnType":"Input","columnName":"Эко-интенсивность по воде, т/ USD"},{"columnType":"Input","columnName":"Эко-интенсивность по отходам, т/ USD"},{"columnType":"Input","columnName":"ВРП на душу населения, USD/чел."},{"columnType":"Input","columnName":"Валовой региональный продукт (в сопоставимых ценах), в процентах к предыдущему году"},{"columnType":"Input","columnName":"Инвестиции в основной капитал (ОК), в % к ВРП"},{"columnType":"Input","columnName":"Инвестиции в ОК на душу населения, USD/чел."},{"columnType":"Input","columnName":"Произ.пром.продук.на душу населения, USD/чел."},{"columnType":"Input","columnName":"Индексы промышлен. производства (в % к предыдущему году)"},{"columnType":"Input","columnName":"Инвестиции в ОК, направленные на охрану окружающей среды, в % к ВРП"},{"columnType":"Input","columnName":"Доля занятого насел. в экономике в общей числен.насел, %"},{"columnType":"Input","columnName":"Уровень безработицы, %"},{"columnType":"Input","columnName":"Доля населения с доходами ниже прожиточного мин, в %"},{"columnType":"Input","columnName":"Среднедушевые доходы населения, USD/чел."},{"columnType":"Output","columnName":"Ожидаемая продолжительность жизни при рождении, лет"}],"legend":{"data":[1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017],"header":"год","increment":{"type":"<class 'numpy.int64'>","increment":1.0}},"neatSettings":[{"show":true,"header":"HEADER_GENETIC_ALGORITHM","params":[{"name":"GENERATOR.SEED","value":1548235723799,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.MUTATION","value":0.25,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.CROSSOVER","value":0.5,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"PROBABILITY.ADDLINK","value":0.1,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.ADDNODE","value":0.03,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.NEWACTIVATIONFUNCTION","value":0.1,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.MUTATEBIAS","value":0.3,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"PROBABILITY.TOGGLELINK","value":0.1,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"PROBABILITY.WEIGHT.REPLACED","value":0.5,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_NICHE_SETTING","params":[{"name":"EXCESS.COEFFICIENT","value":1,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"DISJOINT.COEFFICIENT","value":1,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"WEIGHT.COEFFICIENT","value":0.4,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_SPECIES_CONTROL","params":[{"name":"COMPATABILITY.THRESHOLD","value":0.5,"maxValue":1,"minValue":0,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"COMPATABILITY.CHANGE","value":0.1,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.COUNT","value":3,"maxValue":5,"minValue":1,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SURVIVAL.THRESHOLD","value":0.2,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.AGE.THRESHOLD","value":80,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.YOUTH.THRESHOLD","value":10,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.OLD.PENALTY","value":1.2,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.YOUTH.BOOST","value":0.7,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"SPECIE.FITNESS.MAX","value":15,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_NETWORK_SETTING","params":[{"name":"MAX.PERTURB","value":0.5,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"MAX.BIAS.PERTURB","value":0.1,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"FEATURE.SELECTION","value":false,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"RECURRENCY.ALLOWED","value":false,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_ACTIVATION_FUNCTIONS","params":[{"name":"INPUT.ACTIVATIONFUNCTIONS","value":["org.neat4j.neat.nn.core.functions.LinearFunction","",""],"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"OUTPUT.ACTIVATIONFUNCTIONS","value":["","org.neat4j.neat.nn.core.functions.SigmoidFunction",""],"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"HIDDEN.ACTIVATIONFUNCTIONS","value":["","","org.neat4j.neat.nn.core.functions.TanhFunction"],"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_LIFE_CONTROL","params":[{"name":"ELE.EVENTS","value":false,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"ELE.SURVIVAL.COUNT","value":0.1,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"ELE.EVENT.TIME","value":1000,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true}]},{"show":true,"header":"HEADER_EPOCH_CONTROL","params":[{"name":"KEEP.BEST.EVER","value":true,"maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"EXTRA.FEATURE.COUNT","value":0,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"POP.SIZE","value":150,"maxValue":300,"minValue":1,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"NUMBER.EPOCHS","value":100,"maxValue":1000,"minValue":1,"showInGui":true,"isAdvanced":false,"allowedToChangeByUser":true},{"name":"TERMINATION.VALUE.TOGGLE","value":false,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true},{"name":"TERMINATION.VALUE","value":1.0E-5,"maxValue":null,"minValue":null,"showInGui":true,"isAdvanced":true,"allowedToChangeByUser":true}]},{"show":false,"header":"SERVICE","params":[{"name":"OPERATOR.XOVER","value":"org.neat4j.neat.core.xover.NEATCrossover","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"OPERATOR.FUNCTION","value":"org.neat4j.neat.core.fitness.MSENEATFitnessFunction","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"OPERATOR.PSELECTOR","value":"org.neat4j.neat.core.pselectors.TournamentSelector","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"OPERATOR.MUTATOR","value":"org.neat4j.neat.core.mutators.NEATMutator","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"NATURAL.ORDER.STRATEGY","value":true,"maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"LEARNABLE","value":"org.neat4j.neat.nn.core.learning.GALearnable","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"AI.TYPE","value":"GA","maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false}]},{"show":false,"header":"NODE.COUNTERS","params":[{"name":"INPUT.NODES","value":15,"maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false},{"name":"OUTPUT.NODES","value":2,"maxValue":null,"minValue":null,"showInGui":false,"isAdvanced":true,"allowedToChangeByUser":false}]}],"normalizationMethod":"minMax","enableLogTransform":null,"predictionPeriod":10,"predictionWindowSize":3,"trainEndIndex":14,"testEndIndex":20}'

        jsonReport = ''
        with open('../resources/test.json') as f:
            jsonReport = f.read()


        decoded_body: dict = json.loads(jsonReport)

        experiment_result_id = decoded_body.get("experimentResultId")
        model = decoded_body.get("model")
        train_errors = decoded_body.get("trainErrors")
        test_errors = decoded_body.get("testErrors")
        prediction_error = decoded_body.get("predictionError")
        prediction_result_file_path = decoded_body.get("predictionResultFile")
        window_train_statistic = decoded_body.get("windowTrainStatistic")

        experiment_id = decoded_body.get("experimentId")
        project_id = decoded_body.get("projectId")
        project_folder = decoded_body.get("projectFolder")
        source_file_path: str = decoded_body.get("verifiedFile")
        columns = decoded_body.get("columns")
        legend = decoded_body.get("legend")
        neat_settings = decoded_body.get("neatSettings")

        normalization_method = decoded_body.get("normalizationMethod")
        enable_log_transform = decoded_body.get("enableLogTransform")
        prediction_period = decoded_body.get("predictionPeriod")
        prediction_window_size = decoded_body.get("predictionWindowSize")
        train_end_index = decoded_body.get("trainEndIndex")
        test_end_index = decoded_body.get("testEndIndex")



        temp = f'source-{project_id}-{experiment_id}.csv'
        source_file = sambaWorker.download(source_file_path, temp)
        temp = f'results-{project_id}-{experiment_id}.csv'
        result_file = sambaWorker.download(prediction_result_file_path, temp)

        reportMaker = ReportPredictionResultsExcelMaker()
        reportMaker.makeExcelReport(source_file.name,
                                    result_file.name,
                                    train_errors,
                                    test_errors,
                                    prediction_error,
                                    window_train_statistic,
                                    columns,
                                    legend,
                                    neat_settings,
                                    normalization_method,
                                    enable_log_transform,
                                    prediction_period,
                                    prediction_window_size,
                                    train_end_index,
                                    test_end_index
                                    )


    except BaseException as error:
        traceback.print_exc()
        LOGGER.exception(error)
    finally:
        if rabbitMqWorker is not None:
            rabbitMqWorker.close_connection()
        if sambaWorker is not None:
            sambaWorker.close()

    # normalization_file = '../resources/data.csv'
    # normalization_data: DatasetNormalizer = DatasetStandardNormalizer()
    # normalization_data.normalize(normalization_file)


    # dataset_verification = DatasetVerificationPandas()
    # correct_file = '../resources/data.xlsx'
    # # # file_date_empty = '../resources/data1.xlsx'
    # # file_number_empty = '../resources/data2.xlsx'
    #
    # # dataset_verification.verify_excel(correct_file)
    # legend_error_protocol, legend_info_protocol, legend_inc, legend_values, headers_error_protocol, legend_header, \
    # data_headers, values_error_protocol, values_info_protocol, dataframe_to_save = dataset_verification.verify_excel(
    #     correct_file)
    # verification_protocol = {
    #     "projectId": 1,
    #     "errors": VerifyDocumentConsumer.pack_error_protocols(legend_error_protocol=legend_error_protocol,
    #                                          headers_error_protocol=headers_error_protocol,
    #                                          values_error_protocol=values_error_protocol),
    #     "info": VerifyDocumentConsumer.pack_info_protocols(legend_info_protocol=legend_info_protocol,
    #                                       values_info_protocol=values_info_protocol),
    #     "verifiedFile": '/tmp/{0}'.format("file_name.csv"),
    #     "legend": {
    #         "header": legend_header,
    #         "data": legend_values,
    #         "increment": legend_inc
    #     },
    #     "headers": data_headers,
    # }
    #
    # encoded_body = json.dumps(verification_protocol)
    # print(encoded_body)

# dataset_verification = DatasetVerificationPandas()
# dataset_verification.verify_excel(correct_file)
# legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
# data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)
# #dataset_verification.verify_excel(file_number_empty)

if __name__ == "__main__":
    main()
