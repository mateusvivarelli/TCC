"""PDF de estudo da defesa: fala slide a slide (versao final, 32 slides) e perguntas provaveis.
Saida: Apresentacao/fala_e_perguntas_defesa.pdf"""
import html, os, re
import subprocess

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(BASE, "Apresentacao", "fala_e_perguntas_defesa.pdf")

FALA = [
 (1, "Capa", "Boa tarde a todos. Eu sou o Mateus Vivarelli e vou apresentar o meu trabalho, Espacialização da MUSLE para identificação de áreas críticas de erosão, com um estudo de caso na bacia do rio Jundiaí. Agradeço ao meu orientador, Luis Fernando Murillo-Bermúdez, e ao meu coorientador, professor André Martim."),
 (2, "Título completo", "O título do trabalho é o roteiro desta apresentação. Vou explicar cada termo, nesta ordem: primeiro a MUSLE, depois a área de estudo, a bacia do rio Jundiaí, em seguida o que significa espacializar, e por fim o objetivo, que é identificar áreas críticas de erosão."),
 (3, "MUSLE (Williams, 1975)", "A MUSLE, descrita por Williams em 1975, estima o sedimento produzido por um evento de chuva. Em vez da energia da chuva, ela usa a energia do escoamento: o volume e a vazão de pico. É uma equação empírica: foi ajustada a medições de campo, e não deduzida das leis da física."),
 (4, "Q e qp", "Esta parte é a física da equação: o volume escoado e a vazão de pico, que são grandezas medidas ou calculadas."),
 (5, "K, LS, C e P", "Estes quatro fatores são índices empíricos, relativos a uma parcela padrão, sem vegetação. É como um índice de preços: não é o preço de nada, só compara com uma referência. K é a erodibilidade do solo, LS é o relevo, C é a cobertura e o manejo, que diz quanto da erosão de um solo exposto ainda ocorre, e P são as práticas conservacionistas. Como não há mapa de práticas na bacia, P vale 1."),
 (6, "11,8 e 0,56", "E estes dois números são as constantes de Williams, sem sentido físico. Como os fatores e as constantes são empíricos, o resultado precisa ser calibrado com o sedimento medido na própria bacia."),
 (7, "Área de estudo (mapa pequeno)", "A área de estudo é a parte alta da bacia do rio Jundiaí, com cerca de cento e trinta e oito quilômetros quadrados, nos municípios de Mairiporã, Atibaia, Jarinu e Campo Limpo Paulista, onde fica a seção de medição."),
 (8, "Mapa grande da bacia, com os postos", "Aqui está a bacia inteira do Jundiaí e, em laranja, a parte alta estudada. Os dois círculos azuis são os postos de chuva: o DBT5, a leste, fora da bacia, e o de Campo Limpo, junto ao exutório, onde se mede a vazão e o sedimento."),
 (9, "Solo e uso", "O solo é dominado pelos Cambissolos, em sessenta e nove por cento da área, e pelos Argissolos, em dezoito. No uso, predominam a mata nativa, com quarenta por cento, e o campo, com vinte e nove; há também área urbanizada, catorze, silvicultura, treze, e um pouco de lavoura temporária, quatro."),
 (10, "Espacialização", "Sem espacialização, só temos dados hidrossedimentológicos: quanto escoa e quanto sedimento sai. Com ela, os dados têm referência espacial, e sabemos também onde. A MUSLE costuma ser aplicada à bacia inteira, com fatores médios; foi o que fiz na iniciação científica. Aqui aplico pixel a pixel, em pixels de cerca de trinta metros, cento e cinquenta e quatro mil pixels. O principal guia foi Hao e colaboradores, de 2022, que fizeram esse procedimento, inclusive com uma vazão de pico por pixel."),
 (11, "Objetivo", "O objetivo é desenvolver e aplicar a espacialização da MUSLE, em escala de evento, para identificar áreas críticas de erosão. Como o cálculo é pixel a pixel, o resultado também é um mapa, que mostra onde a erosão é produzida e onde vale priorizar intervenções."),
 (12, "Dados e fontes", "Os dados vêm do monitoramento do grupo do Luis. A chuva é de dois postos com registro horário, o DBT5, fora da bacia, e o de Campo Limpo Paulista. A vazão é da estação do DAEE na saída da bacia. O sedimento vem da turbidez medida de hora em hora pela SABESP, convertida em concentração por uma curva de calibração. Os dados espaciais são o modelo de elevação do USGS, os mapas de solo e uso do Plano de Bacias e o número de curva da Agência Nacional de Águas. São dezessete eventos, de novembro de 2018 a fevereiro de 2020; o gráfico mostra a carga medida em cada um. Vou acompanhar o evento onze."),
 (13, "Evento 11", "O evento onze, de quatro a oito de julho de 2019, teve setenta e quatro milímetros de chuva, intensidade máxima de onze vírgula oito milímetros por hora, cerca de um milhão e meio de metros cúbicos de escoamento direto e mil oitocentas e vinte e duas toneladas de sedimento. É esse valor que o modelo tenta reproduzir."),
 (14, "Chuva em cada pixel (IDW)", "Primeiro, a chuva em cada pixel, interpolada pelo inverso do quadrado da distância a partir dos dois postos, que registraram sessenta e dois vírgula oito e setenta e nove milímetros. Os pixels vão de sessenta e três a setenta e nove. O pixel de exemplo, de lavoura temporária sobre Argissolo, recebeu setenta e cinco vírgula quatro."),
 (15, "Escoamento do pixel (SCS-CN)", "Segundo, o escoamento do pixel pelo método do número de curva. Com a chuva do pixel e a retenção do solo, o escoamento do pixel de exemplo é treze milímetros. Somando a bacia inteira, o modelo calcula novecentos e noventa e sete mil metros cúbicos, contra um milhão e quatrocentos e setenta e nove mil medidos: cerca de dois terços."),
 (16, "Parêntese: CN-I e λ = 0,05", "Um parêntese sobre duas escolhas. Usei o número de curva da condição seca, o CN-I, pela fórmula de Chow, que passa de oitenta e um para sessenta e quatro, e a razão de abstração de zero vírgula zero cinco, com a retenção convertida pela relação de Woodward, de cento e quarenta e dois para duzentos e quarenta e quatro milímetros. Essa combinação aproxima o volume total dos dezessete eventos, com viés de mais três por cento; e Brandão e colaboradores encontraram melhor desempenho médio com zero vírgula zero cinco em três mil e quinhentas bacias. A limitação é que ela foi escolhida olhando os mesmos eventos que uso na avaliação."),
 (17, "Parêntese: vazão de pico local (Hao)", "Terceiro, a vazão de pico local. Não existe hidrograma em cada pixel, então, seguindo Hao, o volume do pixel, onze vírgula sessenta e sete metros cúbicos, é distribuído no tempo conforme a concentração da chuva: a razão entre a intensidade máxima e a chuva do evento, zero vírgula cento e cinquenta e nove por hora. Isso dá um pico de cerca de meio litro por segundo. Atenção: essa razão é um único número por evento, então o pico local é proporcional ao escoamento. Ele não traz informação espacial nova; só dá mais peso aos eventos de chuva concentrada."),
 (18, "Erosão local (MUSLE no pixel)", "Quarto, a erosão local, que é a equação de Williams aplicada ao pixel. O onze vírgula oito aqui é a constante de Williams, não a intensidade da chuva. Com K de zero vírgula zero trezentos e cinquenta e um, LS de quatro vírgula oitenta e sete, C de zero vírgula duzentos e doze e P igual a um, o resultado é um vírgula cento e sessenta e sete. Esse valor é um índice relativo, e não uma massa em toneladas."),
 (19, "Parêntese: o coeficiente c", "Para chegar ao sedimento, somo esse índice nos cento e cinquenta e quatro mil pixels: no evento onze, quarenta mil oitocentos e oitenta e cinco. Se isso fossem toneladas, seria vinte e duas vezes a carga medida. Isso acontece porque Williams ajustou a equação para bacias inteiras, e aqui ela é aplicada a pixels de novecentos metros quadrados. O coeficiente c, calibrado nos dezessete eventos, converte o índice em toneladas: zero vírgula zero trezentos e quarenta e quatro. Ele faz o papel de uma taxa de transferência média, mas também absorve a diferença de escala e parte do erro do escoamento, então não deve ser lido como taxa física. Atenção: c minúsculo é este coeficiente; C maiúsculo é a cobertura."),
 (20, "Calibração e validação cruzada", "O coeficiente c é calibrado em escala logarítmica, com a média geométrica das razões entre o sedimento medido e o índice. Assim nenhum evento grande domina: em escala linear, o evento quinze responderia por quase metade da variabilidade. Isso equivale a maximizar o NSE em log, a função objetivo de Hao. Para saber se o modelo funciona, faço a validação cruzada: tiro um evento, ajusto o c nos outros dezesseis e prevejo o evento retirado, dezessete vezes. No evento onze, o ajuste dá mil quatrocentas e seis toneladas e a validação, mil trezentas e oitenta e três, contra mil oitocentas e vinte e duas medidas."),
 (21, "Resultado: modelo calculado (MC)", "Agora olho os dezessete eventos. O modelo calculado, que usa só a chuva, teve erro mediano de oitenta e um por cento: metade dos eventos erra menos que isso, metade erra mais. E só trinta e cinco por cento dos eventos ficaram dentro de um fator dois, isto é, entre a metade e o dobro do medido. Uma regra simples, com a carga proporcional à chuva do evento, usa a mesma informação e erra quarenta e dois por cento. O modelo foi pior em catorze dos dezessete eventos."),
 (22, "O erro vem do escoamento", "De onde vem esse erro? O SCS-CN acerta o volume total dos dezessete eventos, com três por cento de diferença, mas erra quarenta e seis por cento na mediana de cada evento: superestima as chuvas grandes e subestima as pequenas, e os erros se compensam no total. Esse erro passa para o sedimento, um pouco ampliado, porque a erosão cresce com o escoamento elevado a um vírgula doze. O erro do escoamento explica noventa e um por cento da variação do erro do sedimento. Baert e colaboradores encontraram algo parecido."),
 (23, "Modelo forçado ao medido (MFM)", "Para testar isso, criei o modelo forçado ao medido: troco só o volume do escoamento pelo medido, multiplicando todos os pixels pelo mesmo fator, que no evento onze é um vírgula quarenta e oito. O resto é igual, e o c é recalibrado. Ele não é uma previsão: serve para isolar o efeito do escoamento."),
 (24, "Com o escoamento medido", "Com o escoamento medido, o erro mediano cai de oitenta e um para vinte e um por cento, e noventa e quatro por cento dos eventos ficam dentro de um fator dois. Mas uma regra simples com o volume medido erra dezesseis por cento, e os dois não se distinguem, com p igual a zero vírgula cinquenta e dois. Então o trabalho mostra o peso do escoamento, mas não isola a contribuição da fórmula de erosão. O modelo concentrado da iniciação científica erra vinte e dois por cento, mas foi ajustado nos próprios eventos, então a comparação é só indicativa."),
 (25, "Comparação dos modelos (tabela)", "Esta tabela reúne todos os modelos. As métricas vêm da validação cruzada: o erro mediano, a fração de eventos em fator dois, o NSE em log, que compara o modelo com prever sempre a média, e a correlação de Spearman, que diz se o modelo ordena os eventos do menor ao maior. Com só a chuva, a regra simples supera o modelo; com o volume medido, os dois empatam."),
 (26, "Áreas críticas", "Agora, o que a espacialização acrescenta: onde a erosão é produzida. Campo, silvicultura e lavoura temporária ocupam quarenta e seis por cento da área e respondem por oitenta e três por cento da erosão. Separadamente, noventa e três por cento vêm dos Cambissolos, e as encostas acima de vinte por cento respondem por setenta e oito. As áreas críticas dos dois modelos coincidem em noventa e quatro por cento, o que é esperado, pois usam o mesmo padrão espacial. O mapa é relativo: depende dos K e C adotados e mostra onde a erosão é produzida, não onde o sedimento chega ao rio."),
 (27, "Sedimento por evento", "Aqui, o sedimento em cada pixel nos dezessete eventos: as mesmas manchas se repetem, e muda a intensidade, que acompanha a chuva."),
 (28, "Sedimento médio", "E esta é a média dos dezessete eventos: as manchas mais escuras estão na porção central e oeste, em campo, silvicultura e lavoura sobre Cambissolos, em encostas íngremes."),
 (29, "Solo e uso (repetido)", "[Este slide repete o mapa de solo e uso do slide 9. Se for de apoio, pule; se ficar, diga só: \"Comparando com o mapa de solo e uso, as manchas coincidem com o campo, a silvicultura e a lavoura sobre Cambissolos.\"]"),
 (30, "Conclusões", "Em conclusão: primeiro, a conversão da chuva em escoamento é o principal limite: o modelo erra oitenta e um por cento com a chuva e vinte e um com o volume medido. Segundo, com o volume medido, a MUSLE espacializada não se distingue de uma regra simples com o volume, então não isolamos a contribuição da fórmula. Terceiro, também com o volume medido, ela chega a um erro da mesma ordem do modelo concentrado e acrescenta o mapa. E quarto, as áreas críticas estão no campo, na silvicultura e na lavoura, sobretudo sobre Cambissolos e nas encostas mais íngremes."),
 (31, "Limitações", "Sobre as limitações: a maior parte do erro vem da hidrologia, e não da fórmula de erosão; com o escoamento medido, o erro cai de oitenta e um para vinte e um por cento. As principais: a chuva de só dois postos, um fora da bacia; a delimitação manual dos eventos, por exemplo, no evento onze choveu de doze a catorze milímetros antes da janela; os poucos eventos, só dezessete; e a vazão de base estimada, que deixa incerto até o escoamento direto medido. Além disso, o mapa não tem validação espacial, porque só medimos sedimento na saída da bacia. Os próximos passos são medir sedimento em sub-bacias e verificar as áreas críticas em campo."),
 (32, "Obrigado", "Agradeço ao Luis, pela orientação e pelos dados, ao professor André, pela coorientação, à banca, a quem me apoiou durante a graduação e a todos que estão aqui. [Se quiser mencionar a IA em uma frase: \"Usei um assistente de inteligência artificial como ferramenta, na programação, nas figuras e na redação; as decisões de método e a interpretação foram minhas, com o orientador.\"] Obrigado."),
]

