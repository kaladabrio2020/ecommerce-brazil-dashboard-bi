import pandas as pd
from statsmodels.tsa.stattools import adfuller

# Função para realizar o teste ADF e exibir os resultados de forma organizada
def adf_test(timeseries):
    print("Teste de Dickey-Fuller Aumentado (ADF):")
    result = adfuller(timeseries, autolag='AIC')  # Realiza o teste ADF
    
    # Extrai os resultados
    adf_statistic = result[0]
    p_value = result[1]
    used_lags = result[2]
    n_observations = result[3]
    critical_values = result[4]

    # Cria um DataFrame para exibir os valores críticos
    critical_values_df = pd.DataFrame(
        list(critical_values.items()),
        columns=["Nível de Significância", "Valor Crítico"]
    )

    # Exibe os resultados principais
    print(f"Estatística ADF: {adf_statistic:.4f}")
    print(f"Valor-p: {p_value:.4f}")
    print(f"Número de lags usados: {used_lags}")
    print(f"Número de observações usadas: {n_observations}")
    print("\nValores Críticos:")
    print(critical_values_df.to_string(index=False))

    # Interpretação do teste
    print("\nInterpretação:")
    if p_value <= 0.05:
        print("O valor-p é menor que 0.05. Rejeitamos a hipótese nula.")
        print("A série temporal é ESTACIONÁRIA.")
    else:
        print("O valor-p é maior que 0.05. Não rejeitamos a hipótese nula.")
        print("A série temporal NÃO É ESTACIONÁRIA.")