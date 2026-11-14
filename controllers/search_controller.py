from models.search_model import SearchModel


class SearchController:
    def __init__(self, model=None):
        self.model = model or SearchModel()

    def get_dashboard_stats(self):
        return self.model.get_dashboard_stats()

    def search(self, text="", category="Todo"):
        return self.model.search(text, category)