ANTES = [
 "<b>Slide 31, item 4:</b> diz \"o escoamento direto <u>calculado</u> depende do filtro\". O certo é <u>medido</u> (vazão total menos a base). Troque a palavra, ou fale \"medido\".",
 "<b>Slide 30, 2º item:</b> quem chega a 21%, da ordem do concentrado, é o modelo com o volume medido. Fale \"com o volume medido\".",
 "<b>Slide 30, 3º item:</b> o 46% → 83% vale só para campo, silvicultura e lavoura; Cambissolos e encostas são outras contas. A fala acima já separa.",
 "<b>Slide 29:</b> repete o mapa de solo e uso do slide 9. Decida se fica.",
]

TOP = [
 ("Se uma regra de três com a chuva acerta mais que o seu modelo, para que serve a MUSLE espacializada?",
  "Para prever a carga total no exutório, nesta bacia e com estes dados, a regra simples é melhor; eu não escondo isso. O ganho da espacialização não está no número da carga, está no mapa: onde a erosão acontece. E a comparação localizou o problema: o que estraga o modelo é a conversão da chuva em escoamento, não a fórmula de erosão."),
 ("Com o escoamento medido, a MUSLE empata com carga = c × volume. Então ela não acrescenta nada?",
  "No exutório, não. K, LS e C são os mesmos em todos os eventos; a única coisa que muda entre eventos é o escoamento. Então nenhum teste no exutório consegue avaliar a fórmula e os fatores. O que a espacialização acrescenta é a distribuição dentro da bacia."),
 ("Como você sabe que as áreas críticas estão no lugar certo?",
  "Não sei: o mapa não foi validado no espaço, porque só há medição no exutório. Ele é relativo, depende dos K e C adotados e mostra onde a erosão é produzida, não onde chega ao rio. Os 94% de coincidência entre MC e MFM não são validação (mesmo padrão). Serve para indicar onde verificar primeiro; para validar, medir sedimento em sub-bacias e conferir em campo."),
 ("Condição seca (CN-I) em eventos de verão? O evento 16 começa 13 horas depois de um de 139 mm.",
  "Não tem sentido físico de umidade, e o TCC diz isso: foi uma condição única, escolhida porque, com λ = 0,05 e Woodward, o volume total dos 17 eventos ficou a +3% do medido. Na prática é um CN efetivo da bacia, coerente com o escoamento direto baixo (cerca de 10% da chuva), mas escolhido olhando os mesmos eventos. Acerta o total, não cada evento (46%). <i>Não defenda que o solo estava seco.</i>"),
 ("Quais são as unidades? Williams usa volume em m³; você usa Q em mm vezes área em m².",
  "Segui a forma de Hao et al. (2022). Q em mm vezes m² dá litros, mil vezes o volume em m³. Como o expoente é fixo, isso vira uma constante (cerca de 48) que vai para dentro do c. Não muda nenhuma previsão nem o mapa relativo; por isso o E é um índice, não toneladas. Se insistirem: com m³, o c passaria de 1, sem sentido como taxa; por isso o TCC diz que o c não é taxa física."),
 ("Pico local de um pixel de 30 m, sem tempo de concentração? Isso não é vazão de pico.",
  "Concordo, não é um pico hidráulico. Não há hidrograma no pixel; segui Hao: o volume do pixel vezes o índice de concentração da chuva (RI/R), dividido por 3.600. Como RI/R é um número por evento, o pico é proporcional ao escoamento: não traz informação espacial e só dá peso aos eventos de chuva concentrada. Testou sem o pico? \"Não testei.\""),
 ("Vazão de base com BFImax = 0,70? Eckhardt sugere 0,25 para rocha cristalina.",
  "A série veio com os dados e eu a reproduzi com o filtro de Eckhardt; quem a reproduz é 0,70. O TCC reconhece que é alto e que parte da base pode ser escoamento direto. Não fiz sensibilidade. Isso pesa em cadeia: muda o escoamento direto medido, o MFM, a regra com o volume e até a escolha do CN-I. A conclusão de que o escoamento é o gargalo deve se manter, mas os números mudariam."),
 ("O MFM usa o volume medido no mesmo rio em que se mede o sedimento. Não é óbvio que acerta?",
  "É, e eu digo que não é previsão. A carga é volume vezes concentração, e entre os eventos o volume varia muito mais (variância do log 0,66 contra 0,08). Por isso quem recebe o volume medido acerta a ordem de grandeza. O MFM serve só para isolar o efeito do escoamento. <i>Evite \"por construção\"; diga \"em grande parte por causa do volume\".</i>"),
 ("Você escolheu CN-I e λ olhando os 17 eventos; a validação cruzada só refaz o c. O que ela valida?",
  "Tira o viés do ajuste do c, e só. As escolhas do SCS-CN foram feitas antes, com os mesmos eventos, então as métricas tendem a ser otimistas, em grau que não estimei; a validação aninhada não foi feita. Mas o MC vai mal mesmo com esse viés a favor, então a conclusão sobre o escoamento fica de pé."),
 ("O resultado \"MC pior que a regra com a chuva\" depende do critério de calibração?",
  "Depende. Em log, o do TCC, 81% contra 42%; em escala linear, 45% contra 39%. Escolhi o log porque o evento 15 responde por 48,7% da variabilidade e dominaria um ajuste linear, e porque equivale a maximizar o NSE em log, como Hao. O que não muda: o MC erra de 40 a 80%, e com o escoamento medido o modelo fica em cerca de 20% em qualquer critério."),
 ("O padrão do mapa não é só o gradiente da chuva de dois postos?",
  "Em parte, sim: em log, 63% da variação espacial vem do escoamento (chuva e CN), e eu digo que é a parte menos confiável. Mas, em escala linear, K·LS·C sozinho explica 58%, e a ordem das classes de uso, solo e declive vem dos fatores fixos. As classes críticas são mais robustas que a posição exata das manchas. O teste seria refazer o mapa com chuva uniforme."),
 ("Por que não usou conectividade (índice de Borselli), como Hao et al.?",
  "Com um único ponto de medição e 17 eventos, eu não teria como calibrar nem testar um índice por pixel; ele mudaria o mapa sem dado para conferir. Por isso usei um c único e trato o mapa como erosão produzida, relativa. É um dos próximos passos. <i>Não diga que \"não mudaria nada\".</i>"),
]

