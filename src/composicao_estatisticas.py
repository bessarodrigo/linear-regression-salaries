import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from scipy import stats
from scipy.stats import mode, skew, kurtosis

def composicao_histograma_boxplot(dataframe, coluna, intervalos="auto", titulo="Título do Gráfico", nome_arquivo="distribuicao.png", salvar=False):
    """
    Cria uma visualização composta com boxplot (em cima) e histograma (embaixo) da distribuição de uma variável numérica.

    O gráfico é útil para análise exploratória, permitindo visualizar a densidade da distribuição, presença de outliers, 
    além de linhas de referência para média, mediana e moda. Opcionalmente, pode salvar o gráfico como imagem em uma pasta 'images'.

    Parâmetros
    ----------
    dataframe : pandas.DataFrame
        O DataFrame que contém os dados.

    coluna : str
        O nome da coluna numérica a ser analisada.

    intervalos : int, str ou sequence, default="auto"
        Define o número de bins (faixas) do histograma. Pode ser um inteiro ou um dos métodos aceitos pelo matplotlib/seaborn (ex: 'auto', 'fd', 'sturges').

    titulo : str, default="Título do Gráfico"
        Título exibido no topo do gráfico.

    nome_arquivo : str, default="distribuicao.png"
        Nome do arquivo a ser salvo, caso `salvar=True`.

    salvar : bool, default=False
        Se `True`, salva o gráfico na pasta "images" no diretório atual.

    Outputs
    -------
    Exibe um gráfico composto contendo:
    - Boxplot com média (linha tracejada) e mediana.
    - Histograma com curva de densidade (KDE) e linhas de referência para média, mediana e moda.
    
    Além disso, se `salvar=True`, o gráfico será salvo como imagem no caminho `images/nome_arquivo`.

    Exceções tratadas
    -----------------
    - Erro ao criar a pasta `images`.
    - Erro ao salvar o gráfico.

    Exemplo de uso
    --------------
    composicao_histograma_boxplot(df, "salario", titulo="Distribuição Salarial", salvar=True)
    """
    # Definir o caminho para a pasta 'images'
    pasta_imagens = os.path.join(os.getcwd(), "images")
    
    # Garantir que a pasta seja criada apenas se necessário
    if salvar:
        if not os.path.exists(pasta_imagens):
            try:
                os.makedirs(pasta_imagens)
                print(f"Pasta criada em: {pasta_imagens}")
            except Exception as e:
                print(f"Erro ao criar a pasta {pasta_imagens}: {e}")
                return  # Interromper a execução se houver erro na criação da pasta
    
    # Criação dos gráficos
    fig, (ax1, ax2) = plt.subplots(
        nrows=2, 
        ncols=1, 
        sharex=True,
        gridspec_kw={
            "height_ratios": (0.15, 0.85), # proporção (tamanho) dos gráficos
            "hspace": 0.02 # espaço entre os gráficos
        }
    )

    sns.boxplot(
        data=dataframe, 
        x=coluna, 
        showmeans=True,  
        meanline=True, # traço da média no boxplot
        meanprops={"color": "C1", "linewidth": 1.5, "linestyle": "--"}, # propriedades do traço da média no boxplot
        medianprops={"color": "C2", "linewidth": 1.5, "linestyle": "-"}, # propriedades do traço da mediana no boxplot
        ax=ax1,
    )

    sns.histplot(data=dataframe, x=coluna, kde=True, bins=intervalos, ax=ax2)

    for ax in (ax1, ax2):
        ax.grid(True, linestyle="--", color="gray", alpha=0.5)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xlabel("")
        ax.set_ylabel("")

    ax2.axvline(dataframe[coluna].mean(), color="C1", linestyle="--", label="Média")
    ax2.axvline(dataframe[coluna].median(), color="C2", linestyle="--", label="Mediana")
    ax2.axvline(dataframe[coluna].mode()[0], color="C3", linestyle="--", label="Moda") # A moda pede o índice

    ax2.legend()
    
    fig.suptitle(titulo, fontsize=14, fontweight="bold", color="Gray")
    
    # Salvar o gráfico se 'salvar' for True
    if salvar:
        caminho_arquivo = os.path.join(pasta_imagens, nome_arquivo)
        try:
            plt.savefig(caminho_arquivo, dpi=300, bbox_inches="tight")
            print(f"Gráfico salvo em: {caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo {caminho_arquivo}: {e}")

    plt.show()

