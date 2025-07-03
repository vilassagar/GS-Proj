# from langchain.vectorstores import FAISS
# from langchain_openai import OpenAI
# import os
#
# import fitz  # PyMuPDF
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.schema import Document
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
#
#
# FILE_FOLDER = "D:\!!! Study !!!\Avd-SK-Proj\\app\Static"
#
# embedding_function = OpenAIEmbeddings(openai_api_key="")
#
#
# class CustomDocument:
#     def __init__(self, text: str, metadata: dict = None):
#         self.page_content = text
#         self.metadata = metadata or {}
#
#
# class SearchService:
#     @staticmethod
#     def load_index(index_path):
#         """
#         Load the FAISS index from the given path.
#         """
#         return FAISS.load_local(index_path)
#
#     @staticmethod
#     def initialize_vector_store():
#         if not os.path.exists(FILE_FOLDER):
#             raise ValueError("File folder does not exist!")
#
#         print("Initializing vector store from PDFs in:", FILE_FOLDER)
#
#         documents = []
#         for file_name in os.listdir(FILE_FOLDER):
#             file_path = os.path.join(FILE_FOLDER, file_name)
#
#             if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
#                 try:
#                     print(f"\nProcessing file: {file_name}")
#                     doc = fitz.open(file_path)
#                     pdf_text = ""
#
#                     for page_num in range(doc.page_count):
#                         page = doc.load_page(page_num)
#                         pdf_text += page.get_text()
#
#                     if pdf_text.strip():
#                         documents.append(Document(page_content=pdf_text, metadata={"file_name": file_name}))
#                     else:
#                         print(f"Warning: No text extracted from {file_name}")
#
#                 except Exception as e:
#                     print(f"Error reading PDF {file_name}: {e}")
#
#         if not documents:
#             raise ValueError("No valid PDF files found or processed.")
#
#         # **Step 1**: Use HuggingFace embeddings model (correct approach)
#         embedding_function = HuggingFaceEmbeddings(
#             model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
#
#         # **Step 2**: Create FAISS index
#         vector_store = FAISS.from_documents(documents, embedding_function)
#
#         print("Vector store successfully initialized!")
#         return vector_store
#
#     # Initialize Vector Store (FAISS is an example)
#     # @staticmethod
#     # def initialize_vector_store():
#     #     if not os.path.exists(FILE_FOLDER):
#     #         raise ValueError("File folder does not exist!")
#     #     documents = []
#     #     for file_name in os.listdir(FILE_FOLDER):
#     #         file_path = os.path.join(FILE_FOLDER, file_name)
#     #         if os.path.isfile(file_path):
#     #             with open(file_path, "r", encoding="utf-8") as file:
#     #                 documents.append({"content": file.read(), "file_name": file_name})
#     #
#     #     # Embed and store documents
#     #     embeddings = OpenAIEmbeddings()  # Replace with your LLM provider
#     #     vector_store = FAISS.from_documents(documents, embeddings)
#     #     return vector_store
#
#     @staticmethod
#     def search(index, query: str):
#         """
#         Perform a similarity search on the provided FAISS index.
#         """
#         docs = index.similarity_search(query)
#         return docs