GRUPOS = [
 ("Banca especialista: hidrologia e dados", [
  ("Woodward em cima do CN-I: retenção média de 490 mm, CN equivalente de 34. Plausível?", "Como propriedade do solo, não; como CN efetivo, é coerente com o escoamento direto de cerca de 10% da chuva. O TCC reconhece que a conversão é extrapolada em 8,4% dos pixels e nos eventos 1 e 12."),
  ("Woodward converte o quê?", "Só o λ (de 0,20 para 0,05). O CN-I vem da fórmula de Chow, Maidment e Mays (1988). Combinar as duas foi escolha minha."),
  ("Brandão et al. não associam clima úmido e pastagem a λ mais alto?", "Sim, e o TCC cita isso: o alto Jundiaí tem clima úmido e 29% de campo. O 0,05 não é consenso; foi escolhido pelo volume."),
  ("O coeficiente de escoamento não cresceu com a chuva (r = −0,01). O que isso diz?", "Que boa parte do escoamento rápido deve vir de áreas saturadas perto dos canais e de fluxo subsuperficial, comum em clima úmido com solo profundo, e não de excesso de infiltração nas encostas. Por isso o SCS-CN não acompanha. Com a ressalva de que o coeficiente medido depende da separação da base e da chuva de dois postos."),
  ("De onde vêm os pesos 0,307 e 0,693 da chuva média?", "São os pesos de Thiessen: a fração da bacia mais perto de cada posto (conferido: 30,8% e 69,2%). Servem para a chuva do evento, R, usada no RI/R e na regra simples. A chuva de cada pixel vem do IDW; por isso a média dos pixels no evento 11 é 73,5 mm e R é 74,0 mm."),
  ("RI/R maior que 1 nos eventos 1 e 12?", "Não é físico: RI vem do posto mais intenso e R é a média dos dois. A chuva forte pegou praticamente um posto só (no 12, o DBT5 marcou 0). Num mesmo posto, daria 0,72 e 0,96. Por isso é tratado como índice."),
  ("Como os 17 eventos foram escolhidos e delimitados? O 15 e o 16 estão colados.", "Eventos do monitoramento do grupo, com pico acima de 10 m³/s, delimitados à mão sobre o hidrograma. É uma limitação: no evento 11, 12 a 14 mm caíram antes da janela; no 15 e 16, parte da recessão do 15 pode estar no 16."),
  ("Dois postos, um fora da bacia. Não havia outros?", "Eram os dois com registro horário no período. É a primeira causa de erro. Ficam a cerca de 29 km um do outro."),
 ]),
 ("Banca especialista: modelo e calibração", [
  ("O que é o c? Por que muda de 0,0344 para 0,0222?", "Um coeficiente de escala calibrado. Ocupa o lugar da taxa de transferência, mas absorve também a escala, as unidades e parte do erro do escoamento; por isso muda quando só o escoamento muda."),
  ("40.885 dividido por 1.822 não dá o seu c.", "O c não vem só do evento 11: é a média geométrica das razões medido/índice dos 17 eventos. Com ele, o evento 11 dá 1.406 t, não 1.822 t."),
  ("Somar a fórmula em 154 mil pixels não dá o mesmo que aplicá-la na bacia.", "Certo: para pixels iguais, a razão é n elevado a 0,12. O c absorve essa diferença, como em Hao. Por isso o mapa é relativo."),
  ("Por que não calibrou o expoente 0,56?", "Para ter um só parâmetro com 17 eventos. Calibrar o expoente aproximaria o modelo da regra com o volume, mas continuaria sem testar K, LS e C. O expoente efetivo (1,12) é maior que a relação observada entre carga e volume (0,94), o que amplia um pouco o erro."),
  ("Os 91% não são quase automáticos?", "São esperados pela estrutura: K, LS e C são fixos, então só o escoamento muda entre eventos. A evidência independente é o MFM: trocando só o volume, o erro cai de 81% para 21%."),
  ("Por que mediana e fator 2, e não o NSE linear?", "O evento 15 responde por 48,7% da soma dos quadrados e dominaria o NSE linear. Com 17 eventos, métricas relativas são mais estáveis."),
  ("p = 0,52 quer dizer que são iguais?", "Não: quer dizer que não há evidência de diferença com 17 eventos. O intervalo vai de −5,5 a +10,4 pontos."),
  ("Somando os 17 eventos, o modelo calculado acerta o total?", "No ajuste, o MC soma cerca de 37.300 t contra 23.846 t medidas (+56%), porque superestima os eventos grandes (o 15: 10.361 t contra 3.829 t). O MFM soma 22.964 t (−4%)."),
 ]),
 ("Banca especialista: sedimento e mapa", [
  ("Como a turbidez virou concentração? Amostras, faixa, R²?", "Curva por partes de Murillo-Bermúdez et al. (2023), com quebra em 250 NTU; a incerteza é maior nos picos e eu não a estimei. <i>Confirme com o Luis o número de amostras e a faixa.</i>"),
  ("E a carga de fundo?", "Não foi medida; o alvo é a carga em suspensão, e o c absorve a diferença."),
  ("Você calibra com a carga total, que inclui sedimento do canal e da vazão de base.", "É uma hipótese assumida no TCC. No evento 11, cerca de 72% da carga está na parcela do escoamento direto. O c absorve o resto; muda o valor do c, não o padrão do mapa."),
  ("O pico de concentração vem antes da vazão. E o modelo?", "No evento 11, a concentração chega cerca de 25 h antes, o que costuma indicar sedimento disponível perto do canal. O modelo trabalha com o total do evento e não representa isso. <i>Cuidado: o TCC cita 13 laços em oito e 4 horários (artigo do Luis); não diga \"13 laços horários\".</i>"),
  ("Evento 17?", "3.806 mg/L de carga por m³ de escoamento direto, contra 1.085 a 2.088 nos outros. Pode ser obra, deslizamento ou a curva de turbidez. Mantive porque não há base para excluir; sem ele, o MFM vai a 15,3% e nada muda."),
  ("Os erros do MFM mudam ao longo da série.", "Os primeiros eventos são superestimados e os últimos subestimados. Não identifiquei a causa (sensor, curva, disponibilidade de sedimento, obras). Um c único não representa isso."),
  ("K e C de outras regiões; silvicultura com C = 0,121, mais que o campo.", "Adotados de Vivarelli et al. (2025), sem recalibração; não dá para calibrá-los no exutório. A ordem entre lavoura, silvicultura e campo depende desses valores."),
  ("Área urbana com erosão zero?", "Hipótese do modelo (C = 0, K = 0). Obras e loteamentos podem ser fontes importantes, perto do exutório."),
  ("Por que limitar o LS a 200 m de área de contribuição?", "Sem limite, nos pixels de canal ela chega a milhões de m², onde a USLE, que é de encosta, não vale. O 200 é uma escolha; não testei outros."),
  ("Por que 5% para área crítica?", "É um corte para destacar as manchas principais; não testei outros limiares."),
  ("Onde, concretamente, agir?", "Nos pixels críticos, o mais comum é lavoura temporária sobre Cambissolo com declive de 20 a 45% (26,7%), depois silvicultura na mesma situação (19,2%), na porção central e oeste."),
  ("Na introdução você diz que o modelo pode prever cenários futuros.", "Em valor absoluto, ainda não. Em termos relativos (trocar o C de uma classe), o mapa indicaria a tendência, sem validação."),
  ("A comparação com o seu trabalho anterior é justa?", "Não totalmente; por isso é indicativa: o concentrado foi ajustado nos próprios eventos, sem validação cruzada, e usa o volume total e o pico medidos."),
  ("Qual é a área da bacia: 137,8 ou 138,8 km²?", "137,8 km² pela acumulação de fluxo; 138,8 é a área do contorno usado no mapa. São duas delimitações."),
 ]),
 ("Professor de hidráulica (não conhece a MUSLE)", [
  ("O 11,8 tem unidade? A equação é dimensionalmente consistente?", "Não é: é empírica, ajustada por Williams para um conjunto de unidades. Aqui não importa para o resultado, porque o c é calibrado com a carga medida."),
  ("O que é o número de curva e o λ?", "O CN, de 0 a 100, diz quanto o terreno deixa escoar (mata baixo, asfalto perto de 100). λ é a fração da retenção perdida antes de começar a escoar; o clássico é 0,20, usei 0,05. O 0,95 da fórmula é 1 − 0,05."),
  ("O que é fator 2? Errar o dobro é aceitável?", "É o simulado entre a metade e o dobro do medido: a ordem de grandeza certa. Em sedimentos a própria medição tem incerteza grande. Não digo que errar o dobro está bom; uso para comparar modelos."),
  ("O que é erro mediano?", "O erro do evento do meio: ordeno os 17 erros e pego o 9º. Metade erra menos, metade erra mais. Usei a mediana para que dois ou três eventos muito errados não dominem (a média do MC seria 96%)."),
  ("O que é validação cruzada?", "Tiro um evento, calibro o c com os outros 16 e prevejo o que tirei, como se fosse novo. Repito 17 vezes. O erro mostrado é de previsão, não de ajuste."),
  ("O que é NSE?", "Compara o modelo com prever sempre a média: 1 é perfeito, 0 é igual à média, negativo é pior. Em log, um erro de 50% pesa igual num evento pequeno e num grande."),
  ("21% menos 16% dá 5. Por que a diferença é 1,6?", "Os 21% e 16% são as medianas de cada modelo; o 1,6 é a mediana das diferenças evento a evento, outra conta."),
  ("Por que IDW e não Thiessen?", "Com dois postos, qualquer método dá um gradiente; Thiessen cortaria a bacia em duas metades constantes. Usei IDW de potência 2, padrão do QGIS. (Thiessen foi usado só para a chuva média do evento.)"),
  ("1,48 milhão de m³ para 74 mm é razoável?", "Dá cerca de 10,7 mm de escoamento direto, uns 14% da chuva. Na bacia, vai de 3% a 22% conforme o evento, 10% no conjunto."),
  ("Quanto é isso por hectare?", "Somando os 17 eventos, cerca de 1,7 t/ha; em média, 0,1 t/ha por evento. O pixel de exemplo equivale a uns 0,45 t/ha no evento 11. Mas o mapa é relativo."),
  ("Para que serve isso na prática?", "Para priorizar onde fazer conservação do solo: práticas conservacionistas, recompor cobertura, controlar solo exposto. Reduz o sedimento que assoreia reservatórios e chega à captação da SABESP. O mapa ordena onde agir; não dimensiona toneladas nem obras."),
  ("Por que P = 1?", "Não havia mapa de práticas conservacionistas; P = 1 é o caso sem prática, o mais desfavorável."),
  ("Por que o evento 11 como exemplo?", "É o do Apêndice A: um evento médio e longo (74 mm em 91 h), com chuva nos dois postos, em que dá para seguir todas as etapas."),
 ]),
 ("Plateia (família e amigos)", [
  ("O que você fez, em uma frase?", "Fiz um mapa de onde a terra é mais levada pela chuva numa bacia que abastece a região de Jundiaí e testei o quanto esse tipo de modelo consegue prever o sedimento que chega ao rio."),
  ("Deu certo?", "Em parte. O mapa saiu e mostra onde a erosão se concentra. Para prever a quantidade a partir da chuva, o modelo errou bastante, e descobri por quê: a parte que transforma chuva em água escorrendo é a que mais erra. Saber onde está o erro também é um resultado."),
  ("Por que isso importa?", "A terra que a chuva arrasta vai para o rio: suja a água que a SABESP trata e enche os reservatórios. Saber de onde ela vem ajuda a decidir onde proteger o solo."),
  ("O que é um pixel?", "Um quadradinho de 30 por 30 metros. Dividi a bacia em uns 154 mil e fiz a conta em cada um."),
  ("Onde estão as áreas mais críticas?", "No meio e no oeste da bacia, em pasto, eucalipto e lavoura em morros inclinados. A mata, a leste, quase não erode."),
  ("Por que o Jundiaí?", "O grupo do meu orientador monitora o rio lá desde 2018, com chuva, vazão e turbidez. Sem esses dados não daria para testar o modelo."),
  ("E agora, o que vem depois?", "Medir sedimento em rios menores dentro da bacia para conferir o mapa, ter mais pluviômetros ou radar, e incluir quanto da terra realmente chega ao rio."),
 ]),
]

