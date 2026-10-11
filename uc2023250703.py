"""Primeira parte do projeto: conhecer e explorar o dataset MERGE."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "dataset" / "build" / "MERGE_ECAC" / "merge_ecac"
MEDIA_DIR = PROJECT_DIR / "dataset"
OUTPUT_DIR = PROJECT_DIR / "outputs"

QUADRANTS = ["Q1", "Q2", "Q3", "Q4"]
COLORS = {"Q1": "tab:blue", "Q2": "tab:orange", "Q3": "tab:green", "Q4": "tab:red"}

# O dicionário do dataset é a referência para esta classificação.
COLUMN_INFO = {
    "Audio_Song": ("Identificador", "Identifica o ficheiro de áudio."),
    "Lyric_Song": ("Identificador", "Identifica o ficheiro da letra."),
    "Quadrant": ("Alvo", "Quadrante emocional a prever."),
    "AllMusic Id": ("Identificador", "Identificador da faixa no catálogo AllMusic."),
    "AllMusic Extraction Date": ("Administrativa", "Indica a recolha Old ou New."),
    "Artist": ("Descritiva", "Nome do artista."),
    "Title": ("Descritiva", "Título da faixa."),
    "Relevance": ("Medida", "Relevância devolvida pela pesquisa AllMusic."),
    "Year": ("Medida", "Data de lançamento registada pelo AllMusic."),
    "LowestYear": ("Medida", "Data de lançamento mais antiga encontrada."),
    "Duration": ("Medida", "Duração da faixa, em segundos."),
    "Moods": ("Descritiva", "Etiquetas de humor do vocabulário reduzido."),
    "MoodsAll": ("Descritiva", "Etiquetas de humor do vocabulário completo."),
    "MoodsAllWeights": ("Medida", "Peso associado a cada etiqueta de MoodsAll."),
    "Genres": ("Descritiva", "Etiquetas de género."),
    "GenreWeights": ("Medida", "Peso associado a cada género."),
    "Themes": ("Descritiva", "Etiquetas de tema."),
    "ThemeWeights": ("Medida", "Peso associado a cada tema."),
    "Styles": ("Descritiva", "Etiquetas de estilo."),
    "StyleWeights": ("Medida", "Peso associado a cada estilo."),
    "AppearancesTrackIDs": ("Identificador", "Outras edições da mesma gravação."),
    "AppearancesAlbumIDs": ("Identificador", "Álbuns das outras edições."),
    "Sample": ("Administrativa", "Indica se havia um excerto disponível."),
    "SampleURL": ("Administrativa", "Endereço do excerto recolhido."),
    "ActualYear": ("Medida", "Ano de lançamento usado pelos autores."),
    "num_Genres": ("Medida", "Número de etiquetas de género."),
    "num_MoodsAll": ("Medida", "Número de etiquetas de humor."),
}


def load_data():
    """Carrega os dados e separa o teste antes de qualquer análise."""
    metadata = pd.read_csv(DATA_DIR / "metadata.csv")
    av_values = pd.read_csv(DATA_DIR / "av_values.csv")
    test_songs = pd.read_csv(DATA_DIR / "test_songs.csv")

    test_ids = set(test_songs["Audio_Song"].dropna())
    if not test_ids.issubset(set(metadata["Audio_Song"].dropna())):
        raise ValueError("Há identificadores de teste que não existem em metadata.csv.")

    is_test = metadata["Audio_Song"].isin(test_ids)
    development = metadata.loc[~is_test].copy()
    test = metadata.loc[is_test].copy()
    return metadata, development, test, av_values, test_songs


def numeric_values(values):
    """Converte uma coluna para números quando quase todos os valores o permitem."""
    numbers = pd.to_numeric(values, errors="coerce")
    present = values.notna().sum()
    if present and numbers.notna().sum() / present >= 0.95:
        return numbers
    return None


def column_summary(development):
    """Resume tipo, papel, distribuição e valores em falta de cada coluna."""
    rows = []
    for column in development.columns:
        values = development[column]
        numeric = numeric_values(values)

        if numeric is not None:
            details = (
                f"mín. {numeric.min():g}; mediana {numeric.median():g}; "
                f"máx. {numeric.max():g}"
            )
            data_type = "numérica"
        else:
            common = values.value_counts(dropna=True).head(3)
            details = "; ".join(
                f"{str(value)[:35]}: {count}" for value, count in common.items()
            )
            data_type = "categórica/texto"

        role, meaning = COLUMN_INFO[column]
        rows.append(
            {
                "coluna": column,
                "tipo": data_type,
                "papel": role,
                "significado": meaning,
                "valores_em_falta": int(values.isna().sum()),
                "percentagem_em_falta": round(values.isna().mean() * 100, 2),
                "valores_distintos": int(values.nunique(dropna=True)),
                "distribuicao_ou_intervalo": details,
            }
        )

    summary = pd.DataFrame(rows)
    summary.to_csv(OUTPUT_DIR / "resumo_colunas.csv", index=False)
    distributions = []
    for column in development.columns:
        counts = development[column].fillna("[em falta]").astype(str).value_counts()
        distributions.extend(
            {
                "coluna": column,
                "valor": value,
                "frequencia": int(count),
                "percentagem": round(count / len(development) * 100, 2),
            }
            for value, count in counts.items()
        )
    pd.DataFrame(distributions).to_csv(
        OUTPUT_DIR / "distribuicao_categorias.csv", index=False
    )
    print("\nColunas: tipo, papel, valores em falta e distribuição/intervalo")
    print(
        summary[
            ["coluna", "tipo", "papel", "valores_em_falta", "percentagem_em_falta",
             "valores_distintos", "distribuicao_ou_intervalo"]
        ].to_string(index=False)
    )
    return summary


def media_stems(folder, suffix):
    if not folder.is_dir():
        raise FileNotFoundError(f"Não foi encontrada a pasta de media: {folder}")
    return {
        path.stem
        for path in folder.rglob(f"*{suffix}")
        if path.is_file() and not path.name.startswith("._")
    }


def inspect_sources(metadata, development, av_values):
    """Verifica se identificadores e ficheiros correspondem entre as fontes."""
    print("\n2.2 — Cruzamento das fontes")
    keys = ["Audio_Song", "Lyric_Song"]
    development_pairs = set(map(tuple, development[keys].drop_duplicates().to_numpy()))
    av_pairs = set(map(tuple, av_values[keys].drop_duplicates().to_numpy()))
    matched_pairs = development_pairs & av_pairs
    joined = development.merge(
        av_values,
        on=keys,
        how="left",
        validate="many_to_one",
        indicator=True,
    )

    if (joined["_merge"] != "both").any():
        missing = int((joined["_merge"] != "both").sum())
        raise ValueError(f"{missing} registos de desenvolvimento não têm par em av_values.csv.")

    print(f"Registos de desenvolvimento: {len(development)}")
    print(f"Pares únicos áudio/letra: {len(development_pairs)}")
    print(f"Pares encontrados também em av_values.csv: {len(matched_pairs)}")
    print(f"Linhas repetidas em metadata após a separação: {development.duplicated(keys).sum()}")
    print("O cruzamento com av_values é muitos-para-um por causa das linhas repetidas em metadata.")

    audio_ids = set(development["Audio_Song"])
    lyric_ids = set(development["Lyric_Song"])
    all_audio_ids = set(metadata["Audio_Song"])
    all_lyric_ids = set(metadata["Lyric_Song"])
    audio_files = media_stems(MEDIA_DIR / "audio", ".mp3")
    lyric_files = media_stems(MEDIA_DIR / "lyrics", ".txt")
    cover_files = media_stems(MEDIA_DIR / "album_covers", ".jpg")
    media_by_quadrant = {
        "áudio": (MEDIA_DIR / "audio", ".mp3", "Audio_Song"),
        "letras": (MEDIA_DIR / "lyrics", ".txt", "Lyric_Song"),
        "capas": (MEDIA_DIR / "album_covers", ".jpg", "Audio_Song"),
    }

    for name, development_ids, metadata_ids, files in [
        ("áudio", audio_ids, all_audio_ids, audio_files),
        ("letras", lyric_ids, all_lyric_ids, lyric_files),
        ("capas", audio_ids, all_audio_ids, cover_files),
    ]:
        print(
            f"{name.capitalize()}: {len(development_ids & files)}/{len(development_ids)} "
            f"identificadores do desenvolvimento com ficheiro; "
            f"{len(metadata_ids - files)} registos sem ficheiro; "
            f"{len(files - metadata_ids)} ficheiros sem registo em metadata."
        )
        folder, suffix, id_column = media_by_quadrant[name]
        wrong_quadrant = 0
        for quadrant in QUADRANTS:
            expected_ids = set(
                metadata.loc[metadata["Quadrant"] == quadrant, id_column].dropna()
            )
            actual_ids = media_stems(folder / quadrant, suffix)
            wrong_quadrant += len(
                expected_ids
                & set().union(*(media_stems(folder / other, suffix) for other in QUADRANTS if other != quadrant))
            )
        print(f"  Ficheiros encontrados na pasta do quadrante errado: {wrong_quadrant}.")

    print(
        "Conclusão: cada música tem áudio e letra; as capas não existem para todos os registos. "
        "Há também ficheiros fora de metadata. As pastas de media indicam o quadrante, "
        "por isso o caminho não pode ser usado como variável de entrada."
    )
    return joined.drop(columns="_merge")


def print_dataset_overview(metadata, development, test, test_songs, av_values):
    print("1. O DATASET E A SEPARAÇÃO DO TESTE")
    print(f"metadata.csv: {len(metadata)} linhas, {metadata.shape[1]} colunas.")
    print(f"av_values.csv: {len(av_values)} linhas.")
    print(f"test_songs.csv: {test_songs['Audio_Song'].nunique()} músicas de teste.")
    print(
        f"Após separar o teste: {len(development)} linhas de desenvolvimento "
        f"e {len(test)} linhas de teste (inclui eventuais linhas repetidas)."
    )
    print("O teste não é usado para ajustar ou avaliar os resultados desta análise.")
    print("\nDistribuição de Quadrant no desenvolvimento:")
    print(development["Quadrant"].value_counts().reindex(QUADRANTS, fill_value=0).to_string())


def inspect_column_quality(development):
    print("\n3.2 — Colunas quase vazias, constantes e possíveis problemas de significado")
    missing_rate = development.isna().mean()
    near_empty = missing_rate[missing_rate >= 0.90]
    print("Colunas com pelo menos 90% de valores em falta:")
    print(near_empty.to_string() if not near_empty.empty else "Nenhuma.")

    constant = [
        column for column in development
        if development[column].nunique(dropna=True) <= 1
    ]
    print(f"Colunas constantes: {constant if constant else 'nenhuma'}.")

    duration = pd.to_numeric(development["Duration"], errors="coerce").dropna()
    print(
        f"Duration: mínimo {duration.min():g} e máximo {duration.max():g} segundos; "
        "o valor negativo viola o dicionário e o máximo sugere possível erro de unidade."
    )
    for column, expected in [("Year", "AAAA-MM-DD"), ("LowestYear", "DD/MM/AAAA")]:
        values = development[column].dropna().astype(str)
        slash_dates = values.str.match(r"^\d{1,2}/\d{1,2}/\d{4}$").sum()
        year_first = values.str.match(r"^\d{4}-").sum()
        print(
            f"{column}: {slash_dates} datas com barras e {year_first} no formato AAAA-MM-... "
            f"(formato esperado pelo dicionário: {expected})."
        )
    actual_year = pd.to_numeric(development["ActualYear"], errors="coerce").dropna()
    future_years = int((actual_year > pd.Timestamp.now().year).sum())
    print(
        f"ActualYear: {future_years} valores estão no futuro; "
        f"máximo observado {actual_year.max():g}."
    )


def make_folds(development, number_of_folds=5):
    """Cria folds estratificados por classe, mantendo duplicados da mesma música juntos."""
    songs = development[["Audio_Song", "Quadrant"]].drop_duplicates()
    if songs["Audio_Song"].duplicated().any():
        raise ValueError("Um identificador de áudio aparece associado a mais de um quadrante.")

    random = np.random.default_rng(42)
    fold_by_song = {}
    for quadrant in QUADRANTS:
        ids = songs.loc[songs["Quadrant"] == quadrant, "Audio_Song"].to_numpy().copy()
        random.shuffle(ids)
        for position, song_id in enumerate(ids):
            fold_by_song[song_id] = position % number_of_folds
    return development["Audio_Song"].map(fold_by_song)


def feature_keys(train_values, validation_values):
    """Agrupa números em cinco intervalos ou usa cada valor textual como categoria."""
    train_numbers = numeric_values(train_values)
    validation_numbers = numeric_values(validation_values)
    if train_numbers is not None and validation_numbers is not None:
        cuts = train_numbers.dropna().quantile([0.2, 0.4, 0.6, 0.8]).unique()
        edges = np.r_[-np.inf, np.sort(cuts), np.inf]
        train_keys = pd.cut(train_numbers, bins=edges, include_lowest=True).astype(str)
        validation_keys = pd.cut(
            validation_numbers, bins=edges, include_lowest=True
        ).astype(str)
        train_keys = train_keys.where(train_numbers.notna(), "[em falta]")
        validation_keys = validation_keys.where(validation_numbers.notna(), "[em falta]")
        return train_keys, validation_keys, "numérica (5 intervalos)"

    train_keys = train_values.fillna("[em falta]").astype(str)
    validation_keys = validation_values.fillna("[em falta]").astype(str)
    return train_keys, validation_keys, "categórica"


def macro_f1(actual, predicted):
    scores = []
    for label in QUADRANTS:
        true_positive = ((actual == label) & (predicted == label)).sum()
        false_positive = ((actual != label) & (predicted == label)).sum()
        false_negative = ((actual == label) & (predicted != label)).sum()
        denominator = 2 * true_positive + false_positive + false_negative
        scores.append(0.0 if denominator == 0 else 2 * true_positive / denominator)
    return float(np.mean(scores))


def evaluate_one_column(data, column, folds):
    """Avalia um classificador simples que só conhece uma coluna de cada vez."""
    actual = data["Quadrant"]
    predictions = pd.Series(index=data.index, dtype="object")
    baseline = pd.Series(index=data.index, dtype="object")

    for fold in sorted(folds.unique()):
        validation = folds == fold
        train = ~validation
        train_keys, validation_keys, method = feature_keys(
            data.loc[train, column], data.loc[validation, column]
        )
        labels = data.loc[train, "Quadrant"]
        majority = labels.value_counts().idxmax()
        mapping = pd.DataFrame({"key": train_keys, "label": labels}).groupby("key")[
            "label"
        ].agg(lambda values: values.value_counts().idxmax())
        predictions.loc[validation] = validation_keys.map(mapping).fillna(majority)
        baseline.loc[validation] = majority

    return {
        "coluna": column,
        "metodo": method,
        "accuracy": (predictions == actual).mean(),
        "macro_f1": macro_f1(actual, predictions),
        "accuracy_baseline": (baseline == actual).mean(),
        "macro_f1_baseline": macro_f1(actual, baseline),
    }


def analyse_association(development):
    folds = make_folds(development)
    features = [column for column in development.columns if column != "Quadrant"]
    results = pd.DataFrame(
        [evaluate_one_column(development, column, folds) for column in features]
    ).sort_values("macro_f1", ascending=False)
    results.to_csv(OUTPUT_DIR / "desempenho_por_coluna.csv", index=False)

    print("\n3.3 — Previsão com uma coluna de cada vez (validação cruzada, só desenvolvimento)")
    print("Os duplicados da mesma música ficam sempre no mesmo fold.")
    print(
        results[
            ["coluna", "metodo", "accuracy", "macro_f1", "accuracy_baseline", "macro_f1_baseline"]
        ].round(3).head(15).to_string(index=False)
    )
    baseline = results["macro_f1_baseline"].iloc[0]
    suspects = results[results["coluna"].isin(["Arousal", "Valence"])]
    above_baseline = int((suspects["macro_f1"] > baseline).sum())
    print(
        f"\n3.4 — Arousal e Valence superam a referência de macro-F1 em "
        f"{above_baseline}/{len(suspects)} casos. Em conjunto definem diretamente o alvo; "
        "não devem ser usadas como preditores."
    )
    return results


def report_test_artist_overlap(development, test):
    development_artists = set(development["Artist"].dropna())
    test_songs = test.drop_duplicates("Audio_Song")
    shared = test_songs["Artist"].isin(development_artists)
    print("\n3.5 — Artistas presentes nos dois lados da separação")
    print(
        f"{int(shared.sum())}/{len(test_songs)} músicas de teste partilham o mesmo "
        "nome de artista com pelo menos uma música de desenvolvimento."
    )
    print(
        f"Artistas distintos do teste que também aparecem no desenvolvimento: "
        f"{test_songs.loc[shared, 'Artist'].nunique()}."
    )
    print("A comparação usa o nome escrito no ficheiro; grafias diferentes podem ocultar correspondências.")


def make_plots(development, results):
    """Cria apenas gráficos usados para ler distribuição, fuga do alvo e desempenho."""
    numeric_columns = [
        column
        for column in development.columns
        if column != "Quadrant" and numeric_values(development[column]) is not None
    ]
    columns = 2
    rows = (len(numeric_columns) + columns - 1) // columns
    figure, axes = plt.subplots(rows, columns, figsize=(12, rows * 3.4))
    axes = np.asarray(axes).reshape(-1)

    for axis, column in zip(axes, numeric_columns):
        values = numeric_values(development[column]).dropna()
        axis.hist(values, bins=25, color="steelblue", edgecolor="white")
        axis.set_title(column)
        axis.set_ylabel("Número de registos")
        if column == "Duration" and len(values):
            axis.set_xlim(left=min(0, values.min()), right=values.quantile(0.99))
            axis.set_xlabel("Segundos (eixo limitado ao percentil 99)")
        else:
            axis.set_xlabel("Valor")
    for axis in axes[len(numeric_columns):]:
        axis.remove()
    figure.suptitle("Distribuição das colunas numéricas — desenvolvimento", y=1.01)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "distribuicoes_numericas.png", dpi=180, bbox_inches="tight")
    plt.close(figure)

    ordered = results.sort_values("macro_f1")
    figure, axis = plt.subplots(figsize=(10, max(7, len(ordered) * 0.32)))
    axis.barh(ordered["coluna"], ordered["macro_f1"], color="slateblue")
    axis.axvline(
        ordered["macro_f1_baseline"].mean(),
        color="black",
        linestyle="--",
        label="Referência: prever sempre a classe mais frequente",
    )
    axis.set_xlabel("Macro-F1 em validação cruzada")
    axis.set_title("Desempenho usando uma coluna de cada vez")
    axis.legend(loc="lower right")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "desempenho_por_coluna.png", dpi=180)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7, 6))
    for quadrant in QUADRANTS:
        group = development.loc[development["Quadrant"] == quadrant]
        axis.scatter(
            group["Valence"],
            group["Arousal"],
            s=18,
            alpha=0.55,
            color=COLORS[quadrant],
            label=quadrant,
        )
    axis.axvline(0.5, color="black", linestyle="--")
    axis.axhline(0.5, color="black", linestyle="--")
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Valence", ylabel="Arousal")
    axis.set_title("Quadrant é definido por Valence e Arousal")
    axis.legend(title="Quadrant")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "quadrantes_valence_arousal.png", dpi=180)
    plt.close(figure)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    metadata, development, test, av_values, test_songs = load_data()

    print("2.3 — Suspeitas de fuga do alvo, registadas a partir do enunciado/dicionário")
    print("- Quadrant é o próprio alvo e nunca é uma variável de entrada.")
    print("- Arousal e Valence são suspeitas: o enunciado define Quadrant a partir delas.")
    print("- O nome da pasta de áudio/letras/capas também indica o quadrante; não usar o caminho como entrada.")
    print("- Audio_Song e Lyric_Song são identificadores, mas o dicionário não diz que codificam o quadrante.")

    print_dataset_overview(metadata, development, test, test_songs, av_values)
    column_summary(development)
    joined_development = inspect_sources(metadata, development, av_values)
    inspect_column_quality(development)
    results = analyse_association(joined_development)
    report_test_artist_overlap(development, test)
    make_plots(joined_development, results)

    print(f"\nFicheiros de apoio guardados em: {OUTPUT_DIR}")
    print("Esta etapa não altera nem limpa os dados.")


if __name__ == "__main__":
    main()
