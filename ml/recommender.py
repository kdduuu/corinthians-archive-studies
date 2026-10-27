from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recomendar_produtos(produtos, produto_id, limite=3):

    textos = []

    for produto in produtos:
        colecao = produto[4] or ''
        categoria = produto[6] or ''
        tags = produto[7] or ''

        texto = f'{colecao} {categoria} {tags}'
        textos.append(texto)

    vetorizador = TfidfVectorizer(
        ngram_range=(1, 2)
    )

    matriz_tfidf = vetorizador.fit_transform(textos)

    indice_produto = next(
        i for i, produto in enumerate(produtos)
        if produto[0] == produto_id
    )

    similaridades = cosine_similarity(
        matriz_tfidf[indice_produto],
        matriz_tfidf
    )[0]

    indices_ordenados = similaridades.argsort()[::-1]

    recomendados = []

    for indice in indices_ordenados:

        if indice == indice_produto:
            continue

        recomendados.append(produtos[indice])

        if len(recomendados) == limite:
            break

    return recomendados