FRACOS = [
 ("Mapa sem validação espacial", "É relativo e não validado; serve para indicar onde verificar primeiro."),
 ("MUSLE não testável no exutório", "K, LS e C não mudam entre eventos, então o exutório não consegue testá-los."),
 ("Hidrologia escolhida com os mesmos dados", "CN-I e λ são um ajuste de volume, não umidade real; a validação aninhada não foi feita."),
 ("Vazão de base com BFImax 0,70", "Não testei a sensibilidade; o escoamento direto medido depende dela."),
 ("Chuva de 2 postos", "É a principal fonte de erro, e o padrão leste–oeste do mapa é a parte menos confiável."),
 ("c único, sem conectividade", "O mapa mostra onde a erosão é produzida, não onde chega ao rio."),
 ("Unidades na fórmula", "Segui Hao; a constante de unidade vai para o c, por isso E é índice."),
 ("Turbidez e curva sem incerteza", "A incerteza é maior nos picos e não foi estimada."),
 ("17 eventos", "As conclusões são qualitativas."),
]
FORTES = ["Honestidade: o trabalho diz o que funcionou e o que não; as limitações estão escritas.",
          "Comparação com modelos simples: poucos trabalhos com MUSLE fazem; é ela que mostra onde está o erro.",
          "MC contra MFM separa o erro do escoamento do erro da fórmula: é o diagnóstico mais sólido.",
          "Validação cruzada e métricas robustas (mediana, fator 2, NSE em log), com testes pareados.",
          "Exemplo numérico completo (Apêndice A, evento 11): dá para seguir a conta pixel a pixel.",
          "Mapa lido por classe de uso, solo e declive: útil para priorizar conservação."]
