from grammaire import *

class AnalyseurSyntaxique:
    def __init__(self, grammaire):
        self.grammaire = grammaire
        self.table = TableAnalyse(grammaire)
        self.position = 0
        self.tokens = []

    def analyser(self, tokens):
        """Analyse une liste de tokens et vérifie si elle respecte la grammaire"""
        self.tokens = tokens
        self.position = 0
        try:
            self._analyser_non_terminal(self.grammaire.axiome)
            if self.position < len(self.tokens):
                raise Exception("Erreur: Tokens supplémentaires après la fin de l'analyse")
            return True
        except Exception as e:
            print(f"Erreur d'analyse : {str(e)}")
            return False

    def _analyser_non_terminal(self, non_terminal):
        """Analyse récursivement un non-terminal"""
        if self.position >= len(self.tokens):
            raise Exception(f"Fin inattendue de l'entrée lors de l'analyse de {non_terminal}")

        token_courant = str(self.tokens[self.position])
        production = self.table.obtenir_production(non_terminal, token_courant)

        for symbole in production:
            if symbole.type_token == "terminal":
                if str(self.tokens[self.position]) == symbole.name:
                    self.position += 1
                else:
                    raise Exception(f"Token inattendu : attendu {symbole.name}, reçu {self.tokens[self.position]}")
            elif symbole.type_token == "non_terminal":
                self._analyser_non_terminal(symbole.name)

    def _token_suivant(self):
        """Retourne le prochain token sans avancer dans la liste"""
        if self.position < len(self.tokens):
            return str(self.tokens[self.position])
        return None
    

if __name__ == '__main__':
    grammaire_test = Grammaire('grammaire.txt')
    analyse_code = AnalyseurSyntaxique(grammaire_test)