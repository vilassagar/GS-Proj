# from http.client import HTTPException
#
# from fastapi import APIRouter
# from app.services.search_in_files import SearchService
# from fastapi import APIRouter, HTTPException, Query
# from fastapi.responses import JSONResponse
# from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI
#
#
#
# router = APIRouter(
#     prefix="/v1",
#     tags=["POC"]
#
# )
#
#
# vector_store = SearchService.initialize_vector_store()
#
#
# @router.get("/search")
# async def search_documents(query: str = Query(..., description="Query for searching files")):
#     if not query:
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")
#
#     print("The query is: ", query)
#
#     retriever = vector_store.as_retriever()
#     qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
#
#     try:
#         result = qa_chain.run(query)
#         return JSONResponse(content={"query": query, "result": result})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))