ARMAD = ["c ≠ 1.822 / 40.885: o c vem dos 17 eventos (média geométrica).",
         "21% − 16% ≠ 1,6: o 1,6 é a mediana das diferenças evento a evento.",
         "Histerese: o TCC cita 13 laços em oito e 4 horários (artigo do Luis, 2022). Não diga \"13 laços horários\".",
         "46% → 83% vale só para campo, silvicultura e lavoura. Cambissolos (69% → 93%) e declive > 20% (65% → 78%) são outras contas.",
         "Quem chega a 21%, perto do concentrado (22%), é o modelo com o volume medido, não o MC.",
         "\"Regra com o volume\" usa o escoamento direto; os \"88% explicados pelo volume\" usam o volume total.",
         "Área: 137,8 km² (acumulação de fluxo); o mapa diz 138,8 (contorno da máscara).",
         "Tabela 2, evento 16: R = 97,7 mm, mas pelos pesos daria 98,2 mm. Se perguntarem: \"vou conferir a planilha\"."]
LUIS = ["Se os 17 eventos são os mesmos do artigo de 2022 e qual foi o critério de seleção.",
        "Onde fica a captação da SABESP (turbidez) em relação à estação do DAEE.",
        "Número de amostras, faixa e R² da curva turbidez × CSS (artigo de 2023).",
        "Quem gerou a série de vazão de base e por que BFImax = 0,70.",
        "Se a janela do evento 11 começou de propósito depois da chuva das 3h às 11h de 04/07."]

