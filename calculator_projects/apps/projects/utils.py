from calculator_projects.apps.projects.constants import coefficient


def get_coefficient(post_coefficient: str):
    return coefficient.get(post_coefficient)
