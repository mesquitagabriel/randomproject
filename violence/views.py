from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.base import TemplateView, View
from django.template import Context
from django.http import HttpResponse
from pymongo import MongoClient
import datetime
import pandas as pd
#from nltk.corpus import stopwords
from collections import Counter
import json


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.frases

        words = []
        articles = collection.find().limit(1000)
        for article in articles:
            for frase in article['frases']:
                words += frase

        result = []
        count = 0
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~=”“–'
        mystop = ["está", "às", "até", "tem", "foi", "anos", "dos", "não", "também", "à", "ser", "são", "já", "com", "abaixo", "aca", "acaso","acerca", "acima", "acola", "acula", "ademais", "adentro","adiante", "afinal", "afora", "agora", "agorinha", "ah", "ainda","alem", "algo", "alguem", "algum", "alguma", "algumas", "alguns","ali", "alias", "alo", "ambos", "amiude", "ante", "antes", "ao","aonde", "aos", "apenas", "apesar", "apos", "apud", "aquela","aquelas", "aquele", "aqueles", "aqui", "aquilo", "as", "assim","ate", "atras", "atraves", "basicamente", "bastante", "bastantes","bem", "bis", "bom", "ca", "cada", "cade", "caso", "certa","certamente", "certas", "certeiramente", "certo", "certos", "chez","chi", "comigo", "como", "comumente", "conforme", "confronte","conosco", "conquanto", "consequentemente", "consigo", "consoante","contanto", "contigo", "contra", "contudo", "convosco", "cuja","cujas", "cujo", "cujos", "da", "dai", "dali", "dantes", "daquela","daquelas", "daquele", "daqueles", "daqui", "daquilo", "das", "de","debaixo", "defronte", "dela", "delas", "dele", "deles", "demais","dentre", "dentro", "depois", "desde", "dessa", "dessas", "desse","desses", "desta", "destas", "deste", "destes", "detras","deveras", "diante", "disso", "disto", "diversos", "do", "donde","doravante", "dum", "duma", "dumas", "duns", "durante", "eia","eis", "ela", "elas", "ele", "eles", "em", "embaixo", "embora","enfim", "enquanto", "entanto", "entao", "entre", "entretanto","exceto", "essa", "essas", "esse", "esses", "esta", "estas","este", "estes", "eu", "exatamente", "exceto", "felizmente","frequentemente", "fora", "gracas", "hem", "hum", "ibidem", "idem","in", "inclusive", "inda", "infelizmente", "inicialmente", "isso","ja", "jamais", "la", "las", "largamente", "lha", "lhas", "lhe","lhes", "lho", "lhos", "lo", "los", "logo", "mais", "mal","malgrado", "mas", "me", "mediante", "menos", "meramente", "mesma","mesmas", "mesmo", "mesmos", "meu", "meus", "mim", "minha","minhas", "mui", "muita", "muitas", "muitissimo", "muito","muitos", "mutuamente", "na", "nada", "nadinha", "nalgum","nalguma", "nalgumas", "nalguns", "naquela", "naquelas", "naquele","naqueles", "naquilo", "nao", "nas", "nela", "nelas", "nele","neles", "nem", "nenhum", "nenhuns", "nenhuma", "nenhumas","nessa", "nessas", "nesse", "nesses", "nesta", "nestas", "neste","nestes", "ninguem", "nisso", "nisto", "no", "nos", "nossa","nossas", "nosso", "nossos", "noutra", "noutras", "noutro","noutros", "novamente", "num", "numa", "numas", "nunca","nunquinha", "nuns", "oba", "ola", "onde", "ontem", "opa", "ora","os", "ou", "outra", "outras", "outrem", "outro", "outrora","outros", "outrossim", "para", "pela", "pelas", "pelo", "pelos","per", "perante", "pero", "pois", "por", "porem", "porquanto","porque", "portanto", "porventura", "possivelmente","posteriormente", "posto", "pouca", "poucas", "pouco", "poucos","pra", "praquela", "praquelas", "praquele", "praqueles","praquilo", "pras", "praticamente", "prela", "prelas", "prele","preles", "preste", "prestes", "previamente", "primeiramente","principalmente", "priori", "pronto", "propria", "proprias","proprio", "proprios", "proximo", "qual", "qualquer", "quais","quaisquer", "quando", "quanta", "quantas", "quanto", "quantos","quao", "quase", "que", "quem", "quer", "quica", "raramente","realmente", "recentemente", "salvante", "se", "segundo","seguramente", "seja", "sem", "sempre", "senao", "sequer", "seu","seus", "sim", "simplesmente", "sob", "sobre", "sobremaneira","sobremodo", "sobretudo", "somente", "sua", "suas", "tal", "tais","talvez", "tambem", "tampouco", "tanta", "tantas", "tanto","tantos", "tao", "te", "teu", "teus", "tirante", "toda", "todas","todavia", "todo", "todos", "tras", "tu", "tua", "tuas", "tudo","um", "uma", "umas", "uns", "varias", "varios", "vezes", "visto", "voce", "voces", "vos", "vossa", "vossas", "vossos", "vulgo"]
        #stopw = stopwords.words('portuguese')
        #stopw += mystop
        stopw = mystop+['cdn', 'cb','é','b','td','br','00','img','src','alt','jpg','png','right','r','http','float','style','thumbnail','ss_thumbnails']

        for word_freq in Counter(words).most_common():
            if word_freq[0] not in punctuation+"0123456789£" and word_freq[0] not in stopw:
                for caracter in word_freq[0]:
                    if caracter not in punctuation:
                        result.append(word_freq)
                        count +=1
                        break
            if count == 10:
                break
        suma = float(sum([pair[1] for pair in result]))
        data_cloud = [{'text': pair[0], 'size': int(pair[1]*1000/suma)} for pair in result]

        enddata = datetime.datetime.now() - datetime.timedelta(days=70)
        startdata = enddata.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=29) #last 30 days

        df = pd.DataFrame(columns=['data','count'])
        for article in collection.find({'published':{'$gte': startdata, '$lte': enddata}}):
            df2 = pd.DataFrame([[article['published'], 1]], columns=['data','count'])
            df = df.append(df2)
        df = df.set_index('data')
        df = df.resample(rule = 'D', how = 'sum')

        data_hist = []
        for i, v in df.to_dict()['count'].items():
            t= pd.to_datetime(i)
            t = t.strftime('%Y.%m.%d')
            data_hist.append({'dataX':t, 'dataY':v})

        context.update({
            'data_cloud': json.dumps(data_cloud),
            'data_hist': json.dumps(data_hist)
        })
        return context