e = html.escape
def palavras(t): return len(re.sub(r"\[.*?\]", "", t).split())
tot = sum(palavras(t) for _, _, t in FALA)
rows = "".join(f"<tr><td>{n}</td><td>{e(nome)}</td><td>{palavras(t)}</td><td>{palavras(t)/135*60:.0f} s</td></tr>" for n, nome, t in FALA)
partes = []
partes.append(f"""<h1>Defesa do TCC: fala e perguntas</h1>
<p class="sub">Mateus Guilherme Vivarelli · 19/11/2026, 15h · versão final dos slides (32 slides, 18/11 21h55)</p>
<div class="aviso"><h3>Antes de apresentar</h3><ul>{''.join(f'<li>{a}</li>' for a in ANTES)}</ul></div>
<h2>Parte 1. Fala, slide a slide</h2>
<p>Total: {tot} palavras, cerca de {tot/135:.0f} minutos a 135 palavras por minuto. Sobram cerca de {20-tot/135:.0f} minutos para pausas e trocas de slide. Números escritos por extenso para ler em voz alta.</p>""")
for n, nome, t in FALA:
    t2 = e(t).replace("[", "<span class='nota'>[").replace("]", "]</span>")
    partes.append(f"<div class='slide'><div class='cab'><span class='num'>{n}</span>{e(nome)}<span class='tempo'>~{palavras(t)/135*60:.0f} s</span></div><p>{t2}</p></div>")
