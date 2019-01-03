

def extract_comments(comment_str):
    """Returns a dict of colon-seperated key:value pairs from a string."""
    comments = {}
    for comment in comment_str.split(','):
        key, val = comment.split(':')
        comments[key.lstrip().rstrip()] = val.lstrip().rstrip()
    return comments


def check_for_nonunique_columns(df, columns):
    """Raises ValueError if a given column contains different values in its rows."""
    for col in columns:
        if df[col].nunique() > 1:
            raise ValueError("All Values in column {} should be the same".format(col))