# Função para calcular as estatísticas
def calcular_estatisticas(amostra):
    """
    Calcula estatísticas descritivas de uma amostra numérica.

    Esta função retorna medidas de tendência central, dispersão, assimetria, curtose e quartis, 
    permitindo uma análise completa da distribuição dos dados.

    Parâmetros
    ----------
    amostra : array-like
        Vetor ou lista de valores numéricos (por exemplo, salários, idades, notas etc.).

    Retorno
    -------
    dict
        Um dicionário contendo as seguintes estatísticas:
        
        - 'Média': média aritmética da amostra
        - 'Mediana': valor central da distribuição
        - 'Moda': valor mais frequente (primeira moda, se múltiplas)
        - 'Variância': variância amostral (ddof=1)
        - 'Desvio Padrão': desvio padrão amostral (ddof=1)
        - 'Assimetria': medida de simetria da distribuição
        - 'Curtose': medida de cauda da distribuição (momento de curtose, não Fisher)
        - '1º Quartil': percentil 25 da amostra
        - '2º Quartil (Mediana)': percentil 50 da amostra (igual à mediana)
        - '3º Quartil': percentil 75 da amostra

    Notas
    -----
    - Caso a moda não seja encontrada (conjunto sem repetições), retorna `np.nan` para esse valor.
    - A função utiliza a moda da biblioteca `scipy.stats.mode` com `keepdims=True` para manter a consistência do retorno.

    Exemplo de uso
    --------------
    >>> dados = [10, 12, 14, 10, 18, 20, 10]
    >>> calcular_estatisticas(dados)
    {
        'Média': 13.43,
        'Mediana': 14.0,
        'Moda': 10,
        ...
    }
    """
    moda_result = mode(amostra, keepdims=True)  # Garantir que a moda é retornada como array
    estatisticas = {
        "Média": np.mean(amostra),
        "Mediana": np.median(amostra),
        "Moda": moda_result.mode[0] if len(moda_result.mode) > 0 else np.nan,
        "Variância": np.var(amostra, ddof=1),
        "Desvio Padrão": np.std(amostra, ddof=1),
        "Assimetria": skew(amostra),
        "Curtose": kurtosis(amostra, fisher=False),  # fisher=False retorna a curtose de momento
        "1º Quartil": np.percentile(amostra, 25),
        "2º Quartil (Mediana)": np.percentile(amostra, 50),
        "3º Quartil": np.percentile(amostra, 75)
    }
    return estatisticas

def teste_f_variancias(amostra1, amostra2, nome1="Grupo 1", nome2="Grupo 2", alpha=0.05):
    print("=" * 50)
    print(f" TESTE F PARA IGUALDADE DE VARIÂNCIAS ({nome1} vs. {nome2}) ")
    print("=" * 50)

    # Definição das hipóteses
    print(f"""
    H0: As variâncias de {nome1} e {nome2} são iguais.
    H1: As variâncias de {nome1} e {nome2} são diferentes.
    """)
    
    # Cálculo das variâncias amostrais
    var1 = np.var(amostra1, ddof=1)
    var2 = np.var(amostra2, ddof=1)

    # Definição do F-Estatístico
    if var1 > var2:
        F = var1 / var2
        df1, df2 = len(amostra1) - 1, len(amostra2) - 1
    else:
        F = var2 / var1
        df1, df2 = len(amostra2) - 1, len(amostra1) - 1

    # Cálculo do p-valor bicaudal
    p_value_one_tailed = 1 - stats.f.cdf(F, df1, df2)
    p_value_two_tailed = 2 * min(p_value_one_tailed, 1 - p_value_one_tailed)

    # Exibir resultados
    print("=" * 50)
    print(" RESULTADOS DO TESTE F ")
    print("=" * 50)
    print(f"Variância de {nome1}     : {var1:.5f}")
    print(f"Variância de {nome2}     : {var2:.5f}")
    print(f"Estatística F            : {F:.5f}")
    print(f"Graus de liberdade       : {df1}, {df2}")
    print("-" * 50)
    print(f"p-valor (bicaudal)       : {p_value_two_tailed * 100:.2f}%")
    print("-" * 50)

    # Interpretação
    if p_value_two_tailed < alpha:
        print("Decisão: Rejeitamos H0 → As variâncias são significativamente diferentes.")
    else:
        print("Decisão: Não rejeitamos H0 → As variâncias são estatisticamente iguais.")
    
    print("=" * 50)
    
    return p_value_two_tailed

def grafico_residuos(resultado):
    """
    Gera um gráfico de dispersão dos resíduos padronizados (resid_pearson)
    de um modelo ajustado com statsmodels.

    Parâmetros:
    -----------
    resultado : statsmodels.regression.linear_model.RegressionResultsWrapper
        Resultado do ajuste do modelo OLS (ex: resultado = modelo.fit()).

    Exibe:
    ------
    Um gráfico de dispersão com as linhas de referência em 0, -2 e +2.
    """
    residuos = resultado.resid_pearson
    indices = list(range(len(residuos)))

    plt.figure(figsize=(8, 4))
    ax = sns.scatterplot(x=indices, y=residuos)

    # Define os limites do eixo y considerando -3 e +3 como extremos esperados
    ymin = min(min(residuos), -3) * 1.1
    ymax = max(max(residuos), 3) * 1.1
    ax.set(ylim=(ymin, ymax))

    # Linhas de referência
    ax.axhline(0, color='black', linestyle='--')
    ax.axhline(2, color='black', linestyle='--')
    ax.axhline(-2, color='black', linestyle='--')

    ax.set_title("Gráfico de Resíduos Padronizados")
    ax.set_xlabel("Observações")
    ax.set_ylabel("Resíduos Padronizados")
    plt.tight_layout()
    plt.show()