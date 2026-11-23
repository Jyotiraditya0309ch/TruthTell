import os
import time
import random
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from .reasoning_semantic_analyzer_specs import ReasoningSemanticAnalyzerSpecs
from dotenv import load_dotenv
load_dotenv()

def ReasoningSemanticAnalyzer(posted_article:str):
    # Rotate across multiple Mistral API keys to avoid rate limits
    mistral_keys = [
        os.environ.get("MISTRAL_API_KEY"),
        os.environ.get("MISTRAL_API_KEY2"),
        os.environ.get("MISTRAL_API_KEY3"),
    ]
    # Filter out empty/missing keys and shuffle for load distribution
    valid_keys = [k for k in mistral_keys if k]
    random.shuffle(valid_keys)

    template="""
    You have to analyze the semantic structure of the article and give prediction.
    You are given with the news article.
    Your job is to provide the reason that why such prediction.
    Try to include evidences from the news article and explain how it is contributed in model prediction.
    
    News Article:
    {news_article}
    
    """

    prompt = ChatPromptTemplate.from_template(
        template=template,
        input_variable=["news_article"]
    )

    last_error = None
    for api_key in valid_keys:
        try:
            llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=0,
                max_retries=1,
                api_key=api_key,
            ).with_structured_output(ReasoningSemanticAnalyzerSpecs)

            reasoning_chain = prompt | llm
            response = reasoning_chain.invoke({
                "news_article": posted_article
            })

            result = {}
            result["news_authenticity"] = response.news_authenticity
            result["reason"] = response.reason

            time.sleep(3)
            return result

        except Exception as e:
            error_str = str(e)
            # Skip this key if rate limited or unauthorized, try the next one
            if "429" in error_str or "rate_limited" in error_str or "401" in error_str or "Unauthorized" in error_str:
                print(f"[WARNING] Mistral key rate-limited or unauthorized, trying next key...")
                last_error = e
                continue
            # For other errors (content issues, bad request, etc.), re-raise
            raise

    raise RuntimeError(
        f"All Mistral API keys are rate-limited or invalid. Last error: {last_error}"
    )