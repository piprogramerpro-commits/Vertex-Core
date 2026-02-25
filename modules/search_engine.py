from duckduckgo_search import DDGS

class VertexSearch:
    def search(self, query):
        try:
            with DDGS() as ddgs:
                # Buscamos los 3 mejores resultados
                results = [r for r in ddgs.text(query, max_results=3)]
                combined = ""
                for r in results:
                    combined += f"Título: {r['title']}\nResumen: {r['body']}\n"
                return combined
        except Exception as e:
            return f"Error en espionaje web: {str(e)}"
