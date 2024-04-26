from langchain_community.embeddings import SentenceTransformersEmbeddings
from shared.qdrant_db.langchain import get_langchain_qdrant
from shared.shell.flags import Flags


def similatiry_search(query):
    embeddings = SentenceTransformersEmbeddings()
    qdrant = get_langchain_qdrant(embeddings)
    return qdrant.similarity_search(query)


def main():
    flags = Flags().parse_args()
    flags = Flags()
    query = flags.get("query")
    print(similatiry_search(query))


if __name__ == "__main__":
    main()
