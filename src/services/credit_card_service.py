from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analyze_credit_card(card_url):
    credential = AzureKeyCredential(Config.KEY)

    document_Client = DocumentIntelligenceClient(endpoint=Config.ENDPOINT, credential=credential)

    card_info = document_Client.begin_analyze_document(
        "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url)        )
    result = card_info.result()

    for document in result.documents:
        fields = document.fields("fields", {})
        return {
            "card_name": fields.get("CardHolderName", {}).get("content"),
            "card_number": fields.get("BankName", {}).get("content"),
            "expiry_date": fields.get("ExpiryDate", {}).get("content"),
            "bank_name": fields.get("CardNumber", {}).get("content")
        }