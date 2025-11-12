from azure.ai.evaluation import GroundednessEvaluator, AzureOpenAIModelConfiguration, RelevanceEvaluator
from factuality_evaluator import FactualityEvaluator

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint="",
    api_key="",
    azure_deployment="gpt-4.1",
    api_version="",
)

groundedness_eval = GroundednessEvaluator(model_config)
relevance_eval = RelevanceEvaluator(model_config)
factuality_eval = FactualityEvaluator(model_config)

def get_evals(user_message: str, assistant_message: str):
    relevance_result = relevance_eval(query=user_message, response=assistant_message)
    factuality_score = factuality_eval(response=assistant_message)

    return {
        "relevance": relevance_result,
        "factuality": factuality_score
    }
    
def build_evaluation_summary(evaluation_results):
    summary = {}
    for key, result in evaluation_results.items():
        if isinstance(result, dict):
            # Handle different evaluation result formats
            eval_summary = {}
            
            # Extract score (could be under different keys)
            if "score" in result:
                eval_summary["score"] = result["score"]
            elif "gpt_relevance" in result:
                eval_summary["score"] = result["gpt_relevance"]
            else:
                eval_summary["score"] = "N/A"
            
            # Extract rationale/reason (different evaluators use different keys)
            if "rationale" in result:
                eval_summary["rationale"] = result["rationale"]
            elif "relevance_reason" in result:
                eval_summary["rationale"] = result["relevance_reason"]
            elif "reason" in result:
                eval_summary["rationale"] = result["reason"]
            else:
                eval_summary["rationale"] = "N/A"
            
            summary[key] = eval_summary
        else:
            summary[key] = {"score": "N/A", "rationale": "N/A"}
    
    return summary
