from app.ai.document_classifier import DocumentClassifier
from app.domain.entities import DocumentClassification


class ClassifyDocumentUseCase:
    """
    Application use case for classifying business documents.
    """

    def __init__(self, classifier: DocumentClassifier | None = None) -> None:
        self.classifier = classifier or DocumentClassifier()

    def execute(self, filename: str, content: str) -> DocumentClassification:
        """
        Classify a document based on its filename and content.
        """
        return self.classifier.classify(filename=filename, content=content)