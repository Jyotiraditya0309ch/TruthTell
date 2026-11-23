import os
import time
import random
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from .reasoning_structured_analyzer_specs import ReasoningStructuredAnalyzerSpecs
from dotenv import load_dotenv
load_dotenv()

def ReasoningStructuredAnalyzer(news_authenticity:str, posted_article:str):
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
    We have trained a machine learning model to detect the fake or real news.
    The model is trained on the structure of the news including features such as grammatical mistakes,punctuation errors,etc.
    
    You will be provided with the prediction of the ML model along with the news.
    Your job is to provide the reason that why model has given this prediction.
    Try to include evidences from the news article that will support your reasoning.
    Be sure and don't use the phrases such as 'May be' or 'I think so'.
    
    Model Prediction:
    {model_prediction}
    
    News Article:
    {news_article}
    """

    prompt = ChatPromptTemplate.from_template(
        template=template,
        input_variable=["model_prediction", "news_article"]
    )
    
    last_error = None
    for api_key in valid_keys:
        try:
            llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=0,
                max_retries=1,
                api_key=api_key,
            ).with_structured_output(ReasoningStructuredAnalyzerSpecs)

            reasoning_chain = prompt | llm
            response = reasoning_chain.invoke({
                "model_prediction": news_authenticity,
                "news_article": posted_article
            }).reason

            time.sleep(3)
            print("Reason provided...")
            return response

        except Exception as e:
            error_str = str(e)
            # Skip this key if rate limited or unauthorized, try the next one
            if "429" in error_str or "rate_limited" in error_str or "401" in error_str or "Unauthorized" in error_str:
                print(f"[WARNING] Mistral key rate-limited or unauthorized, trying next key...")
                last_error = e
                continue
            # For other errors, re-raise
            raise

    raise RuntimeError(
        f"All Mistral API keys are rate-limited or invalid. Last error: {last_error}"
    )