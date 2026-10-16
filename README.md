# ECAC26
PROJECT OF SENSES RECOGNITION - so far...

**Interpretação:** esta contagem compara os nomes dos artistas tal como estão escritos; diferenças de grafia podem esconder correspondências. É uma verificação de possível sobreposição entre desenvolvimento e teste, pedida no enunciado. Não usa os rótulos do teste nem mede o desempenho de um modelo.

## Síntese das perguntas 2 e 3

### O que foi analisado

Começámos por separar o teste e trabalhar apenas com o desenvolvimento. Consultámos o significado e o tipo das colunas, contámos valores em falta e distintos, cruzámos `metadata.csv` com `av_values.csv` e verificámos os ficheiros de áudio, letras e capas. Depois, explorámos as distribuições e os valores numéricos, observámos as relações entre variáveis e comparamos a associação de cada coluna ao quadrante através de uma validação com base na classe e agrupada por música. Nesta fase, os dados foram observados, não limpos.

### O que os resultados mostram

- **Estrutura e classes:** o desenvolvimento tem 932 linhas referentes a 914 músicas únicas; 18 linhas repetem os mesmos IDs de áudio e letra. As classes não aparecem por igual: há 374 registos Q1, 112 Q2, 356 Q3 e 90 Q4. Assim, Q1 e Q3 são as mais frequentes, enquanto Q2 e Q4 tEm menos exemplos.
- **Cruzamento das fontes:** os 914 pares únicos de IDs encontram correspondência em `av_values.csv`; não ficaram linhas sem correspondência. Há áudio e letra para as 914 músicas. Das capas, existem 825 e faltam 89. Nenhum dos ficheiros encontrados está guardado numa pasta de quadrante diferente da indicada nos metadados.
- **Qualidade dos metadados:** nenhuma coluna é constante, mas `num_Genres` e `num_MoodsAll` têm 98,9% de valores em falta e são pouco informativas tal como estão. Também faltam valores em `LowestYear` (34,5%), `ActualYear` (22,7%), `Duration` (20,4%) e `Relevance` (17,2%). Os gráficos e os resumos numéricos confirmam casos a investigar: `Duration` vai de -1 a 367 000, apesar de representar segundos, e `ActualYear` inclui 0 e 9999. Estes valores não foram corrigidos nesta etapa.
- **Relação com o quadrante:** a comparação individual deu os maiores macro-F1 a `Genres` (0,497), `Styles` (0,495) e `Arousal` (0,494); `Valence` obteve 0,407. Como referência, prever sempre a classe mais frequente teve macro-F1 de 0,143. Estes valores servem para uma primeira comparação, não medem o desempenho de um modelo final. Em particular, `Arousal` e `Valence` não podem ser usadas como preditores: o quadrante é definido a partir delas, com limites de 0,5. O gráfico dos quadrantes torna essa relação visível.
- **Partilha de artistas:** 200 das 409 músicas de teste têm um artista com a mesma grafia no desenvolvimento (104 artistas distintos). Portanto, o teste inclui artistas já vistos e artistas não vistos; uma avaliação destinada a medir generalização para artistas novos deve manter cada artista num único grupo.

### Conclusão

O cruzamento confirma que os metadados têm correspondência completa com `av_values.csv` e que áudio e letras estão disponíveis para todas as músicas de desenvolvimento; as capas são opcionais e estão em falta em cerca de uma em cada dez músicas. A exploração revela desequilíbrio entre quadrantes, ausência elevada em algumas colunas e valores suspeitos em duração e ano, que ficam para a limpeza do exercício 4. Para a modelação, excluímos a classe, `Arousal`, `Valence` e qualquer caminho de ficheiro que exponha o quadrante. As pontuações por coluna são apenas indícios exploratórios; não permitem concluir causalidade nem escolher, por si só, as variáveis de um modelo.
