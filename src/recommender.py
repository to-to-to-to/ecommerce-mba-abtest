import pandas as pd

def recommend_products(basket, rules_df, top_n=3):
    """
    basket: list of products the user already has
    rules_df: DataFrame containing association rules
    top_n: number of recommendations to return (default n= 3)

    returns: list of recommended products
    """

    # convert basket to set for efficient checking
    basket_set = set(basket)

    # find all rules where the antecedent is a subset of the basket
    matched_rules = rules_df[
        rules_df["antecedents_set"].apply(lambda x: x.issubset(basket_set))
    ].copy()

    # if no rules match → return empty list
    if matched_rules.empty:
        return []

    # sort matching rules by confidence (highest first)
    matched_rules = matched_rules.sort_values("confidence", ascending=False)

    # collect all consequent items from the matched rules
    recommended_items = []
    for items in matched_rules["consequents_set"]:
        recommended_items.extend(list(items))

    # remove products the user already has
    filtered = [item for item in recommended_items if item not in basket_set]

    # remove duplicates while keeping order
    unique_filtered = list(dict.fromkeys(filtered))

    # return top-n results
    return unique_filtered[:top_n]