partes.append("<h3>Se precisar cortar</h3><ol><li>Slide 25 (tabela): uma frase só.</li><li>Slides 27 e 28: fale só o 28.</li><li>Slide 29 (repetido): pule.</li><li>Juntar 13 e 14.</li></ol>")
partes.append("<h2 class='quebra'>Parte 2. As 12 perguntas mais prováveis (decore)</h2>")
for i, (q, a) in enumerate(TOP, 1):
    partes.append(f"<div class='q top'><p class='pq'><b>{i}.</b> {e(q)}</p><p class='pa'>{a}</p></div>")
partes.append("<h2 class='quebra'>Parte 3. Outras perguntas, por tema</h2>")
for titulo, itens in GRUPOS:
    partes.append(f"<h3>{e(titulo)}</h3>")
    for q, a in itens:
        partes.append(f"<div class='q'><p class='pq'>{e(q)}</p><p class='pa'>{a}</p></div>")
partes.append("<h2 class='quebra'>Parte 4. Pontos fracos e fortes</h2><h3>Pontos fracos: assuma, com a frase pronta</h3><table><tr><th>Ponto fraco</th><th>Frase</th></tr>"
              + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in FRACOS) + "</table>")
partes.append("<h3>Pontos fortes: use nas respostas</h3><ul>" + "".join(f"<li>{e(f)}</li>" for f in FORTES) + "</ul>")
partes.append("<h3>Armadilhas de números</h3><ul>" + "".join(f"<li>{e(a)}</li>" for a in ARMAD) + "</ul>")
partes.append("<h3>Confirmar com o Luis, se der tempo</h3><ul>" + "".join(f"<li>{e(a)}</li>" for a in LUIS) + "</ul>")
partes.append("<p class='fim'>Quando uma pergunta tocar num ponto fraco: assuma e diga o que faria para resolver. A banca valoriza isso.</p>")

