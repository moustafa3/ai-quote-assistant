import re
import unicodedata
from pathlib import Path

from app.domain.entities import RagAnswer, SourcePassage


class RagService:
    """
    Simple local-document RAG service.

    This MVP implementation uses keyword matching over local text files.
    It is intentionally simple and can later be replaced by embeddings,
    vector search, and pgvector.
    """

    def __init__(self, docs_directory: Path | None = None) -> None:
        self.docs_directory = docs_directory or Path("docs")

    def answer_question(self, question: str) -> RagAnswer:
        """
        Answer a question using the most relevant local document passage.
        """
        passages = self._load_passages()

        if not passages:
            return RagAnswer(
                answer="Aucun document métier n'est disponible pour répondre à cette question.",
                sources=[],
            )

        question_tokens = self._tokenize(question)
        scored_passages = [
            SourcePassage(
                filename=passage.filename,
                content=passage.content,
                score=self._score_passage(question_tokens, passage.content),
            )
            for passage in passages
        ]

        relevant_passages = sorted(
            [passage for passage in scored_passages if passage.score > 0],
            key=lambda passage: passage.score,
            reverse=True,
        )

        if not relevant_passages:
            return RagAnswer(
                answer=(
                    "Je n'ai pas trouvé d'information suffisamment pertinente "
                    "dans les documents disponibles."
                ),
                sources=[],
            )

        best_passage = relevant_passages[0]
        sources = self._unique_sources(relevant_passages[:3])

        return RagAnswer(
            answer=self._clean_passage(best_passage.content),
            sources=sources,
        )

    def _load_passages(self) -> list[SourcePassage]:
        """
        Load text passages from local .txt documents.
        """
        if not self.docs_directory.exists():
            return []

        passages: list[SourcePassage] = []

        for file_path in sorted(self.docs_directory.glob("*.txt")):
            content = file_path.read_text(encoding="utf-8")
            for raw_passage in self._split_into_passages(content):
                passages.append(
                    SourcePassage(
                        filename=file_path.name,
                        content=raw_passage,
                        score=0,
                    )
                )

        return passages

    def _split_into_passages(self, content: str) -> list[str]:
        """
        Split a document into small searchable passages.
        """
        lines = [line.strip() for line in content.splitlines()]
        return [line for line in lines if line]

    def _score_passage(self, question_tokens: set[str], passage: str) -> int:
        """
        Score a passage using token overlap with the question.
        """
        passage_tokens = self._tokenize(passage)
        return len(question_tokens.intersection(passage_tokens))

    def _tokenize(self, text: str) -> set[str]:
        """
        Normalize and tokenize text for simple keyword search.
        """
        normalized_text = self._normalize_text(text)
        tokens = set(re.findall(r"[a-z0-9]+", normalized_text))

        stopwords = {
            "avec",
            "cette",
            "dans",
            "des",
            "de",
            "du",
            "elle",
            "est",
            "et",
            "la",
            "le",
            "les",
            "pour",
            "que",
            "quel",
            "quelle",
            "quelles",
            "quels",
            "qui",
            "sur",
            "une",
            "un",
            "aux",
            "au",
            "a",
            "l",
            "d",
        }

        return {
            token
            for token in tokens
            if len(token) > 2 and token not in stopwords
        }

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text by removing accents and lowering case.
        """
        normalized = unicodedata.normalize("NFKD", text)
        without_accents = "".join(
            char for char in normalized if not unicodedata.combining(char)
        )
        return without_accents.lower()

    def _clean_passage(self, passage: str) -> str:
        """
        Clean bullet prefixes before returning the answer.
        """
        return passage.lstrip("-*• ").strip()

    def _unique_sources(self, passages: list[SourcePassage]) -> list[str]:
        """
        Return unique source filenames while preserving order.
        """
        sources: list[str] = []

        for passage in passages:
            if passage.filename not in sources:
                sources.append(passage.filename)

        return sources