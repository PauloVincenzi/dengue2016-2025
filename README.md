---

IMPORTANTE !!! Os scripts deste projeto utilizam uma lista chamada bancos_de_dados contendo os caminhos para os arquivos .csv referentes aos dados da dengue entre 2016 e 2025. No entanto, esses caminhos estão atualmente configurados para um diretório específico do computador local do autor. Para que os scripts funcionem corretamente no seu computador, é necessário alterar os caminhos dos arquivos na lista bancos_de_dados para refletirem o local onde os arquivos .csv estão salvos no seu sistema.

---
Introdução

A dengue é uma doença infecciosa causada por um vírus e transmitida, principalmente, pelo mosquito Aedes aegypti. É considerada um grave problema de saúde pública no Brasil, com ciclos epidêmicos que se repetem quase todos os anos, especialmente nos períodos de calor e chuvas. A doença pode se manifestar de forma leve, mas também pode evoluir para formas graves, com risco de morte. O controle da dengue depende fortemente da vigilância epidemiológica, do combate ao mosquito transmissor e do monitoramento constante dos casos notificados. Nesse contexto, a análise estatística de dados parciais e históricos sobre a doença pode auxiliar na estimativa de casos futuros, contribuindo para a prevenção e o planejamento das ações de saúde pública.
Nos últimos anos, diversos municípios brasileiros enfrentam surtos expressivos da doença, com impacto significativo na rede pública de saúde. Um exemplo notório é o município de São Carlos (SP), onde os casos de dengue notificados em 2024 totalizaram um montante expressivo, com um número crescente de óbitos causados pela doença, evidenciando mais ainda a urgência do problema. Dessa forma, o presente trabalho buscou analisar dados relacionados à dengue no município de São Carlos, considerando o período de 2016 até 2025. Ressalta-se que, para o ano de 2025, os dados disponíveis correspondem apenas até a primeira quinzena do mês de junho. A análise envolveu o tratamento e organização das informações disponíveis, seguido de sua exploração por meio de tabelas e gráficos anuais. Posteriormente, aplicaram-se técnicas de inferência estatística com o objetivo de estimar o total anual de notificações, casos confirmados, negativos e óbitos por dengue no município de São Carlos, utilizando registros parciais do próprio ano e o histórico consolidado dos anos anteriores (2016–2024).
Cabe destacar que a unidade amostral escolhida nesta análise foi o ano epidemiológico completo. Essa decisão se justifica pelo objetivo prático do trabalho: estimar valores anuais totais com base em dados acumulados até determinados pontos do ano (como março, junho ou setembro). A escolha por estimativas anuais, e não mensais, deve-se ao fato de que medidas de saúde pública só são eficazes se tomadas com alguma antecedência e visão de longo prazo. 

---
Descrição dos dados

Os dados utilizados neste trabalho foram gentilmente fornecidos pela Supervisão de Vigilância Epidemiológica do município de São Carlos, com acesso autorizado para fins acadêmicos. Os arquivos originais estavam no formato ‘.dbf’, sendo posteriormente convertidos para o formato ‘.csv’, mais adequado à análise estatística por sua compatibilidade com ferramentas modernas e com a linguagem de programação Python.
Entre as diversas variáveis disponíveis nos bancos de dados, foram selecionadas para análise:

1. Data da notificação
2. Data de nascimento do paciente
3. Resultado do exame sorológico
4. Resultado do exame NS1
5. Resultado do exame PCR
6. Classificação final do caso (confirmado, negativo, inconclusivo, etc)
7. Data do óbito (quando aplicável
	
Antes da análise dos dados, foi feito um processo de limpeza dos dados, onde registros preenchidos incorretamente ou registros com dados faltantes foram classificados foram padronizados como nulos (NaT e None). Esses registros foram mantidos nos bancos, mas foram excluídos das etapas de visualização e inferência. Vale destacar que a quantidade de registros com dados faltantes foi pequena, não impactando significativamente as análises posteriores.
O volume de registros variou significativamente ao longo dos anos, com alguns anos apresentando apenas algumas centenas de notificações, enquanto outros ultrapassaram a marca de trinta mil registros. A análise exploratória foi realizada com base nos dados completos dos dez anos disponíveis (2016 a 2025). Já as técnicas de inferência estatística foram aplicadas apenas aos nove anos com dados consolidados (2016 a 2024), uma vez que os dados de 2025 estavam disponíveis apenas até a metade do mês de junho, não representando o ano completo.

---
Conclusão

A partir de dados parciais de 2025, a análise estatística desenvolvida neste trabalho permitiu estimar o total de notificações, confirmações, casos negativos e óbitos por dengue no município de São Carlos. Dado que os dados estão disponíveis em apenas nove anos, a metodologia aponta que a aproximação normal é pouco precisa para estimar parâmetros utilizando o intervalo de confiança tradicional. Dessa forma, ao construir novas amostras através da simulação computacional, a técnica de reamostragem Bootstrap permitiu que estimativas mais precisas e com mais fundamentação teórica fossem apresentadas. Além disso, ao considerar apenas os valores acumulados até março, junho ou setembro, parte das informações intermediárias acaba sendo desconsiderada, o que restringe o aproveitamento total dos dados disponíveis. Para superar essa limitação, seria necessário um algoritmo mais robusto, capaz de realizar estimativas com base em dados acumulados continuamente — mês a mês, semana a semana ou até diariamente. Com um volume maior de dados utilizados, a tendência é que as estimativas se tornem significativamente mais precisas.

---