CSS = """
@page { size: A4; margin: 16mm 16mm 16mm 16mm; }
body { font-family: Calibri, Carlito, sans-serif; font-size: 11.5pt; color: #222; line-height: 1.38; }
h1 { color: #1B3A6B; font-size: 22pt; margin: 0 0 2pt 0; }
.sub { color: #5F6670; margin: 0 0 10pt 0; }
h2 { color: #fff; background: #3D85C6; padding: 5pt 9pt; font-size: 15pt; margin: 16pt 0 8pt 0; }
h3 { color: #1B3A6B; font-size: 13pt; margin: 12pt 0 5pt 0; }
.quebra { page-break-before: always; }
.aviso { border: 1.5pt solid #C77B12; background: #FCEFD9; padding: 4pt 10pt; border-radius: 4pt; }
.aviso h3 { color: #8a5208; margin-top: 4pt; }
.slide { border-left: 4pt solid #3D85C6; padding: 2pt 0 2pt 9pt; margin: 0 0 8pt 0; page-break-inside: avoid; }
.cab { font-weight: bold; color: #1B3A6B; }
.num { display: inline-block; background: #1B3A6B; color: #fff; border-radius: 3pt; padding: 0 5pt; margin-right: 6pt; }
.tempo { float: right; color: #5F6670; font-weight: normal; font-size: 10pt; }
.slide p { margin: 3pt 0 0 0; }
.nota { color: #8a5208; font-style: italic; }
.q { margin: 0 0 8pt 0; page-break-inside: avoid; }
.q .pq { margin: 0; font-weight: bold; color: #1B3A6B; }
.q .pa { margin: 2pt 0 0 0; padding-left: 10pt; border-left: 2pt solid #C9D3E0; }
.q.top { background: #EEF3FA; padding: 5pt 8pt; border-radius: 4pt; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 0.6pt solid #C9D3E0; padding: 3pt 6pt; vertical-align: top; text-align: left; }
th { background: #3D85C6; color: #fff; }
.fim { margin-top: 14pt; font-weight: bold; color: #1B3A6B; }
"""
doc = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(partes)}</body></html>"
tmp = os.path.join(BASE, "Apresentacao", "_fala.html"); open(tmp, "w", encoding="utf-8").write(doc)
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file://{tmp}'); await pg.waitForTimeout(300);
  await pg.pdf({{ path: '{OUT}', format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: "<div style='font-size:8pt;width:100%;text-align:center;color:#888'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
    margin: {{ top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' }} }});
  await b.close();
}})();
"""
subprocess.run(["node", "-e", js], check=True, env=dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules"))
os.remove(tmp)
print("ok", OUT, tot, "palavras")
